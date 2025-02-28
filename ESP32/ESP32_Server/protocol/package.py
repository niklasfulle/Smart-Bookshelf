"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from protocol.data_upload_package import data_upload_package
from protocol.data_package import data_package
from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum
from utils.checksumme import get_checksumme

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

    complete_data: bytearray
    def __init__(
        self,
        message_type: bytearray,
        receiver_id: bytearray,
        sender_id: bytearray,
        sequence_number: bytearray,
        confirmed_sequence_number: bytearray,
        timestamp: bytearray,
        confirmed_timestamp: bytearray,
        data: data_upload_package | data_package | bytearray | None,
    ) -> None:
        self.message_type = message_type
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.sequence_number = sequence_number
        self.confirmed_sequence_number = confirmed_sequence_number
        self.timestamp = timestamp
        self.confirmed_timestamp = confirmed_timestamp

        if isinstance(data, data_upload_package):
            self.data = data.complete_data
        elif isinstance(data, data_package):
            self.data = data.complete_data
        elif isinstance(data, bytearray):
            self.data = data

        if data is not None:
            self.lenght = int_to_2byte_array(get_bytearrays_size_sum([message_type,
                                                                      receiver_id,
                                                                      sender_id,
                                                                      sequence_number,
                                                                      confirmed_sequence_number,
                                                                      data
                                                                      ])
                                             + 2 + 4)
        else:
            self.lenght = int_to_2byte_array(get_bytearrays_size_sum([message_type,
                                                                      receiver_id,
                                                                      sender_id,
                                                                      sequence_number,
                                                                      confirmed_sequence_number])
                                             + 2 + 4)

        if data is not None:
            self.complete_data = (self.lenght +
                                  message_type +
                                  receiver_id +
                                  sender_id +
                                  sequence_number +
                                  confirmed_sequence_number +
                                  data)
        else:
            self.complete_data = (self.lenght +
                                  message_type +
                                  receiver_id +
                                  sender_id +
                                  sequence_number +
                                  confirmed_sequence_number)

        self.checksumme = get_checksumme(self.complete_data, 1)

        self.complete_data = self.complete_data + self.checksumme

    def print_data(self) -> None:
        """
            -
        """
        split_data = get_hex_string_arrs(self.complete_data)

        lenList: int = len(split_data)

        count: int = round(lenList / 8)

        index1: int = 0
        index2: int = 0

        matrix = [[0 for x in range(8)] for y in range(count)]


        for i in enumerate(split_data):
            matrix[index1][index2] = split_data[i[0]]

            index2 += 1
            if (i[0] + 1) % 8 == 0:
                index1 += 1
                index2 = 0

        print(matrix)
