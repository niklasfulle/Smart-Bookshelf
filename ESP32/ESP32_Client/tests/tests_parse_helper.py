"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import unittest
import sys
sys.path.append('../')
from utils.converter import get_hex_string
from utils.parse_helper import get_data_string_array, parse_data_start_end


class TestParseHelper(unittest.TestCase):
    """
        -
    """
    def test_parse_data_start_end1(self):
        """Tests whether the data is read in correctly"""

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 12, 10)
        result = int.from_bytes(result, "little")
        self.assertEqual(result, 6240)

    def test_parse_data_start_end2(self):
        """Tests whether the data is read in correctly"""

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 24, 20)
        result = int.from_bytes(result, "little")
        self.assertEqual(result, 425492977)

    def test_parse_data_start_end3(self):
        """Tests whether the data is read in correctly"""

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, len(data), len(data) - 8)
        self.assertEqual(result, bytearray(b"R\xc6\xf3\xb4\xe3\x8b\xf6F"))

    def test_parse_data_start_end4(self):
        """Tests whether the data is read in correctly"""

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 39, 38)
        self.assertEqual(result, bytearray(b"@"))
        result2 = get_hex_string(result)
        self.assertEqual(result2, "0x40")

    def test_parse_data_start_end5(self):
        """Tests whether the data is read in correctly"""

        data = "59 00 00 00 03 00 00 00 51 00 60 18 30 01 00 00 02 00 00 00 f1 81 5c 19 f9 ff ff ff 3f dd c1 ce e7 90 9d 1b 2b 00 40 21 00 74 65 63 44 53 54 57 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 74 65 63 34 37 57 31 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 5f 52 c6 f3 b4 e3 8b f6 46"
        data = get_data_string_array(data)
        result = parse_data_start_end(data, 61, 41)
        self.assertEqual(result, bytearray(b"tecDSTW_____________"))
        result2 = get_hex_string(result)
        self.assertEqual(
            result2,
            "0x74, 0x65, 0x63, 0x44, 0x53, 0x54, 0x57, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f, 0x5f",
        )

if __name__ == "__main__":
    unittest.main()
