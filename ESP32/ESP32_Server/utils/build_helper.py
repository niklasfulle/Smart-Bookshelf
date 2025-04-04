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
    """
    Generates a 4-byte array representing the current Unix timestamp.

    The function retrieves the current time as the number of seconds since
    the Unix epoch (January 1, 1970) and converts it into a 4-byte array.

    Returns:
        bytearray: A 4-byte array representing the current Unix timestamp.
    """

    number = int(time.time())
    return int_to_4byte_array(number)


def get_random_sequence_number() -> bytearray:
    """
    Generates a random 4-byte sequence number.
    This function generates a random integer between 0 and 2147483646 (inclusive),
    and converts it into a 4-byte array representation.
    Returns:
        bytearray: A 4-byte array representing the randomly generated number.
    """

    number = random.randint(0, 2147483646)

    return int_to_4byte_array(number)


def increment_sequence_number(number: bytearray) -> bytearray:
    """
    Increment a 4-byte sequence number represented as a little-endian bytearray.
    This function takes a 4-byte little-endian bytearray, converts it to an integer,
    increments the integer by 1 if it is less than 2147483646, and resets it to 0
    otherwise. The resulting integer is then converted back to a 4-byte little-endian
    bytearray and returned.
    Args:
        number (bytearray): A 4-byte little-endian bytearray representing the sequence number.
    Returns:
        bytearray: A 4-byte little-endian bytearray representing the incremented sequence number.
    """

    number = int.from_bytes(number, "little")
    if number < 2147483646:
        number += 1
    else:
        number = 0

    return int_to_4byte_array(number)


def get_bytearrays_size_sum(array: bytearray) -> int:
    """
    Calculates the total size (in bytes) of all bytearrays in the given iterable.
    Args:
        array (bytearray): An iterable containing bytearray objects.
    Returns:
        int: The sum of the sizes of all bytearrays in the iterable.
    """

    length = 0
    for bytearrays in enumerate(array):
        length += len(bytearrays[1])

    return length


def get_protocol_version() -> bytearray:
    """
    Retrieves the protocol version from the configuration file and returns it as a bytearray.

    The protocol version is composed of a major and minor version, both of which are read
    from the configuration file. Each version component is converted into a 1-byte array
    and concatenated to form the final protocol version.

    Returns:
        bytearray: A bytearray representing the protocol version, where the first byte is
                   the major version and the second byte is the minor version.
    """

    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["protocol_version_major"], 1)
    ) + int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["protocol_version_minor"], 1)
    )


def get_server_version() -> bytearray:
    """
    Retrieves the client version as a bytearray by reading the major and minor
    version numbers from the configuration file.

    The function reads the "client_version_major" and "client_version_minor"
    fields from the configuration file, converts them into 1-byte arrays, and
    concatenates them to form the complete version bytearray.

    Returns:
        bytearray: A bytearray representing the client version, where the first
        byte is the major version and the second byte is the minor version.
    """

    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["server_version_major"], 1)
    ) + int_to_1byte_array(json_data_reader(FILES.CONFIG, ["server_version_minor"], 1))


def get_bookshelf_version() -> bytearray:
    """
    Retrieves the bookshelf version as a bytearray by combining the major and minor version numbers.

    The function reads the major and minor version numbers from a configuration file using the
    `json_data_reader` function. Each version number is converted to a 1-byte array using the
    `int_to_1byte_array` function, and the results are concatenated to form the final bytearray.

    Returns:
        bytearray: A bytearray representing the bookshelf version, where the first byte is the
                   major version and the second byte is the minor version.
    """

    return int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["Bookshelf_version_major"], 1)
    ) + int_to_1byte_array(
        json_data_reader(FILES.CONFIG, ["Bookshelf_version_minor"], 1)
    )
