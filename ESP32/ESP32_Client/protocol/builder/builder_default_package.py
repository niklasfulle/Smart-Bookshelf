"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from protocol.constants.constants import PACKAGE_MESSAGE_TYPE
from protocol.init_package import initialize_package
from protocol.package import package


def build_connection_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a connection request package with the specified parameters.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The current sequence number for the package.
        confirmed_sequence_number (bytearray): The last confirmed sequence number.
        timestamp (bytearray): The current timestamp of the request.
        confirmed_timestamp (bytearray): The last confirmed timestamp.

    Returns:
        package: A connection request package initialized with the provided parameters.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_connection_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a connection response package with the specified parameters.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number being acknowledged.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp being acknowledged.

    Returns:
        package: A connection response package initialized with the provided parameters.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_connection_approve(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a connection approval package.

    This function initializes a package with the message type `ConnApprove`
    and includes the provided parameters to facilitate communication between
    the sender and receiver.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.

    Returns:
        package: A package object containing the connection approval message.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.ConnApprove,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_version_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a version request package for communication between devices.

    Args:
        receiver_id (bytearray): The unique identifier of the receiving device.
        sender_id (bytearray): The unique identifier of the sending device.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number of the last confirmed message.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp of the last confirmed message.

    Returns:
        package: A package object representing the version request message.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.VerRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_version_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    protocol_version: bytearray,
    config_version: bytearray,
    control_version: bytearray,
) -> package:
    """
    Constructs a version response package with the provided parameters.

    Args:
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the message.
        confirmed_sequence_number (bytearray): The confirmed sequence number.
        timestamp (bytearray): The timestamp of the message.
        confirmed_timestamp (bytearray): The confirmed timestamp.
        protocol_version (bytearray): The protocol version information.
        config_version (bytearray): The configuration version information.
        control_version (bytearray): The control version information.

    Returns:
        package: A package object representing the version response message.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.VerResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        (protocol_version + config_version + control_version),
    )


def build_status_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a status request package with the provided parameters.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The current sequence number of the message.
        confirmed_sequence_number (bytearray): The last confirmed sequence number.
        timestamp (bytearray): The current timestamp of the message.
        confirmed_timestamp (bytearray): The last confirmed timestamp.

    Returns:
        package: A package object representing the status request message.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.StatusRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_status_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    status: bytearray,
) -> package:
    """
    Constructs a status response package with the specified parameters.

    Args:
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.
        status (bytearray): The status information to include in the package.

    Returns:
        package: The constructed status response package.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.StatusResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        status,
    )


def build_disconnection_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    reason: bytearray,
) -> package:
    """
    Constructs a disconnection request package.

    This function initializes and returns a package representing a
    disconnection request. The package contains metadata about the
    sender, receiver, sequence numbers, timestamps, and the reason
    for the disconnection.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.
        reason (bytearray): The reason for the disconnection.

    Returns:
        package: A package object representing the disconnection request.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DiscRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        reason,
    )


def build_disconnection_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    reason: bytearray,
) -> package:
    """
    Constructs a disconnection response package.

    This function initializes and returns a package of type `DiscResponse`
    with the provided parameters. It is used to communicate a disconnection
    response between devices.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.
        reason (bytearray): The reason for the disconnection.

    Returns:
        package: A package object representing the disconnection response.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DiscResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        reason,
    )


def build_sleep_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a SleepRequest package using the provided parameters.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.

    Returns:
        package: A SleepRequest package initialized with the provided parameters.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.SleepRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_sleep_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a SleepResponse package with the specified parameters.

    Args:
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the package.
        confirmed_sequence_number (bytearray): The confirmed sequence number.
        timestamp (bytearray): The timestamp of the package.
        confirmed_timestamp (bytearray): The confirmed timestamp.

    Returns:
        package: The initialized SleepResponse package.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.SleepResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_reboot_request(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a reboot request package.

    This function initializes a package with the message type `RebootRequest`
    and the provided parameters. It is used to request a reboot from the receiver.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current message.
        confirmed_sequence_number (bytearray): The sequence number of the last confirmed message.
        timestamp (bytearray): The timestamp of the current message.
        confirmed_timestamp (bytearray): The timestamp of the last confirmed message.

    Returns:
        package: A package object representing the reboot request.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.RebootRequest,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_reboot_response(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
) -> package:
    """
    Constructs a reboot response package with the specified parameters.

    Args:
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the message.
        confirmed_sequence_number (bytearray): The sequence number being confirmed.
        timestamp (bytearray): The timestamp of the message.
        confirmed_timestamp (bytearray): The timestamp being confirmed.

    Returns:
        package: The constructed reboot response package.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.RebootResponse,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        None,
    )


def build_data(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    data: bytearray,
) -> package:
    """
    Builds a data package with the specified parameters.

    Args:
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the package.
        confirmed_sequence_number (bytearray): The confirmed sequence number.
        timestamp (bytearray): The timestamp of the package.
        confirmed_timestamp (bytearray): The confirmed timestamp.
        data (bytearray): The data payload to include in the package.

    Returns:
        package: The constructed data package.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.Data,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        data,
    )


def build_upload_data(
    receiver_id: bytearray,
    sender_id: bytearray,
    sequence_number: bytearray,
    confirmed_sequence_number: bytearray,
    timestamp: bytearray,
    confirmed_timestamp: bytearray,
    data: bytearray,
) -> package:
    """
    Constructs and initializes a data upload package with the specified parameters.

    Args:
        receiver_id (bytearray): The unique identifier of the receiver.
        sender_id (bytearray): The unique identifier of the sender.
        sequence_number (bytearray): The sequence number of the current package.
        confirmed_sequence_number (bytearray): The last confirmed sequence number.
        timestamp (bytearray): The timestamp of the current package.
        confirmed_timestamp (bytearray): The last confirmed timestamp.
        data (bytearray): The payload data to be included in the package.

    Returns:
        package: The initialized data upload package.
    """

    return initialize_package(
        PACKAGE_MESSAGE_TYPE.DataUpload,
        receiver_id,
        sender_id,
        sequence_number,
        confirmed_sequence_number,
        timestamp,
        confirmed_timestamp,
        data,
    )
