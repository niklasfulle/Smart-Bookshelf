"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0301

from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum
from utils.checksumme import get_checksumme


class package:
    """
    A class representing a data package with various attributes and methods for handling
    and processing the package's data.
    Attributes:
        length (int): The length of the package in bytes.
        message_type (bytearray): The type of message being sent.
        receiver_id (bytearray): The ID of the receiver.
        sender_id (bytearray): The ID of the sender.
        sequence_number (bytearray): The sequence number of the package.
        confirmed_sequence_number (bytearray): The confirmed sequence number.
        timestamp (bytearray): The timestamp of the package.
        confirmed_timestamp (bytearray): The confirmed timestamp.
        data (bytearray): The payload data of the package.
        checksumme (bytearray): The checksum of the package for validation.
        complete_data (bytearray): The complete serialized data of the package.
    Methods:
        __init__:
            Initializes a new instance of the package class with the provided attributes.
            Calculates the length, checksum, and complete data of the package.
        print_data:
            Prints the complete data of the package in a formatted matrix of hexadecimal values.
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
        """
        Initializes a package object with the given parameters and computes its
        length, complete data, and checksum.
        Args:
            message_type (bytearray): The type of the message.
            receiver_id (bytearray): The ID of the receiver.
            sender_id (bytearray): The ID of the sender.
            sequence_number (bytearray): The sequence number of the message.
            confirmed_sequence_number (bytearray): The confirmed sequence number.
            timestamp (bytearray): The timestamp of the message.
            confirmed_timestamp (bytearray): The confirmed timestamp.
            data (bytearray): The payload data of the message. Can be None.
        Attributes:
            message_type (bytearray): The type of the message.
            receiver_id (bytearray): The ID of the receiver.
            sender_id (bytearray): The ID of the sender.
            sequence_number (bytearray): The sequence number of the message.
            confirmed_sequence_number (bytearray): The confirmed sequence number.
            timestamp (bytearray): The timestamp of the message.
            confirmed_timestamp (bytearray): The confirmed timestamp.
            data (bytearray): The payload data of the message.
            lenght (bytearray): The computed length of the package as a 2-byte array.
            complete_data (bytearray): The complete package data including the checksum.
        """

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
                1,
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
                1,
            )

        self.complete_data = complete_data + checksumme

    def print_data(self) -> None:
        """
        Prints the complete data in a formatted matrix form.
        The method processes the `complete_data` attribute by splitting it into
        hexadecimal string arrays using the `get_hex_string_arrs` function. It then
        organizes the data into a matrix with 8 columns per row and prints the matrix.
        Steps:
        1. Splits the `complete_data` into an array of hexadecimal strings.
        2. Calculates the number of rows required for the matrix based on the length
           of the split data.
        3. Initializes a matrix with the calculated number of rows and 8 columns.
        4. Populates the matrix with the split data.
        5. Prints the resulting matrix.
        Note:
            - Assumes `complete_data` is already set and `get_hex_string_arrs` is
              a valid function that processes the data correctly.
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
