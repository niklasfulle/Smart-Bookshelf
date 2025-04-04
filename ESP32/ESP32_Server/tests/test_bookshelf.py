"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from utils.json_data_reader import json_data_reader
from hardware.bookshelf import bookshelf


class Testbookshelf:
    """
    Testbookshelf is a test class designed to validate the functionality of the `bookshelf` class.
    Attributes:
        client_config (str): A JSON string representing the client configuration, including client ID, name,
            connection details (IP and port), and server information.
        bookshelf_config (str): A JSON string representing the bookshelf configuration, including the name
            of the bookshelf and a list of shelving units with their order and length.
    Methods:
        test_bookshelf1():
            Tests the initialization of a `bookshelf` object using the provided configurations.
            Validates the following:
            - The name of the bookshelf matches the expected value.
            - The IP address of the bookshelf matches the expected value.
            - The number of LED stripes matches the expected count.
            - The order and length of the first and last LED stripes are as expected.
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40000 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50000}}'
    bookshelf_config: str = '{"name": "bookshelf_Name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'

    def test_bookshelf1(self):
        """
        Test case for the `bookshelf` class initialization.
        This test verifies the following:
        - The `bookshelf` object is correctly initialized with the provided name, IP address, and shelving units.
        - The `name` attribute of the `bookshelf` object matches the expected value.
        - The `ip` attribute of the `bookshelf` object matches the expected value.
        - The number of LED stripes in the `bookshelf` object matches the expected count.
        - The order and length of the first and last LED stripes are correctly set.
        Assertions:
        - `bookshelf_object.name` is "bookshelf_Name1".
        - `bookshelf_object.ip` is "127.0.0.1".
        - The length of `bookshelf_object.ledstripes` is 8.
        - The `order` and `length` of the first LED stripe are 1 and 50, respectively.
        - The `order` and `length` of the last LED stripe are 8 and 50, respectively.
        """

        ip = json_data_reader(self.client_config, ["connection", "ip"], 2)
        bookshelf_name = json_data_reader(self.bookshelf_config, ["name"], 2)
        shelving_units = json_data_reader(self.bookshelf_config, ["shelving_units"], 2)

        bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

        assert bookshelf_object.name == "bookshelf_Name1"
        assert bookshelf_object.ip == "127.0.0.1"
        assert len(bookshelf_object.ledstripes) == 8
        assert bookshelf_object.ledstripes[0].order == 1
        assert bookshelf_object.ledstripes[0].length == 50
        assert bookshelf_object.ledstripes[7].order == 8
        assert bookshelf_object.ledstripes[7].length == 50
