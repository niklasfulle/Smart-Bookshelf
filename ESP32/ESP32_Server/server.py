"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301,W0621,W0602

import _thread
import gc
import time
import sys

from connection.connection import connection
from utils.json_data_reader import json_data_reader
from utils.checks import handle_checks
from utils.constants import FILES, BUFFER_SIZE
from utils.connection_helper import get_last_databuffer_element
from hardware.bookshelf import bookshelf
from protocol.parser.parser_default_package import parse_package

gc.enable()

databuffer: list = []

bookshelfs: bookshelf = []
connections: connection = []

threads: int = 1

bookshelfs_json = json_data_reader(FILES.BOOKSHELFS, [], 1)
clients_json = json_data_reader(FILES.SERVER, ["clients"], 1)

if len(bookshelfs_json) != len(clients_json):
    print("bookshelfes and customers do not match")
    sys.exit(0)


for i, bookshelf_json in enumerate(bookshelfs_json):
    _bookshelf: bookshelf = bookshelf(
        bookshelf_json["name"],
        clients_json[i]["ip"],
        bookshelf_json["shelving_units"],
    )

    bookshelfs.append(_bookshelf)

server_ip = json_data_reader(FILES.SERVER, ["connection", "ip"], 1)
server_port = json_data_reader(FILES.SERVER, ["connection", "port"], 1)
sender_id = json_data_reader(FILES.SERVER, ["connection", "port"], 1)


for i, client_json in enumerate(clients_json):
    _connection: connection = connection(
        (client_json["ip"], client_json["port"]),
        (server_ip, server_port),
        receiver_id=client_json["id"],
        sender_id=sender_id,
        bookshelf_object=bookshelfs[i],
    )

    connections.append(_connection)


def listening_thread(sock):
    """
    -
    """
    global databuffer

    while True:
        data_received = sock.recvfrom(BUFFER_SIZE)
        databuffer.insert(0, (data_received[1], data_received[0]))


def threaded(connection: connection, threads: int):
    """
    -
    """
    data = bytearray(b"")

    while True:
        index = get_last_databuffer_element(databuffer, connection.client)

        if index is not None:
            data = databuffer[index][1]
            databuffer.pop(index)

        try:
            if data != bytearray(b""):
                _package = parse_package(data)

                print(_package.complete_data)

                if not handle_checks(_connection, _package):
                    print("Check Error")
                    data = bytearray(b"")

            gc.collect()
        except KeyboardInterrupt:
            print("ESP terminated")
            data = bytearray(b"")
            sys.exit(0)

        time.sleep(2)


def main(threads: int):
    """
    -
    """
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
                    _thread.start_new_thread(threaded, (_connection, threads))

                    threads += 1

            else:
                pass

        except KeyboardInterrupt:
            print("Server terminated")
            sys.exit(0)


if __name__ == "__main__":
    main(threads)
