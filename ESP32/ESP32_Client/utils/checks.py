"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.package import package
from connection.connection import connection
from utils.build_helper import (
    get_protocol_version,
    get_client_version,
    get_bookshelf_version,
)


def handle_checks(_connection: connection, _package: package) -> bool:
    """
    -
    """
    if not check_for_valid_id(_connection, _package):
        print("check_for_valid_id")
        return False

    if not check_for_valid_message_type(_package):
        print(int.from_bytes(_package.message_type, "little"))
        print("check_for_valid_message_type")
        return False

    if not check_for_valid_message_type_moment(_connection, _package):
        print(int.from_bytes(_package.message_type, "little"))
        print("connection_request_send", _connection.connection_request_send)
        print("handshake", _connection.handshake)
        print("version_check", _connection.version_check)

        print("check_for_valid_message_type_moment")
        return False

    if not check_for_valid_sequence_number(_connection, _package):
        print("check_for_valid_sequence_number")
        return False

    return True


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


def check_for_valid_message_type(_package: package) -> bool:
    """
    -
    """

    message_type = _package.message_type

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


def check_for_valid_message_type_moment(
    _connection: connection, _package: package
) -> bool:
    """
    -
    """

    message_type = _package.message_type

    valid_types = []

    if isinstance(message_type, bytearray):
        message_type = int.from_bytes(message_type, "little")

    if (
        not _connection.connection_request_send
        and not _connection.handshake
        and not _connection.version_check
    ):
        valid_types = [
            PACKAGE_MESSAGE_TYPE.ConnResponse,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
        ]

    elif (
        _connection.connection_request_send
        and not _connection.handshake
        and not _connection.version_check
    ):
        valid_types = [
            PACKAGE_MESSAGE_TYPE.ConnResponse,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
            PACKAGE_MESSAGE_TYPE.DiscResponse,
        ]

    elif (
        _connection.connection_request_send
        and _connection.handshake
        and not _connection.version_check
    ):
        valid_types = [
            PACKAGE_MESSAGE_TYPE.VerResponse,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
            PACKAGE_MESSAGE_TYPE.DiscResponse,
        ]

    elif (
        _connection.connection_request_send
        and _connection.handshake
        and _connection.version_check
    ):
        valid_types = [
            PACKAGE_MESSAGE_TYPE.StatusRequest,
            PACKAGE_MESSAGE_TYPE.SleepRequest,
            PACKAGE_MESSAGE_TYPE.RebootRequest,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
            PACKAGE_MESSAGE_TYPE.DiscResponse,
            PACKAGE_MESSAGE_TYPE.Data,
            PACKAGE_MESSAGE_TYPE.DataUpload,
        ]

    if message_type in valid_types:
        return True

    return False


def check_for_valid_sequence_number(_connection: connection, _package: package) -> bool:
    """
    -
    """
    message_type = _package.message_type
    sequence_number = _package.sequence_number
    confirmed_sequence_number = _package.confirmed_sequence_number
    last_send_package_sequence_number = None
    last_received_package_sequence_number = None

    if _connection.last_send_package is not None:
        last_send_package_sequence_number = int.from_bytes(
            _connection.last_send_package.sequence_number, "little"
        )

    if _connection.last_received_package is not None:
        last_received_package_sequence_number = int.from_bytes(
            _connection.last_received_package.sequence_number, "little"
        )

    if isinstance(message_type, bytearray):
        message_type = int.from_bytes(message_type, "little")

    if isinstance(sequence_number, bytearray):
        sequence_number = int.from_bytes(sequence_number, "little")

    if isinstance(confirmed_sequence_number, bytearray):
        confirmed_sequence_number = int.from_bytes(confirmed_sequence_number, "little")

    if message_type == PACKAGE_MESSAGE_TYPE.ConnRequest:
        if sequence_number != 0 and confirmed_sequence_number == 0:
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.ConnResponse:
        if (
            sequence_number != 0
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.ConnApprove:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.VerRequest:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.VerResponse:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.StatusRequest:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.StatusResponse:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.SleepRequest:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.SleepResponse:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.RebootRequest:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.RebootResponse:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    elif message_type == PACKAGE_MESSAGE_TYPE.DiscRequest:
        return True

    elif message_type == PACKAGE_MESSAGE_TYPE.Data:
        return True

    elif message_type == PACKAGE_MESSAGE_TYPE.DataUpload:
        return True

    else:
        if (
            sequence_number == last_received_package_sequence_number
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    return False


def check_versions(_package: package) -> bool:
    """
    -
    """
    package_data: bytearray = _package.data

    if package_data[0:2] != get_protocol_version():
        return False

    if package_data[2:4] != get_client_version():
        return False

    if package_data[4:6] != get_bookshelf_version():
        return False

    return True
