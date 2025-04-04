"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_package import data_package
from utils.parse_helper import parse_data_start_end, get_data_string_array


def parse_data_package(data: bytearray) -> data_package:
    """
    Parses a data package from a given bytearray.
    Args:
        data (bytearray): The raw data to be parsed.
    Returns:
        data_package: An object containing the parsed message type and upload package data.
    Raises:
        ValueError: If the data cannot be parsed correctly.
    Notes:
        - The function extracts the message type and upload package data from the input.
        - It assumes the data format adheres to specific start and end indices for parsing.
    """

    data_str: str = get_data_string_array(data)

    message_type: bytearray = parse_data_start_end(data_str, 4, 2)
    upload_package_data: bytearray = parse_data_start_end(data_str, len(data), 4)

    return data_package(message_type, upload_package_data)
