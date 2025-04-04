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
    Initializes a package with the provided parameters and generates default values
    for certain fields if necessary.
    Args:
        message_type (PACKAGE_MESSAGE_TYPE or int): The type of the message. If an integer
            is provided, it will be converted to a 2-byte array.
        receiver_id (bytearray or int): The ID of the receiver. If an integer is provided,
            it will be converted to a 4-byte array.
        sender_id (bytearray or int): The ID of the sender. If an integer is provided,
            it will be converted to a 4-byte array.
        sequence_number (bytearray or int): The sequence number of the package. If it is
            0 or a 4-byte array of zeros, a random sequence number will be generated.
            Otherwise, it will be incremented.
        confirmed_sequence_number (bytearray or int): The confirmed sequence number. If it
            is 0, it will be set to a 4-byte array of zeros.
        timestamp (bytearray or int): The timestamp of the package. If both `timestamp` and
            `confirmed_timestamp` are 0, a new timestamp will be generated.
        confirmed_timestamp (bytearray or int): The confirmed timestamp. If it is an integer,
            it will be converted to a 4-byte array.
        data (bytearray): The payload data of the package.
    Returns:
        package: An instance of the `package` class initialized with the provided and
        generated values.
    Notes:
        - If `sequence_number` is 0 and `confirmed_sequence_number` is 0, a random sequence
          number is generated.
        - If `sequence_number` is not 0 but `confirmed_sequence_number` is 0, the sequence
          number is incremented.
        - If `timestamp` and `confirmed_timestamp` are both 0, a new timestamp is generated
          and `confirmed_timestamp` is set to a 4-byte array of zeros.
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
    Initializes a data package with the specified message type and data.
    Args:
        message_type (DATA_MESSAGE_TYPE): The type of the message. If an integer is provided,
                                          it will be converted to a 2-byte array.
        data (bytearray): The data to be included in the package.
    Returns:
        data_package: An instance of the data_package class containing the message type and data.
    """

    if isinstance(message_type, int):
        message_type = int_to_2byte_array(message_type)

    return data_package(message_type, data)


def initialize_data_upload_package(
    message_type: DATA_UPLOAD_MESSAGE_TYPE, data: bytearray
) -> data_upload_package:
    """
    Initializes a data upload package with the specified message type and data.
    Args:
        message_type (DATA_UPLOAD_MESSAGE_TYPE or int): The type of the message.
            If an integer is provided, it will be converted to a 2-byte array.
        data (bytearray): The data to be included in the package.
    Returns:
        data_upload_package: An instance of the data upload package containing
        the message type and data.
    """

    if isinstance(message_type, int):
        message_type = int_to_2byte_array(message_type)

    return data_upload_package(message_type, data)
