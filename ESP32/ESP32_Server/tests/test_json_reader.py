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
    path1: str = "/Users/niklasfulle/Code/Smarts-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config1.json"
    path2: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config2.json"
    path3: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config3.json"
    path4: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config4.json"

    def test_json_data_reader1(self):
        """Tests whether the checksum is correct"""
        print(self.path1)
        with pytest.raises(FileNotFoundError):
            json_data_reader(self.path1, [])

    def test_json_data_reader2(self):
        """Tests whether the checksum is correct"""
        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.path2, [])

    def test_json_data_reader3(self):
        """Tests whether the checksum is correct"""
        with pytest.raises(json.decoder.JSONDecodeError):
            json_data_reader(self.path3, [])

    def test_json_data_reader4(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.path4, [])
        assert data == {
                            "id": 10,
                            "name": "Client_0",
                            "connection": { "ip": "127.0.0.1", "port": 40000 },
                            "server": {
                                "id": 20,
                                "name": "Server",
                                "ip": "127.0.0.1",
                                "port": 50000
                            }
                        }

    def test_json_data_reader5(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.path4, ["name"])
        assert data == "Client_0"

    def test_json_data_reader6(self):
        """Tests whether the checksum is correct"""

        data = json_data_reader(self.path4, ["connection", "ip"])
        assert data == "127.0.0.1"
