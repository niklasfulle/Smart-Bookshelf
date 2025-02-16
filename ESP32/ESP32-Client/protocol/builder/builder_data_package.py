"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from data_package import data_package
from utils.build_helper import get_bytearrays_size_sum
from utils.converter import int_to_2byte_array
from builder.init_package import initialize_data_package

def build_data_package_light_on (
    message_type: bytearray
) -> data_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type])

    return initialize_data_package(int_to_2byte_array(lenght), message_type, None)


def build_data_package_light_off (
    message_type: bytearray
) -> data_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type])

    return initialize_data_package(int_to_2byte_array(lenght), message_type, None)


def build_data_package_book (
    message_type: bytearray,
    data: bytearray
) -> data_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, data])

    return initialize_data_package(int_to_2byte_array(lenght), message_type, data)


def build_data_package_books (
    message_type: bytearray,
    data: bytearray
) -> data_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, data])

    return initialize_data_package(int_to_2byte_array(lenght), message_type, data)


def build_data_package_mode (
    message_type: bytearray,
    data: bytearray
) -> data_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, data])

    return initialize_data_package(int_to_2byte_array(lenght), message_type, data)
