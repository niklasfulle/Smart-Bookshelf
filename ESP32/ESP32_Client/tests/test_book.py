"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from datatype.book import book

class TestBookshelf:
    """
    -
    """

    def test_book1(self):
        """
        -
        """
        book1 = book(1,2)

        assert book1.shelving_unit == 1
        assert book1.position == 2
        assert book1.data == bytearray(b'\x01\x00\x02\x00')
        assert int.from_bytes(book1.data[0:2], "little") == 1
        assert int.from_bytes(book1.data[2:4], "little") == 2
