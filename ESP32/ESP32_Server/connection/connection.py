"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
import socket
from hardware.bookshelf import bookshelf
from protocol.package import package
from protocol.constants.constants import STATUS
from utils.converter import int_to_4byte_array
from datatype.task import task


class connection:
    """
    The `connection` class represents a network connection between a client and a server
    using the UDP protocol. It manages the state of the connection, handles data transfer,
    and provides methods for sending and receiving messages.
    Attributes:
        sock (socket): The UDP socket used for communication.
        client (tuple[str, int]): The client's address and port.
        server (tuple[str, int]): The server's address and port.
        receiver_id_int (int): The integer representation of the receiver's ID.
        sender_id_int (int): The integer representation of the sender's ID.
        receiver_id (bytearray): The receiver's ID in bytearray format.
        sender_id (bytearray): The sender's ID in bytearray format.
        bookshelf_object (bookshelf): The bookshelf object associated with the connection.
        last_send_package (package): The last package sent over the connection.
        last_received_package (package): The last package received over the connection.
        status (STATUS): The current status of the connection.
        handshake (bool): Indicates whether the handshake process is complete.
        connection_request_send (bool): Tracks if a connection request has been sent.
        version_check (bool): Tracks if the version check has been performed.
        status_request_send (bool): Tracks if a status request has been sent.
        _task (task): Holds the current task being processed.
        _wait_for_task_response (bool): Indicates if waiting for a task response.
        waiting_count (int): Counter for general waiting operations.
        status_request_waiting_count (int): Counter for status request waiting operations.
        data_send_mode (bool): Indicates if the connection is in data send mode.
        data_reveiv_mode (bool): Indicates if the connection is in data receive mode.
        data_to_send (list): Holds the data to be sent.
        data_to_reveiv (bytearray): Holds the data to be received.
        timeout_counter (int): Tracks the number of timeout occurrences.
    Methods:
        __init__(client, server, receiver_id, sender_id, Bookshelf_object):
            Initializes a new connection object with the specified client, server, and IDs.
        reset() -> None:
        send_message(msg: bytearray, addressPort: tuple[str, int]) -> None:
        send_message_to_client(_package: package) -> None:
        send_message_to_server(_package: package) -> None:
        print_info() -> None:
    """

    sock: socket
    client: tuple[str, int]
    server: tuple[str, int]
    receiver_id_int: int
    sender_id_int: int
    receiver_id: bytearray
    sender_id: bytearray
    bookshelf_object: bookshelf
    last_send_package: package
    last_received_package: package
    status: STATUS
    handshake: bool
    connection_request_send: bool
    version_check: bool
    status_request_send: bool
    _task: task
    _wait_for_task_response: bool

    waiting_count: int
    status_request_waiting_count: int

    data_send_mode: bool
    data_reveiv_mode: bool

    data_to_send: list
    data_to_reveiv: bytearray

    timeout_counter: int

    def __init__(
        self,
        client: tuple[str, int],
        server: tuple[str, int],
        receiver_id: int,
        sender_id: int,
        Bookshelf_object: bookshelf,
    ):
        """
        Initializes a connection object for managing communication between a client and a server.
        Args:
            client (tuple[str, int]): A tuple containing the client's IP address and port.
            server (tuple[str, int]): A tuple containing the server's IP address and port.
            receiver_id (int): The unique identifier for the receiver.
            sender_id (int): The unique identifier for the sender.
            Bookshelf_object (bookshelf): An instance of the bookshelf object to manage bookshelf-related operations.
        Attributes:
            sock (socket.socket): The UDP socket used for communication.
            client (tuple[str, int]): The client's IP address and port.
            server (tuple[str, int]): The server's IP address and port.
            receiver_id_int (int): The receiver's unique identifier as an integer.
            sender_id_int (int): The sender's unique identifier as an integer.
            receiver_id (bytes): The receiver's unique identifier as a 4-byte array.
            sender_id (bytes): The sender's unique identifier as a 4-byte array.
            bookshelf_object (bookshelf): The bookshelf object instance.
            last_send_package (Any): The last package sent.
            last_received_package (Any): The last package received.
            status (STATUS): The current connection status.
            handshake (bool): Indicates whether the handshake process is complete.
            connection_request_send (bool): Indicates whether a connection request has been sent.
            version_check (bool): Indicates whether the version check is complete.
            status_request_send (bool): Indicates whether a status request has been sent.
            _task (Any): The current task being processed.
            _wait_for_task_response (bool): Indicates whether the system is waiting for a task response.
            _wait_for_task_response_count (int): Counter for task response waiting attempts.
            waiting_count (int): Counter for general waiting attempts.
            status_request_waiting_count (int): Counter for status request waiting attempts.
            data_send_mode (bool): Indicates whether the system is in data send mode.
            data_reveiv_mode (bool): Indicates whether the system is in data receive mode.
            data_to_send (Any): The data to be sent.
            data_to_reveiv (Any): The data to be received.
            timeout_counter (int): Counter for timeout occurrences.
        Raises:
            OSError: If the socket binding to the server address fails.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = client
        self.server = server
        self.receiver_id_int = receiver_id
        self.sender_id_int = sender_id
        self.receiver_id = int_to_4byte_array(receiver_id)
        self.sender_id = int_to_4byte_array(sender_id)
        self.bookshelf_object = Bookshelf_object

        self.last_send_package = None
        self.last_received_package = None

        self.status = STATUS.OFFLINE

        self.handshake = False
        self.connection_request_send = False
        self.version_check = False
        self.status_request_send = False
        self._task = None
        self._wait_for_task_response = False
        self._wait_for_task_response_count = 0

        self.waiting_count = 0
        self.status_request_waiting_count = 0

        self.data_send_mode = False
        self.data_reveiv_mode = False

        self.data_to_send = None
        self.data_to_reveiv = None

        self.timeout_counter = 0

        self.sock.bind((self.server[0], self.server[1]))

    def reset(self) -> None:
        """
        Resets the connection state to its initial values.
        This method reinitializes all attributes related to the connection state,
        including handshake status, connection requests, version checks, task
        management, status, data transfer modes, and timeout counters. It ensures
        that the connection object is ready for a fresh start.
        Attributes Reset:
            - handshake: Indicates whether the handshake process is complete.
            - connection_request_send: Tracks if a connection request has been sent.
            - version_check: Tracks if the version check has been performed.
            - status_request_send: Tracks if a status request has been sent.
            - _task: Holds the current task being processed.
            - _wait_for_task_response: Indicates if waiting for a task response.
            - _wait_for_task_response_count: Counter for task response waiting attempts.
            - status: Represents the current connection status (default: STATUS.OFFLINE).
            - waiting_count: Counter for general waiting operations.
            - status_request_waiting_count: Counter for status request waiting operations.
            - data_send_mode: Indicates if the connection is in data send mode.
            - data_reveiv_mode: Indicates if the connection is in data receive mode.
            - data_to_send: Holds the data to be sent.
            - data_to_reveiv: Holds the data to be received.
            - timeout_counter: Tracks the number of timeout occurrences.
        """

        self.handshake = False
        self.connection_request_send = False
        self.version_check = False
        self.status_request_send = False
        self._task = None
        self._wait_for_task_response = False
        self._wait_for_task_response_count = 0
        self.status = STATUS.OFFLINE
        self.waiting_count = 0
        self.status_request_waiting_count = 0

        self.data_send_mode = False
        self.data_reveiv_mode = False

        self.data_to_send = None
        self.data_to_reveiv = None

        self.timeout_counter = 0

    def send_message(self, msg: bytearray, addressPort: tuple[str, int]) -> None:
        """
        Sends a message to the specified address and port.

        Args:
            msg (bytearray): The message to send.
            addressPort (tuple[str, int]): The address and port to send the message to.
        """

        self.sock.sendto(msg, addressPort)

    def send_message_to_client(self, _package: package) -> None:
        """
        Sends a message to the client.

        Args:
            _package (package): The package to send.
        """

        self.send_message(_package.complete_data, self.client)
        self.last_send_package = _package

    def send_message_to_server(self, _package: package) -> None:
        """
        Sends a message to the server.

        Args:
            _package (package): The package to send.
        """

        self.send_message(_package.complete_data, self.server)
        self.last_send_package = _package

    def print_info(self) -> None:
        """
        Prints detailed information about the current state of the connection object.

        This method outputs the following attributes to the console:
        - client: The client object associated with the connection.
        - server: The server object associated with the connection.
        - receiver_id_int: The integer representation of the receiver's ID.
        - sender_id_int: The integer representation of the sender's ID.
        - receiver_id: The receiver's ID in its original format.
        - sender_id: The sender's ID in its original format.
        - bookshelf_object: The bookshelf object associated with the connection.
        - last_send_package: The last package sent over the connection.
        - last_received_package: The last package received over the connection.
        - status: The current status of the connection.
        - handshake: The handshake status of the connection.
        - connection_request_send: Indicates whether a connection request was sent.
        - version_check: Indicates whether the version check was performed.
        - task: The task associated with the connection.

        This method is primarily used for debugging purposes to inspect the internal
        state of the connection object.
        """

        print("####################")
        print(self.client)
        print(self.server)
        print(self.receiver_id_int)
        print(self.sender_id_int)
        print(self.receiver_id)
        print(self.sender_id)
        print(self.bookshelf_object)
        print(self.last_send_package)
        print(self.last_received_package)
        print(self.status)
        print(self.handshake)
        print(self.connection_request_send)
        print(self.version_check)
        print(self._task.type)
        print("####################")
