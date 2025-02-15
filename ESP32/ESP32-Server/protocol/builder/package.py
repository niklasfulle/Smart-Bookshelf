"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from data_upload_package import data_upload_package
from data_package import data_package

class package:
    """
        -
    """
    length: int
    message_type: bytearray

    receiver_id: bytearray
    sender_id: bytearray

    sequence_number: bytearray
    confirmed_sequence_number: bytearray

    timestamp: bytearray
    confirmed_timestamp: bytearray

    data: data_upload_package | data_package

    checksumme: bytearray
    def __init__(
      self,
      length: bytearray,
      message_type: bytearray,
      receiver_id: bytearray,
      sender_id: bytearray,
      sequence_number: bytearray,
      confirmed_sequence_number: bytearray,
      timestamp: bytearray,
      confirmed_timestamp: bytearray,
      data: data_upload_package | data_package,
      checksumme: bytearray,
    ) -> None:
        self.length = length
        self.message_type = message_type
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.sequence_number = sequence_number
        self.confirmed_sequence_number = confirmed_sequence_number
        self.timestamp = timestamp
        self.confirmed_timestamp = confirmed_timestamp
        self.data = data
        self.checksumme = checksumme
