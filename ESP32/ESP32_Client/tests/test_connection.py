"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys
import socket

sys.path.append("../")
from utils.json_data_reader import json_data_reader
from hardware.bookshelf import bookshelf
from connection.connection import connection


class TestConnection:
    """
    TestConnection class contains unit tests for verifying the functionality of the connection
    and bookshelf objects used in the Smart Bookshelf ESP32 client application.
    Attributes:
        client_config (str): JSON string containing client configuration details such as
            client ID, name, connection IP and port, and server details.
        bookshelf_config (str): JSON string containing bookshelf configuration details such as
            bookshelf name and shelving unit specifications.
    Methods:
        test_connection1():
            Tests the creation and initialization of a connection object, ensuring that
            all attributes are correctly set, including socket creation, client and server
            details, sender and receiver IDs, and handshake/task flags.
        test_connection2():
            Tests the creation of a connection object and verifies the attributes of the
            associated bookshelf object, including its name, IP, and the details of its
            shelving units (order and length).
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40001 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50001}}'
    bookshelf_config: str = '{"name": "bookshelf_name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'

    def test_connection1(self):
        """
        Test the initialization and properties of the `connection` object.
        This test verifies the following:
        - Proper creation of a `bookshelf` object using configuration data.
        - Proper creation of a `connection` object using configuration data.
        - The `connection` object has a valid socket instance.
        - The `client` and `server` attributes of the `connection` object are correctly set.
        - The `receiver_id` and `sender_id` attributes are correctly set as both integers and bytearrays.
        - The `handshake` and `task` attributes are initialized to `False`.
        Assertions:
        - `connection_object.sock` is an instance of `socket.socket`.
        - `connection_object.client` matches the expected client address and port.
        - `connection_object.server` matches the expected server address and port.
        - `connection_object.receiver_id_int` matches the expected integer value.
        - `connection_object.receiver_id` matches the expected bytearray value.
        - `connection_object.sender_id_int` matches the expected integer value.
        - `connection_object.sender_id` matches the expected bytearray value.
        - `connection_object.handshake` is `False`.
        - `connection_object.task` is `False`.
        """

        ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        bookshelf_name = json_data_reader(self.bookshelf_config, ["name"], 2)
        shelving_units = json_data_reader(self.bookshelf_config, ["shelving_units"], 2)

        bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

        client_ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        client_port = json_data_reader(self.client_config, ["connection", "port"], 2)
        server_ip = json_data_reader(self.client_config, ["server", "ip"], 2)
        server_port = json_data_reader(self.client_config, ["server", "port"], 2)
        sender_id = json_data_reader(self.client_config, ["id"], 2)
        receiver_id = json_data_reader(self.client_config, ["server", "id"], 2)

        connection_object: connection = connection(
            (client_ip, client_port),
            (server_ip, server_port),
            receiver_id,
            sender_id,
            bookshelf_object,
        )

        assert isinstance(connection_object.sock, socket.socket)
        assert connection_object.client == ("127.0.0.1", 40001)
        assert connection_object.server == ("127.0.0.1", 50001)
        assert connection_object.receiver_id_int == 20
        assert connection_object.receiver_id == bytearray(b"\x14\x00\x00\x00")
        assert connection_object.sender_id_int == 10
        assert connection_object.sender_id == bytearray(b"\n\x00\x00\x00")
        assert connection_object.handshake is False
        assert connection_object.task is False

        connection_object = None

    def test_connection2(self):
        """
        Test the creation and initialization of a `connection` object and its associated `bookshelf` object.
        This test verifies:
        - The `bookshelf` object is correctly initialized with the expected name, IP address, and shelving unit details.
        - The `connection` object is correctly initialized with the client and server connection details, as well as the associated `bookshelf` object.
        - The attributes of the `bookshelf` object, including the number of LED stripes and their properties (order and length), are as expected.
        Assertions:
        - The `bookshelf` object's name matches the expected value.
        - The `bookshelf` object's IP address matches the expected value.
        - The number of LED stripes in the `bookshelf` object matches the expected count.
        - The order and length of the first and last LED stripes in the `bookshelf` object match the expected values.
        """

        ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        bookshelf_name = json_data_reader(self.bookshelf_config, ["name"], 2)
        shelving_units = json_data_reader(self.bookshelf_config, ["shelving_units"], 2)

        bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

        client_ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        client_port = json_data_reader(self.client_config, ["connection", "port"], 2)
        server_ip = json_data_reader(self.client_config, ["server", "ip"], 2)
        server_port = json_data_reader(self.client_config, ["server", "port"], 2)
        sender_id = json_data_reader(self.client_config, ["id"], 2)
        receiver_id = json_data_reader(self.client_config, ["server", "id"], 2)

        connection_object: connection = connection(
            (client_ip, client_port),
            (server_ip, server_port),
            receiver_id,
            sender_id,
            bookshelf_object,
        )

        assert connection_object.bookshelf_object.name == "bookshelf_name1"
        assert connection_object.bookshelf_object.ip == "127.0.0.1"
        assert len(connection_object.bookshelf_object.ledstripes) == 8
        assert connection_object.bookshelf_object.ledstripes[0].order == 1
        assert connection_object.bookshelf_object.ledstripes[0].length == 50
        assert connection_object.bookshelf_object.ledstripes[7].order == 8
        assert connection_object.bookshelf_object.ledstripes[7].length == 50

        connection_object = None
