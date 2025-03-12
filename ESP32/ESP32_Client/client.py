"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301

from utils.json_data_reader import json_data_reader
from hardware.bookshelf import bookshelf

client_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/client.json"
bookshelf_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/bookshelf.json"
config_file: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/config.json"

ip = json_data_reader(client_file, ["connection", "ip"], 1)
bookshelf_name = json_data_reader(bookshelf_file, ["name"], 1)
shelving_units = json_data_reader(bookshelf_file, ["shelving_units"], 1)

bookshelf_objet: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)


