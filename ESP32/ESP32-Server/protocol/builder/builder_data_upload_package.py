"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from data_upload_package import data_upload_package
from utils.build_helper import get_bytearrays_size_sum
from utils.converter import int_to_2byte_array
from builder.init_package import initialize_data_upload_package

def build_data_upload_package_upload_data_start (
    message_type: bytearray,
    datatype: bytearray
) -> data_upload_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, datatype])

    return initialize_data_upload_package(int_to_2byte_array(lenght), message_type, datatype)


def build_data_package_upload_data (
    message_type: bytearray,
    package_number: bytearray,
    datapackage: bytearray
) -> data_upload_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, package_number, datapackage])

    return initialize_data_upload_package(int_to_2byte_array(lenght), message_type, None)


def build_data_upload_package_upload_data_end (
    message_type: bytearray
) -> data_upload_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type])

    return initialize_data_upload_package(int_to_2byte_array(lenght), message_type, None)


def build_data_upload_package_upload_data_error (
    message_type: bytearray,
    error: bytearray,
) -> data_upload_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type, error])

    return initialize_data_upload_package(int_to_2byte_array(lenght), message_type, error)


def build_data_upload_package_upload_data_cancel (
    message_type: bytearray
) -> data_upload_package:
    """
        - 
    """
    lenght = get_bytearrays_size_sum([message_type])

    return initialize_data_upload_package(int_to_2byte_array(lenght), message_type, None)
