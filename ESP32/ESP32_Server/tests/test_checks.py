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
    build_status_response,
    build_disconnection_request,
    build_disconnection_response,
    build_sleep_response,
    build_reboot_response,
    build_data,
    build_upload_data,
)
from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data_start,
)
from protocol.builder.builder_data_package import build_data_package_mode
from protocol.constants.constants import DISC_REASON, STATUS


class TestChecks:
    """
    TestChecks is a test suite designed to validate the behavior of the `check_for_valid_message_type_moment` function
    under various conditions. It simulates different states of a connection object and verifies the correctness of
    message type handling for a smart bookshelf system.
    Attributes:
        client_config (str): JSON string containing client configuration details such as ID, name, connection IP, and port.
        bookshelf_config (str): JSON string containing bookshelf configuration details such as name and shelving units.
        file1 (str): JSON string containing protocol, server, and bookshelf version information.
        ip (str): Extracted IP address of the client from the client configuration.
        bookshelf_name (str): Extracted name of the bookshelf from the bookshelf configuration.
        shelving_units (list): Extracted shelving unit details from the bookshelf configuration.
        bookshelf_object (bookshelf): Bookshelf object initialized with the extracted details.
        client_ip (str): Extracted client IP address from the client configuration.
        client_port (int): Extracted client port from the client configuration.
        server_ip (str): Extracted server IP address from the client configuration.
        server_port (int): Extracted server port from the client configuration.
        sender_id (int): Extracted sender ID from the client configuration.
        receiver_id (int): Extracted receiver ID from the client configuration.
        connection_object (connection): Connection object initialized with the extracted details.
    Methods:
        test_checks1():
            Tests the behavior of `check_for_valid_message_type_moment` when no connection request has been sent.
            Asserts the expected results for various message types.
        test_checks2():
            Tests the behavior of `check_for_valid_message_type_moment` when a connection request has been sent.
            Asserts the expected results for various message types.
        test_checks3():
            Tests the behavior of `check_for_valid_message_type_moment` when a connection request has been sent
            and the handshake is complete. Asserts the expected results for various message types.
        test_checks4():
            Tests the behavior of `check_for_valid_message_type_moment` when a connection request has been sent,
            the handshake is complete, and the version check is complete. Asserts the expected results for various
            message types.
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40008 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50008}}'
    bookshelf_config: str = '{"name": "bookshelf_name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'
    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"server_version_major": 1,"server_version_minor": 0,"Bookshelf_version_major": 1,"Bookshelf_version_minor": 0}'

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
        This test validates the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the constructed packages.
        Test Cases:
        - Connection Request: Should return True.
        - Connection Response: Should return False.
        - Connection Approve: Should return False.
        - Version Request: Should return False.
        - Version Response: Should return False.
        - Status Response: Should return False.
        - Sleep Response: Should return False.
        - Reboot Response: Should return False.
        - Disconnection Request: Should return True.
        - Disconnection Response: Should return False.
        - Data Package: Should return False.
        - Data Upload Package: Should return False.
        Assertions:
        - Each result is asserted against the expected outcome to verify correctness.
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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

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

        assert result1 is True
        assert result2 is False
        assert result3 is False
        assert result4 is False
        assert result5 is False
        assert result6 is False
        assert result7 is False
        assert result8 is False
        assert result9 is True
        assert result10 is False
        assert result11 is False
        assert result12 is False

    def test_checks2(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test validates the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the current state of the connection object.
        Test Cases:
            1. Connection Request: Should return False.
            2. Connection Response: Should return False.
            3. Connection Approve: Should return True.
            4. Version Request: Should return False.
            5. Version Response: Should return False.
            6. Status Response: Should return False.
            7. Sleep Response: Should return False.
            8. Reboot Response: Should return False.
            9. Disconnection Request: Should return True.
            10. Disconnection Response: Should return True.
            11. Data Package: Should return False.
            12. Data Upload Package: Should return False.
        Assertions:
            - Each result is asserted against its expected value to ensure correctness.
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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

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
        assert result3 is True
        assert result4 is False
        assert result5 is False
        assert result6 is False
        assert result7 is False
        assert result8 is False
        assert result9 is True
        assert result10 is True
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
        - Connection Request: Should return False.
        - Connection Response: Should return False.
        - Connection Approve: Should return False.
        - Version Request: Should return True.
        - Version Response: Should return False.
        - Status Response: Should return False.
        - Sleep Response: Should return False.
        - Reboot Response: Should return False.
        - Disconnection Request: Should return True.
        - Disconnection Response: Should return True.
        - Data Package: Should return False.
        - Data Upload Package: Should return False.
        Assertions:
        - Each result is asserted against the expected outcome for the corresponding message type.
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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

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
        assert result4 is True
        assert result5 is False
        assert result6 is False
        assert result7 is False
        assert result8 is False
        assert result9 is True
        assert result10 is True
        assert result11 is False
        assert result12 is False

    def test_checks4(self):
        """
        Test the `check_for_valid_message_type_moment` function with various message types.
        This test verifies the behavior of the `check_for_valid_message_type_moment` function
        when provided with different types of messages. It ensures that the function correctly
        identifies valid and invalid message types based on the current state of the connection object.
        Test Steps:
        1. Set up the connection object with initial states for connection request, handshake, and version check.
        2. Build and test the following message types:
            - Connection Request
            - Connection Response
            - Connection Approve
            - Version Request
            - Version Response
            - Status Response
            - Sleep Response
            - Reboot Response
            - Disconnection Request
            - Disconnection Response
            - Data Message
            - Upload Data Message
        3. Assert the expected results for each message type.
        Expected Results:
        - Messages of types Connection Request, Connection Response, Connection Approve,
          Version Request, and Version Response should return `False`.
        - Messages of types Status Response, Sleep Response, Reboot Response,
          Disconnection Request, Disconnection Response, Data Message, and Upload Data Message
          should return `True`.
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

        result5 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result6 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result7 = check_for_valid_message_type_moment(self.connection_object, package)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        result8 = check_for_valid_message_type_moment(self.connection_object, package)

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

        result9 = check_for_valid_message_type_moment(self.connection_object, package)

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
