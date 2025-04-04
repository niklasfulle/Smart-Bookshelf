"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")

from protocol.builder.builder_data_package import (
    build_data_package_light_on,
    build_data_package_light_off,
    build_data_package_book,
    build_data_package_books,
    build_data_package_mode,
)
from protocol.parser.parser_data_package import parse_data_package
from utils.converter import int_to_2byte_array


class TestParseDataPackage:
    """
    Test suite for verifying the functionality of parsing and building data packages.
    This test class contains the following test cases:
    1. `test_parse_data_package_light_on`:
        - Verifies that a data package for turning the light on is correctly parsed.
        - Asserts the length and message type of the parsed package.
    2. `test_build_data_package_light_off`:
        - Verifies that a data package for turning the light off is correctly parsed.
        - Asserts the length and message type of the parsed package.
    3. `test_build_data_package_book`:
        - Verifies that a data package for a single book is correctly parsed.
        - Asserts the length, message type, and data content of the parsed package.
    4. `test_build_data_package_books`:
        - Verifies that a data package for multiple books is correctly parsed.
        - Asserts the length, message type, and data content of the parsed package.
    5. `test_build_data_package_mode`:
        - Verifies that a data package for setting a mode is correctly parsed.
        - Asserts the length, message type, and data content of the parsed package.
    """

    def test_parse_data_package_light_on(self) -> None:
        """
        Test the `parse_data_package` function for a light-on data package.
        This test verifies that the `parse_data_package` function correctly parses
        a data package representing a "light on" message. It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package matches the expected value.
        Assertions:
            - The `lenght` field of the parsed package is 4 (converted from bytes).
            - The `message_type` field of the parsed package is 5001 (converted from bytes).
        """

        package = build_data_package_light_on()

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 5001

    def test_build_data_package_light_off(self) -> None:
        """
        Test case for verifying the functionality of building and parsing a data package
        when the light is turned off.
        This test ensures that:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package corresponds to the expected identifier (5002).
        """

        package = build_data_package_light_off()

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 5002

    def test_build_data_package_book(self) -> None:
        """
        Test the `build_data_package_book` function to ensure it correctly builds a data package
        and that the resulting package can be parsed accurately.
        This test verifies:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correctly set to 5003.
        - The data content of the parsed package matches the input data.
        Assertions:
        - The length of the parsed package is 6.
        - The message type of the parsed package is 5003.
        - The data content of the parsed package is a bytearray representing the input integer.
        """

        package = build_data_package_book(int_to_2byte_array(5))

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 5003
        assert parsed_package.data == bytearray(b"\x05\x00")

    def test_build_data_package_books(self) -> None:
        """
        Test the `build_data_package_books` function to ensure it correctly builds
        a data package and that the resulting package can be parsed accurately.
        This test verifies:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The data content of the parsed package matches the expected byte array.
        Assertions:
        - The length of the parsed package should be 10.
        - The message type of the parsed package should be 5004.
        - The data content of the parsed package should be `bytearray(b"\x05\x00\x07\x00\x14\x00")`.
        """

        package = build_data_package_books(
            (int_to_2byte_array(5) + int_to_2byte_array(7) + int_to_2byte_array(20))
        )

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 10
        assert int.from_bytes(parsed_package.message_type, "little") == 5004
        assert parsed_package.data == bytearray(b"\x05\x00\x07\x00\x14\x00")

    def test_build_data_package_mode(self) -> None:
        """
        Test the `build_data_package_mode` function to ensure it correctly constructs
        a data package and that the resulting package can be parsed back to its
        original components.
        This test verifies:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package matches the expected value.
        - The data content of the parsed package matches the expected input.
        Assertions:
        - The length of the parsed package should be 6.
        - The message type of the parsed package should be 5020.
        - The data content of the parsed package should be a bytearray equivalent to `b"\x01\x00"`.
        """

        package = build_data_package_mode(int_to_2byte_array(1))

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 5020
        assert parsed_package.data == bytearray(b"\x01\x00")
