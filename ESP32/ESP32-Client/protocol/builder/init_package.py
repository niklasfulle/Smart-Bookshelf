"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from package import package
from constants.constants import PACKAGE_MESSAGE_TYPE, DATA_MESSAGE_TYPE, DATA_UPLOAD_MESSAGE_TYPE
from data_package import data_package
from data_upload_package import data_upload_package
from utils.converter import int_to_2byte_array, int_to_4byte_array
from utils.build_helper import get_random_sequence_number, increment_sequence_number, get_timestamp

def initialize_package(
    message_type: PACKAGE_MESSAGE_TYPE,
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
    data: data_upload_package | data_package | bytearray | None,
) -> package | None:
    """
        - 
    """
    standard = [
        int_to_2byte_array(message_type),
        int_to_4byte_array(receiver_id),
        int_to_4byte_array(sender_id),
    ]

    if isinstance(sequence_number, int):
        if sequence_number == 0 and confirmed_sequence_number == 0:
            sequence_number = get_random_sequence_number()
        elif sequence_number == 0 and confirmed_sequence_number != 0:
            sequence_number = get_random_sequence_number()
        elif sequence_number != 0 and confirmed_sequence_number == 0:
            sequence_number = increment_sequence_number(sequence_number)

    elif isinstance(sequence_number, bytearray):
        sequence_number = increment_sequence_number(sequence_number)

    standard = standard + [int_to_4byte_array(sequence_number)]

    if confirmed_sequence_number == 0:
        confirmed_sequence_number = int_to_4byte_array(0)

    standard = standard + [int_to_4byte_array(confirmed_sequence_number)]

    if timestamp == 0 and confirmed_timestamp == 0:
        timestamp = get_timestamp()
        confirmed_timestamp = int_to_4byte_array(0)
    else:
        timestamp = get_timestamp()

    standard = standard + [int_to_4byte_array(timestamp), int_to_4byte_array(confirmed_timestamp)]

    return package(*standard, data)


def initialize_data_package(
    message_type: DATA_MESSAGE_TYPE,
    data: bytearray
) -> data_package:
    """
        - 
    """
    return data_package(message_type, data)

def initialize_data_upload_package(
    message_type: DATA_UPLOAD_MESSAGE_TYPE,
    data: bytearray
) -> data_upload_package | None:
    """
        - 
    """
    return data_upload_package(message_type, data)
