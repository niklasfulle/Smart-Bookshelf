"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0301

from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum
from utils.checksumme import get_checksumme
from utils.constants import MD4_Type


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

    data: bytearray

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
        data: bytearray,
    ) -> None:
        self.message_type = message_type
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.sequence_number = sequence_number
        self.confirmed_sequence_number = confirmed_sequence_number
        self.timestamp = timestamp
        self.confirmed_timestamp = confirmed_timestamp
        self.data = data

        if data is not None:
            self.lenght = int_to_2byte_array(
                get_bytearrays_size_sum(
                    [
                        self.message_type,
                        self.receiver_id,
                        self.sender_id,
                        self.sequence_number,
                        self.confirmed_sequence_number,
                        self.timestamp,
                        self.confirmed_timestamp,
                        self.data,
                    ]
                )
                + 2
                + 8
            )

        else:
            self.lenght = int_to_2byte_array(
                get_bytearrays_size_sum(
                    [
                        self.message_type,
                        self.receiver_id,
                        self.sender_id,
                        self.sequence_number,
                        self.confirmed_sequence_number,
                        self.timestamp,
                        self.confirmed_timestamp,
                    ]
                )
                + 2
                + 8
            )

        complete_data: bytearray
        if data is not None:
            complete_data = (
                self.lenght
                + self.message_type
                + self.receiver_id
                + self.sender_id
                + self.sequence_number
                + self.confirmed_sequence_number
                + self.timestamp
                + self.confirmed_timestamp
                + self.data
            )
        else:
            complete_data = (
                self.lenght
                + self.message_type
                + self.receiver_id
                + self.sender_id
                + self.sequence_number
                + self.confirmed_sequence_number
                + self.timestamp
                + self.confirmed_timestamp
            )

        checksumme: bytearray
        if data is not None:
            checksumme = get_checksumme(
                (
                    self.lenght
                    + self.message_type
                    + self.receiver_id
                    + self.sender_id
                    + self.sequence_number
                    + self.confirmed_sequence_number
                    + self.timestamp
                    + self.confirmed_timestamp
                    + self.data
                ),
                MD4_Type.LOWER_HALF,
            )
        else:
            checksumme = get_checksumme(
                (
                    self.lenght
                    + self.message_type
                    + self.receiver_id
                    + self.sender_id
                    + self.sequence_number
                    + self.confirmed_sequence_number
                    + self.timestamp
                    + self.confirmed_timestamp
                ),
                MD4_Type.LOWER_HALF,
            )

        self.complete_data = complete_data + checksumme

    def print_data(self) -> None:
        """
        -
        """
        split_data = get_hex_string_arrs(self.complete_data)

        lenList: int = len(split_data)

        count: int = round(lenList / 8)

        index1: int = 0
        index2: int = 0

        matrix = [[0 for _ in range(8)] for _ in range(count)]

        for i in enumerate(split_data):
            matrix[index1][index2] = split_data[i[0]]

            index2 += 1
            if (i[0] + 1) % 8 == 0:
                index1 += 1
                index2 = 0

        print(matrix)
