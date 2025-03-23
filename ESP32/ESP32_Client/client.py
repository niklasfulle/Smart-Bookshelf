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
from utils.checks import handle_checks, check_versions
from hardware.bookshelf import bookshelf
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.parser.parser_default_package import parse_package
from protocol.builder.builder_default_package import (
    build_connection_request,
    build_disconnection_request,
    build_connection_approve,
    build_version_request,
)


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
    -
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

while True:
    try:
        if data == bytearray(b""):
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
                time.sleep(3.5)

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
                    )
                )
                _connection.connection_request_send = False
                time.sleep(1.0)

            elif (
                _connection.connection_request_send
                and _connection.handshake
                and not _connection.version_check
            ):
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
                time.sleep(2.0)

            elif (
                _connection.connection_request_send
                and _connection.handshake
                and _connection.version_check
            ):
                time.sleep(0.1)

        elif data != bytearray(b""):
            _package = parse_package(data)

            _connection.last_received_package = _package

            if not handle_checks(_connection, _package):
                print("Check Error")
                data = bytearray(b"")

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
                data = bytearray(b"")
                time.sleep(0.2)

            elif PACKAGE_MESSAGE_TYPE.VerResponse == int.from_bytes(
                _package.message_type, "little"
            ):
                if check_versions(_package):
                    _connection.version_check = True

                data = bytearray(b"")
                time.sleep(0.2)

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
