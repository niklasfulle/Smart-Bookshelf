"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
import socket
from hardware.bookshelf import bookshelf
from protocol.package import package
from utils.converter import int_to_4byte_array


class connection:
    """_summary_

    Returns:
        _type_: _description_
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

    handshake: bool
    connection_request_send: bool
    version_check: bool
    task: bool

    waiting_count: int

    def __init__(
        self,
        client: tuple[str, int],
        server: tuple[str, int],
        receiver_id: int,
        sender_id: int,
        Bookshelf_object: bookshelf,
    ):
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

        self.handshake = False
        self.connection_request_send = False
        self.version_check = False
        self.task = False

        self.waiting_count = 0

        self.sock.bind((self.server[0], self.server[1]))

    def reset(self) -> None:
        """
        resets the data of the connections object
        """
        self.handshake = False
        self.connection_request_send = False
        self.version_check = False
        self.task = False
        self.waiting_count = 0

    def send_message(self, msg: bytearray, addressPort: tuple[str, int]) -> None:
        """
        -
        """

        self.sock.sendto(msg, addressPort)

    def send_message_to_client(self, _package: package) -> None:
        """
        -
        """
        self.send_message(_package.complete_data, self.client)
        self.last_send_package = _package

    def send_message_to_server(self, _package: package) -> None:
        """
        -
        """
        self.send_message(_package.complete_data, self.server)
        self.last_send_package = _package
