"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum


class data_package:
    """
    A class to represent a data package for communication protocols.
    Attributes:
    ----------
    length : bytearray
        The length of the complete data package, represented as a 2-byte array.
    message_type : bytearray
        The type of the message, represented as a byte array.
    data : bytearray
        The actual data payload of the package, represented as a byte array.
    complete_data : bytearray
        The complete data package, including length, message type, and data.
    Methods:
    -------
    __init__(message_type: bytearray, data: bytearray) -> None
        Initializes the data_package object with the given message type and data.
    print_data() -> None
        Prints the complete data in a formatted matrix of hexadecimal strings.
    """

    length: bytearray
    message_type: bytearray
    data: bytearray
    complete_data: bytearray

    def __init__(self, message_type: bytearray, data: bytearray) -> None:
        """
        Initializes a data package with a message type and optional data.
        Args:
            message_type (bytearray): The type of the message, represented as a bytearray.
            data (bytearray): The data payload of the message, represented as a bytearray.
                              Can be None if no data is provided.
        Attributes:
            message_type (bytearray): Stores the provided message type.
            data (bytearray): Stores the provided data payload.
            lenght (bytearray): A 2-byte array representing the total length of the package,
                                including the message type, data, and length field itself.
            complete_data (bytearray): The complete serialized data package, including the
                                       length, message type, and data (if provided).
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
        The method splits the `complete_data` into an array of hexadecimal strings
        using the `get_hex_string_arrs` function. It then organizes the split data
        into a matrix with 8 columns per row and prints the resulting matrix.
        Steps:
        1. Split the `complete_data` into an array of hexadecimal strings.
        2. Calculate the number of rows required for the matrix based on the length
           of the split data and the fixed column size (8).
        3. Populate a 2D list (matrix) with the split data.
        4. Print the matrix.
        Note:
            - The matrix will have `count` rows and 8 columns.
            - Any remaining data that does not fill a complete row will not be included.
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
