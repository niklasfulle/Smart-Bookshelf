"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301

from utils.json_data_reader import json_data_reader
from hardware.bookshelf import bookshelf
from connection.connection import connection

client_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/client.json"
bookshelf_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/bookshelf.json"
config_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/config.json"

ip = json_data_reader(client_file, ["connection", "ip"], 1)
bookshelf_name = json_data_reader(bookshelf_file, ["name"], 1)
shelving_units = json_data_reader(bookshelf_file, ["shelving_units"], 1)

bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

client_ip = json_data_reader(client_file, ["connection", "ip"], 1)
client_port = json_data_reader(client_file, ["connection", "port"], 1)
server_ip = json_data_reader(client_file, ["server", "ip"], 1)
server_port = json_data_reader(client_file, ["server", "port"], 1)
sender_id = json_data_reader(client_file, ["id"], 1)
receiver_id = json_data_reader(client_file, ["server", "id"], 1)
connection_object: connection = connection((client_ip, client_port), (server_ip, server_port), receiver_id, sender_id, bookshelf_object)
