"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
import socket
from hardware.bookshelf import bookshelf
from protocol.package import package
from protocol.constants.constants import STATUS
from utils.converter import int_to_4byte_array


class connection:
    """
    A class to manage the connection between a client and a server using UDP sockets.
    Attributes:
        sock (socket): The UDP socket used for communication.
        client (tuple[str, int]): The client's IP address and port.
        server (tuple[str, int]): The server's IP address and port.
        receiver_id_int (int): The receiver's ID as an integer.
        sender_id_int (int): The sender's ID as an integer.
        receiver_id (bytearray): The receiver's ID as a 4-byte array.
        sender_id (bytearray): The sender's ID as a 4-byte array.
        bookshelf_object (bookshelf): The associated bookshelf object.
        last_send_package (package): The last package sent.
        last_received_package (package): The last package received.
        status (STATUS): The current connection status.
        handshake (bool): Indicates if the handshake process is complete.
        connection_request_send (bool): Indicates if a connection request has been sent.
        version_check (bool): Indicates if the version check is complete.
        task (bool): Indicates if a task is being processed.
        waiting_count (int): Counter for waiting operations.
        data_send_mode (bool): Indicates if the connection is in data send mode.
        data_reveiv_mode (bool): Indicates if the connection is in data receive mode.
        data_to_send (bytearray): Data to be sent.
        data_to_reveiv (bytearray): Data to be received.
        timeout_counter (int): Counter for timeout operations.
    Methods:
        __init__(client, server, receiver_id, sender_id, Bookshelf_object):
            Initializes the connection object with the given parameters.
        reset() -> None:
            Resets the connection attributes to their default values.
        send_message(msg: bytearray, addressPort: tuple[str, int]) -> None:
            Sends a message to the specified address and port.
        send_message_to_client(_package: package) -> None:
            Sends a package to the client and updates the last sent package.
        send_message_to_server(_package: package) -> None:
            Sends a package to the server and updates the last sent package.
        print_info() -> None:
            Prints detailed information about the connection object.
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
    task: bool

    waiting_count: int

    data_send_mode: bool
    data_reveiv_mode: bool

    data_to_send: bytearray
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
        Initializes a connection object for managing UDP communication between a client and a server.
        Args:
            client (tuple[str, int]): A tuple containing the client's IP address and port number.
            server (tuple[str, int]): A tuple containing the server's IP address and port number.
            receiver_id (int): The unique identifier for the receiver.
            sender_id (int): The unique identifier for the sender.
            Bookshelf_object (bookshelf): An instance of the bookshelf object to manage bookshelf-related operations.
        Attributes:
            sock (socket.socket): The UDP socket used for communication.
            client (tuple[str, int]): The client's IP address and port number.
            server (tuple[str, int]): The server's IP address and port number.
            receiver_id_int (int): The receiver's unique identifier as an integer.
            sender_id_int (int): The sender's unique identifier as an integer.
            receiver_id (bytes): The receiver's unique identifier as a 4-byte array.
            sender_id (bytes): The sender's unique identifier as a 4-byte array.
            bookshelf_object (bookshelf): The bookshelf object instance.
            last_send_package (Any): Stores the last sent package (initially None).
            last_received_package (Any): Stores the last received package (initially None).
            status (STATUS): The current connection status (default is STATUS.OFFLINE).
            handshake (bool): Indicates whether the handshake process is complete.
            connection_request_send (bool): Indicates whether a connection request has been sent.
            version_check (bool): Indicates whether the version check is complete.
            task (bool): Indicates whether a task is being processed.
            waiting_count (int): Counter for tracking waiting states.
            data_send_mode (bool): Indicates whether the connection is in data send mode.
            data_reveiv_mode (bool): Indicates whether the connection is in data receive mode.
            data_to_send (Any): Data to be sent (initially None).
            data_to_reveiv (Any): Data to be received (initially None).
            timeout_counter (int): Counter for tracking timeout occurrences.
        Raises:
            socket.error: If there is an error binding the socket to the client address and port.
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
        self.task = False

        self.waiting_count = 0

        self.data_send_mode = False
        self.data_reveiv_mode = False

        self.data_to_send = None
        self.data_to_reveiv = None

        self.timeout_counter = 0

        self.sock.bind((client[0], client[1]))

    def reset(self) -> None:
        """
        Resets the connection state to its initial values.
        This method reinitializes all attributes related to the connection state,
        including handshake status, connection request status, version check status,
        task reference, connection status, waiting count, data send/receive modes,
        data buffers, and timeout counter.
        Attributes Reset:
            handshake (bool): Indicates whether the handshake process is complete.
            connection_request_send (bool): Tracks if a connection request has been sent.
            version_check (bool): Tracks if the version check has been performed.
            _task (Optional[Task]): Reference to the current task, set to None.
            status (STATUS): The current connection status, reset to STATUS.OFFLINE.
            waiting_count (int): Counter for the number of waiting attempts, reset to 0.
            data_send_mode (bool): Indicates if the system is in data send mode.
            data_reveiv_mode (bool): Indicates if the system is in data receive mode.
            data_to_send (Optional[Any]): Buffer for data to be sent, reset to None.
            data_to_reveiv (Optional[Any]): Buffer for data to be received, reset to None.
            timeout_counter (int): Counter for timeout occurrences, reset to 0.
        """

        self.handshake = False
        self.connection_request_send = False
        self.version_check = False
        self._task = None
        self.status = STATUS.OFFLINE
        self.waiting_count = 0

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
        print(self.task)
        print("####################")
