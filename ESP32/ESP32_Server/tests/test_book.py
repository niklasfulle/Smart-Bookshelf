"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from datatype.book import book


class TestBookshelf:
    """
    A test suite for verifying the functionality of the `book` class.
    Methods:
        test_book1():
            Tests the initialization and data representation of a `book` object.
        Validates the attributes and data representation of a `book` object
        initialized with specific shelving unit and position values.
        Asserts:
            - The shelving unit is correctly assigned.
            - The position is correctly assigned.
            - The data attribute is correctly constructed as a bytearray.
            - The shelving unit can be correctly extracted from the data attribute.
            - The position can be correctly extracted from the data attribute.
    """

    def test_book1(self):
        """
        Test the functionality of the `book` class by creating an instance with specific
        shelving unit and position values, and verifying its attributes and data representation.
        Assertions:
        - The `shelving_unit` attribute of the `book` instance should match the provided value.
        - The `position` attribute of the `book` instance should match the provided value.
        - The `data` attribute should be a `bytearray` representing the shelving unit and position.
        - The first two bytes of `data` should correctly decode to the shelving unit.
        - The last two bytes of `data` should correctly decode to the position.
        """

        book1 = book(1, 2)

        assert book1.shelving_unit == 1
        assert book1.position == 2
        assert book1.data == bytearray(b"\x01\x00\x02\x00")
        assert int.from_bytes(book1.data[0:2], "little") == 1
        assert int.from_bytes(book1.data[2:4], "little") == 2
