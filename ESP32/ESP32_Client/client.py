"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301

import _thread
import gc
import time
import sys

from connection.connection import connection

from utils.json_data_reader import json_data_reader
from utils.constants import FILES, BUFFER_SIZE
from utils.checks import (
    handle_checks,
    check_versions,
    check_data_message_type,
    check_data_upload_message_type,
)
from utils.converter import int_to_2byte_array
from hardware.bookshelf import bookshelf
from protocol.constants.constants import (
    PACKAGE_MESSAGE_TYPE,
    DISC_REASON,
    STATUS,
    DATA_MESSAGE_TYPE,
    DATA_UPLOAD_MESSAGE_TYPE,
)
from protocol.parser.parser_default_package import parse_package
from protocol.builder.builder_default_package import (
    build_connection_request,
    build_disconnection_request,
    build_connection_approve,
    build_version_request,
    build_status_response,
    build_sleep_response,
    build_reboot_response,
)
from protocol.parser.parser_data_package import parse_data_package
from protocol.parser.parser_data_upload_package import parse_data_upload_package


# _thread.stack_size(2048)

gc.enable()

SSID = ""
KEY = ""

# wifi(SSID, KEY, 10000)

data = bytearray(b"")

ip = json_data_reader(FILES.CLIENT, ["connection", "ip"], 1)
Bookshelf_name = json_data_reader(FILES.Bookshelf, ["name"], 1)
shelving_units = json_data_reader(FILES.Bookshelf, ["shelving_units"], 1)

_Bookshelf: bookshelf = bookshelf(
    Bookshelf_name,
    ip,
    shelving_units,
)

client_ip = json_data_reader(FILES.CLIENT, ["connection", "ip"], 1)
client_port = json_data_reader(FILES.CLIENT, ["connection", "port"], 1)
server_ip = json_data_reader(FILES.CLIENT, ["server", "ip"], 1)
server_port = json_data_reader(FILES.CLIENT, ["server", "port"], 1)
sender_id = json_data_reader(FILES.CLIENT, ["id"], 1)
receiver_id = json_data_reader(FILES.CLIENT, ["server", "id"], 1)

_connection: connection = connection(
    (client_ip, client_port),
    (server_ip, server_port),
    receiver_id,
    sender_id,
    _Bookshelf,
)


def listening_thread():
    """
    Continuously listens for incoming data on a socket connection and updates the global `data` variable.
    This function runs in an infinite loop, receiving data from a socket connection using the `recvfrom` method.
    The received data is stored as a bytearray in the global variable `data`.
    Global Variables:
        data (bytearray): A global variable that is updated with the received data.
    Notes:
        - The function assumes that `_connection.sock` is a valid socket object and `BUFFER_SIZE` is defined.
        - This function is designed to run indefinitely and should be executed in a separate thread to avoid blocking the main program.
    """

    global data

    while True:
        data_received = _connection.sock.recvfrom(BUFFER_SIZE)
        data = bytearray(data_received[0])


try:
    _thread.start_new_thread(listening_thread, ())

except Exception as error:  # noqa: E722
    print("Error: unable to start thread")
    print(error)

print("ESP runs on IP:{}, PORt:{}".format(client_ip, client_port))

gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

_connection.status = STATUS.RUNNING

