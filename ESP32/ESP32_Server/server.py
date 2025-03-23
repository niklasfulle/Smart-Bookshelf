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
from hardware.bookshelf import bookshelf
from protocol.parser.parser_default_package import parse_package
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.builder.builder_default_package import (
    build_connection_response,
    build_version_response,
    build_status_request,
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
    -
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
    -
    """
    global databuffer

    while True:
        data_received = sock.recvfrom(BUFFER_SIZE)
        databuffer.insert(0, (data_received[1], bytearray(data_received[0])))


def threaded(_connection: connection) -> None:
    """
    -
    """
    data = bytearray(b"")

    while True:
        index = get_last_databuffer_element(databuffer, _connection.client)

        if index is not None:
            data = databuffer[index][1]
            databuffer.pop(index)

        try:
            if data == bytearray(b""):
                if (
                    _connection.connection_request_send
                    and _connection.handshake
                    and _connection.version_check
                ):
                    if _connection.waiting_count < 50:
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

                        _connection.waiting_count = 0
                        time.sleep(0)

            elif data != bytearray(b""):
                _package = parse_package(data)

                _connection.last_received_package = _package

                if not handle_checks(_connection, _package):
                    print("Check Error")
                    data = bytearray(b"")

                if PACKAGE_MESSAGE_TYPE.ConnRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
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
                    time.sleep(0.5)

                if PACKAGE_MESSAGE_TYPE.VerRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    _connection.handshake = True
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

                elif PACKAGE_MESSAGE_TYPE.DiscRequest == int.from_bytes(
                    _package.message_type, "little"
                ):
                    _connection.reset()
                    data = bytearray(b"")

            gc.collect()
        except KeyboardInterrupt:
            print("ESP terminated")
            data = bytearray(b"")
            sys.exit(0)

        time.sleep(2)


def main():
    """
    -
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
            sys.exit(0)


if __name__ == "__main__":
    main()
