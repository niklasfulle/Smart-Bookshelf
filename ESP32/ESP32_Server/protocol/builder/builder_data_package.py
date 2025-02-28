"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_package import data_package
from protocol.init_package import initialize_data_package
from protocol.constants.constants import DATA_MESSAGE_TYPE


def build_data_package_light_on() -> data_package:
    """
    -
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowOnLight, None)


def build_data_package_light_off() -> data_package:
    """
    -
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowOffLight, None)


def build_data_package_book(data: bytearray) -> data_package:
    """
    -
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowBook, data)


def build_data_package_books(data: bytearray) -> data_package:
    """
    -
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowBooks, data)


def build_data_package_mode(data: bytearray) -> data_package:
    """
    -
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.LightMode, data)
