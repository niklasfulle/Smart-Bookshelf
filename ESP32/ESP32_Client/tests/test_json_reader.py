"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys
import json
import pytest

sys.path.append("../")
from utils.json_data_reader import json_data_reader


class TestJsonReader:
    """
    TestJsonReader is a test suite for validating the functionality of the `json_data_reader` function.
    Attributes:
        file1 (str): An empty string representing invalid JSON data.
        file2 (str): A string containing an incomplete JSON object.
        file3 (str): A valid JSON string representing a nested data structure.
    Methods:
        test_json_data_reader1():
            Tests that `json_data_reader` raises a `json.decoder.JSONDecodeError` when provided with an empty string.
        test_json_data_reader2():
            Tests that `json_data_reader` raises a `json.decoder.JSONDecodeError` when provided with an incomplete JSON string.
        test_json_data_reader3():
            Tests that `json_data_reader` correctly parses a valid JSON string and returns the expected dictionary.
        test_json_data_reader4():
            Tests that `json_data_reader` retrieves a specific value ("name") from the JSON data when provided with a key path.
        test_json_data_reader5():
            Tests that `json_data_reader` retrieves a nested value ("connection -> ip") from the JSON data when provided with a key path.
    """

    file1: str = ""
    file2: str = "{"
    file3: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40000 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50000}}'

    def test_json_data_reader1(self):
        """
        Test case for the `json_data_reader` function to ensure it raises a
        `json.decoder.JSONDecodeError` when provided with invalid JSON data.

        This test verifies that the function correctly handles and raises an
        exception when attempting to decode malformed or invalid JSON content.

        Raises:
            json.decoder.JSONDecodeError: If the JSON data is invalid.
        """

        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.file1, [], 2)

    def test_json_data_reader2(self):
        """
        Test case for the `json_data_reader` function to ensure it raises a
        `json.decoder.JSONDecodeError` when provided with invalid JSON data.

        This test verifies that the function correctly handles and raises an
        exception when attempting to decode improperly formatted JSON.

        Expected Behavior:
        - The `json_data_reader` function should raise a `json.decoder.JSONDecodeError`.

        Test Parameters:
        - `self.file2`: A file path or file-like object containing invalid JSON data.
        - `[]`: An empty list passed as an argument (purpose depends on the function implementation).
        - `2`: An integer argument (purpose depends on the function implementation).

        Raises:
        - `json.decoder.JSONDecodeError`: If the JSON data in `self.file2` is invalid.
        """

        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.file2, [], 2)

    def test_json_data_reader3(self):
        """
        Test case for the `json_data_reader` function.

        Verifies that the function correctly reads and parses JSON data from the specified file
        and returns the expected dictionary structure.

        Test Scenario:
        - Reads JSON data from `self.file3` with an empty list and a depth value of 2.
        - Asserts that the returned data matches the expected dictionary.

        Expected Output:
        {
        """

        data = json_data_reader(self.file3, [], 2)
        assert data == {
            "id": 10,
            "name": "Client_0",
            "connection": {"ip": "127.0.0.1", "port": 40000},
            "server": {"id": 20, "name": "Server", "ip": "127.0.0.1", "port": 50000},
        }

    def test_json_data_reader4(self):
        """
        Test case for the `json_data_reader` function.

        Verifies that the function correctly reads and retrieves the value
        associated with the specified key from the JSON file.

        Test Scenario:
        - Reads data from `self.file3` using the key "name" and index 2.
        - Asserts that the returned value matches the expected result "Client_0".

        Expected Outcome:
        - The function should return "Client_0" for the given input.
        """

        data = json_data_reader(self.file3, ["name"], 2)
        assert data == "Client_0"

    def test_json_data_reader5(self):
        """
        Test case for the `json_data_reader` function.

        Verifies that the function correctly retrieves the value associated with
        the specified keys from a JSON file. In this test, it checks if the IP
        address "127.0.0.1" is correctly extracted from the JSON structure
        using the keys ["connection", "ip"].

        Expected Behavior:
        - The function should return the string "127.0.0.1" when provided with
          the specified file and keys.

        Test Parameters:
        - self.file3: Path to the JSON file used for testing.
        - ["connection", "ip"]: List of keys to navigate the JSON structure.
        - 2: The expected depth of the JSON structure.

        Asserts:
        - The returned value matches the expected IP address "127.0.0.1".
        """

        data = json_data_reader(self.file3, ["connection", "ip"], 2)
        assert data == "127.0.0.1"
