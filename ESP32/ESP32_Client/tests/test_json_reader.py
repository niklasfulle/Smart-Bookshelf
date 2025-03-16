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
    -
    """

    file1: str = ""
    file2: str = "{"
    file3: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40000 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50000}}'

    def test_json_data_reader1(self):
        """Tests whether the checksum is correct"""
        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.file1, [], 2)

    def test_json_data_reader2(self):
        """Tests whether the checksum is correct"""
        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.file2, [], 2)

    def test_json_data_reader3(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.file3, [], 2)
        assert data == {
            "id": 10,
            "name": "Client_0",
            "connection": {"ip": "127.0.0.1", "port": 40000},
            "server": {"id": 20, "name": "Server", "ip": "127.0.0.1", "port": 50000},
        }

    def test_json_data_reader4(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.file3, ["name"], 2)
        assert data == "Client_0"

    def test_json_data_reader5(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.file3, ["connection", "ip"], 2)
        assert data == "127.0.0.1"
