"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from utils.converter import int_to_2byte_array, get_hex_string_arrs
from utils.build_helper import get_bytearrays_size_sum

class data_upload_package:
    """
        -
    """
    length: bytearray
    message_type: bytearray
    data: bytearray | None
    complete_data: bytearray
    def __init__(
        self,
        message_type: bytearray,
        data: bytearray | None
    ) -> None:
        self.message_type = message_type
        self.data = data

        if data is not None:
            self.lenght = int_to_2byte_array(get_bytearrays_size_sum([message_type, data]) + 2)
        else:
            self.lenght = int_to_2byte_array(get_bytearrays_size_sum([message_type]) + 2)

        if data is not None:
            self.complete_data = self.lenght + self.message_type + data
        else:
            self.complete_data = self.lenght + self.message_type

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
