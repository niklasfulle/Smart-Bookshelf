"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")
from protocol.builder.builder_default_package import (
    build_connection_request,
    build_connection_response,
    build_connection_approve,
    build_version_request,
    build_version_response,
    build_status_request,
    build_status_response,
    build_disconnection_request,
    build_disconnection_response,
    build_sleep_request,
    build_sleep_response,
    build_reboot_request,
    build_reboot_response,
    build_data,
    build_upload_data,
)
from protocol.builder.builder_data_package import build_data_package_mode
from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data_start,
)
from protocol.constants.constants import DISC_REASON, STATUS

from utils.build_helper import (
    get_random_sequence_number,
    get_timestamp,
    increment_sequence_number,
)
from utils.converter import int_to_1byte_array, int_to_2byte_array
from utils.json_data_reader import json_data_reader


class TestBuildDefaultPackage:
    """
    -
    """

    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"client_version_major": 1,"client_version_minor": 0,"Bookshelf_version_major": 1,"Bookshelf_version_minor": 0}'

    def test_build_connection_request(self) -> None:
        """
        -
        """
        package = build_connection_request(10, 20, 0, 0, 0, 0)

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\xb8\x0b")
        assert int.from_bytes(package.message_type, "little") == 3000
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.confirmed_sequence_number == bytearray(b"\x00\x00\x00\x00")
        assert int.from_bytes(package.confirmed_sequence_number, "little") == 0
        assert package.confirmed_timestamp == bytearray(b"\x00\x00\x00\x00")
        assert int.from_bytes(package.confirmed_timestamp, "little") == 0

    def test_build_connection_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        package = build_connection_response(10, 20, 0, sequence_number, 0, 0)

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\xc2\x0b")
        assert int.from_bytes(package.message_type, "little") == 3010
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.confirmed_sequence_number == sequence_number
        assert package.confirmed_timestamp == bytearray(b"\x00\x00\x00\x00")
        assert int.from_bytes(package.confirmed_timestamp, "little") == 0

    def test_build_connection_approve(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\xcc\x0b")
        assert int.from_bytes(package.message_type, "little") == 3020
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_version_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\xd6\x0b")
        assert int.from_bytes(package.message_type, "little") == 3030
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_version_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_response(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["protocol_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["protocol_version_minor"], 2)
                )
            ),
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["client_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["client_version_minor"], 2)
                )
            ),
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["Bookshelf_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["Bookshelf_version_minor"], 2)
                )
            ),
        )

        assert int.from_bytes(package.lenght, "little") == 42
        assert package.message_type == bytearray(b"\xe0\x0b")
        assert int.from_bytes(package.message_type, "little") == 3040
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == bytearray(b"\x01\x00\x01\x00\x01\x00")
        assert package.data[0:2] == bytearray(b"\x01\x00")
        assert int.from_bytes(package.data[0:1], "little") == 1
        assert int.from_bytes(package.data[1:2], "little") == 0
        assert int.from_bytes(package.data[2:3], "little") == 1
        assert int.from_bytes(package.data[3:4], "little") == 0
        assert int.from_bytes(package.data[4:5], "little") == 1
        assert int.from_bytes(package.data[5:6], "little") == 0

    def test_build_status_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\xea\x0b")
        assert int.from_bytes(package.message_type, "little") == 3050
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_status_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp, int_to_2byte_array(STATUS.RUNNING)
        )

        assert int.from_bytes(package.lenght, "little") == 38
        assert package.message_type == bytearray(b"\xf4\x0b")
        assert int.from_bytes(package.message_type, "little") == 3060
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == bytearray(B"\x01\x00")

    def test_build_disconnection_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp, int_to_2byte_array(DISC_REASON.USERREQUEST)
        )

        assert int.from_bytes(package.lenght, "little") == 38
        assert package.message_type == bytearray(b"\xfe\x0b")
        assert int.from_bytes(package.message_type, "little") == 3070
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == bytearray(B"\x00\x00")

    def test_build_disconnection_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp, int_to_2byte_array(DISC_REASON.USERREQUEST)
        )

        assert int.from_bytes(package.lenght, "little") == 38
        assert package.message_type == bytearray(b"\x08\x0c")
        assert int.from_bytes(package.message_type, "little") == 3080
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == bytearray(B"\x00\x00")

    def test_build_sleep_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\x12\x0c")
        assert int.from_bytes(package.message_type, "little") == 3090
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_sleep_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"\x1c\x0c")
        assert int.from_bytes(package.message_type, "little") == 3100
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_reboot_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"&\x0c")
        assert int.from_bytes(package.message_type, "little") == 3110
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_reboot_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        assert int.from_bytes(package.lenght, "little") == 36
        assert package.message_type == bytearray(b"0\x0c")
        assert int.from_bytes(package.message_type, "little") == 3120
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp

    def test_build_data(self) -> None:
        """
        -
        """
        data_package = build_data_package_mode(int_to_2byte_array(1))

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        assert int.from_bytes(package.lenght, "little") == 42
        assert package.message_type == bytearray(b"\x88\x13")
        assert int.from_bytes(package.message_type, "little") == 5000
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == data_package.complete_data
        assert int.from_bytes(package.data[0:2], "little") == 6
        assert int.from_bytes(package.data[2:4], "little") == 5020
        assert int.from_bytes(package.data[4:6], "little") == 1

    def test_build_upload_data(self) -> None:
        """
        -
        """
        data_upload_package = build_data_upload_package_data_start(
            int_to_2byte_array(1)
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        assert int.from_bytes(package.lenght, "little") == 42
        assert package.message_type == bytearray(b"p\x17")
        assert int.from_bytes(package.message_type, "little") == 6000
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == data_upload_package.complete_data
        assert int.from_bytes(package.data[0:2], "little") == 6
        assert int.from_bytes(package.data[2:4], "little") == 6001
        assert int.from_bytes(package.data[4:6], "little") == 1
