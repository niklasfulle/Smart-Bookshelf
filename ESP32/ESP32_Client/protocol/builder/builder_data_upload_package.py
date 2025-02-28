"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.data_upload_package import data_upload_package
from protocol.init_package import initialize_data_upload_package
from protocol.constants.constants import DATA_UPLOAD_MESSAGE_TYPE


def build_data_upload_package_data(
    package_number: bytearray, datapackage: bytearray
) -> data_upload_package:
    """
    -
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUp, (package_number + datapackage)
    )


def build_data_upload_package_data_start(datatype: bytearray) -> data_upload_package:
    """
    -
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpStart, datatype
    )


def build_data_upload_package_data_end() -> data_upload_package:
    """
    -
    """

    return initialize_data_upload_package(
        DATA_UPLOAD_MESSAGE_TYPE.DataUpCompleted, None
    )


def build_data_upload_package_data_error(
    error: bytearray,
) -> data_upload_package:
    """
    -
    """

    return initialize_data_upload_package(DATA_UPLOAD_MESSAGE_TYPE.DataUpError, error)


def build_data_upload_package_data_cancel() -> data_upload_package:
    """
    -
    """

    return initialize_data_upload_package(DATA_UPLOAD_MESSAGE_TYPE.DataUpCancel, None)
