"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from package import package
from init_package import initialize_package
from data_package import data_package
from data_upload_package import data_upload_package
from constants.constants import PACKAGE_MESSAGE_TYPE

def build_connection_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_connection_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_connection_approve (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnApprove,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_version_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.VerRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_version_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
    protocol_version: bytearray,
    config_version: bytearray,
    control_version: bytearray
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.VerResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        (protocol_version + config_version + control_version)
    )


def build_status_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.StatusRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_status_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.StatusResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_disconnection_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DiscRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_disconnection_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DiscResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_sleep_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.SleepRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_sleep_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.SleepResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_reboot_request (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.RebootRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_reboot_response (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.RebootResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None
    )


def build_data (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
    data: data_package
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.Data,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        data
    )


def build_upload_data  (
    receiver_id: int,
    sender_id: int,
    sequence_number: int,
    confirmed_sequence_number: int,
    timestamp: int,
    confirmed_timestamp: int,
    data: data_upload_package
) -> package:
    """
        - 
    """
    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DataUpload,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        data
    )
