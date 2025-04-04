"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys
import pytest

sys.path.append("../")
from utils.converter import (
    int_to_1byte_array,
    int_to_2byte_array,
    int_to_4byte_array,
    get_hex_string,
    get_hex_string_arrs,
)


class TestConverter:
    """
    Test suite for testing various utility functions related to integer-to-bytearray
    conversions and hexadecimal string representations.
    Test Cases:
    - `test_int_to_1byte_array1`: Tests conversion of integer 0 to a 1-byte array.
    - `test_int_to_1byte_array2`: Tests conversion of integer 255 to a 1-byte array.
    - `test_int_to_1byte_array3`: Ensures a ValueError is raised for integers > 255.
    - `test_int_to_2byte_array1`: Tests conversion of integer 0 to a 2-byte array.
    - `test_int_to_2byte_array2`: Tests conversion of integer 1234 to a 2-byte array.
    - `test_int_to_2byte_array3`: Ensures a ValueError is raised for integers > 65535.
    - `test_int_to_4byte_array1`: Tests conversion of integer 0 to a 4-byte array.
    - `test_int_to_4byte_array2`: Tests conversion of integer 1234 to a 4-byte array.
    - `test_int_to_4byte_array3`: Tests conversion of integer 425492990 to a 4-byte array.
    - `test_int_to_4byte_array4`: Ensures a ValueError is raised for integers > 4294967295.
    - `test_get_hex_string1`: Tests conversion of a single byte to its hexadecimal string representation.
    - `test_get_hex_string2`: Tests conversion of a byte sequence "RaSTA" to its hexadecimal string representation.
    - `test_get_hex_string3`: Tests conversion of a byte sequence "0303" to its hexadecimal string representation.
    - `test_get_hex_arr1`: Tests conversion of a single byte to a list containing its hexadecimal string representation.
    - `test_get_hex_arr2`: Tests conversion of a byte sequence "RaSTA" to a list of hexadecimal string representations.
    - `test_get_hex_arr3`: Tests conversion of a byte sequence "0303" to a list of hexadecimal string representations.
    """

    def test_int_to_1byte_array1(self):
        """
        Test case for the `int_to_1byte_array` function.

        Verifies that the function correctly converts the integer 0
        into a 1-byte array representation.

        Expected behavior:
        - When the input is 0, the output should be a bytearray containing a single byte with the value 0x00.
        """

        result = int_to_1byte_array(0)
        assert result == bytearray(b"\x00")

    def test_int_to_1byte_array2(self):
        """
        Test case for the `int_to_1byte_array` function.

        Verifies that the function correctly converts the integer 255
        into a 1-byte `bytearray` representation.

        Expected behavior:
        - Input: 255
        - Output: bytearray(b"\xff")
        """

        result = int_to_1byte_array(255)
        assert result == bytearray(b"\xff")

    def test_int_to_1byte_array3(self):
        """
        Test case for the `int_to_1byte_array` function to ensure it raises a ValueError
        when the input integer exceeds the range of a single byte (0-255).

        This test verifies that the function correctly handles invalid input by raising
        the appropriate exception.
        """

        with pytest.raises(ValueError):
            int_to_1byte_array(256)

    def test_int_to_2byte_array1(self):
        """
        Test case for the `int_to_2byte_array` function.

        Verifies that the function correctly converts the integer 0 into a
        2-byte array representation. The expected result is a bytearray
        containing two zero bytes: b"\x00\x00".
        """

        result = int_to_2byte_array(0)
        assert result == bytearray(b"\x00\x00")

    def test_int_to_2byte_array2(self):
        """
        Test case for the `int_to_2byte_array` function.

        Verifies that the function correctly converts an integer (1234)
        into a 2-byte little-endian bytearray representation.

        Expected result:
        - The integer 1234 should be converted to bytearray(b"\xd2\x04").
        """

        result = int_to_2byte_array(1234)
        assert result == bytearray(b"\xd2\x04")

    def test_int_to_2byte_array3(self):
        """
        Test case for the `int_to_2byte_array` function to ensure it raises a ValueError
        when the input integer exceeds the range that can be represented in 2 bytes.

        This test verifies that the function correctly handles invalid input by raising
        an appropriate exception.

        Expected behavior:
        - When the input integer (e.g., 21231256) exceeds the 2-byte range, a ValueError
          should be raised.

        Raises:
            ValueError: If the input integer is out of the valid 2-byte range.
        """

        with pytest.raises(ValueError):
            int_to_2byte_array(21231256)

    def test_int_to_4byte_array1(self):
        """
        Test case for the `int_to_4byte_array` function.

        Verifies that the function correctly converts the integer 0
        into a 4-byte array representation. The expected result is
        a bytearray containing four zero bytes: b"\x00\x00\x00\x00".
        """

        result = int_to_4byte_array(0)
        assert result == bytearray(b"\x00\x00\x00\x00")

    def test_int_to_4byte_array2(self):
        """
        Test the `int_to_4byte_array` function with the integer value 1234.

        This test verifies that the function correctly converts the integer 1234
        into a 4-byte little-endian bytearray representation.

        Expected Result:
            bytearray(b"\xd2\x04\x00\x00")
        """

        result = int_to_4byte_array(1234)
        assert result == bytearray(b"\xd2\x04\x00\x00")

    def test_int_to_4byte_array3(self):
        """
        Test case for the `int_to_4byte_array` function.

        Verifies that the function correctly converts the integer 425492990
        into a 4-byte little-endian bytearray representation.

        Expected result:
            bytearray(b"\xfe\x81\\\x19")
        """

        result = int_to_4byte_array(425492990)
        assert result == bytearray(b"\xfe\x81\\\x19")

    def test_int_to_4byte_array4(self):
        """
        Test case for the `int_to_4byte_array` function to ensure it raises a ValueError
        when the input integer exceeds the maximum value that can be represented
        in a 4-byte array.

        This test verifies that the function correctly handles invalid input by
        raising the appropriate exception.
        """

        with pytest.raises(ValueError):
            int_to_4byte_array(42549222990)

    def test_get_hex_string1(self):
        """
        Test case for the `get_hex_string` function.

        This test verifies that the `get_hex_string` function correctly converts
        a given byte string to its corresponding hexadecimal string representation.

        Test Scenario:
        - Input: b"0" (byte string representing the character '0')
        - Expected Output: "0x30" (hexadecimal representation of the ASCII value of '0')

        Asserts:
        - The result of `get_hex_string(b"0")` is equal to "0x30".
        """

        result = get_hex_string(b"0")
        assert result == "0x30"

    def test_get_hex_string2(self):
        """
        Test case for the `get_hex_string` function.

        This test verifies that the `get_hex_string` function correctly converts
        a given byte string into a formatted hexadecimal string.

        Steps:
        - Pass the byte string `b"RaSTA"` to the `get_hex_string` function.
        - Assert that the returned result matches the expected hexadecimal string:
          "0x52, 0x61, 0x53, 0x54, 0x41".

        Expected Behavior:
        The function should return a string representation of the input bytes
        in hexadecimal format, prefixed with "0x" and separated by commas.
        """

        result = get_hex_string(b"RaSTA")
        assert result == "0x52, 0x61, 0x53, 0x54, 0x41"

    def test_get_hex_string3(self):
        """
        Test case for the `get_hex_string` function.

        This test verifies that the `get_hex_string` function correctly converts
        a given byte string into a formatted hexadecimal string representation.

        Test Input:
        - A byte string `b"0303"`.

        Expected Output:
        - A string `"0x30, 0x33, 0x30, 0x33"`.

        The test asserts that the output of the function matches the expected
        hexadecimal string format.
        """

        result = get_hex_string(b"0303")
        assert result == "0x30, 0x33, 0x30, 0x33"

    def test_get_hex_arr1(self):
        """
        Test case for the `get_hex_string_arrs` function.

        This test verifies that the function correctly converts a single byte
        input into its corresponding hexadecimal string representation.

        Steps:
        - Pass the byte input `b"0"` to the `get_hex_string_arrs` function.
        - Assert that the returned result matches the expected output `["0x30"]`.

        Expected Behavior:
        The function should return a list containing the hexadecimal string
        representation of the input byte.

        """

        result = get_hex_string_arrs(b"0")
        assert result == ["0x30"]

    def test_get_hex_arr2(self):
        """
        Test case for the `get_hex_string_arrs` function.

        This test verifies that the `get_hex_string_arrs` function correctly converts
        a given byte string into a list of hexadecimal string representations.

        Steps:
        - Pass the byte string `b"RaSTA"` to the `get_hex_string_arrs` function.
        - Assert that the returned result matches the expected list of hexadecimal strings:
          ["0x52", "0x61", "0x53", "0x54", "0x41"].

        Expected Behavior:
        - The function should return a list of hexadecimal string representations
          corresponding to each byte in the input byte string.
        """

        result = get_hex_string_arrs(b"RaSTA")
        assert result == ["0x52", "0x61", "0x53", "0x54", "0x41"]

    def test_get_hex_arr3(self):
        """
        Test case for the `get_hex_string_arrs` function.

        This test verifies that the function correctly converts a given byte string
        into a list of hexadecimal string representations.

        Steps:
        - Pass the byte string `b"0303"` to the `get_hex_string_arrs` function.
        - Assert that the returned result matches the expected list:
          ["0x30", "0x33", "0x30", "0x33"].

        Expected Behavior:
        The function should return a list of hexadecimal string representations
        for each byte in the input byte string.
        """

        result = get_hex_string_arrs(b"0303")
        assert result == ["0x30", "0x33", "0x30", "0x33"]
