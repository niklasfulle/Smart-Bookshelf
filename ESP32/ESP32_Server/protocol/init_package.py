"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from protocol.constants.constants import (
    DATA_MESSAGE_TYPE,
    DATA_UPLOAD_MESSAGE_TYPE,
    PACKAGE_MESSAGE_TYPE,
)
from protocol.data_package import data_package
from protocol.data_upload_package import data_upload_package
from protocol.package import package
from utils.build_helper import (
    get_random_sequence_number,
    get_timestamp,
    increment_sequence_number,
)
from utils.converter import int_to_2byte_array, int_to_4byte_array


def initialize_package(
    message_type: PACKAGE_MESSAGE_TYPE,
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    data: bytearray,
) -> package:
    """
    -
    """

    if isinstance(message_type, int):
        message_type = int_to_2byte_array(message_type)

    if isinstance(receiver_id, int):
        receiver_id = int_to_4byte_array(receiver_id)

    if isinstance(sender_id, int):
        sender_id = int_to_4byte_array(sender_id)

    standard = [
        message_type,
        receiver_id,
        sender_id,
    ]

    if isinstance(sequence_number, int):
        if sequence_number == 0 and confirmed_sequence_number == 0:
            sequence_number = get_random_sequence_number()
        elif sequence_number == 0 and confirmed_sequence_number != 0:
            sequence_number = get_random_sequence_number()
        elif sequence_number != 0 and confirmed_sequence_number == 0:
            sequence_number = increment_sequence_number(sequence_number)

    elif isinstance(sequence_number, bytearray):
        if sequence_number == bytearray(b"\x00\x00\x00\x00"):
            sequence_number = get_random_sequence_number()
        else:
            sequence_number = increment_sequence_number(sequence_number)

    standard = standard + [sequence_number]

    if confirmed_sequence_number == 0:
        confirmed_sequence_number = int_to_4byte_array(0)

    standard = standard + [confirmed_sequence_number]

    if timestamp == 0 and confirmed_timestamp == 0:
        timestamp = get_timestamp()
        confirmed_timestamp = int_to_4byte_array(0)
    else:
        timestamp = get_timestamp()

    if isinstance(confirmed_timestamp, int):
        confirmed_timestamp = int_to_4byte_array(confirmed_timestamp)

    standard = standard + [timestamp, confirmed_timestamp]

    return package(*standard, data)


def initialize_data_package(
    message_type: DATA_MESSAGE_TYPE, data: bytearray
) -> data_package:
    """
    -
    """
    if isinstance(message_type, int):
        message_type = int_to_2byte_array(message_type)

    return data_package(message_type, data)


def initialize_data_upload_package(
    message_type: DATA_UPLOAD_MESSAGE_TYPE, data: bytearray
) -> data_upload_package:
    """
    -
    """
    if isinstance(message_type, int):
        message_type = int_to_2byte_array(message_type)

    return data_upload_package(message_type, data)