while True:
    try:
        # If no data is received, handle connection and handshake processes
        if data == bytearray(b""):
            # Send connection request if not already sent and handshake/version check not done
            if (
                not _connection.connection_request_send
                and not _connection.handshake
                and not _connection.version_check
            ):
                _connection.send_message_to_server(
                    build_connection_request(
                        _connection.receiver_id_int,
                        _connection.sender_id_int,
                        *[0] * 4,
                    )
                )
                _connection.connection_request_send = True
                data = bytearray(b"")
                time.sleep(2)

            # Handle timeout if connection request was sent but handshake/version check not done
            elif (
                _connection.connection_request_send
                and not _connection.handshake
                and not _connection.version_check
            ):
                _connection.send_message_to_server(
                    build_disconnection_request(
                        _connection.receiver_id_int,
                        _connection.sender_id_int,
                        *[0] * 4,
                        int_to_2byte_array(DISC_REASON.TIMEOUT),
                    )
                )
                _connection.connection_request_send = False
                time.sleep(0.2)

            # Wait if handshake is in progress but version check not done
            elif (
                _connection.connection_request_send
                and _connection.handshake
                and not _connection.version_check
            ):
                time.sleep(0.1)

            # Wait if both handshake and version check are completed
            elif (
                _connection.connection_request_send
                and _connection.handshake
                and _connection.version_check
            ):
                time.sleep(0.1)

            # Default wait
            else:
                time.sleep(0.1)

        # If data is received, parse and handle it
        elif data != bytearray(b""):
            _package = parse_package(data)

            # Store the last received package
            _connection.last_received_package = _package

            # Perform checks on the received package
            if not handle_checks(_connection, _package):
                print("Check Error")
                data = bytearray(b"")

            else:
                # Handle connection response
                if PACKAGE_MESSAGE_TYPE.ConnResponse == int.from_bytes(
                    _package.message_type, "little"
                ):
                    _connection.send_message_to_server(
                        build_connection_approve(
                            _connection.receiver_id_int,
                            _connection.sender_id_int,
                            _connection.last_send_package.sequence_number,
                            _connection.last_received_package.sequence_number,
                            0,
                            _connection.last_received_package.timestamp,
                        )
                    )
                    _connection.handshake = True
                    time.sleep(2)

                    # Send version request after handshake
                    _connection.send_message_to_server(
                        build_version_request(
                            _connection.receiver_id_int,
                            _connection.sender_id_int,
                            _connection.last_send_package.sequence_number,
                            _connection.last_received_package.sequence_number,
                            0,
                            _connection.last_received_package.timestamp,
                        )
                    )

                    time.sleep(1)
                    data = bytearray(b"")

                # Handle version response
                elif PACKAGE_MESSAGE_TYPE.VerResponse == int.from_bytes(
                    _package.message_type, "little"
                ):
                    if check_versions(_package):
                        _connection.version_check = True
                    else:
                        _connection.version_check = False
                        _connection.send_message_to_server(
                            build_disconnection_request(
                                _connection.receiver_id_int,
                                _connection.sender_id_int,
                                _connection.last_send_package.sequence_number,
                                _connection.last_received_package.sequence_number,
                                0,
                                _connection.last_received_package.timestamp,
                                int_to_2byte_array(DISC_REASON.INCOMPATIBLEVERSION),
                            )
                        )
                    data = bytearray(b"")
                    time.sleep(0.2)

                # Handle status request
                elif PACKAGE_MESSAGE_TYPE.StatusRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    _connection.send_message_to_server(
                        build_status_response(
                            _connection.receiver_id_int,
                            _connection.sender_id_int,
                            _connection.last_send_package.sequence_number,
                            _connection.last_received_package.sequence_number,
                            0,
                            _connection.last_received_package.timestamp,
                            int_to_2byte_array(_connection.status),
                        )
                    )
                    data = bytearray(b"")
                    time.sleep(0.2)

                # Handle sleep request
                elif PACKAGE_MESSAGE_TYPE.SleepRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    time.sleep(0.2)
                    _connection.send_message_to_server(
                        build_sleep_response(
                            _connection.receiver_id_int,
                            _connection.sender_id_int,
                            _connection.last_send_package.sequence_number,
                            _connection.last_received_package.sequence_number,
                            0,
                            _connection.last_received_package.timestamp,
                        )
                    )
                    data = bytearray(b"")
                    time.sleep(0.2)

                # Handle reboot request
                elif PACKAGE_MESSAGE_TYPE.RebootRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    time.sleep(0.2)
                    _connection.send_message_to_server(
                        build_reboot_response(
                            _connection.receiver_id_int,
                            _connection.sender_id_int,
                            _connection.last_send_package.sequence_number,
                            _connection.last_received_package.sequence_number,
                            0,
                            _connection.last_received_package.timestamp,
                        )
                    )
                    data = bytearray(b"")
                    time.sleep(0.2)

                # Handle data package
                elif PACKAGE_MESSAGE_TYPE.Data == int.from_bytes(
                    _package.message_type, "little"
                ):
                    print("Data")

                    parsed_data_package = parse_data_package(_package.complete_data)

                    if not check_data_message_type(parsed_data_package):
                        print("Check Error")
                        data = bytearray(b"")

                    else:
                        if DATA_MESSAGE_TYPE.ShowOnLight == int.from_bytes(
                            parsed_data_package.message_type, "little"
                        ):
                            print("ShowOnLight")

                        elif DATA_MESSAGE_TYPE.ShowOffLight == int.from_bytes(
                            parsed_data_package.message_type, "little"
                        ):
                            print("ShowOffLight")

                        elif DATA_MESSAGE_TYPE.ShowBook == int.from_bytes(
                            parsed_data_package.message_type, "little"
                        ):
                            print("ShowBook")

                        elif DATA_MESSAGE_TYPE.ShowBooks == int.from_bytes(
                            parsed_data_package.message_type, "little"
                        ):
                            print("ShowBooks")

                        elif DATA_MESSAGE_TYPE.LightMode == int.from_bytes(
                            parsed_data_package.message_type, "little"
                        ):
                            print("LightMode")

                # Handle data upload package
                elif PACKAGE_MESSAGE_TYPE.DataUpload == int.from_bytes(
                    _package.message_type, "little"
                ):
                    print("DataUpload")

                    parsed_data_upload_package = parse_data_upload_package(
                        _package.complete_data
                    )

                    if not check_data_upload_message_type(parsed_data_upload_package):
                        print("Check Error")
                        data = bytearray(b"")

                    else:
                        if DATA_UPLOAD_MESSAGE_TYPE.DataUpStart == int.from_bytes(
                            parsed_data_upload_package.message_type, "little"
                        ):
                            print("DataUpStart")

                        elif DATA_UPLOAD_MESSAGE_TYPE.DataUpRequest == int.from_bytes(
                            parsed_data_upload_package.message_type, "little"
                        ):
                            print("DataUpRequest")

                # Handle disconnection request
                elif PACKAGE_MESSAGE_TYPE.DiscRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    if int.from_bytes(_package.data, "little") != DISC_REASON.TIMEOUT:
                        _connection.reset()
                    data = bytearray(b"")

        # Perform garbage collection
        gc.collect()

    # Handle keyboard interrupt for graceful termination
    except KeyboardInterrupt:
        print("Start terminating the Client...")
        confirmed_sequence_number = 0
        confirmed_timestamp = 0

        if _connection.last_received_package is not None:
            confirmed_sequence_number = (
                _connection.last_received_package.sequence_number
            )

            confirmed_timestamp = _connection.last_received_package.timestamp

        _connection.send_message_to_server(
            build_disconnection_request(
                _connection.receiver_id_int,
                _connection.sender_id_int,
                _connection.last_send_package.sequence_number,
                confirmed_sequence_number,
                0,
                confirmed_timestamp,
                int_to_2byte_array(DISC_REASON.USERREQUEST),
            )
        )
        data = bytearray(b"")

        time.sleep(2)
        print("Client terminated")
        sys.exit(0)
