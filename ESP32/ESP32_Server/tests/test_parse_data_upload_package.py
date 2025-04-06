"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")

from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data,
    build_data_upload_package_data_start,
    build_data_upload_package_data_request,
    build_data_upload_package_data_response,
    build_data_upload_package_data_end,
    build_data_upload_package_data_cancel,
    build_data_upload_package_data_error,
)
from protocol.parser.parser_data_upload_package import parse_data_upload_package
from utils.converter import int_to_2byte_array


class TestParseDataUploadPackage:
    """
    Test suite for verifying the functionality of parsing data upload packages.
    This class contains unit tests for the following scenarios:
    1. Parsing a standard data upload package.
    2. Parsing a data upload package that marks the start of data transmission.
    3. Parsing a data upload package that marks the end of data transmission.
    4. Parsing a data upload package that indicates an error during data transmission.
    5. Parsing a data upload package that cancels the data transmission.
    Each test ensures that the parsed package's length and message type match the expected values.
    """

    def test_parse_data_upload_package_data_start(self) -> None:
        """
        Test the `parse_data_upload_package` function for a data upload package
        with a "data start" message type.
        This test verifies that the parsed package has the correct length and
        message type when provided with a package created using
        `build_data_upload_package_data_start`.
        Assertions:
            - The length of the parsed package matches the expected value (6).
            - The message type of the parsed package matches the expected value (6001).
        """

        package = build_data_upload_package_data_start(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6001

    def test_parse_data_upload_package_data_request(self) -> None:
        package = build_data_upload_package_data_request(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6002

    def test_parse_data_upload_package_data_response(self) -> None:
        package = build_data_upload_package_data_response(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6003

    def test_parse_data_upload_package_data(self) -> None:
        """
        Test the `parse_data_upload_package` function to ensure it correctly parses
        a data upload package created by `build_data_upload_package_data`.
        This test verifies:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package matches the expected value.
        Assertions:
        - The length of the parsed package should be 22.
        - The message type of the parsed package should be 6002.
        """

        package = build_data_upload_package_data(
            int_to_2byte_array(1),
            bytearray(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
        )

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 22
        assert int.from_bytes(parsed_package.message_type, "little") == 6004

    def test_parse_data_upload_package_data_end(self) -> None:
        """
        Test the `parse_data_upload_package` function for handling a data upload package
        with a "data end" message type.
        This test verifies:
        - The `lenght` field in the parsed package matches the expected value.
        - The `message_type` field in the parsed package matches the expected value.
        Assertions:
        - The `lenght` field, when converted from bytes, should equal 4.
        - The `message_type` field, when converted from bytes, should equal 6003.
        """

        package = build_data_upload_package_data_end()

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 6006

    def test_parse_data_upload_package_data_error(self) -> None:
        """
        Test the `parse_data_upload_package` function for handling a data error package.
        This test verifies that the `parse_data_upload_package` function correctly parses
        a data upload package with an error and extracts the expected fields, such as
        `length` and `message_type`.
        Assertions:
            - The `length` field of the parsed package matches the expected value (6).
            - The `message_type` field of the parsed package matches the expected value (6004).
        Preconditions:
            - The `build_data_upload_package_data_error` function is used to construct
              a package with a specific error payload.
        """

        package = build_data_upload_package_data_error(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6007

    def test_parse_data_upload_package_data_cancel(self) -> None:
        """
        Test the `parse_data_upload_package` function for handling a data upload package
        with a "cancel" message type.
        This test verifies that the parsed package correctly interprets the length and
        message type fields from the provided package data.
        Assertions:
            - The `lenght` field of the parsed package matches the expected value (4).
            - The `message_type` field of the parsed package matches the expected value (6005).
        """

        package = build_data_upload_package_data_cancel()

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 6008
