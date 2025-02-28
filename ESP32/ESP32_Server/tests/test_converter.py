"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys
sys.path.append('../')
from utils.converter import int_to_2byte_array, int_to_4byte_array, get_hex_string, get_hex_string_arrs


class TestConverter:
    """
        -
    """
    def test_int_to_2byte_array1(self):
        """Tests whether the correct 2 byte value is returned"""

        result = int_to_2byte_array(0)
        assert result == bytearray(b"\x00\x00")

    def test_int_to_2byte_array2(self):
        """Tests whether the correct 2 byte value is returned"""

        result = int_to_2byte_array(1234)
        assert result == bytearray(b"\xd2\x04")

    def test_int_to_4byte_array1(self):
        """Tests whether the correct 4 byte value is returned"""

        result = int_to_4byte_array(0)
        assert result == bytearray(b"\x00\x00\x00\x00")

    def test_int_to_4byte_array2(self):
        """Tests whether the correct 4 byte value is returned"""

        result = int_to_4byte_array(1234)
        assert result == bytearray(b"\xd2\x04\x00\x00")

    def test_int_to_4byte_array3(self):
        """Tests whether the correct 4 byte value is returned"""

        result = int_to_4byte_array(425492990)
        assert result == bytearray(b"\xfe\x81\\\x19")

    def test_get_hex_string1(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string(b"0")
        assert result == "0x30"

    def test_get_hex_string2(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string(b"RaSTA")
        assert result == "0x52, 0x61, 0x53, 0x54, 0x41"

    def test_get_hex_string3(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string(b"0303")
        assert result == "0x30, 0x33, 0x30, 0x33"

    def test_get_hex_arr1(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string_arrs(b"0")
        assert result == ['0x30']

    def test_get_hex_arr2(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string_arrs(b"RaSTA")
        assert result == ['0x52', '0x61', '0x53', '0x54', '0x41']

    def test_get_hex_arr3(self):
        """Tests whether the byte array is output correctly"""

        result = get_hex_string_arrs(b"0303")
        assert result == ['0x30', '0x33', '0x30', '0x33']
