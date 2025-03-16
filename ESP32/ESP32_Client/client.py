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
from hardware.Bookshelf import Bookshelf


# _thread.stack_size(2048)

gc.enable()

SSID = ""
KEY = ""

# wifi(SSID, KEY, 10000)

data = bytearray(b"")

ip = json_data_reader(FILES.CLIENT, ["connection", "ip"], 1)
Bookshelf_name = json_data_reader(FILES.Bookshelf, ["name"], 1)
shelving_units = json_data_reader(FILES.Bookshelf, ["shelving_units"], 1)

_Bookshelf: Bookshelf = Bookshelf(
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
        data = data_received[0]


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
        gc.collect()
    except KeyboardInterrupt:
        print("ESP terminated")
        data = bytearray(b"")
        sys.exit(0)
