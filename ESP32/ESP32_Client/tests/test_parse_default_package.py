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
from protocol.parser.parser_default_package import parse_package
from protocol.constants.constants import DISC_REASON, STATUS
from utils.build_helper import (
    get_timestamp,
    get_random_sequence_number,
    increment_sequence_number,
)
from utils.converter import int_to_2byte_array


class TestParseDefaultPackage:
    """
    -
    """

    def test_parse_connection_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3000
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_connection_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3010
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_connection_approve(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3020
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_version_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3030
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_version_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        placeholder = int_to_2byte_array(0)
        package = build_version_response(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            placeholder,
            placeholder,
            placeholder,
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 42
        assert int.from_bytes(parsed_package.message_type, "little") == 3040
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_status_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3050
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_status_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_response(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(STATUS.RUNNING),
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 38
        assert int.from_bytes(parsed_package.message_type, "little") == 3060
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_disconnection_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_request(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.TIMEOUT),
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 38
        assert int.from_bytes(parsed_package.message_type, "little") == 3070
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_disconnection_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_response(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.TIMEOUT),
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 38
        assert int.from_bytes(parsed_package.message_type, "little") == 3080
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_sleep_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3090
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_sleep_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3100
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_reboot_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3110
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_reboot_response(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.message_type, "little") == 3120
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp

    def test_parse_data(self) -> None:
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

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 42
        assert int.from_bytes(parsed_package.message_type, "little") == 5000
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp
        assert parsed_package.data == data_package.complete_data

    def test_parse_upload_data(self) -> None:
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

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 42
        assert int.from_bytes(parsed_package.message_type, "little") == 6000
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(
            sequence_number
        )
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp
        assert parsed_package.data == data_upload_package.complete_data
