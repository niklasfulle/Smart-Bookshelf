"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622
from utils.enum import enum

MD4_Type = enum(NONE=0, LOWER_HALF=1, FULL=2)

FILES = enum(
    SERVER="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Server/configs/server.json",
    BOOKSHELFS="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Server/configs/bookshelfs.json",
    CONFIG="/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Server/configs/config.json",
)

BUFFER_SIZE: int = 1024

TASK_TYPES = enum(
    SLEEP="task_sleep",
    REBOOT="task_reboot",
    CONFIG_SEND="task_config_send",
    CONFIG_REQUEST="task_config_request",
    DATA_SEND_BOOK="task_data_send_book",
    DATA_SEND_BOOKS="task_data_send_books",
    DATA_SEND_MODE="task_data_send_mode",
    DATA_SEND_LIGHT_ON="task_data_send_ligh_on",
    DATA_SEND_LIGHT_OFF="task_data_send_ligh_off",
)

BOOKSHELF_MODE = enum(BOOKS="books", LIGHT="light", SLEEP="sleep")
