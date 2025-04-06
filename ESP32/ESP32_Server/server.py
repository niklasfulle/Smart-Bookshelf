"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301,W0621,W0602

import _thread
import gc
import os
import time
import sys
import psycopg2

sys.path.append("../")
from dotenv import load_dotenv

from connection.connection import connection
from utils.json_data_reader import json_data_reader
from utils.checks import handle_checks
from utils.constants import FILES, BUFFER_SIZE
from utils.connection_helper import get_last_databuffer_element
from utils.build_helper import (
    get_protocol_version,
    get_server_version,
    get_bookshelf_version,
)
from utils.converter import int_to_2byte_array
from utils.tasks import check_tasks, handle_tasks
from utils.send_data import handle_data_reveiv_mode, handle_data_send_mode
from hardware.bookshelf import bookshelf
from protocol.parser.parser_default_package import parse_package
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE, DISC_REASON, STATUS
from protocol.builder.builder_default_package import (
    build_connection_response,
    build_version_response,
    build_status_request,
    build_disconnection_request,
)

load_dotenv()

postgres = psycopg2.connect(
    database=os.getenv("DATABASE"),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)

cursor = postgres.cursor()

gc.enable()

databuffer: list = []

bookshelfs: bookshelf = []
connections: connection = []

threads: int = 0


def fetch_configs() -> int:
    """
    Fetches configuration data for bookshelves and connections, initializes objects,
    and validates the consistency between the number of bookshelves and clients.
    This function performs the following tasks:
    1. Reads bookshelf configuration data from a JSON file.
    2. Fetches client connection data from a database.
    3. Validates that the number of bookshelves matches the number of clients.
    4. Initializes `bookshelf` objects for each bookshelf configuration.
    5. Reads server connection details from a JSON file.
    6. Initializes `connection` objects for each client-server connection.
    Returns:
        int: The number of clients (and bookshelves) successfully processed.
    Raises:
        SystemExit: If the number of bookshelves and clients do not match.
    """

    bookshelfs_json = json_data_reader(FILES.BOOKSHELFS, [], 1)

    cursor.execute('SELECT * FROM "connection"')

    clients = cursor.fetchall()

    if len(bookshelfs_json) != len(clients):
        print("bookshelfes and customers do not match")
        sys.exit(0)

    for i, bookshelf_json in enumerate(bookshelfs_json):
        _bookshelf: bookshelf = bookshelf(
            bookshelf_json["name"],
            clients[i][2],
            bookshelf_json["shelving_units"],
        )

        bookshelfs.append(_bookshelf)

    server_ip = json_data_reader(FILES.SERVER, ["connection", "ip"], 1)
    server_port = json_data_reader(FILES.SERVER, ["connection", "port"], 1)
    sender_id = json_data_reader(FILES.SERVER, ["id"], 1)

    for i, _ in enumerate(clients):
        _connection: connection = connection(
            (clients[i][2], clients[i][3]),
            (server_ip, server_port),
            receiver_id=clients[i][0],
            sender_id=sender_id,
            Bookshelf_object=bookshelfs[i],
        )

        connections.append(_connection)

    return len(clients)


def listening_thread(sock) -> None:
    """
    Listens for incoming data on the provided socket and updates the global databuffer.
    This function runs in an infinite loop, continuously receiving data from the socket.
    The received data is stored in the global `databuffer` as a tuple containing the
    sender's address and the received data as a bytearray. New data is inserted at the
    beginning of the buffer.
    Args:
        sock (socket.socket): The socket object used to receive data.
    Returns:
        None
    """

    global databuffer

    while True:
        data_received = sock.recvfrom(BUFFER_SIZE)
        databuffer.insert(0, (data_received[1], bytearray(data_received[0])))


