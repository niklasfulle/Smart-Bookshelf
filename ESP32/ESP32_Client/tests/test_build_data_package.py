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
    -
    """

    def test_build_data_package_light_on(self) -> None:
        """
        -
        """
        package = build_data_package_light_on()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 5001

    def test_build_data_package_light_off(self) -> None:
        """
        -
        """
        package = build_data_package_light_off()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 5002

    def test_build_data_package_book(self) -> None:
        """
        -
        """
        package = build_data_package_book(book(1,12).data)

        assert int.from_bytes(package.lenght, "little") == 8
        assert int.from_bytes(package.message_type, "little") == 5003
        assert int.from_bytes(package.data[0:2], "little") == 1
        assert int.from_bytes(package.data[2:4], "little") == 12

    def test_build_data_package_books(self) -> None:
        """
        -
        """
        package = build_data_package_books(
            data = (book(1,12).data + book(3,2).data)
        )

        assert int.from_bytes(package.lenght, "little") == 12
        assert int.from_bytes(package.message_type, "little") == 5004
        assert int.from_bytes(package.data[0:2], "little") == 1
        assert int.from_bytes(package.data[2:4], "little") == 12
        assert int.from_bytes(package.data[4:6], "little") == 3
        assert int.from_bytes(package.data[6:8], "little") == 2

    def test_build_data_package_mode(self) -> None:
        """
        -
        """
        package = build_data_package_mode(int_to_2byte_array(1))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 5020
        assert int.from_bytes(package.data[0:2], "little") == 1
