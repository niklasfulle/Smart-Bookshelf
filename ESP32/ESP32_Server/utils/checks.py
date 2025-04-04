"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.package import package
from connection.connection import connection


def handle_checks(_connection: connection, _package: package) -> bool:
    """
    Performs a series of validation checks on the provided connection and package.
    This function sequentially verifies the validity of the ID, message type,
    message type moment, and sequence number associated with the given connection
    and package. If any of these checks fail, the function prints the name of the
    failed check and returns False. If all checks pass, it returns True.
    Args:
        _connection (connection): The connection object to validate.
        _package (package): The package object to validate.
    Returns:
        bool: True if all checks pass, False otherwise.
    """

    if not check_for_valid_id(_connection, _package):
        print("check_for_valid_id")
        return False

    if not check_for_valid_message_type(_package):
        print("check_for_valid_message_type")
        return False

    if not check_for_valid_message_type_moment(_connection, _package):
        print("check_for_valid_message_type_moment")
        return False

    if not check_for_valid_sequence_number(_connection, _package):
        print("check_for_valid_sequence_number")
        return False

    return True


def check_for_valid_id(_connection: connection, _package: package) -> bool:
    """
    Validates whether the sender and receiver IDs in the given package match the
    expected client and server IDs from the connection.
    Args:
        _connection (connection): The connection object containing the client
            (receiver) and server (sender) IDs as integers.
        _package (package): The package object containing the sender and receiver
            IDs, which may be integers or bytearrays.
    Returns:
        bool: True if the package sender ID matches the client ID and the package
        receiver ID matches the server ID, otherwise False.
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
    Checks if the message type of the given package is valid.
    Args:
        _package (package): The package object containing a message_type attribute.
    Returns:
        bool: True if the message type is valid, False otherwise.
    Notes:
        - The function supports message_type as either an integer or a bytearray.
        - If message_type is a bytearray, it is converted to an integer using little-endian format.
        - Valid message types are defined in the PACKAGE_MESSAGE_TYPE enumeration.
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
    Validates whether the message type of a given package is valid based on the
    current state of the connection.
    The function determines the valid message types by evaluating the state of
    the connection, which is defined by the attributes `connection_request_send`,
    `handshake`, and `version_check`. It then checks if the message type of the
    provided package is within the list of valid types for the current state.
    Args:
        _connection (connection): The connection object representing the current
            state of the connection.
        _package (package): The package object containing the message type to be
            validated.
    Returns:
        bool: True if the message type is valid for the current connection state,
        False otherwise.
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
        print(1)
        valid_types = [
            PACKAGE_MESSAGE_TYPE.ConnRequest,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
        ]

    elif (
        _connection.connection_request_send
        and not _connection.handshake
        and not _connection.version_check
    ):
        print(2)
        valid_types = [
            PACKAGE_MESSAGE_TYPE.ConnApprove,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
            PACKAGE_MESSAGE_TYPE.DiscResponse,
        ]

    elif (
        _connection.connection_request_send
        and _connection.handshake
        and not _connection.version_check
    ):
        print(3)
        valid_types = [
            PACKAGE_MESSAGE_TYPE.VerRequest,
            PACKAGE_MESSAGE_TYPE.DiscRequest,
            PACKAGE_MESSAGE_TYPE.DiscResponse,
        ]

    elif (
        _connection.connection_request_send
        and _connection.handshake
        and _connection.version_check
    ):
        print(4)
        valid_types = [
            PACKAGE_MESSAGE_TYPE.StatusResponse,
            PACKAGE_MESSAGE_TYPE.SleepResponse,
            PACKAGE_MESSAGE_TYPE.RebootResponse,
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
    Validates the sequence number and confirmed sequence number of a package
    based on the message type and the connection's last sent and received packages.
    Args:
        _connection (connection): The connection object containing information
            about the last sent and received packages.
        _package (package): The package object containing the message type,
            sequence number, and confirmed sequence number.
    Returns:
        bool: True if the sequence number and confirmed sequence number are valid
            for the given message type, otherwise False.
    Message Types:
        - PACKAGE_MESSAGE_TYPE.ConnRequest: Valid if sequence_number is 0 and
          confirmed_sequence_number is 0.
        - PACKAGE_MESSAGE_TYPE.ConnResponse: Valid if sequence_number is not 0 and
          confirmed_sequence_number matches the last sent package's sequence number.
        - PACKAGE_MESSAGE_TYPE.ConnApprove: Valid if sequence_number matches the
          last received package's sequence number and confirmed_sequence_number matches
          the last sent package's sequence number.
        - PACKAGE_MESSAGE_TYPE.VerRequest, VerResponse, StatusRequest, StatusResponse,
          SleepRequest, SleepResponse, RebootRequest, RebootResponse: Valid if
          sequence_number matches the last received package's sequence number and
          confirmed_sequence_number matches the last sent package's sequence number.
        - PACKAGE_MESSAGE_TYPE.DiscRequest, Data, DataUpload: Always valid.
        - Other message types: Valid if sequence_number is one greater than the
          last received package's sequence number and confirmed_sequence_number matches
          the last sent package's sequence number.
    """

    message_type = int.from_bytes(_package.message_type, "little")
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
            sequence_number == last_received_package_sequence_number + 1
            and confirmed_sequence_number == last_send_package_sequence_number
        ):
            return True

    return False
