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
    Test suite for verifying the functionality of various package-building methods.
    This class contains unit tests for different types of packages used in the
    communication protocol. Each test ensures that the generated package adheres
    to the expected structure, values, and behavior.
    Attributes:
        file1 (str): A JSON string containing version information for protocol,
            client, and bookshelf versions.
    Test Methods:
        test_build_connection_request:
            Verifies the structure and values of a connection request package.
        test_build_connection_response:
            Verifies the structure and values of a connection response package.
        test_build_connection_approve:
            Verifies the structure and values of a connection approval package.
        test_build_version_request:
            Verifies the structure and values of a version request package.
        test_build_version_response:
            Verifies the structure and values of a version response package,
            including version data.
        test_build_status_request:
            Verifies the structure and values of a status request package.
        test_build_status_response:
            Verifies the structure and values of a status response package,
            including status data.
        test_build_disconnection_request:
            Verifies the structure and values of a disconnection request package,
            including disconnection reason.
        test_build_disconnection_response:
            Verifies the structure and values of a disconnection response package,
            including disconnection reason.
        test_build_sleep_request:
            Verifies the structure and values of a sleep request package.
        test_build_sleep_response:
            Verifies the structure and values of a sleep response package.
        test_build_reboot_request:
            Verifies the structure and values of a reboot request package.
        test_build_reboot_response:
            Verifies the structure and values of a reboot response package.
        test_build_data:
            Verifies the structure and values of a data package, including data
            payload.
        test_build_upload_data:
            Verifies the structure and values of an upload data package, including
            data payload.
    """

    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"server_version_major": 1,"server_version_minor": 0,"Bookshelf_version_major": 1,"Bookshelf_version_minor": 0}'

    def test_build_connection_request(self) -> None:
        """
        Test the `build_connection_request` function to ensure it constructs a valid
        connection request package with the expected attributes.
        This test verifies:
        - The `lenght` field of the package is correctly set to 36.
        - The `message_type` field is correctly set to 3000 (as a bytearray and integer).
        - The `receiver_id` field is correctly set to the provided value (10).
        - The `sender_id` field is correctly set to the provided value (20).
        - The `confirmed_sequence_number` field is correctly set to 0 (as a bytearray and integer).
        - The `confirmed_timestamp` field is correctly set to 0 (as a bytearray and integer).
        Assertions:
        - The `lenght` field matches the expected value.
        - The `message_type` field matches the expected bytearray and integer values.
        - The `receiver_id` and `sender_id` fields match the provided values.
        - The `confirmed_sequence_number` and `confirmed_timestamp` fields are correctly initialized.
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
        Test the `build_connection_response` function to ensure it constructs a valid
        connection response package with the correct attributes.
        This test verifies:
        - The length of the package is correctly set to 36 bytes.
        - The `message_type` is correctly set to `0x0BC2` (3010 in little-endian).
        - The `receiver_id` and `sender_id` are correctly assigned.
        - The `confirmed_sequence_number` matches the provided sequence number.
        - The `confirmed_timestamp` is correctly set to zero.
        Assertions:
        - The length of the package matches the expected value.
        - The `message_type` matches the expected byte sequence and integer value.
        - The `receiver_id` and `sender_id` match the expected integer values.
        - The `confirmed_sequence_number` matches the input sequence number.
        - The `confirmed_timestamp` matches the expected zero value.
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
        Test the `build_connection_approve` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The length of the package is correctly set to 36.
        - The `message_type` is correctly set to `bytearray(b"\xcc\x0b")` and its integer
          representation matches the expected value (3020).
        - The `receiver_id` and `sender_id` are correctly set to 10 and 20, respectively.
        - The `sequence_number` is incremented correctly using `increment_sequence_number`.
        - The `confirmed_sequence_number` matches the original `sequence_number`.
        - The `timestamp` and `confirmed_timestamp` are correctly set to the provided values.
        Assertions:
            - Validates the correctness of each field in the constructed package.
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
        Test the `build_version_request` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The length of the package is correctly calculated.
        - The message type is correctly set and matches the expected value.
        - The receiver ID and sender ID are correctly assigned.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the input sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        Assertions:
        - The package length matches the expected value.
        - The message type matches both the byte representation and integer value.
        - The receiver ID and sender ID are correctly converted from bytes.
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the input sequence number.
        - The timestamp and confirmed timestamp are correctly set.
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
        Test the `build_version_response` function to ensure it constructs a package
        with the correct attributes and data.
        This test verifies:
        - The length of the package is correctly set to 42.
        - The message type is correctly set to `0x0be0` (3040 in little-endian).
        - The receiver ID and sender ID are correctly set to 10 and 20, respectively.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly set.
        - The data field is correctly constructed as a bytearray with the expected values.
        - Individual bytes and slices of the data field match the expected values.
        Assertions:
        - Validate the length, message type, receiver ID, sender ID, sequence numbers,
          timestamps, and data field of the constructed package.
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
                    json_data_reader(self.file1, ["server_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["server_version_minor"], 2)
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
        Test the `build_status_request` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The length of the package is correctly set to 36 bytes.
        - The `message_type` is correctly set to `0x0bea` (3050 in decimal).
        - The `receiver_id` and `sender_id` are correctly assigned.
        - The `sequence_number` is incremented correctly.
        - The `confirmed_sequence_number` matches the original sequence number.
        - The `timestamp` and `confirmed_timestamp` are correctly assigned.
        Assertions:
        - The `lenght` field of the package matches the expected value.
        - The `message_type` field matches the expected bytearray and integer values.
        - The `receiver_id` and `sender_id` fields match the expected values.
        - The `sequence_number` is incremented as expected.
        - The `confirmed_sequence_number` matches the input sequence number.
        - The `timestamp` and `confirmed_timestamp` fields match the input timestamp.
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
        Test the `build_status_response` function to ensure it constructs a valid status
        response package with the correct attributes.
        This test verifies:
        - The length of the package is correctly set to 38 bytes.
        - The message type is correctly set to `0x0BF4` (3060 in decimal).
        - The receiver ID and sender ID are correctly assigned.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the input sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        - The data field is correctly set to represent the `STATUS.RUNNING` value.
        Assertions:
            - The package length matches the expected value.
            - The message type matches the expected value in both byte and integer forms.
            - The receiver ID and sender ID match the input values.
            - The sequence number is incremented as expected.
            - The confirmed sequence number matches the input sequence number.
            - The timestamp and confirmed timestamp match the input values.
            - The data field matches the expected byte representation of the status.
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

        assert int.from_bytes(package.lenght, "little") == 38
        assert package.message_type == bytearray(b"\xf4\x0b")
        assert int.from_bytes(package.message_type, "little") == 3060
        assert int.from_bytes(package.receiver_id, "little") == 10
        assert int.from_bytes(package.sender_id, "little") == 20
        assert package.sequence_number == increment_sequence_number(sequence_number)
        assert package.confirmed_sequence_number == sequence_number
        assert package.timestamp == timestamp
        assert package.confirmed_timestamp == timestamp
        assert package.data == bytearray(b"\x01\x00")

    def test_build_disconnection_request(self) -> None:
        """
        Test the `build_disconnection_request` function to ensure it constructs a
        disconnection request package correctly.
        This test verifies the following:
        - The length of the package is correctly set to 38 bytes.
        - The message type is correctly set to `0x0bfe` (3070 in decimal).
        - The receiver ID and sender ID are correctly assigned.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        - The data field is correctly set to `b"\x00\x00"`.
        Assertions:
            - The package length matches the expected value.
            - The message type matches the expected value in both byte and integer forms.
            - The receiver ID and sender ID are correctly converted from integers.
            - The sequence number is incremented as expected.
            - The confirmed sequence number matches the input sequence number.
            - The timestamp and confirmed timestamp are correctly assigned.
            - The data field matches the expected byte array.
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
            int_to_2byte_array(DISC_REASON.USERREQUEST),
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
        assert package.data == bytearray(b"\x00\x00")

    def test_build_disconnection_response(self) -> None:
        """
        Test the `build_disconnection_response` function to ensure it constructs
        a valid disconnection response package with the correct attributes.
        This test verifies:
        - The length of the package is correctly set to 38 bytes.
        - The message type is correctly set to `0x080C` (3080 in decimal).
        - The receiver ID and sender ID are correctly assigned.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the input sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        - The data field is correctly set to `0x0000`.
        Raises:
            AssertionError: If any of the package attributes do not match the expected values.
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
            int_to_2byte_array(DISC_REASON.USERREQUEST),
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
        assert package.data == bytearray(b"\x00\x00")

    def test_build_sleep_request(self) -> None:
        """
        Test the `build_sleep_request` function to ensure it constructs a package
        with the correct attributes.
        This test verifies the following:
        - The length of the package is correctly set to 36.
        - The `message_type` is correctly set to `bytearray(b"\x12\x0c")` and its
          integer representation matches 3090.
        - The `receiver_id` and `sender_id` are correctly set to 10 and 20, respectively.
        - The `sequence_number` is incremented correctly using `increment_sequence_number`.
        - The `confirmed_sequence_number` matches the original `sequence_number`.
        - The `timestamp` and `confirmed_timestamp` are correctly set to the provided value.
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
        Test the `build_sleep_response` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The length of the package is correctly set to 36.
        - The `message_type` is correctly set to `b"\x1c\x0c"` and its integer value is 3100.
        - The `receiver_id` and `sender_id` are correctly set to 10 and 20, respectively.
        - The `sequence_number` is incremented correctly using `increment_sequence_number`.
        - The `confirmed_sequence_number` matches the original `sequence_number`.
        - The `timestamp` and `confirmed_timestamp` are correctly set to the provided values.
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
        Test the `build_reboot_request` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The `lenght` field of the package is correctly set to 36.
        - The `message_type` field matches the expected bytearray and integer values.
        - The `receiver_id` and `sender_id` fields are correctly set.
        - The `sequence_number` is incremented correctly using `increment_sequence_number`.
        - The `confirmed_sequence_number` matches the original sequence number.
        - The `timestamp` and `confirmed_timestamp` fields are correctly set.
        Assertions:
            - The length of the package matches the expected value.
            - The message type is correctly encoded as a bytearray and integer.
            - Receiver and sender IDs are correctly encoded.
            - Sequence numbers and timestamps are correctly set and confirmed.
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
        Test the `build_reboot_response` function to ensure it constructs a package
        with the correct attributes and values.
        This test verifies:
        - The length of the package is correctly set to 36 bytes.
        - The `message_type` is correctly set to `0x0c` (3120 in little-endian).
        - The `receiver_id` and `sender_id` are correctly assigned.
        - The `sequence_number` is incremented correctly.
        - The `confirmed_sequence_number` matches the input sequence number.
        - The `timestamp` and `confirmed_timestamp` are correctly assigned.
        Assertions:
            - The length of the package matches the expected value.
            - The `message_type` matches the expected bytearray and integer values.
            - The `receiver_id` and `sender_id` match the expected values.
            - The `sequence_number` is incremented as expected.
            - The `confirmed_sequence_number` matches the input sequence number.
            - The `timestamp` and `confirmed_timestamp` match the input timestamp.
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
        Test the `build_data` function to ensure it constructs a data package correctly.
        This test verifies the following:
        - The length of the package is correctly calculated.
        - The message type is correctly set and matches the expected value.
        - The receiver ID and sender ID are correctly assigned.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        - The data payload matches the complete data from the data package.
        - Specific fields within the data payload are correctly encoded.
        Assertions:
        - The length of the package matches the expected value (42).
        - The message type matches the expected bytearray and integer value (5000).
        - The receiver ID and sender ID match the expected values (10 and 20, respectively).
        - The sequence number is incremented as expected.
        - The confirmed sequence number matches the original sequence number.
        - The timestamp and confirmed timestamp match the expected value.
        - The data payload matches the expected complete data.
        - Specific fields within the data payload are correctly encoded:
            - The first 2 bytes represent the value 6.
            - The next 2 bytes represent the value 5020.
            - The next 2 bytes represent the value 1.
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
        Test the `build_upload_data` function to ensure it constructs a data upload package
        correctly with the expected attributes and values.
        This test verifies:
        - The length of the package is correctly set.
        - The message type is correctly assigned and matches the expected values.
        - The receiver ID and sender ID are correctly encoded.
        - The sequence number is incremented correctly.
        - The confirmed sequence number matches the input sequence number.
        - The timestamp and confirmed timestamp are correctly assigned.
        - The data payload matches the expected complete data from the data upload package.
        - Specific parts of the data payload are correctly encoded.
        Assertions:
        - The length of the package matches the expected value.
        - The message type matches the expected byte array and integer value.
        - The receiver ID and sender ID match the expected integer values.
        - The sequence number and confirmed sequence number are correctly set.
        - The timestamp and confirmed timestamp are correctly set.
        - The data payload matches the expected structure and values.
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
