"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_upload_package import data_upload_package
from protocol.init_package import initialize_data_upload_package
from protocol.constants.constants import DATA_UPLOAD_MESSAGE_TYPE


def build_data_upload_package_data_start(datatype: bytearray) -> data_upload_package:
    """
    Constructs and initializes a data upload package with the "DataUpStart" message type.

    Args:
        datatype (bytearray): The type of data to be included in the upload package.

    Returns:
        data_upload_package: An initialized data upload package with the specified message type and data type.
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpStart, datatype
    )


def build_data_upload_package_data_request(datatype: bytearray) -> data_upload_package:
    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpRequest, datatype
    )


def build_data_upload_package_data_response(datatype: bytearray) -> data_upload_package:
    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpResponse, datatype
    )


def build_data_upload_package_data(
    package_number: bytearray, datapackage: bytearray
) -> data_upload_package:
    """
    Constructs a data upload package by combining the package number and data package.

    Args:
        package_number (bytearray): The bytearray representing the package number.
        datapackage (bytearray): The bytearray containing the data to be uploaded.

    Returns:
        data_upload_package: An initialized data upload package object containing the
        combined package number and data package.
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUp, (package_number + datapackage)
    )


def build_data_upload_package_data_confirm(
    package_number: bytearray,
) -> data_upload_package:
    """
    Constructs a data upload package with a "DataConfirm" message type.

    Args:
        package_number (bytearray): The package number to include in the data upload package.

    Returns:
        data_upload_package: The constructed data upload package with the specified message type and package number.
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataConfirm, (package_number)
    )


def build_data_upload_package_data_end() -> data_upload_package:
    """
    Builds a data upload package indicating the end of a data upload process.

    Returns:
        data_upload_package: An instance of `data_upload_package` initialized with
        the `DataUpCompleted` message type and no additional data.
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpCompleted, None
    )


def build_data_upload_package_data_error(
    error: bytearray,
) -> data_upload_package:
    """
    Constructs a data upload package with an error message.

    Args:
        error (bytearray): The error data to be included in the package.

    Returns:
        data_upload_package: A data upload package initialized with the
        error message type and the provided error data.
    """

    return initialize_data_upload_package(DATA_UPLOAD_MESSAGE_TYPE.DataUpError, error)


def build_data_upload_package_data_cancel() -> data_upload_package:
    """
    Builds a data upload package with a cancellation message type.

    This function creates and initializes a `data_upload_package` object
    with the `DataUpCancel` message type, indicating that the data upload
    process should be canceled. The payload for this package is set to `None`.

    Returns:
        data_upload_package: An instance of `data_upload_package` initialized
        with the cancellation message type.
    """

    return initialize_data_upload_package(DATA_UPLOAD_MESSAGE_TYPE.DataUpCancel, None)
