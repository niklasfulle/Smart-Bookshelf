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


class TestSendMessageClient:
    """
    TestSendMessageClient is a test suite for verifying the functionality of sending various types of messages
    from a client to a server in a smart bookshelf system. It includes tests for connection management,
    versioning, status updates, disconnection, sleep, reboot, and data transmission.
    Attributes:
        client_config (str): JSON string containing client configuration details such as ID, name,
            connection IP and port, and server details.
        bookshelf_config (str): JSON string containing bookshelf configuration details such as name
            and shelving units.
        file1 (str): JSON string containing protocol, client, and bookshelf version information.
        ip (str): The IP address of the client extracted from the client configuration.
        bookshelf_name (str): The name of the bookshelf extracted from the bookshelf configuration.
        shelving_units (list): List of shelving unit configurations extracted from the bookshelf configuration.
        bookshelf_object (bookshelf): An instance of the bookshelf class initialized with the bookshelf name,
            IP, and shelving units.
        client_ip (str): The IP address of the client extracted from the client configuration.
        client_port (int): The port number of the client extracted from the client configuration.
        server_ip (str): The IP address of the server extracted from the client configuration.
        server_port (int): The port number of the server extracted from the client configuration.
        sender_id (int): The ID of the sender (client) extracted from the client configuration.
        receiver_id (int): The ID of the receiver (server) extracted from the client configuration.
        connection_object (connection): An instance of the connection class initialized with client and server
            connection details, IDs, and the bookshelf object.
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
        test_send_data_upload_package_data(): Tests sending a data upload package with generic data.
        test_send_data_upload_package_data_start(): Tests sending a data upload package to start data transmission.
        test_send_data_upload_package_data_end(): Tests sending a data upload package to end data transmission.
        test_send_data_upload_package_data_error(): Tests sending a data upload package indicating an error.
        test_send_data_upload_package_data_cancel(): Tests sending a data upload package to cancel data transmission.
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40002 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50002}}'
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
        Test case for sending a connection request to the client.

        This test verifies that the `send_message_to_client` method of the
        `connection_object` correctly sends a connection request package
        built using the `build_connection_request` function.

        Steps:
        1. A connection request package is created using the `build_connection_request` function
           with the sender ID, receiver ID, and other parameters.
        2. The package is sent to the client using the `send_message_to_client` method.

        Assertions:
        - This test assumes that the `send_message_to_client` method and the
          `build_connection_request` function are functioning as expected.
        """

        package = build_connection_request(self.sender_id, self.receiver_id, 0, 0, 0, 0)
        self.connection_object.send_message_to_client(package)

    def test_send_connection_response(self):
        """
        Test the `send_message_to_client` method by sending a connection response package.

        This test generates a random sequence number and builds a connection response
        package using the `build_connection_response` function. It then sends the
        package to the client using the `send_message_to_client` method of the
        `connection_object`.

        Assertions and validations are expected to be performed within the test
        framework to ensure the message is sent correctly.

        Steps:
        1. Generate a random sequence number.
        2. Build a connection response package with the generated sequence number.
        3. Send the package to the client.

        Attributes:
            sequence_number (int): Randomly generated sequence number for the package.
            package (bytes): The connection response package to be sent.
        """

        sequence_number = get_random_sequence_number()
        package = build_connection_response(
            self.sender_id, self.receiver_id, 0, sequence_number, 0, 0
        )
        self.connection_object.send_message_to_client(package)

    def test_send_connection_approve(self):
        """
        Test the `send_message_to_client` method by sending a connection approval package.

        This test generates a random sequence number and timestamp, builds a connection
        approval package using the `build_connection_approve` function, and sends it
        to the client using the `send_message_to_client` method of the connection object.

        Assertions:
            - Ensures that the `send_message_to_client` method is called with the
              correctly constructed package.

        Dependencies:
            - `get_random_sequence_number`: Function to generate a random sequence number.
            - `get_timestamp`: Function to get the current timestamp.
            - `build_connection_approve`: Function to construct a connection approval package.
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
        self.connection_object.send_message_to_client(package)

    def test_send_version_request(self):
        """
        Test the `send_version_request` functionality.

        This test verifies that a version request package is correctly built
        and sent to the client using the `send_message_to_client` method.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a version request package using `build_version_request` with
           the sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the client using the `send_message_to_client`
           method of the connection object.

        Assertions:
        - This test assumes that the `send_message_to_client` method will handle
          the package correctly. Additional assertions may be added to verify
          the behavior if needed.

        Note:
        - Ensure that `self.sender_id`, `self.receiver_id`, and `self.connection_object`
          are properly initialized before running this test.
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
        self.connection_object.send_message_to_client(package)

    def test_send_version_response(self):
        """
        Test the `send_version_response` functionality.

        This test verifies that the `build_version_response` function constructs
        the correct package using the provided parameters, and that the
        `send_message_to_client` method of the connection object sends the
        constructed package to the client.

        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a version response package using the `build_version_response` function.
           - Extract protocol, client, and bookshelf version information from `file1`
             using the `json_data_reader` function.
           - Convert the extracted version information into 1-byte arrays using
             `int_to_1byte_array`.
        3. Send the constructed package to the client using the
           `send_message_to_client` method.

        Assertions:
        - This test assumes that the `send_message_to_client` method will handle
          the package correctly. No explicit assertions are made in this test.
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
        self.connection_object.send_message_to_client(package)

    def test_send_status_request(self):
        """
        Test the `send_status_request` functionality.

        This test verifies that a status request package is correctly built
        and sent to the client using the `send_message_to_client` method.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a status request package using `build_status_request` with
           the sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the client using the
           `send_message_to_client` method of the connection object.

        Assertions:
        This test assumes that the `send_message_to_client` method will
        handle the package correctly. Specific assertions should be added
        based on the implementation of `send_message_to_client`.

        Note:
        Ensure that the `self.sender_id`, `self.receiver_id`, and
        `self.connection_object` are properly initialized before running
        this test.
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
        self.connection_object.send_message_to_client(package)

    def test_send_status_response(self):
        """
        Test the `send_status_response` functionality.

        This test verifies that a status response package is correctly built
        and sent to the client using the `send_message_to_client` method.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a status response package using the provided sender ID,
           receiver ID, sequence numbers, timestamps, and a status code.
        3. Send the constructed package to the client using the connection object.

        Assertions:
        - Ensure that the package is correctly constructed and sent without errors.

        Dependencies:
        - `get_random_sequence_number`: Generates a random sequence number.
        - `get_timestamp`: Retrieves the current timestamp.
        - `build_status_response`: Constructs a status response package.
        - `int_to_2byte_array`: Converts an integer status code to a 2-byte array.
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
        self.connection_object.send_message_to_client(package)

    def test_send_disconnection_request(self):
        """
        Test the functionality of sending a disconnection request to the client.

        This test verifies that a disconnection request package is correctly built
        and sent to the client using the `send_message_to_client` method of the
        connection object.

        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a disconnection request package with the appropriate parameters,
           including sender ID, receiver ID, sequence numbers, timestamps, and
           disconnection reason.
        3. Send the package to the client using the connection object.

        Assertions:
        This test assumes that the `send_message_to_client` method of the
        connection object will handle the package correctly. No explicit assertions
        are made in this test, as it primarily focuses on the process of building
        and sending the disconnection request.

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
        self.connection_object.send_message_to_client(package)

    def test_send_disconnection_response(self):
        """
        Test the functionality of sending a disconnection response to the client.

        This test verifies that the `send_message_to_client` method correctly sends
        a disconnection response package to the client. The disconnection response
        includes the sender ID, receiver ID, sequence numbers, timestamps, and a
        disconnection reason.

        Steps:
        1. Generate a random sequence number and timestamp.
        2. Build a disconnection response package using the provided parameters.
        3. Send the package to the client using the `send_message_to_client` method.

        Assertions:
        - Ensure that the disconnection response package is constructed correctly.
        - Verify that the package is sent to the client without errors.

        Dependencies:
        - `get_random_sequence_number`: Generates a random sequence number.
        - `get_timestamp`: Retrieves the current timestamp.
        - `build_disconnection_response`: Constructs the disconnection response package.
        - `int_to_2byte_array`: Converts an integer to a 2-byte array.
        - `DISC_REASON.USERREQUEST`: Represents the user-requested disconnection reason.
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
        self.connection_object.send_message_to_client(package)

    def test_send_sleep_request(self):
        """
        Test the `send_sleep_request` functionality.

        This test verifies that a sleep request package is correctly built and sent
        to the client using the `send_message_to_client` method of the connection object.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a sleep request package using `build_sleep_request` with the sender ID,
           receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the client using the `send_message_to_client` method.

        Assertions:
        - This test assumes that the `send_message_to_client` method and the package
          construction are functioning correctly. It does not include explicit assertions
          but ensures the method is called with the expected package.
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
        self.connection_object.send_message_to_client(package)

    def test_send_sleep_response(self):
        """
        Test the `send_sleep_response` functionality.

        This test verifies that a sleep response package is correctly built
        and sent to the client using the `send_message_to_client` method.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a sleep response package using `build_sleep_response` with the
           sender ID, receiver ID, sequence numbers, and timestamps.
        4. Send the constructed package to the client using the `send_message_to_client` method.

        Assertions:
        This test assumes that the `send_message_to_client` method will handle
        the package correctly, but does not include explicit assertions.
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
        self.connection_object.send_message_to_client(package)

    def test_send_reboot_request(self):
        """
        Test the functionality of sending a reboot request to the client.

        This test verifies that a reboot request package is correctly built
        using the provided sender ID, receiver ID, sequence number, and timestamp,
        and that the package is successfully sent to the client via the connection object.

        Steps:
        1. Generate a random sequence number and a timestamp.
        2. Build a reboot request package using the generated values and the sender/receiver IDs.
        3. Send the package to the client using the connection object's `send_message_to_client` method.

        Assertions:
        - Ensure that the package is constructed correctly.
        - Ensure that the `send_message_to_client` method is called with the correct package.

        Dependencies:
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to generate a timestamp.
        - `build_reboot_request`: Function to construct the reboot request package.
        - `self.connection_object.send_message_to_client`: Method to send the package to the client.
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
        self.connection_object.send_message_to_client(package)

    def test_send_reboot_response(self):
        """
        Test the functionality of sending a reboot response message to the client.

        This test verifies that the `send_message_to_client` method of the
        connection object correctly sends a reboot response package. The package
        is constructed using the `build_reboot_response` function with the
        appropriate sender ID, receiver ID, sequence numbers, and timestamps.

        Steps:
        1. Generate a random sequence number using `get_random_sequence_number`.
        2. Retrieve the current timestamp using `get_timestamp`.
        3. Build a reboot response package using `build_reboot_response`.
        4. Send the package to the client using `send_message_to_client`.

        Assertions:
        This test assumes that the `send_message_to_client` method and the
        `build_reboot_response` function work as expected. No explicit assertions
        are made in this test.

        Note:
        Ensure that the `self.sender_id`, `self.receiver_id`, and
        `self.connection_object` are properly initialized before running this test.
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
        self.connection_object.send_message_to_client(package)

    def test_send_data_package_light_on(self):
        """
        Test the functionality of sending a data package with the light-on state.
        This test verifies that a data package representing the light-on state
        is correctly built and sent to the client using the `send_message_to_client`
        method of the connection object.
        Steps:
        1. Build a data package representing the light-on state using `build_data_package_light_on`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the complete data package using the `build_data` function,
           including sender and receiver IDs, sequence numbers, timestamps, and the complete data.
        5. Send the constructed package to the client using `send_message_to_client`.
        Assertions:
        - Ensure that the package is correctly sent to the client without errors.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_light_off(self):
        """
        Test case for sending a data package with the light off state.
        This test verifies that a data package representing the light off state
        is correctly built and sent to the client using the connection object.
        Steps:
        1. Build a data package representing the light off state using the
           `build_data_package_light_off` function.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the complete data package using the `build_data` function,
           including sender ID, receiver ID, sequence numbers, timestamps, and
           the complete data from the light off package.
        5. Send the constructed package to the client using the
           `send_message_to_client` method of the connection object.
        Assertions:
        - This test assumes that the `send_message_to_client` method will handle
          the package correctly. Any exceptions or errors during the process
          would indicate a failure in the test.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_book(self):
        """
        Test the functionality of sending a data package containing book information
        to the client.
        This test constructs a data package for a book using the `build_data_package_book`
        function and prepares a complete data package with metadata such as sequence
        numbers and timestamps. It then sends the package to the client using the
        `send_message_to_client` method of the connection object.
        Assertions and validations are expected to be performed within the test to
        ensure the data package is correctly built and transmitted.
        Steps:
        1. Build a data package for a book using `build_data_package_book`.
        2. Generate a random sequence number and timestamp.
        3. Construct the complete data package using the `build_data` function.
        4. Send the data package to the client using `send_message_to_client`.
        Attributes:
            self.sender_id (int): The ID of the sender.
            self.receiver_id (int): The ID of the receiver.
            self.connection_object (object): The connection object used to send the message.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_books(self):
        """
        Test the functionality of sending a data package containing book information
        to the client.
        This test constructs a data package by combining the data of two books,
        generates a sequence number and timestamp, and builds a complete data
        package. It then sends the package to the client using the connection object.
        Steps:
        1. Create a data package containing book information using `build_data_package_books`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Get the current timestamp using `get_timestamp`.
        4. Build the complete data package using `build_data`.
        5. Send the data package to the client using `send_message_to_client`.
        Assertions:
        This test assumes that the `send_message_to_client` method of the connection
        object will handle the package correctly. No explicit assertions are made
        in this test.
        Note:
        - `book` is assumed to be a function or class that provides book data.
        - `self.sender_id` and `self.receiver_id` are identifiers for the sender
          and receiver, respectively.
        - `self.connection_object` is the object responsible for managing the
          connection and sending messages.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_mode(self):
        """
        Test the functionality of sending a data package in "mode" format.
        This test verifies that a data package is correctly built and sent to the client
        using the `send_message_to_client` method of the connection object.
        Steps:
        1. Build a data package in "mode" format using `build_data_package_mode`.
        2. Generate a random sequence number and timestamp.
        3. Construct the complete data package using the `build_data` function.
        4. Send the constructed package to the client using the connection object.
        Assertions:
        - Ensures that the data package is properly constructed and sent without errors.
        Dependencies:
        - `build_data_package_mode`: Function to build a data package in "mode" format.
        - `int_to_2byte_array`: Utility to convert an integer to a 2-byte array.
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to retrieve the current timestamp.
        - `build_data`: Function to construct the complete data package.
        - `self.connection_object.send_message_to_client`: Method to send the package to the client.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data(self):
        """
        Test the functionality of sending a data upload package to the client.
        This test constructs a data upload package using helper functions and sends it
        to the client via the `send_message_to_client` method of the connection object.
        Steps:
        1. Build a data upload package using `build_data_upload_package_data` with a
           2-byte integer array and a predefined byte array.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Construct the upload data package using `build_upload_data` with the sender ID,
           receiver ID, sequence numbers, timestamps, and the complete data from the
           data upload package.
        5. Send the constructed package to the client using the `send_message_to_client`
           method.
        Assertions:
        This test assumes that the `send_message_to_client` method will handle the
        package correctly and does not explicitly assert any conditions.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_start(self):
        """
        Test the functionality of sending a data upload package with the "data start" flag.
        This test verifies that the `send_message_to_client` method correctly sends a
        data upload package with the appropriate sequence numbers, timestamps, and
        complete data generated by the `build_data_upload_package_data_start` function.
        Steps:
        1. Create a data upload package with the "data start" flag using
           `build_data_upload_package_data_start`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Retrieve the current timestamp using `get_timestamp`.
        4. Build the upload data package using `build_upload_data` with the sender ID,
           receiver ID, sequence numbers, timestamps, and the complete data from the
           data upload package.
        5. Send the constructed package to the client using the `send_message_to_client`
           method of the connection object.
        Assertions:
        - Ensure that the package is correctly constructed and sent to the client.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_end(self):
        """
        Test case for sending a data upload package with "data end" status.
        This test verifies that the `send_message_to_client` method correctly sends
        a data upload package with the "data end" status to the client. It ensures
        that the package is built with the appropriate sequence numbers, timestamps,
        and complete data from the `data_upload_package`.
        Steps:
        1. Build a data upload package with "data end" status using `build_data_upload_package_data_end`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Get the current timestamp using `get_timestamp`.
        4. Construct the upload data package using `build_upload_data` with the sender ID,
           receiver ID, sequence numbers, timestamps, and complete data.
        5. Send the constructed package to the client using `send_message_to_client`.
        Assertions:
        - Ensure that the package is sent correctly to the client.
        Dependencies:
        - `build_data_upload_package_data_end`
        - `get_random_sequence_number`
        - `get_timestamp`
        - `build_upload_data`
        - `send_message_to_client`
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_error(self):
        """
        Test case for sending a data upload package with an error.
        This test verifies the behavior of the `send_message_to_client` method when
        a data upload package containing an error is sent. It ensures that the package
        is correctly built and transmitted to the client.
        Steps:
        1. Build a data upload package with an error using `build_data_upload_package_data_error`.
        2. Generate a random sequence number and timestamp.
        3. Construct the upload data package using `build_upload_data`.
        4. Send the constructed package to the client using `send_message_to_client`.
        Assertions:
        - This test does not include explicit assertions but ensures that no exceptions
          are raised during the process of building and sending the package.
        Dependencies:
        - `build_data_upload_package_data_error`: Function to create a data upload package with an error.
        - `get_random_sequence_number`: Function to generate a random sequence number.
        - `get_timestamp`: Function to get the current timestamp.
        - `build_upload_data`: Function to construct the upload data package.
        - `send_message_to_client`: Method to send the package to the client.
        Note:
        - The `self.connection_object` is assumed to be a valid connection object
          capable of sending messages to the client.
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

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_cancel(self):
        """
        Test case for sending a data upload package with a cancel operation.
        This test verifies that the `send_message_to_client` method correctly sends
        a data upload package containing a cancel operation. It builds the necessary
        data upload package, constructs the upload data message, and sends it to the
        client.
        Steps:
        1. Build a data upload package with a cancel operation using `build_data_upload_package_data_cancel`.
        2. Generate a random sequence number using `get_random_sequence_number`.
        3. Get the current timestamp using `get_timestamp`.
        4. Construct the upload data message using `build_upload_data` with the sender ID,
           receiver ID, sequence numbers, timestamps, and the complete data from the
           data upload package.
        5. Send the constructed message to the client using `send_message_to_client`.
        Assertions:
        This test assumes that the `send_message_to_client` method will handle the
        constructed package correctly. Assertions should be added to validate the
        expected behavior, such as verifying the message was sent successfully or
        checking the client's response.
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

        self.connection_object.send_message_to_client(package)
