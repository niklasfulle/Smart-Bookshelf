"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import unittest
import sys
sys.path.append('../')
from utils.converter import int_to_4byte_array
from utils.build_helper import increment_sequence_number


class TestBuildHelper(unittest.TestCase):
    """
        -
    """
    def test_increment_sequence_number1(self):
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(345)
        result = increment_sequence_number(number)
        result = int.from_bytes(result, "little")
        self.assertEqual(result, 346)

    def test_increment_sequence_number2(self):
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(2147483645)
        result = increment_sequence_number(number)
        result = int.from_bytes(result, "little")
        self.assertEqual(result, 2147483646)

    def test_increment_sequence_number3(self):
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(2147483646)
        result = increment_sequence_number(number)
        result = int.from_bytes(result, "little")
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
