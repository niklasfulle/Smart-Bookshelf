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

def parse_package (
    data: bytearray
) -> package:
    """
        - 
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
            data_str: str = get_data_string_array(data)
            message_type_int = int.from_bytes(message_type, "little")

            if message_type_int == 5000:
                data_package_data: data_package = parse_data_package(data_str)
                data = data_package_data.complete_data
            elif message_type_int == 6000:
                data_upload_package_data: data_upload_package = parse_data_upload_package(data_str)
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
            data
        )

    return None