def threaded(_connection: connection) -> None:
    """
    Handles the communication and task management for a single connection.
    This function runs in an infinite loop, processing incoming data, managing
    connection states, and handling tasks or requests based on the protocol.

    Args:
        _connection (connection): The connection object representing a client-server connection.

    Returns:
        None
    """
    data = bytearray(b"")  # Initialize an empty bytearray for incoming data
    _connection.status = STATUS.UNKOWN  # Set the initial status of the connection

    while True:
        # Check if there is new data in the global databuffer for this connection
        index = get_last_databuffer_element(databuffer, _connection.client)

        if index is not None:
            # Retrieve and remove the data from the databuffer
            data = databuffer[index][1]
            databuffer.remove(databuffer[index])

        try:
            if data == bytearray(b""):  # No new data received
                # Handle tasks if the connection is established and ready
                if (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is not None
                    and not _connection._wait_for_task_response
                    and not _connection.data_reveiv_mode
                    and not _connection.data_send_mode
                ):
                    handle_tasks(_connection)

                elif (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is not None
                    and not _connection._wait_for_task_response
                    and (_connection.data_reveiv_mode or _connection.data_send_mode)
                ):
                    if _connection.data_reveiv_mode:
                        handle_data_reveiv_mode(_connection)
                    elif _connection.data_send_mode:
                        handle_data_send_mode(_connection)

                # Handle task response waiting logic

                elif (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is not None
                    and _connection._wait_for_task_response
                    and not _connection.data_reveiv_mode
                    and not _connection.data_send_mode
                ):
                    if _connection._wait_for_task_response_count < 51:
                        _connection._wait_for_task_response_count += 1
                        time.sleep(0.1)
                    else:
                        # Disconnect if task response timeout occurs
                        _connection.send_message_to_client(
                            build_disconnection_request(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                _connection.last_send_package.sequence_number,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                                int_to_2byte_array(DISC_REASON.USERREQUEST),
                            )
                        )
                        _connection.reset()

                # Check for new tasks if no task is currently assigned
                elif (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is None
                ):
                    check_tasks(postgres, cursor, _connection)

                # Send a status request if no task is assigned and no status request is pending
                if (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is None
                    and not _connection.status_request_send
                ):
                    if _connection.waiting_count < 26:
                        _connection.waiting_count += 1
                        time.sleep(0.1)
                    else:
                        _connection.send_message_to_client(
                            build_status_request(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                _connection.last_send_package.sequence_number,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                            )
                        )
                        _connection.status_request_send = True
                        _connection.waiting_count = 0
                        time.sleep(0.2)

                # Handle status request timeout
                elif (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                    and _connection._task is None
                    and _connection.status_request_send
                ):
                    if _connection.status_request_waiting_count < 51:
                        _connection.status_request_waiting_count += 1
                        time.sleep(0.1)
                    else:
                        # Disconnect if status request timeout occurs
                        _connection.send_message_to_client(
                            build_disconnection_request(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                _connection.last_send_package.sequence_number,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                                int_to_2byte_array(DISC_REASON.USERREQUEST),
                            )
                        )
                        _connection.reset()

                else:
                    # No action needed, wait for new data or events
                    time.sleep(0.1)

            elif data != bytearray(b""):  # New data received
                _package = parse_package(data)  # Parse the received package

                # Update the last received package if it's not a disconnect request
                if PACKAGE_MESSAGE_TYPE.DiscRequest != int.from_bytes(
                    _package.message_type, "little"
                ):
                    _connection.last_received_package = _package

                # Validate the package and handle errors
                if not handle_checks(_connection, _package):
                    print("Check Error")
                    data = bytearray(b"")
                else:
                    # Handle different package types based on the protocol
                    if PACKAGE_MESSAGE_TYPE.ConnRequest == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Respond to connection request
                        _connection.send_message_to_client(
                            build_connection_response(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                0,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                            )
                        )
                        _connection.connection_request_send = True
                        _connection.waiting_count = 0
                        data = bytearray(b"")
                        time.sleep(0.2)

                    elif PACKAGE_MESSAGE_TYPE.ConnApprove == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle connection approval
                        _connection.handshake = True
                        _connection.waiting_count = 0
                        data = bytearray(b"")
                        time.sleep(0.2)

                    elif PACKAGE_MESSAGE_TYPE.VerRequest == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Respond to version request
                        _connection.send_message_to_client(
                            build_version_response(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                _connection.last_send_package.sequence_number,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                                get_protocol_version(),
                                get_server_version(),
                                get_bookshelf_version(),
                            )
                        )
                        _connection.version_check = True
                        _connection.waiting_count = 0
                        data = bytearray(b"")
                        time.sleep(0.1)

                    elif PACKAGE_MESSAGE_TYPE.StatusResponse == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Update connection status
                        _connection.status = int.from_bytes(_package.data, "little")
                        _connection.status_request_send = False
                        _connection.status_request_waiting_count = 0
                        data = bytearray(b"")
                        time.sleep(0.2)

                    elif PACKAGE_MESSAGE_TYPE.SleepResponse == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle sleep response
                        _connection._wait_for_task_response = False
                        _connection._task = None
                        _connection._wait_for_task_response_count = 0
                        data = bytearray(b"")
                        time.sleep(0.2)

                    elif PACKAGE_MESSAGE_TYPE.RebootResponse == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle reboot response
                        _connection._wait_for_task_response = False
                        _connection._task = None
                        _connection._wait_for_task_response_count = 0
                        data = bytearray(b"")
                        time.sleep(0.2)

                    elif PACKAGE_MESSAGE_TYPE.Data == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle data package
                        print("Data")

                    elif PACKAGE_MESSAGE_TYPE.DataUpload == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle data upload package
                        print("DataUpload")

                    elif PACKAGE_MESSAGE_TYPE.DiscRequest == int.from_bytes(
                        _package.message_type, "little"
                    ):
                        # Handle disconnect request
                        if (
                            int.from_bytes(_package.data, "little")
                            != DISC_REASON.TIMEOUT
                        ):
                            _connection.reset()
                            data = bytearray(b"")
                        else:
                            _connection.timeout_counter += 1
                        data = bytearray(b"")
                        time.sleep(0.2)

            gc.collect()  # Perform garbage collection to free memory
        except KeyboardInterrupt:
            # Handle server termination
            print("Server terminated")
            _connection.send_message_to_client(
                build_disconnection_request(
                    _connection.receiver_id_int,
                    _connection.sender_id_int,
                    _connection.last_send_package.sequence_number,
                    _connection.last_received_package.sequence_number,
                    0,
                    _connection.last_received_package.timestamp,
                    int_to_2byte_array(DISC_REASON.USERREQUEST),
                )
            )
            data = bytearray(b"")
            sys.exit(0)

        time.sleep(2)  # Wait before the next iteration


