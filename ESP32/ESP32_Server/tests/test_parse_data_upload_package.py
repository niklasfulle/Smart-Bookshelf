"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")

from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data,
    build_data_upload_package_data_start,
    build_data_upload_package_data_end,
    build_data_upload_package_data_cancel,
    build_data_upload_package_data_error,
)
from protocol.parser.parser_data_upload_package import parse_data_upload_package
from utils.converter import int_to_2byte_array


class TestParseDataUploadPackage:
    """
    -
    """

    def test_parse_data_upload_package_data(self) -> None:
        """
        -
        """
        package = build_data_upload_package_data(
            int_to_2byte_array(1),
            bytearray(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
        )

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 22
        assert int.from_bytes(parsed_package.message_type, "little") == 6002

    def test_parse_data_upload_package_data_start(self) -> None:
        """
        -
        """
        package = build_data_upload_package_data_start(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6001

    def test_parse_data_upload_package_data_end(self) -> None:
        """
        -
        """
        package = build_data_upload_package_data_end()

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 6004

    def test_parse_data_upload_package_data_error(self) -> None:
        """
        -
        """
        package = build_data_upload_package_data_error(bytearray(b"\x00\x00"))

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 6005

    def test_parse_data_upload_package_data_cancel(self) -> None:
        """
        -
        """
        package = build_data_upload_package_data_cancel()

        parsed_package = parse_data_upload_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 6006
