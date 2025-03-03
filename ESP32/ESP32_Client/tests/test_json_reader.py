"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")
from utils.json_data_reader import json_data_reader


class TestJsonReader:
    """
    -
    """
    path1: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config1.json"
    path2: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config2.json"
    path3: str = "/Users/niklasfulle/Code/Smart-Bookshelf/ESP32/ESP32_Client/tests/test_configs/test_config3.json"

    def test_json_data_reader1(self):
        """Tests whether the checksum is correct"""
