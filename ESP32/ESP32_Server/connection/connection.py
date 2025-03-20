"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
import socket
from hardware.bookshelf import bookshelf
from protocol.builder.builder_default_package import package
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
    task: bool

    def __init__(
        self,
        client: tuple[str, int],
        server: tuple[str, int],
        receiver_id: int,
        sender_id: int,
        bookshelf_object: bookshelf,
    ):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = client
        self.server = server
        self.receiver_id_int = receiver_id
        self.sender_id_int = sender_id
        self.receiver_id = int_to_4byte_array(receiver_id)
        self.sender_id = int_to_4byte_array(sender_id)
        self.bookshelf_object = bookshelf_object
        self.handshake = False
        self.task = False

        self.sock.bind((client[0], client[1]))

    def reset(self):
        """
        resets the data of the connections object
        """

    def send_message(self, msg: bytearray, addressPort: tuple[str, int]) -> None:
        """
        -
        """

        self.sock.sendto(msg, addressPort)

    def send_message_to_client(self, msg: bytearray) -> None:
        """
        -
        """
        self.send_message(msg, self.client)

    def send_message_to_server(self, msg: bytearray) -> None:
        """
        -
        """
        self.send_message(msg, self.server)
