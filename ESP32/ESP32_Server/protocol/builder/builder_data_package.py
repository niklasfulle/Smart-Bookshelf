"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_package import data_package
from protocol.init_package import initialize_data_package
from protocol.constants.constants import DATA_MESSAGE_TYPE


def build_data_package_light_on() -> data_package:
    """
    Constructs and returns a data package indicating that the light should be turned on.

    This function initializes a data package with the message type `ShowOnLight`
    and no additional payload.

    Returns:
        data_package: A data package object with the `ShowOnLight` message type.
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowOnLight, None)


def build_data_package_light_off() -> data_package:
    """
    Constructs and returns a data package indicating that the light should be turned off.

    This function initializes a data package with the message type `ShowOffLight`
    and no additional payload.

    Returns:
        data_package: A data package object with the `ShowOffLight` message type.
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowOffLight, None)


def build_data_package_book(data: bytearray) -> data_package:
    """
    Constructs a data package for transmitting book-related information.

    Args:
        data (bytearray): The data to be included in the package, typically representing book information.

    Returns:
        data_package: A data package object initialized with the specified data and the message type `ShowBook`.
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowBook, data)


def build_data_package_books(data: bytearray) -> data_package:
    """
    Constructs a data package containing book information.

    This function initializes a data package with the specified data
    and assigns it the message type `ShowBooks`.

    Args:
        data (bytearray): The data to be included in the data package,
                          typically representing book information.

    Returns:
        data_package: A data package object initialized with the
                      `ShowBooks` message type and the provided data.
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.ShowBooks, data)


def build_data_package_mode(data: bytearray) -> data_package:
    """
    Constructs a data package for the LightMode message type.

    Args:
        data (bytearray): The payload data to be included in the data package.

    Returns:
        data_package: A data package object initialized with the LightMode message type and the provided data.
    """

    return initialize_data_package(DATA_MESSAGE_TYPE.LightMode, data)

