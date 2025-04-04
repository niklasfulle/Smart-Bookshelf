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
    Test suite for parsing various types of packages in the Smart Bookshelf ESP32 Client.
    This test class contains methods to validate the parsing functionality for different
    package types, ensuring that the parsed data matches the expected values.
    Test Methods:
        - test_parse_connection_request: Tests parsing of a connection request package.
        - test_parse_connection_response: Tests parsing of a connection response package.
        - test_parse_connection_approve: Tests parsing of a connection approval package.
        - test_parse_version_request: Tests parsing of a version request package.
        - test_parse_version_response: Tests parsing of a version response package.
        - test_parse_status_request: Tests parsing of a status request package.
        - test_parse_status_response: Tests parsing of a status response package.
        - test_parse_disconnection_request: Tests parsing of a disconnection request package.
        - test_parse_disconnection_response: Tests parsing of a disconnection response package.
        - test_parse_sleep_request: Tests parsing of a sleep request package.
        - test_parse_sleep_response: Tests parsing of a sleep response package.
        - test_parse_reboot_request: Tests parsing of a reboot request package.
        - test_parse_reboot_response: Tests parsing of a reboot response package.
        - test_parse_data: Tests parsing of a data package.
        - test_parse_upload_data: Tests parsing of an upload data package.
    Each test validates:
        - The length of the parsed package.
        - The message type of the parsed package.
        - The receiver and sender IDs.
        - The sequence number and confirmed sequence number.
        - The timestamp and confirmed timestamp.
        - Additional data fields, if applicable, such as status, disconnection reason, or data payload.
    """

    def test_parse_connection_request(self) -> None:
        """
        Test the `parse_package` function for correctly parsing a connection request package.
        This test verifies that the `parse_package` function correctly interprets the data
        from a connection request package built using the `build_connection_request` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correctly identified.
        - The receiver ID and sender ID are correctly extracted.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The length of the parsed package matches the expected value (36).
            - The message type of the parsed package is 3000.
            - The receiver ID is 10.
            - The sender ID is 20.
            - The sequence number is incremented correctly.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp and confirmed timestamp are correctly parsed.
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
        Test the parsing of a connection response package.
        This test verifies that the `parse_package` function correctly parses
        a connection response package built using the `build_connection_response`
        function. It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The length of the parsed package is 36.
            - The message type of the parsed package is 3010.
            - The receiver ID is 10.
            - The sender ID is 20.
            - The sequence number is incremented correctly.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp and confirmed timestamp match the original values.
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
        Test the parsing of a connection approve package.
        This test verifies that the `parse_package` function correctly parses
        a connection approve package built using the `build_connection_approve` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The parsed package's length matches the expected value (36).
            - The parsed package's message type matches the expected value (3020).
            - The parsed package's receiver ID matches the expected value (10).
            - The parsed package's sender ID matches the expected value (20).
            - The parsed package's sequence number is incremented correctly.
            - The parsed package's confirmed sequence number matches the original.
            - The parsed package's timestamp matches the original timestamp.
            - The parsed package's confirmed timestamp matches the original timestamp.
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
        Test the `parse_package` function for correctly parsing a version request package.
        This test verifies that the `parse_package` function correctly interprets the
        data from a version request package built using the `build_version_request` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correctly identified.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The length of the parsed package matches the expected value (36).
            - The message type matches the expected value (3030).
            - The receiver ID and sender ID are correctly parsed.
            - The sequence number is incremented correctly.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp and confirmed timestamp are correctly parsed.
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
        Test the parsing of a version response package.
        This test verifies that the `parse_package` function correctly parses a
        version response package created by the `build_version_response` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The length of the parsed package is 42.
            - The message type of the parsed package is 3040.
            - The receiver ID is 10.
            - The sender ID is 20.
            - The sequence number is incremented correctly.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp and confirmed timestamp are correctly parsed.
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
        Test the `parse_package` function for a status request package.
        This test verifies that the `parse_package` function correctly parses a
        status request package created by the `build_status_request` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The length of the parsed package is 36.
            - The message type of the parsed package is 3050.
            - The receiver ID is 10.
            - The sender ID is 20.
            - The sequence number is incremented correctly.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp and confirmed timestamp match the original values.
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
        Test the `parse_package` function for correctly parsing a status response package.
        This test verifies that the `parse_package` function correctly interprets a
        status response package built using the `build_status_response` function.
        It ensures that all fields in the parsed package match the expected values.
        Assertions:
            - The length of the parsed package matches the expected value (38 bytes).
            - The message type of the parsed package matches the expected value (3060).
            - The receiver ID matches the expected value (10).
            - The sender ID matches the expected value (20).
            - The sequence number is correctly incremented.
            - The confirmed sequence number matches the original sequence number.
            - The timestamp matches the original timestamp.
            - The confirmed timestamp matches the original timestamp.
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
        Test the parsing of a disconnection request package.
        This test verifies that a disconnection request package is correctly built
        and parsed, ensuring all fields match the expected values.
        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a disconnection request package with specific parameters.
        3. Parse the package and validate the parsed fields.
        Assertions:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
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
        Test the parsing of a disconnection response package.
        This test verifies that the `parse_package` function correctly parses a
        disconnection response package built using the `build_disconnection_response`
        function. It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is correctly incremented and matches the expected value.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed and match the expected values.
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
        Test the parsing of a sleep request package.
        This test verifies that a sleep request package is correctly parsed
        and its fields match the expected values. It ensures that the package
        length, message type, receiver ID, sender ID, sequence number, confirmed
        sequence number, timestamp, and confirmed timestamp are properly extracted
        and validated.
        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a sleep request package using the generated values.
        3. Parse the package data.
        4. Assert that the parsed fields match the expected values:
           - Length of the package.
           - Message type identifier.
           - Receiver and sender IDs.
           - Sequence number and confirmed sequence number.
           - Timestamp and confirmed timestamp.
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
        Test the `parse_package` function for parsing a sleep response package.
        This test verifies that the `parse_package` function correctly parses a
        sleep response package built using the `build_sleep_response` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The parsed package length matches the expected value (36).
            - The parsed package message type matches the expected value (3100).
            - The parsed receiver ID and sender ID match the input values.
            - The parsed sequence number is correctly incremented.
            - The parsed confirmed sequence number matches the input sequence number.
            - The parsed timestamp and confirmed timestamp match the input values.
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
        Test the parsing of a reboot request package.
        This test verifies that a reboot request package is correctly built and
        parsed, ensuring all fields match the expected values.
        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a reboot request package using the generated values.
        3. Parse the package's complete data.
        4. Assert that the parsed package fields match the expected values:
           - Length of the package.
           - Message type.
           - Receiver ID.
           - Sender ID.
           - Sequence number (incremented correctly).
           - Confirmed sequence number.
           - Timestamp.
           - Confirmed timestamp.
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
        Test the `parse_package` function with a reboot response package.
        This test verifies that the `parse_package` function correctly parses a
        reboot response package built using the `build_reboot_response` function.
        It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver ID and sender ID are correctly parsed.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        Assertions:
            - The parsed package's length matches the expected value.
            - The parsed package's message type matches the expected value.
            - The parsed package's receiver ID and sender ID match the expected values.
            - The parsed package's sequence number is incremented correctly.
            - The parsed package's confirmed sequence number matches the original.
            - The parsed package's timestamp and confirmed timestamp match the original.
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
        Test the parsing of a data package.
        This test verifies that a data package is correctly built, sent, and parsed,
        ensuring all fields match the expected values.
        Steps:
        1. Build a data package using `build_data_package_mode` with a sample input.
        2. Generate a random sequence number and timestamp.
        3. Construct a complete data package using `build_data`.
        4. Parse the constructed package using `parse_package`.
        5. Assert that all parsed fields match the expected values:
           - Length of the package.
           - Message type.
           - Receiver ID.
           - Sender ID.
           - Sequence number (incremented correctly).
           - Confirmed sequence number.
           - Timestamp.
           - Confirmed timestamp.
           - Data content.
        Raises:
            AssertionError: If any of the parsed fields do not match the expected values.
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
        Test the parsing of an upload data package.
        This test verifies that the `parse_package` function correctly parses
        a package created by `build_upload_data`. It checks the following:
        - The length of the parsed package matches the expected value.
        - The message type of the parsed package is correct.
        - The receiver and sender IDs are correctly parsed.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly parsed.
        - The data in the parsed package matches the original data.
        Assertions:
            - The parsed package length is 42.
            - The parsed message type is 6000.
            - The parsed receiver ID is 10.
            - The parsed sender ID is 20.
            - The parsed sequence number is the incremented value of the original.
            - The parsed confirmed sequence number matches the original.
            - The parsed timestamp matches the original.
            - The parsed confirmed timestamp matches the original.
            - The parsed data matches the original data.
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
