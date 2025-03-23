"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
import time
import random

from utils.converter import int_to_4byte_array, int_to_1byte_array
from utils.json_data_reader import json_data_reader
from utils.constants import FILES


def get_timestamp() -> bytearray:
    """Returns the current system time in s since 1970 as 4 byte

    Returns:
        bytearray: the timestamp as 4-byte bytearray
    """

    number = int(time.time())
    return int_to_4byte_array(number)


def get_random_sequence_number() -> bytearray:
    """generates a random sequence number between 0 - 4294967295

    Returns:
        bytearray: sequence number as 4-byte bytearray
    """

    number = random.randint(0, 2147483646)

    return int_to_4byte_array(number)


def increment_sequence_number(number: bytearray) -> bytearray:
    """Increases the passed sequence number by one and if the value is greater than 4294967295,
        counting starts again at 0

    Args:
        number (bytearray): sequence number

    Returns:
        bytearray: incremented sequence number as 4-byte bytearray
    """

    number = int.from_bytes(number, "little")
    if number < 2147483646:
        number += 1
    else:
        number = 0

    return int_to_4byte_array(number)


def get_bytearrays_size_sum(array: bytearray) -> int:
    """the function is passed an array of byte arrays and adds up
        the lengths of the individual byte arrays

    Args:
        array (bytearray): the array with the bytearrays

    Returns:
        int: the size of the arrays
    """

    length = 0
    for bytearrays in enumerate(array):
        length += len(bytearrays[1])

    return length


def get_protocol_version() -> bytearray:
    """
    -
    """
    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["protocol_version_major"], 2)
    ) + int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["protocol_version_minor"], 2)
    )


def get_server_version() -> bytearray:
    """
    -
    """
    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["server_version_major"], 2)
    ) + int_to_1byte_array(json_data_reader(FILES.CONFIG, ["server_version_minor"], 2))


def get_bookshelf_version() -> bytearray:
    """
    -
    """
    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["Bookshelf_version_major"], 2)
    ) + int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["Bookshelf_version_minor"], 2)
    )
