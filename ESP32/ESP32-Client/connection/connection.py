"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103
import socket
from hardware.bookshelf import bookshelf

class connection:
    """_summary_

    Returns:
        _type_: _description_
    """
    sock: socket
    client: tuple[str, int]
    server: tuple[str, int]
    receiver_id: bytearray
    sender_id: bytearray
    bookshelf: bookshelf
    def __init__(
      self,
      receiver_id: int,
      sender_id: int,
      sock: socket,
    ):
        self.sock = sock
        self.receiver_id_int = receiver_id
        self.sender_id_int = sender_id
        