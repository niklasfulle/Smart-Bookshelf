"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import unittest
import sys
sys.path.append('../')
from utils.checksumme import get_checksumme
from utils.constants import MD4_Type


class TestChecksumme(unittest.TestCase):
    """
        -
    """
    def test_get_checksumme1(self):
        """Tests whether the checksum is correct"""

        result = get_checksumme(b"", MD4_Type.NONE)
        self.assertEqual(result, b"")

    def test_get_checksumme2(self):
        """Tests whether the checksum is correct"""

        result = get_checksumme(b"RaSTA", MD4_Type.LOWER_HALF)
        self.assertEqual(result, bytearray(b"\xc3\x03\xf2\xd8K\x91\xd8\xa7"))

    def test_get_checksumme3(self):
        """Tests whether the checksum is correct"""

        result = get_checksumme(b"RaSTA", MD4_Type.FULL)
        self.assertEqual(result, bytearray(b"\xc3\x03\xf2\xd8K\x91\xd8\xa7-\x8a\n\x13;/\xdd\xdf"))


if __name__ == "__main__":
    unittest.main()
