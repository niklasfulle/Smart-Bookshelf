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
    -
    """

    def test_parse_data_package_light_on(self) -> None:
        """
        -
        """
        package = build_data_package_light_on()

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 5001

    def test_build_data_package_light_off(self) -> None:
        """
        -
        """
        package = build_data_package_light_off()

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 4
        assert int.from_bytes(parsed_package.message_type, "little") == 5002

    def test_build_data_package_book(self) -> None:
        """
        -
        """
        package = build_data_package_book(int_to_2byte_array(5))

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 5003
        assert parsed_package.data == bytearray(b"\x05\x00")

    def test_build_data_package_books(self) -> None:
        """
        -
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
        -
        """
        package = build_data_package_mode(int_to_2byte_array(1))

        parsed_package = parse_data_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 6
        assert int.from_bytes(parsed_package.message_type, "little") == 5020
        assert parsed_package.data == bytearray(b"\x01\x00")
