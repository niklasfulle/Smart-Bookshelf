"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622
from utils.enum import enum

MD4_Type = enum(NONE=0, LOWER_HALF=1, FULL=2)

FILES = enum(
    CLIENT="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/client.json",
    Bookshelf="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/Bookshelf.json",
    CONFIG="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/configs/config.json",
)

BUFFER_SIZE: int = 1024
