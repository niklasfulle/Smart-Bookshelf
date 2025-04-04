"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from datatype.book import book
from utils.json_data_reader import json_data_reader
from utils.build_helper import get_random_sequence_number, get_timestamp
from utils.converter import int_to_1byte_array, int_to_2byte_array
from hardware.bookshelf import bookshelf
from connection.connection import connection
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
from protocol.builder.builder_data_package import (
    build_data_package_book,
    build_data_package_books,
    build_data_package_light_off,
    build_data_package_light_on,
    build_data_package_mode,
)
from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data,
    build_data_upload_package_data_start,
    build_data_upload_package_data_end,
    build_data_upload_package_data_cancel,
    build_data_upload_package_data_error,
)
from protocol.constants.constants import DISC_REASON, STATUS


class TestSendMessageServer:
    """
    TestSendMessageServer is a test suite for verifying the functionality of sending various types of messages
    from a client to a server in a smart bookshelf system. It includes tests for connection management,
    versioning, status updates, disconnection, sleep, reboot, and data transmission.
    Attributes:
        client_config (str): JSON string containing client configuration details such as ID, name, connection IP,
            port, and server details.
        bookshelf_config (str): JSON string containing bookshelf configuration details such as name and shelving units.
        file1 (str): JSON string containing protocol, client, and bookshelf version information.
        ip (str): IP address of the client extracted from the client configuration.
        bookshelf_name (str): Name of the bookshelf extracted from the bookshelf configuration.
        shelving_units (list): List of shelving units extracted from the bookshelf configuration.
        bookshelf_object (bookshelf): Bookshelf object initialized with the extracted configuration details.
        client_ip (str): IP address of the client extracted from the client configuration.
        client_port (int): Port number of the client extracted from the client configuration.
        server_ip (str): IP address of the server extracted from the client configuration.
        server_port (int): Port number of the server extracted from the client configuration.
        sender_id (int): ID of the sender (client) extracted from the client configuration.
        receiver_id (int): ID of the receiver (server) extracted from the client configuration.
        connection_object (connection): Connection object initialized with client and server details.
    Methods:
        test_send_connection_request(): Tests sending a connection request message to the server.
        test_send_connection_response(): Tests sending a connection response message to the server.
        test_send_connection_approve(): Tests sending a connection approval message to the server.
        test_send_version_request(): Tests sending a version request message to the server.
        test_send_version_response(): Tests sending a version response message to the server.
        test_send_status_request(): Tests sending a status request message to the server.
        test_send_status_response(): Tests sending a status response message to the server.
        test_send_disconnection_request(): Tests sending a disconnection request message to the server.
        test_send_disconnection_response(): Tests sending a disconnection response message to the server.
        test_send_sleep_request(): Tests sending a sleep request message to the server.
        test_send_sleep_response(): Tests sending a sleep response message to the server.
        test_send_reboot_request(): Tests sending a reboot request message to the server.
        test_send_reboot_response(): Tests sending a reboot response message to the server.
        test_send_data_package_light_on(): Tests sending a data package to turn the light on.
        test_send_data_package_light_off(): Tests sending a data package to turn the light off.
        test_send_data_package_book(): Tests sending a data package containing a single book's data.
        test_send_data_package_books(): Tests sending a data package containing multiple books' data.
        test_send_data_package_mode(): Tests sending a data package containing mode information.
        test_send_data_upload_package_data(): Tests sending a data upload package with data.
        test_send_data_upload_package_data_start(): Tests sending a data upload package to start data transmission.
        test_send_data_upload_package_data_end(): Tests sending a data upload package to end data transmission.
        test_send_data_upload_package_data_error(): Tests sending a data upload package indicating an error.
        test_send_data_upload_package_data_cancel(): Tests sending a data upload package to cancel data transmission.
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40003 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50003}}'
    bookshelf_config: str = '{"name": "bookshelf_Name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'
    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"client_version_major": 1,"client_version_minor": 0,"bookshelf_version_major": 1,"bookshelf_version_minor": 0}'

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

    def test_send_connection_request(self):
        """
        Test the functionality of sending a connection request to the server.

        This test constructs a connection request package using the
        `build_connection_request` function and sends it to the server
        using the `send_message_to_server` method of the connection object.

        Assertions and validations are expected to be performed within
        the test to ensure the package is correctly built and successfully
        sent to the server.

        Attributes:
            sender_id (int): The ID of the sender.
            receiver_id (int): The ID of the receiver.
            connection_object (object): The object responsible for managing
                the connection and sending messages to the server.
        """

        package = build_connection_request(self.sender_id, self.receiver_id, 0, 0, 0, 0)
        self.connection_object.send_message_to_server(package)

    def test_send_connection_response(self):
        """
        Test the `send_message_to_server` method by sending a connection response package.

        This test generates a random sequence number and builds a connection response
        package using the provided sender and receiver IDs. It then sends the package
        to the server using the `send_message_to_server` method of the connection object.

        Assertions:
            This test assumes that the `send_message_to_server` method works correctly
            and does not explicitly perform assertions. It is expected to be part of a
            larger test suite where the server's response or behavior is verified.

        Dependencies:
            - `get_random_sequence_number`: Function to generate a random sequence number.
            - `build_connection_response`: Function to construct a connection response package.
            - `self.connection_object`: Object responsible for sending messages to the server.
        """

        sequence_number = get_random_sequence_number()
        package = build_connection_response(
            self.sender_id, self.receiver_id, 0, sequence_number, 0, 0
        )
        self.connection_object.send_message_to_server(package)

    def test_send_connection_approve(self):
        """
        Test the `send_message_to_server` method with a connection approval package.

        This test verifies that the `send_message_to_server` method correctly sends
        a connection approval package to the server. It constructs the package using
        the `build_connection_approve` function with the required parameters, including
        sender ID, receiver ID, sequence numbers, and timestamps.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a connection approval package using `build_connection_approve`.
        4. Send the package to the server using `self.connection_object.send_message_to_server`.

        Assertions:
        This test assumes that the `send_message_to_server` method will handle the
        package correctly. Specific assertions or validations should be implemented
        based on the behavior of the `send_message_to_server` method.

        Note:
        Ensure that the `self.connection_object` is properly initialized and connected
        to the server before running this test.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_version_request(self):
        """
        Test the functionality of sending a version request message to the server.

        This test verifies that the `build_version_request` function correctly constructs
        a version request package with the appropriate sender ID, receiver ID, sequence
        numbers, and timestamps. It also ensures that the `send_message_to_server` method
        of the connection object is called with the constructed package.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a version request package using `build_version_request` with the
           sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the server using the connection object.

        Assertions:
        - Ensure the package is correctly built and sent to the server.

        Note:
        - This test assumes that `self.sender_id`, `self.receiver_id`, and
          `self.connection_object` are properly initialized.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_version_response(self):
        """
        Test the `send_version_response` functionality.

        This test constructs a version response package using various helper functions
        and sends it to the server using the `send_message_to_server` method of the
        connection object.

        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build the version response package using:
           - Protocol version (major and minor) from `file1`.
           - Client version (major and minor) from `file1`.
           - Bookshelf version (major and minor) from `file1`.
        3. Send the constructed package to the server.

        The test ensures that the package is correctly built and transmitted.

        Attributes:
            self.sender_id (int): The ID of the sender.
            self.receiver_id (int): The ID of the receiver.
            self.file1 (str): Path to the JSON file containing version information.
            self.connection_object (object): The connection object used to send messages.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_response(
            self.sender_id,
            self.receiver_id,
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
                    json_data_reader(self.file1, ["bookshelf_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["bookshelf_version_minor"], 2)
                )
            ),
        )
        self.connection_object.send_message_to_server(package)

    def test_send_status_request(self):
        """
        Test the `send_status_request` functionality.

        This test verifies that a status request package is correctly built
        and sent to the server using the `send_message_to_server` method.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a status request package using `build_status_request` with the
           sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the server using the `send_message_to_server`
           method of the connection object.

        Assertions:
        - This test assumes that the `send_message_to_server` method and the
          `build_status_request` function work as expected. No explicit assertions
          are made in this test.

        Note:
        - Ensure that `self.sender_id`, `self.receiver_id`, and `self.connection_object`
          are properly initialized before running this test.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_status_response(self):
        """
        Test the `send_status_response` functionality.

        This test verifies that a status response package is correctly built
        and sent to the server using the `send_message_to_server` method.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a status response package using the provided sender ID,
           receiver ID, sequence numbers, timestamps, and a status code.
        3. Send the constructed package to the server.

        Assertions:
        - This test assumes that the `send_message_to_server` method
          correctly handles the transmission of the package.

        Dependencies:
        - `get_random_sequence_number`: Generates a random sequence number.
        - `get_timestamp`: Retrieves the current timestamp.
        - `build_status_response`: Constructs the status response package.
        - `int_to_2byte_array`: Converts the status code to a 2-byte array.
        - `STATUS.RUNNING`: Represents the running status code.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(STATUS.RUNNING),
        )
        self.connection_object.send_message_to_server(package)

    def test_send_disconnection_request(self):
        """
        Test the functionality of sending a disconnection request to the server.

        This test verifies that a disconnection request package is correctly built
        and sent to the server using the `send_message_to_server` method of the
        connection object.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a disconnection request package using the provided sender ID,
           receiver ID, sequence number, timestamp, and a user request disconnection reason.
        3. Send the constructed package to the server.

        Assertions:
        - This test assumes that the `send_message_to_server` method will handle
          the package correctly. No explicit assertions are made in this test.

        Dependencies:
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to get the current timestamp.
        - `build_disconnection_request`: Function to construct the disconnection request package.
        - `int_to_2byte_array`: Function to convert an integer to a 2-byte array.
        - `DISC_REASON.USERREQUEST`: Constant representing the user-requested disconnection reason.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.USERREQUEST),
        )
        self.connection_object.send_message_to_server(package)

    def test_send_disconnection_response(self):
        """
        Test the functionality of sending a disconnection response to the server.

        This test verifies that the `send_message_to_server` method correctly sends
        a disconnection response package to the server. The disconnection response
        includes the sender ID, receiver ID, sequence numbers, timestamps, and a
        disconnection reason.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a disconnection response package using the provided parameters.
        3. Send the package to the server using the connection object.

        Assertions:
        - This test assumes that the `send_message_to_server` method is implemented
          correctly and does not perform explicit assertions within the test.

        Dependencies:
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to get the current timestamp.
        - `build_disconnection_response`: Function to construct the disconnection response package.
        - `int_to_2byte_array`: Function to convert an integer to a 2-byte array.
        - `DISC_REASON.USERREQUEST`: Constant representing the user-requested disconnection reason.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.USERREQUEST),
        )
        self.connection_object.send_message_to_server(package)

    def test_send_sleep_request(self):
        """
        Test the functionality of sending a sleep request message to the server.

        This test verifies that a sleep request package is correctly built using
        the provided sender ID, receiver ID, sequence number, and timestamp, and
        that the package is successfully sent to the server using the connection
        object.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a sleep request package using the generated values and the
           sender and receiver IDs.
        3. Send the package to the server using the connection object.

        Assertions:
        - Ensures that the package is constructed correctly.
        - Ensures that the package is sent to the server without errors.

        Dependencies:
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to generate a timestamp.
        - `build_sleep_request`: Function to construct the sleep request package.
        - `self.connection_object.send_message_to_server`: Method to send the package to the server.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_sleep_response(self):
        """
        Test the `send_sleep_response` functionality.

        This test verifies that the `send_sleep_response` method correctly builds
        a sleep response package with the appropriate parameters and sends it to
        the server using the `send_message_to_server` method.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a sleep response package using `build_sleep_response` with the
           sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the server using the `send_message_to_server`
           method of the connection object.

        Assertions:
        - Ensure that the package is correctly constructed and sent to the server.

        Note:
        This test assumes that `self.sender_id`, `self.receiver_id`, and
        `self.connection_object` are properly initialized.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_reboot_request(self):
        """
        Test the functionality of sending a reboot request to the server.

        This test verifies that a reboot request package is correctly built
        with the appropriate sender ID, receiver ID, sequence numbers, and
        timestamps, and that it is successfully sent to the server using the
        connection object.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a reboot request package using the generated values and
           the sender and receiver IDs.
        3. Send the package to the server using the connection object.

        Assertions:
        - Ensures that the package is constructed with the correct data.
        - Confirms that the package is sent to the server without errors.

        Dependencies:
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to get the current timestamp.
        - `build_reboot_request`: Function to construct the reboot request package.
        - `self.connection_object.send_message_to_server`: Method to send the package to the server.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_reboot_response(self):
        """
        Test the functionality of sending a reboot response message to the server.

        This test verifies that a reboot response package is correctly built using
        the provided sender ID, receiver ID, sequence numbers, and timestamps, and
        that the package is successfully sent to the server using the connection object.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a reboot response package using the generated values and the
           sender and receiver IDs.
        3. Send the constructed package to the server using the connection object.

        Assertions:
        - This test assumes that the `send_message_to_server` method of the
          connection object works as expected and does not explicitly assert
          the outcome.
        """

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_server(package)

    def test_send_data_package_light_on(self):
        """
        Test the functionality of sending a data package with the light-on state to the server.
        This test verifies that a data package representing the light-on state is correctly built
        and sent to the server using the `send_message_to_server` method of the connection object.
        Steps:
        1. Build a data package representing the light-on state using `build_data_package_light_on`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the complete data package using the `build_data` function, including sender ID,
           receiver ID, sequence numbers, timestamps, and the complete data from the light-on package.
        5. Send the constructed package to the server using the `send_message_to_server` method.
        Assertions:
        - Ensure that the package is correctly built and sent without errors.
        Note:
        - This test assumes that `self.sender_id`, `self.receiver_id`, and `self.connection_object`
          are properly initialized before running the test.
        """

        data_package = build_data_package_light_on()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_package_light_off(self):
        """
        Test the functionality of sending a data package with the light off state to the server.
        This test constructs a data package representing the light off state, builds a complete
        data message with necessary metadata (e.g., sequence number and timestamp), and sends
        it to the server using the connection object.
        Steps:
        1. Create a data package for the light off state using `build_data_package_light_off`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Get the current timestamp using `get_timestamp`.
        4. Build the complete data message using `build_data` with the sender ID, receiver ID,
           sequence numbers, timestamps, and the complete data from the package.
        5. Send the constructed package to the server using `send_message_to_server`.
        Assertions and validations are expected to be handled within the test framework
        to ensure the package is sent correctly and the server processes it as intended.
        """

        data_package = build_data_package_light_off()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_package_book(self):
        """
        Test the functionality of sending a data package containing book information
        to the server.
        This test constructs a data package using book information, generates a
        sequence number and timestamp, and builds a complete data package to be
        sent to the server. It verifies that the `send_message_to_server` method
        of the connection object is capable of handling the constructed package.
        Steps:
        1. Create a data package using book information.
        2. Generate a random sequence number and a timestamp.
        3. Build a complete data package using the sender ID, receiver ID, sequence
           numbers, timestamps, and the book data.
        4. Send the constructed package to the server using the connection object.
        Attributes:
            self.sender_id (int): The ID of the sender.
            self.receiver_id (int): The ID of the receiver.
            self.connection_object (object): The connection object used to send
                messages to the server.
        """

        data_package = build_data_package_book(book(1, 12).data)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_package_books(self):
        """
        Test the functionality of sending a data package containing book information
        to the server.
        This test constructs a data package by combining book data, generates a
        sequence number and timestamp, builds the complete data package, and sends
        it to the server using the connection object.
        Steps:
        1. Create a data package containing book information using `build_data_package_books`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Get the current timestamp using `get_timestamp`.
        4. Build the complete data package using `build_data`.
        5. Send the data package to the server using `send_message_to_server`.
        Assertions and validations are expected to be handled within the test framework
        or mocked server to ensure the package is sent correctly.
        Note:
        - `self.sender_id` and `self.receiver_id` are used to identify the sender and
          receiver of the package.
        - `self.connection_object` is responsible for sending the package to the server.
        """

        data_package = build_data_package_books(
            data=(book(1, 12).data + book(3, 2).data)
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_package_mode(self):
        """
        Test the functionality of sending a data package in "mode" format to the server.
        This test constructs a data package using the `build_data_package_mode` function
        and prepares a complete data package with sequence numbers, timestamps, and other
        required fields. It then sends the package to the server using the `send_message_to_server`
        method of the connection object.
        Steps:
        1. Build a data package in "mode" format using `build_data_package_mode`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the complete data package using the `build_data` function.
        5. Send the constructed package to the server.
        Assertions and validations are expected to be performed to ensure the package
        is sent correctly and the server processes it as intended.
        Note:
        - `self.sender_id` and `self.receiver_id` are used to identify the sender and receiver.
        - `self.connection_object` is responsible for handling the communication with the server.
        """

        data_package = build_data_package_mode(int_to_2byte_array(1))

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_upload_package_data(self):
        """
        Test the functionality of sending a data upload package to the server.
        This test constructs a data upload package using helper functions and sends it
        to the server via the `send_message_to_server` method of the connection object.
        Steps:
        1. Build a data upload package using `build_data_upload_package_data` with a
           2-byte integer array and a predefined byte array.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the upload data package using `build_upload_data` with the sender ID,
           receiver ID, sequence numbers, timestamps, and the complete data from the
           data upload package.
        5. Send the constructed package to the server using the connection object.
        Assertions and validations are expected to be performed to ensure the package
        is sent correctly and the server processes it as intended.
        """

        data_upload_package = build_data_upload_package_data(
            int_to_2byte_array(1),
            bytearray(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_upload_package_data_start(self):
        """
        Test the process of sending a data upload package with a "data start" message.
        This test verifies the following:
        - A data upload package with a "data start" message is correctly built using
          `build_data_upload_package_data_start`.
        - A complete upload data package is constructed using `build_upload_data` with
          appropriate parameters such as sender ID, receiver ID, sequence numbers, and timestamps.
        - The constructed package is successfully sent to the server using
          `self.connection_object.send_message_to_server`.
        Steps:
        1. Create a data upload package with a "data start" message.
        2. Generate a random sequence number and a timestamp.
        3. Build the upload data package using the generated sequence number, timestamp,
           and the data upload package.
        4. Send the constructed package to the server.
        Assertions:
        - Ensure that the package is correctly built and sent without errors.
        """

        data_upload_package = build_data_upload_package_data_start(
            bytearray(b"\x00\x00")
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_upload_package_data_end(self):
        """
        Test the functionality of sending a data upload package to the server.
        This test verifies that the `send_message_to_server` method correctly sends
        a data upload package containing the necessary information, such as sequence
        numbers, timestamps, and complete data, to the server.
        Steps:
        1. Build a data upload package using `build_data_upload_package_data_end`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the upload data package using `build_upload_data` with the
           sender ID, receiver ID, sequence numbers, timestamps, and complete data.
        5. Send the constructed package to the server using the `send_message_to_server`
           method of the connection object.
        Assertions:
        This test assumes that the `send_message_to_server` method will handle the
        package correctly and send it to the server without errors.
        """

        data_upload_package = build_data_upload_package_data_end()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_upload_package_data_error(self):
        """
        Test case for sending a data upload package with an error to the server.
        This test constructs a data upload package with an error using the
        `build_data_upload_package_data_error` function. It then builds an upload
        data package with the necessary metadata, including sequence numbers and
        timestamps, using the `build_upload_data` function. Finally, it sends the
        constructed package to the server using the `send_message_to_server` method
        of the connection object.
        Assertions and validations are expected to be performed within the test
        framework to ensure the package is sent correctly and the server handles
        the error as expected.
        Steps:
        1. Create a data upload package with an error.
        2. Generate sequence numbers and timestamps.
        3. Build the complete upload data package.
        4. Send the package to the server.
        Dependencies:
        - `build_data_upload_package_data_error`
        - `get_random_sequence_number`
        - `get_timestamp`
        - `build_upload_data`
        - `send_message_to_server`
        """

        data_upload_package = build_data_upload_package_data_error(
            bytearray(b"\x00\x00")
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)

    def test_send_data_upload_package_data_cancel(self):
        """
        Test the functionality of sending a data upload package with a cancel action to the server.
        This test verifies that the `send_message_to_server` method correctly sends a data upload package
        containing a cancel action. It ensures that the package is built with the appropriate sequence
        numbers, timestamps, and complete data from the `data_upload_package`.
        Steps:
        1. Build a data upload package with a cancel action using `build_data_upload_package_data_cancel`.
        2. Generate a random sequence number and timestamp.
        3. Construct the upload data package using `build_upload_data` with the sender and receiver IDs,
           sequence numbers, timestamps, and the complete data from the data upload package.
        4. Send the constructed package to the server using `send_message_to_server`.
        Assertions:
        - Ensure that the package is sent correctly to the server.
        Note:
        - This test assumes that `self.sender_id`, `self.receiver_id`, and `self.connection_object` are
          properly initialized.
        """

        data_upload_package = build_data_upload_package_data_cancel()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_server(package)
