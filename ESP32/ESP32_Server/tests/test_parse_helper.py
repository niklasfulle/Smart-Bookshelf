"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")
from utils.converter import get_hex_string
from utils.parse_helper import get_data_string_array, parse_data_start_end


class TestParseHelper:
    """
    Test suite for the `parse_data_start_end` function and related helper functions.
    This class contains multiple test cases to validate the functionality of parsing
    data from a hexadecimal string representation. The tests ensure that the parsing
    logic works correctly for various start and end indices, and that the resulting
    data matches the expected values.
    Test Cases:
        - `test_parse_data_start_end1`: Verifies that the parsed data between indices
          12 and 10 (inclusive) matches the expected integer value when converted
          from bytes.
        - `test_parse_data_start_end2`: Validates parsing between indices 24 and 20,
          ensuring the result matches the expected integer value.
        - `test_parse_data_start_end3`: Tests parsing the last 8 bytes of the data
          and checks that the result matches the expected byte array.
        - `test_parse_data_start_end4`: Ensures parsing between indices 39 and 38
          produces the correct single-byte result and its hexadecimal string
          representation.
        - `test_parse_data_start_end5`: Verifies parsing between indices 61 and 41,
          ensuring the result matches the expected byte array and its hexadecimal
          string representation.
    Helper Functions:
        - `get_data_string_array`: Converts a space-separated hexadecimal string
          into a byte array.
        - `parse_data_start_end`: Extracts a subset of bytes from the given data
          based on the specified start and end indices.
        - `get_hex_string`: Converts a byte array into a hexadecimal string
          representation.
    """

    def test_parse_data_start_end1(self):
        """
        Test case for the `parse_data_start_end` function.
        This test verifies that the `parse_data_start_end` function correctly extracts
        a subset of bytes from the provided data array and converts it to an integer
        using little-endian byte order.
        Steps:
        1. Converts the input hexadecimal string `data` into an array of bytes using
           the `get_data_string_array` helper function.
        2. Calls `parse_data_start_end` with the processed data, start index 12, and
           length 10 to extract a specific range of bytes.
        3. Asserts that the extracted bytes, when interpreted as a little-endian integer,
           equal the expected value of 6240.
        Expected Outcome:
        The test passes if the extracted and converted integer matches the expected value.
        """

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 12, 10)

        assert int.from_bytes(result, "little") == 6240

    def test_parse_data_start_end2(self):
        """
        Test case for verifying the functionality of `parse_data_start_end` function.
        This test:
        - Converts a hexadecimal string into an array of bytes using `get_data_string_array`.
        - Extracts a specific range of bytes from the data using `parse_data_start_end`.
        - Converts the extracted bytes into an integer using little-endian byte order.
        - Asserts that the resulting integer matches the expected value.
        Expected Result:
        - The integer value extracted from the specified range of bytes should be 425492977.
        """

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 24, 20)
        result = int.from_bytes(result, "little")

        assert result == 425492977

    def test_parse_data_start_end3(self):
        """
        Test case for the `parse_data_start_end` function.
        This test verifies that the `parse_data_start_end` function correctly extracts
        a specific portion of a data string when provided with the start and end indices.
        Steps:
        1. A hexadecimal string `data` is provided as input.
        2. The `get_data_string_array` function is used to process the input data into
           the required format.
        3. The `parse_data_start_end` function is called with the processed data, its
           length, and a calculated start index.
        4. The result is compared to the expected bytearray to ensure correctness.
        Assertions:
        - The result of `parse_data_start_end` must match the expected bytearray
          `b"R\xc6\xf3\xb4\xe3\x8b\xf6F"`.
        """

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, len(data), len(data) - 8)

        assert result == bytearray(b"R\xc6\xf3\xb4\xe3\x8b\xf6F")

    def test_parse_data_start_end4(self):
        """
        Test case for verifying the functionality of `parse_data_start_end` and related helper functions.
        This test checks the ability of the `parse_data_start_end` function to correctly extract a
        specific portion of data from a given input string and validate its output.
        Steps:
        1. Convert the input hexadecimal string `data` into an array of data strings using
           `get_data_string_array`.
        2. Use `parse_data_start_end` to extract a portion of the data starting at index 39 and
           ending at index 38.
        3. Assert that the extracted data matches the expected `bytearray(b"@")`.
        4. Convert the extracted data to a hexadecimal string using `get_hex_string`.
        5. Assert that the resulting hexadecimal string matches the expected value `"0x40"`.
        Assertions:
        - The extracted data matches the expected bytearray.
        - The hexadecimal representation of the extracted data matches the expected string.
        """

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 39, 38)

        assert result == bytearray(b"@")

        result2 = get_hex_string(result)

        assert result2 == "0x40"

    def test_parse_data_start_end5(self):
        """
        Test case for verifying the functionality of parsing a specific range of data
        from a hexadecimal string and converting it into a bytearray and its corresponding
        hexadecimal string representation.
        This test:
        - Converts a given hexadecimal string into an array of data.
        - Extracts a specific range of data from the array using `parse_data_start_end`.
        - Verifies that the extracted data matches the expected bytearray.
        - Converts the extracted bytearray into a hexadecimal string using `get_hex_string`.
        - Asserts that the resulting hexadecimal string matches the expected value.
        Assertions:
        - The extracted bytearray should match the expected value.
        - The hexadecimal string representation of the extracted bytearray should match the expected value.
        """

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 61, 41)

        assert result == bytearray(b"tecDSTW_____________")

        result2 = get_hex_string(result)

        assert (
            result2
            == "0x74, 0x65, 0x63, 0x44, 0x53, 0x54, 0x57, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f"
        )
