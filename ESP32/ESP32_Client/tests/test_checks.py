"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from utils.json_data_reader import json_data_reader
from utils.converter import int_to_2byte_array, int_to_1byte_array
from utils.build_helper import get_timestamp, get_random_sequence_number
from utils.checks import check_for_valid_message_type_moment
from hardware.bookshelf import bookshelf
from connection.connection import connection
from protocol.builder.builder_default_package import (
    build_connection_request,
    build_connection_response,
    build_connection_approve,
    build_version_request,
    build_version_response,
    build_status_request,
    build_disconnection_request,
    build_disconnection_response,
    build_sleep_request,
    build_reboot_request,
    build_data,
    build_upload_data,
)
from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data_start,
)
from protocol.builder.builder_data_package import build_data_package_mode
from protocol.constants.constants import DISC_REASON


class TestChecks:
    """
    TestChecks is a test suite for validating the behavior of the `check_for_valid_message_type_moment` function
    under various conditions and states of the `connection_object`. It uses a series of predefined configurations
    and message types to simulate different scenarios.
    Attributes:
        client_config (str): JSON string representing the client configuration, including connection and server details.
        bookshelf_config (str): JSON string representing the bookshelf configuration, including shelving units.
        file1 (str): JSON string representing version information for protocol, client, and bookshelf.
        ip (str): Extracted IP address of the client from `client_config`.
        bookshelf_name (str): Extracted name of the bookshelf from `bookshelf_config`.
        shelving_units (list): Extracted shelving units configuration from `bookshelf_config`.
        bookshelf_object (bookshelf): Bookshelf object initialized with the extracted name, IP, and shelving units.
        client_ip (str): Extracted client IP address from `client_config`.
        client_port (int): Extracted client port from `client_config`.
        server_ip (str): Extracted server IP address from `client_config`.
        server_port (int): Extracted server port from `client_config`.
        sender_id (int): Extracted sender ID from `client_config`.
        receiver_id (int): Extracted receiver ID from `client_config`.
        connection_object (connection): Connection object initialized with client and server details, IDs, and the bookshelf object.
    Methods:
        test_checks1():
            Tests the behavior of `check_for_valid_message_type_moment` when no connection request has been sent.
            Asserts the expected results for various message types.
        test_checks2():
            Tests the behavior of `check_for_valid_message_type_moment` after a connection request has been sent.
            Asserts the expected results for various message types.
        test_checks3():
            Tests the behavior of `check_for_valid_message_type_moment` after a connection request has been sent
            and a handshake has been completed. Asserts the expected results for various message types.
        test_checks4():
            Tests the behavior of `check_for_valid_message_type_moment` after a connection request, handshake,
            and version check have been completed. Asserts the expected results for various message types.
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40006 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50006}}'
    bookshelf_config: str = '{"name": "bookshelf_name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'
    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"client_version_major": 1,"client_version_minor": 0,"Bookshelf_version_major": 1,"Bookshelf_version_minor": 0}'

    ip = json_data_reader(client_config, ["connection", "ip"], 2)
    bookshelf_name = json_data_reader(bookshelf_config, ["name"], 2)
    shelving_units = json_data_reader(bookshelf_config, ["shelving_units"], 2)

    bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

    client_ip = json_data_reader(client_config, ["connection", "ip"], 2)
    client_port = json_data_reader(client_config, ["connection", "port"], 2)
    server_ip = json_data_reader(client_config, ["server", "ip"], 2)
    server_port = json_data_reader(client_config, ["server", "port"], 2)
    sender_id = json_data_reader(client_config, ["id"], 2)
    receiver_id = json_data_reader(client_config, ["server", "id"], 2)

    connection_object: connection = connection(
        (client_ip, client_port),
        (server_ip, server_port),
        receiver_id,
        sender_id,
        bookshelf_object,
    )

    def test_checks1(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test verifies the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the provided connection object and
        message packages.
        Test Cases:
        - Connection Request: Expected result is False.
        - Connection Response: Expected result is False.
        - Connection Approve: Expected result is False.
        - Version Request: Expected result is False.
        - Version Response: Expected result is False.
        - Status Request: Expected result is False.
        - Disconnection Request: Expected result is True.
        - Disconnection Response: Expected result is False.
        - Sleep Request: Expected result is False.
        - Reboot Request: Expected result is False.
        - Data Package: Expected result is False.
        - Data Upload Package: Expected result is False.
        Assertions:
        - Each result is asserted against its expected value to ensure correctness.
        """

        package = build_connection_request(10, 20, 0, 0, 0, 0)

        result1 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        package = build_connection_response(10, 20, 0, sequence_number, 0, 0)

        result2 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result3 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result4 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result10 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result11 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result12 = check_for_valid_message_type_moment(self.connection_object, package)

        assert result1 is False
        assert result2 is True
        assert result3 is False
        assert result4 is False
        assert result5 is False
        assert result6 is False
        assert result7 is True
        assert result8 is False
        assert result9 is False
        assert result10 is False
        assert result11 is False
        assert result12 is False

    def test_checks2(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test verifies the behavior of the `check_for_valid_message_type_moment` function
        when processing different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the current state of the connection
        object and the provided package.
        Test Cases:
            1. Connection Request: Should return False.
            2. Connection Response: Should return True.
            3. Connection Approve: Should return False.
            4. Version Request: Should return False.
            5. Version Response: Should return False.
            6. Status Request: Should return False.
            7. Disconnection Request: Should return True.
            8. Disconnection Response: Should return True.
            9. Sleep Request: Should return False.
            10. Reboot Request: Should return False.
            11. Data Package: Should return False.
            12. Data Upload Package: Should return False.
        Assertions:
            - Each result is asserted against the expected outcome for the corresponding
              message type to validate the function's correctness.
        """

        self.connection_object.connection_request_send = True

        package = build_connection_request(10, 20, 0, 0, 0, 0)

        result1 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        package = build_connection_response(10, 20, 0, sequence_number, 0, 0)

        result2 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result3 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result4 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result10 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result11 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result12 = check_for_valid_message_type_moment(self.connection_object, package)

        assert result1 is False
        assert result2 is True
        assert result3 is False
        assert result4 is False
        assert result5 is False
        assert result6 is False
        assert result7 is True
        assert result8 is True
        assert result9 is False
        assert result10 is False
        assert result11 is False
        assert result12 is False

    def test_checks3(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test verifies the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the current state of the connection
        object.
        Test Cases:
            1. Connection Request: Should return False.
            2. Connection Response: Should return False.
            3. Connection Approve: Should return False.
            4. Version Request: Should return False.
            5. Version Response: Should return True.
            6. Status Request: Should return False.
            7. Disconnection Request: Should return True.
            8. Disconnection Response: Should return True.
            9. Sleep Request: Should return False.
            10. Reboot Request: Should return False.
            11. Data Package: Should return False.
            12. Data Upload Package: Should return False.
        Assertions:
            - Each result is compared against the expected outcome to ensure correctness.
        """

        self.connection_object.connection_request_send = True
        self.connection_object.handshake = True

        package = build_connection_request(10, 20, 0, 0, 0, 0)

        result1 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        package = build_connection_response(10, 20, 0, sequence_number, 0, 0)

        result2 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result3 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result4 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result10 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result11 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result12 = check_for_valid_message_type_moment(self.connection_object, package)

        assert result1 is False
        assert result2 is False
        assert result3 is False
        assert result4 is False
        assert result5 is True
        assert result6 is False
        assert result7 is True
        assert result8 is True
        assert result9 is False
        assert result10 is False
        assert result11 is False
        assert result12 is False

    def test_checks4(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test verifies the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the current state of the connection
        object.
        Test Scenarios:
        - Connection Request: Should return False.
        - Connection Response: Should return False.
        - Connection Approve: Should return False.
        - Version Request: Should return False.
        - Version Response: Should return False.
        - Status Request: Should return True.
        - Disconnection Request: Should return True.
        - Disconnection Response: Should return True.
        - Sleep Request: Should return True.
        - Reboot Request: Should return True.
        - Data Message: Should return True.
        - Data Upload Message: Should return True.
        Preconditions:
        - The connection object is initialized with `connection_request_send`, `handshake`,
          and `version_check` set to True.
        - Various helper functions are used to build the respective message packages.
        Assertions:
        - The results of `check_for_valid_message_type_moment` are asserted against the
          expected outcomes for each message type.
        """

        self.connection_object.connection_request_send = True
        self.connection_object.handshake = True
        self.connection_object.version_check = True

        package = build_connection_request(10, 20, 0, 0, 0, 0)

        result1 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        package = build_connection_response(10, 20, 0, sequence_number, 0, 0)

        result2 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result3 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result4 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result10 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result11 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result12 = check_for_valid_message_type_moment(self.connection_object, package)

        assert result1 is False
        assert result2 is False
        assert result3 is False
        assert result4 is False
        assert result5 is False
        assert result6 is True
        assert result7 is True
        assert result8 is True
        assert result9 is True
        assert result10 is True
        assert result11 is True
        assert result12 is True
