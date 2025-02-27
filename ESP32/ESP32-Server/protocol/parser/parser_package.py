"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from package import package
from data_package import data_package
from data_upload_package import data_upload_package
from utils.parse_helpers import parse_data_start_end
from utils.checksumme import get_checksumme
from protocol.parser.parser_data_package import parse_data_package
from protocol.parser.parser_data_upload_package import parse_data_upload_package

def parse_package (
    data: bytearray
) -> package | None:
    """
        - 
    """
    length: bytearray = int.from_bytes(parse_data_start_end(data, 2, 0))
    checksum = parse_data_start_end(data, length, length - 8)

    check = get_checksumme(parse_data_start_end(data, length - 8, 0), 1)

    if check == checksum:
        message_type: bytearray = parse_data_start_end(data, 4, 2)
        receiver_id: bytearray = parse_data_start_end(data, 8, 4)
        sender_id: bytearray = parse_data_start_end(data, 12, 8)

        sequence_number: bytearray = parse_data_start_end(data, 16, 12)
        confirmed_sequence_number: bytearray = parse_data_start_end(data, 20, 16)
        timestamp: bytearray = parse_data_start_end(data, 24, 20)
        confirmed_timestamp: bytearray = parse_data_start_end(data, 28, 24)

        if len(data) > 36:
            data: bytearray = parse_data_start_end(data, length - 8, 28)

            message_type_int = int.from_bytes(message_type)

            if message_type_int == 5000:
                data_package_data: data_package = parse_data_package(data)
                data = data_package_data
            elif message_type_int == 6000:
                data_upload_package_data: data_upload_package = parse_data_upload_package(data)
                data = data_upload_package_data

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
