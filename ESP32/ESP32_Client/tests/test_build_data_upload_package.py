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
    build_data_upload_package_data_confirm,
)
from utils.converter import int_to_2byte_array


class TestBuildDataUploadPackage:
    """
    Test suite for verifying the functionality of building data upload packages.
    This class contains unit tests for various functions that create different types
    of data upload packages. Each test ensures that the generated package has the
    correct length, message type, and data content.
    Tests:
        - test_build_data_upload_package_data: Verifies the creation of a standard
          data upload package with specific data and checks its length, message type,
          and data content.
        - test_build_data_upload_package_data_start: Verifies the creation of a
          "start" data upload package and checks its length and message type.
        - test_build_data_upload_package_data_end: Verifies the creation of an "end"
          data upload package and checks its length and message type.
        - test_build_data_upload_package_data_error: Verifies the creation of an
          "error" data upload package with specific data and checks its length,
          message type, and data content.
        - test_build_data_upload_package_data_cancel: Verifies the creation of a
          "cancel" data upload package and checks its length and message type.
    """

    def test_build_data_upload_package_data_start(self) -> None:
        """
        Test the `build_data_upload_package_data_start` function.
        This test verifies that the `build_data_upload_package_data_start` function
        correctly constructs a data upload package with the expected length and
        message type.
        Assertions:
            - The `length` field of the package should be 6 when converted from bytes.
            - The `message_type` field of the package should be 6001 when converted from bytes.
        """

        package = build_data_upload_package_data_start(bytearray(b"\x00\x00"))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 6001

    def test_build_data_upload_package_data_request(self) -> None:
        package = build_data_upload_package_data_request(bytearray(b"\x00\x00"))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 6002

    def test_build_data_upload_package_data_response(self) -> None:
        package = build_data_upload_package_data_response(bytearray(b"\x00\x00"))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 6003

    def test_build_data_upload_package_data(self) -> None:
        """
        Test the `build_data_upload_package_data` function.
        This test verifies that the `build_data_upload_package_data` function correctly
        constructs a data upload package with the expected length, message type, and data.
        Assertions:
            - The `lenght` field of the package is correctly set to 22.
            - The `message_type` field of the package is correctly set to 6002.
            - The first two bytes of the `data` field in the package are correctly set to 1.
        """

        package = build_data_upload_package_data(
            int_to_2byte_array(1),
            bytearray(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
        )

        assert int.from_bytes(package.lenght, "little") == 22
        assert int.from_bytes(package.message_type, "little") == 6004
        assert int.from_bytes(package.data[0:2], "little") == 1

    def test_build_data_upload_package_data_confirm(self) -> None:
        """
        Test the `build_data_upload_package_data_confirm` function.
        This test verifies that the `build_data_upload_package_data_confirm` function
        correctly builds a data upload package with the expected structure and values.
        Assertions:
        - The `lenght` field of the package is correctly set to 6.
        - The `message_type` field of the package is correctly set to 6003.
        - The first two bytes of the `data` field in the package are correctly set to 1.
        Returns:
            None
        """

        package = build_data_upload_package_data_confirm(
            int_to_2byte_array(1),
        )

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 6005
        assert int.from_bytes(package.data[0:2], "little") == 1

    def test_build_data_upload_package_data_end(self) -> None:
        """
        Test the `build_data_upload_package_data_end` function.
        This test verifies that the `build_data_upload_package_data_end` function
        correctly constructs a data upload package with the expected length and
        message type.
        Assertions:
            - The `length` field of the package should be 4 when interpreted as a
              little-endian integer.
            - The `message_type` field of the package should be 6003 when interpreted
              as a little-endian integer.
        """

        package = build_data_upload_package_data_end()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 6006

    def test_build_data_upload_package_data_error(self) -> None:
        """
        Test case for the `build_data_upload_package_data_error` function.
        This test verifies that the `build_data_upload_package_data_error` function
        correctly constructs a data upload package with the expected structure and values.
        Assertions:
        - The `length` field of the package should be 6 when converted from bytes.
        - The `message_type` field of the package should be 6004 when converted from bytes.
        - The first two bytes of the `data` field should be 0 when converted from bytes.
        """

        package = build_data_upload_package_data_error(bytearray(b"\x00\x00"))

        assert int.from_bytes(package.lenght, "little") == 6
        assert int.from_bytes(package.message_type, "little") == 6007
        assert int.from_bytes(package.data[0:2], "little") == 0

    def test_build_data_upload_package_data_cancel(self) -> None:
        """
        Test the `build_data_upload_package_data_cancel` function.
        This test verifies that the `build_data_upload_package_data_cancel` function
        correctly constructs a data upload package with the expected length and
        message type.
        Assertions:
            - The `lenght` field of the package, when converted from bytes, should be 4.
            - The `message_type` field of the package, when converted from bytes, should be 6005.
        """

        package = build_data_upload_package_data_cancel()

        assert int.from_bytes(package.lenght, "little") == 4
        assert int.from_bytes(package.message_type, "little") == 6008