def main():
    """
    Main function to manage server connections and threads.
    This function initializes the server by fetching the number of threads
    from the configuration and continuously monitors the active connections.
    It starts new threads for handling client connections and listens for
    incoming messages. The server shuts down gracefully upon a keyboard
    interrupt or when there are no active connections.
    Workflow:
    - Fetch the initial number of threads from the configuration.
    - Monitor the number of active connections.
    - Start new threads for handling client connections if needed.
    - Handle server termination on a keyboard interrupt or when no clients are connected.
    Exceptions:
    - Handles and prints any exceptions that occur while starting new threads.
    - Gracefully terminates the server on a KeyboardInterrupt by sending a
      disconnection request to all connected clients.
    Note:
    - The function assumes the existence of global variables `connections` and
      `DISC_REASON`, as well as utility functions like `fetch_configs`,
      `listening_thread`, `threaded`, `build_disconnection_request`, and
      `int_to_2byte_array`.
    Raises:
    - SystemExit: When there are no active connections or during server termination.
    """
    threads = fetch_configs()
    while True:
        try:
            if len(connections) == 0:
                sys.exit(0)

            if len(connections) != threads - 1:
                for _connection in connections:
                    try:
                        _thread.start_new_thread(listening_thread, (_connection.sock,))

                    except Exception as error:
                        print(error)

                    print("Server runs with {} Clients".format(len(connections)))
                    _thread.start_new_thread(threaded, (_connection,))

                    threads += 1

            else:
                pass

            time.sleep(5)

        except KeyboardInterrupt:
            print("Server terminated")
            for _connection in connections:
                _connection.send_message_to_client(
                    build_disconnection_request(
                        _connection.receiver_id_int,
                        _connection.sender_id_int,
                        _connection.last_send_package.sequence_number,
                        _connection.last_received_package.sequence_number,
                        0,
                        _connection.last_received_package.timestamp,
                        int_to_2byte_array(DISC_REASON.USERREQUEST),
                    )
                )
            sys.exit(0)


if __name__ == "__main__":
    main()
