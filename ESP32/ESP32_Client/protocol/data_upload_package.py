"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum


class data_upload_package:
    """
    A class representing a data upload package for communication.
    Attributes:
        length (bytearray): The length of the complete data package as a bytearray.
        message_type (bytearray): The type of the message as a bytearray.
        data (bytearray): The data payload of the package as a bytearray.
        complete_data (bytearray): The complete data package including length, message type, and data.
    Methods:
        __init__(message_type: bytearray, data: bytearray) -> None:
            Initializes a data_upload_package instance with the given message type and data.
            Calculates the length and constructs the complete data package.
        print_data() -> None:
            Prints the complete data package in a formatted matrix of hexadecimal strings.
    """

    length: bytearray
    message_type: bytearray
    data: bytearray
    complete_data: bytearray

    def __init__(self, message_type: bytearray, data: bytearray) -> None:
        """
        Initializes a data upload package with a message type and optional data.
        Args:
            message_type (bytearray): The type of the message, represented as a bytearray.
            data (bytearray): The data to be included in the package, represented as a bytearray.
                              Can be None if no data is provided.
        Attributes:
            message_type (bytearray): Stores the provided message type.
            data (bytearray): Stores the provided data or None if no data is provided.
            lenght (bytearray): A 2-byte array representing the total length of the package,
                                including the message type, data, and length field itself.
            complete_data (bytearray): The complete package data, including the length,
                                       message type, and optional data.
        """

        self.message_type = message_type
        self.data = data

        if data is not None:
            self.lenght = int_to_2byte_array(
                get_bytearrays_size_sum([message_type, data]) + 2
            )
        else:
            self.lenght = int_to_2byte_array(
                get_bytearrays_size_sum([message_type]) + 2
            )

        if data is not None:
            self.complete_data = self.lenght + self.message_type + data
        else:
            self.complete_data = self.lenght + self.message_type

    def print_data(self) -> None:
        """
        Prints the complete data in a formatted matrix form.
        This method processes the `complete_data` attribute by splitting it into
        hexadecimal string arrays using the `get_hex_string_arrs` function. It then
        organizes the data into an 8-column matrix and prints the resulting matrix.
        Steps:
        1. Splits the `complete_data` into an array of hexadecimal strings.
        2. Calculates the number of rows required for an 8-column matrix.
        3. Initializes a matrix with the calculated dimensions.
        4. Fills the matrix with the split data.
        5. Prints the matrix.
        Note:
            The matrix will have 8 columns, and the number of rows is determined
            by rounding the length of the split data divided by 8.
        Returns:
            None
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
