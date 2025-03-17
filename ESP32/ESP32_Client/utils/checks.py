"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.package import package
from connection.connection import connection


def check_for_valid_id(_connection: connection, _package: package) -> bool:
    """
    -
    """
    client_id = _connection.receiver_id_int
    server_id = _connection.sender_id_int
    package_sender_id = _package.sender_id
    package_reciver_id = _package.receiver_id

    if isinstance(package_sender_id, bytearray):
        package_sender_id = int.from_bytes(package_sender_id, "little")

    if isinstance(package_reciver_id, bytearray):
        package_reciver_id = int.from_bytes(package_reciver_id, "little")

    if package_sender_id == client_id and package_reciver_id == server_id:
        return True

    return False


def check_for_valid_message_type(message_type: PACKAGE_MESSAGE_TYPE) -> bool:
    """
    -
    """

    valid_types = [
        PACKAGE_MESSAGE_TYPE.ConnRequest,
        PACKAGE_MESSAGE_TYPE.ConnResponse,
        PACKAGE_MESSAGE_TYPE.ConnApprove,
        PACKAGE_MESSAGE_TYPE.VerRequest,
        PACKAGE_MESSAGE_TYPE.VerResponse,
        PACKAGE_MESSAGE_TYPE.StatusRequest,
        PACKAGE_MESSAGE_TYPE.StatusResponse,
        PACKAGE_MESSAGE_TYPE.DiscRequest,
        PACKAGE_MESSAGE_TYPE.DiscResponse,
        PACKAGE_MESSAGE_TYPE.SleepRequest,
        PACKAGE_MESSAGE_TYPE.SleepResponse,
        PACKAGE_MESSAGE_TYPE.RebootRequest,
        PACKAGE_MESSAGE_TYPE.RebootResponse,
        PACKAGE_MESSAGE_TYPE.Data,
        PACKAGE_MESSAGE_TYPE.DataUpload,
    ]

    if isinstance(message_type, bytearray):
        message_type = int.from_bytes(message_type, "little")

    if message_type in valid_types:
        return True

    return False


def check_for_valid_sequence_number() -> bool:
    """
    -
    """
    return False
