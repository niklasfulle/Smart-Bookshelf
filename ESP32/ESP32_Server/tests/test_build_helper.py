"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys
import pytest

sys.path.append("../")
from utils.converter import int_to_2byte_array, int_to_4byte_array
from utils.build_helper import increment_sequence_number, get_bytearrays_size_sum


class TestBuildHelper:
    """
    -
    """

    def test_increment_sequence_number1(self) -> None:
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(345)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 346

    def test_increment_sequence_number2(self):
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(2147483645)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 2147483646

    def test_increment_sequence_number3(self):
        """Tests whether the sequence number is incremented correctly"""

        number = int_to_4byte_array(2147483646)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 0

    def test_increment_sequence_number4(self):
        """Tests whether the sequence number is incremented correctly"""

        with pytest.raises(ValueError):
            int_to_4byte_array(2147483647)

    def test_get_bytearrays_size_sum1(self):
        """Tests whether the lengths of the arrays are added together correctly"""

        assert get_bytearrays_size_sum(b"") == 0

    def test_get_bytearrays_size_sum2(self):
        """Tests whether the lengths of the arrays are added together correctly"""

        a = int_to_2byte_array(1)

        value = [a]

        assert get_bytearrays_size_sum(value) == 2

    def test_get_bytearrays_size_sum3(self):
        """Tests whether the lengths of the arrays are added together correctly"""

        a = int_to_4byte_array(1)

        value = [a]

        assert get_bytearrays_size_sum(value) == 4

    def test_get_bytearrays_size_sum4(self):
        """Tests whether the lengths of the arrays are added together correctly"""

        a = int_to_2byte_array(1)
        b = int_to_2byte_array(2)
        c = int_to_4byte_array(3)
        d = int_to_4byte_array(4)

        value = [a, b, c, d]

        assert get_bytearrays_size_sum(value) == 12
