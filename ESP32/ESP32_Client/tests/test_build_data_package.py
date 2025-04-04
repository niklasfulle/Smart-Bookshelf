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
from utils.converter import int_to_2byte_array
from datatype.book import book


class TestBuildDataPackage:
    """
    Test suite for verifying the functionality of data package building functions.
    This test class contains unit tests for various functions that construct data
    packages with specific message types and data payloads. Each test ensures that
    the generated package has the correct length, message type, and data content.
    Test Cases:
    - `test_build_data_package_light_on`: Verifies the package for turning the light on.
    - `test_build_data_package_light_off`: Verifies the package for turning the light off.
    - `test_build_data_package_book`: Verifies the package for a single book's data.
    - `test_build_data_package_books`: Verifies the package for multiple books' data.
    - `test_build_data_package_mode`: Verifies the package for setting a specific mode.
    """

    def test_build_data_package_light_on(self) -> None:
        """
        Test the `build_data_package_light_on` function.
        This test verifies that the `build_data_package_light_on` function correctly
        constructs a data package with the expected length and message type.
        Assertions:
            - The `lenght` field of the package, when converted from bytes to an integer
              using little-endian byte order, should equal 4.
            - The `message_type` field of the package, when converted from bytes to an integer
              using little-endian byte order, should equal 5001.
        """

        package = build_data_package_light_on()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 5001

    def test_build_data_package_light_off(self) -> None:
        """
        Test the `build_data_package_light_off` function.
        This test verifies that the `build_data_package_light_off` function correctly
        constructs a data package with the expected length and message type when the
        light is turned off.
        Assertions:
            - The `length` field of the package should be 4 when converted from bytes.
            - The `message_type` field of the package should be 5002 when converted from bytes.
        """

        package = build_data_package_light_off()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 5002

    def test_build_data_package_book(self) -> None:
        """
        Test the `build_data_package_book` function.
        This test verifies that the `build_data_package_book` function correctly
        constructs a data package for a book with the given parameters.
        Assertions:
        - The `length` field of the package is correctly set to 8 when converted
          from bytes using little-endian format.
        - The `message_type` field of the package is correctly set to 5003 when
          converted from bytes using little-endian format.
        - The first two bytes of the `data` field represent the book ID (1) when
          converted from bytes using little-endian format.
        - The next two bytes of the `data` field represent the book value (12)
          when converted from bytes using little-endian format.
        """

        package = build_data_package_book(book(1, 12).data)

        assert int.from_bytes(package.lenght, "little") == 8
        assert int.from_bytes(package.message_type, "little") == 5003
        assert int.from_bytes(package.data[0:2], "little") == 1
        assert int.from_bytes(package.data[2:4], "little") == 12

    def test_build_data_package_books(self) -> None:
        """
        Test the `build_data_package_books` function to ensure it correctly constructs
        a data package for books.
        This test verifies:
        - The `length` field of the package is correctly set to 12.
        - The `message_type` field of the package is correctly set to 5004.
        - The `data` field contains the correct book information, including:
            - Book 1 with ID 1 and quantity 12.
            - Book 2 with ID 3 and quantity 2.
        Assertions:
        - The `length` field is converted from bytes and matches the expected value.
        - The `message_type` field is converted from bytes and matches the expected value.
        - The `data` field is parsed and matches the expected book IDs and quantities.
        """

        package = build_data_package_books(data=(book(1, 12).data + book(3, 2).data))

        assert int.from_bytes(package.lenght, "little") == 12
        assert int.from_bytes(package.message_type, "little") == 5004
        assert int.from_bytes(package.data[0:2], "little") == 1
        assert int.from_bytes(package.data[2:4], "little") == 12
        assert int.from_bytes(package.data[4:6], "little") == 3
        assert int.from_bytes(package.data[6:8], "little") == 2

    def test_build_data_package_mode(self) -> None:
        """
        Test the `build_data_package_mode` function to ensure it correctly constructs
        a data package with the given input.
        This test verifies:
        - The `length` field of the package is correctly set to 6.
        - The `message_type` field of the package is correctly set to 5020.
        - The `data` field of the package contains the expected value derived from the input.
        Assertions:
        - The `length` field matches the expected value.
        - The `message_type` field matches the expected value.
        - The `data` field contains the correct representation of the input.
        Raises:
            AssertionError: If any of the assertions fail.
        """

        package = build_data_package_mode(int_to_2byte_array(1))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 5020
        assert int.from_bytes(package.data[0:2], "little") == 1
