"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.package import package
from protocol.data_package import data_package
from protocol.data_upload_package import data_upload_package
from protocol.parser.parser_data_package import parse_data_package
from protocol.parser.parser_data_upload_package import parse_data_upload_package
from utils.parse_helper import parse_data_start_end, get_data_string_array
from utils.checksumme import get_checksumme


def parse_package(data: bytearray) -> package:
    """
    Parses a given bytearray into a `package` object if the checksum is valid.
    Args:
        data (bytearray): The raw bytearray data to be parsed.
    Returns:
        package: A `package` object containing parsed data fields if the checksum is valid.
        None: If the checksum validation fails.
    The function performs the following steps:
    1. Converts the bytearray into a string array for easier manipulation.
    2. Extracts the length of the package, checksum, and validates the checksum.
    3. If the checksum is valid, extracts the following fields:
        - message_type: The type of the message.
        - receiver_id: The ID of the receiver.
        - sender_id: The ID of the sender.
        - sequence_number: The sequence number of the message.
        - confirmed_sequence_number: The confirmed sequence number.
        - timestamp: The timestamp of the message.
        - confirmed_timestamp: The confirmed timestamp.
    4. If the data length exceeds 36 bytes, processes the data field based on the message type:
        - For message type 5000, parses the data as a `data_package`.
        - For message type 6000, parses the data as a `data_upload_package`.
    5. Returns a `package` object with all the parsed fields or `None` if the checksum is invalid.
    """

    data_str: str = get_data_string_array(data)

    length = int.from_bytes(parse_data_start_end(data_str, 1, 0), "little")

    checksum = parse_data_start_end(data_str, length, length - 8)

    check = get_checksumme(parse_data_start_end(data_str, length - 8, 0), 1)

    if check == checksum:
        message_type: bytearray = parse_data_start_end(data_str, 4, 2)
        receiver_id: bytearray = parse_data_start_end(data_str, 8, 4)
        sender_id: bytearray = parse_data_start_end(data_str, 12, 8)

        sequence_number: bytearray = parse_data_start_end(data_str, 16, 12)
        confirmed_sequence_number: bytearray = parse_data_start_end(data_str, 20, 16)
        timestamp: bytearray = parse_data_start_end(data_str, 24, 20)
        confirmed_timestamp: bytearray = parse_data_start_end(data_str, 28, 24)

        if len(data) > 36:
            data: bytearray = parse_data_start_end(data_str, length - 8, 28)

            message_type_int = int.from_bytes(message_type, "little")

            if message_type_int == 5000:
                data_package_data: data_package = parse_data_package(data)
                data = data_package_data.complete_data
            elif message_type_int == 6000:
                data_upload_package_data: data_upload_package = (
                    parse_data_upload_package(data)
                )
                data = data_upload_package_data.complete_data
        else:
            data = None

        return package(
            message_type,
            receiver_id,
            sender_id,
            sequence_number,
            confirmed_sequence_number,
            timestamp,
            confirmed_timestamp,
            data,
        )

    return None
