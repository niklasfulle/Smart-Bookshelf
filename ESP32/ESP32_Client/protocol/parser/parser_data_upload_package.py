"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_upload_package import data_upload_package
from utils.parse_helper import parse_data_start_end, get_data_string_array


def parse_data_upload_package(data: bytearray) -> data_upload_package:
    """
    Parses a data upload package from the given bytearray.
    This function extracts specific components from the input data, including
    the message type and the upload package data, by processing the data as a string
    and slicing it based on predefined indices.
    Args:
        data (bytearray): The raw data to be parsed, provided as a bytearray.
    Returns:
        data_upload_package: An instance of `data_upload_package` containing the
        parsed message type and upload package data.
    Raises:
        ValueError: If the input data is invalid or does not conform to the expected format.
    """

    data_str: str = get_data_string_array(data)

    message_type: bytearray = parse_data_start_end(data_str, 4, 2)
    upload_package_data: bytearray = parse_data_start_end(data_str, len(data), 4)

    return data_upload_package(message_type, upload_package_data)
