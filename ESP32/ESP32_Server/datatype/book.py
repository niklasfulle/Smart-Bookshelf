"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from utils.converter import int_to_2byte_array


class book:
    """
    Represents a book with its shelving unit and position information.
    Attributes:
        shelving_unit (int): The shelving unit where the book is located.
        position (int): The position of the book within the shelving unit.
        data (bytearray): A bytearray representation of the shelving unit and position.
    Methods:
        __init__(shelving_unit: int, position: int) -> None:
            Initializes a book instance with the given shelving unit and position.
    """

    shelving_unit: int
    position: int
    data: bytearray

    def __init__(self, shelving_unit: int, position: int) -> None:
        self.shelving_unit = shelving_unit
        self.position = position
        self.data = int_to_2byte_array(shelving_unit) + int_to_2byte_array(position)
