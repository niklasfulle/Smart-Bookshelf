"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

from utils.converter import int_to_2byte_array
from utils.build_helper import get_bytearrays_size_sum

class data_package:
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
        