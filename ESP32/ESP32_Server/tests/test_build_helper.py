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
    Test suite for testing helper functions related to building and manipulating byte arrays.
    Classes:
        TestBuildHelper: Contains unit tests for functions that handle byte array operations.
    Methods:
        test_increment_sequence_number1:
            Tests incrementing a 4-byte array representation of the number 345.
        test_increment_sequence_number2:
            Tests incrementing a 4-byte array representation of the number 2147483645.
        test_increment_sequence_number3:
            Tests incrementing a 4-byte array representation of the number 2147483646,
            ensuring it wraps around to 0.
        test_increment_sequence_number4:
            Tests that attempting to convert the number 2147483647 to a 4-byte array raises a ValueError.
        test_get_bytearrays_size_sum1:
            Tests that the size sum of an empty byte array is 0.
        test_get_bytearrays_size_sum2:
            Tests the size sum of a list containing a single 2-byte array.
        test_get_bytearrays_size_sum3:
            Tests the size sum of a list containing a single 4-byte array.
        test_get_bytearrays_size_sum4:
            Tests the size sum of a list containing multiple 2-byte and 4-byte arrays.
    """

    def test_increment_sequence_number1(self) -> None:
        """
        Test case for the `increment_sequence_number` function.
        This test verifies that the `increment_sequence_number` function correctly
        increments a 4-byte array representation of an integer by 1.
        Steps:
        1. Convert the integer 345 into a 4-byte array using `int_to_4byte_array`.
        2. Pass the 4-byte array to `increment_sequence_number`.
        3. Assert that the resulting 4-byte array, when converted back to an integer,
           equals 346.
        Expected Result:
        The function should return a 4-byte array representing the integer 346.
        """

        number = int_to_4byte_array(345)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 346

    def test_increment_sequence_number2(self):
        """
        Test case for the `increment_sequence_number` function.
        This test verifies that the `increment_sequence_number` function correctly
        increments a 4-byte array representation of an integer. Specifically, it
        checks that the function increments the value 2147483645 (represented as a
        4-byte array) to 2147483646.
        Steps:
        1. Convert the integer 2147483645 to a 4-byte array using `int_to_4byte_array`.
        2. Pass the 4-byte array to `increment_sequence_number`.
        3. Assert that the result, when converted back to an integer, equals 2147483646.
        """

        number = int_to_4byte_array(2147483645)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 2147483646

    def test_increment_sequence_number3(self):
        """
        Test the `increment_sequence_number` function with a sequence number
        close to the maximum value for a 4-byte integer.
        This test verifies that the function correctly wraps around to 0
        when the sequence number exceeds the maximum value (2147483647).
        Steps:
        1. Convert the integer 2147483646 to a 4-byte array.
        2. Increment the sequence number using `increment_sequence_number`.
        3. Assert that the result wraps around to 0.
        Expected Behavior:
        - The function should handle the overflow and reset the sequence number
          to 0 when the maximum value is exceeded.
        """

        number = int_to_4byte_array(2147483646)
        result = increment_sequence_number(number)

        assert int.from_bytes(result, "little") == 0

    def test_increment_sequence_number4(self):
        """
        Test case for the `int_to_4byte_array` function to ensure it raises a ValueError
        when provided with an integer that exceeds the maximum allowable value for a
        4-byte array (2147483647).

        This test verifies that the function correctly handles invalid input by raising
        the appropriate exception.
        """

        with pytest.raises(ValueError):
            int_to_4byte_array(2147483647)

    def test_get_bytearrays_size_sum1(self):
        """
        Test case for the `get_bytearrays_size_sum` function.

        This test verifies that the function correctly calculates the total size
        of an empty bytearray. The expected result is 0 since the input is an
        empty bytearray.
        """

        assert get_bytearrays_size_sum(b"") == 0

    def test_get_bytearrays_size_sum2(self):
        """
        Test the `get_bytearrays_size_sum` function with a list containing a single 2-byte array.
        This test verifies that the function correctly calculates the total size of byte arrays
        in the input list. Specifically, it checks that a list containing one 2-byte array
        returns the correct size sum of 2.
        """

        a = int_to_2byte_array(1)

        value = [a]

        assert get_bytearrays_size_sum(value) == 2

    def test_get_bytearrays_size_sum3(self):
        """
        Test case for the `get_bytearrays_size_sum` function.
        This test verifies that the function correctly calculates the total size
        of a list containing a single 4-byte array. The input is a list with one
        4-byte array, and the expected result is 4.
        """

        a = int_to_4byte_array(1)

        value = [a]

        assert get_bytearrays_size_sum(value) == 4

    def test_get_bytearrays_size_sum4(self):
        """
        Test the `get_bytearrays_size_sum` function with a list of byte arrays.
        This test verifies that the function correctly calculates the total size
        of a list of byte arrays. The input consists of two 2-byte arrays and
        two 4-byte arrays, and the expected total size is 12 bytes.
        Steps:
        - Convert integers to byte arrays using `int_to_2byte_array` and `int_to_4byte_array`.
        - Pass the list of byte arrays to `get_bytearrays_size_sum`.
        - Assert that the returned size matches the expected value.
        Expected Result:
        The function should return 12, which is the sum of the sizes of the
        provided byte arrays.
        """

        a = int_to_2byte_array(1)
        b = int_to_2byte_array(2)
        c = int_to_4byte_array(3)
        d = int_to_4byte_array(4)

        value = [a, b, c, d]

        assert get_bytearrays_size_sum(value) == 12
