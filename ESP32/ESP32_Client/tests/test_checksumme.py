"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")
from utils.checksumme import get_checksumme
from utils.constants import MD4_Type


class TestChecksumme:
    """
    Test suite for the `get_checksumme` function.
    This class contains unit tests to verify the correctness of the `get_checksumme`
    function under different input conditions and checksum types.
    Methods:
        test_get_checksumme1:
            Tests the `get_checksumme` function with an empty byte string and
            `MD4_Type.NONE`. Expects an empty byte string as the result.
        test_get_checksumme2:
            Tests the `get_checksumme` function with the byte string "RaSTA" and
            `MD4_Type.LOWER_HALF`. Expects a specific byte array as the result.
        test_get_checksumme3:
            Tests the `get_checksumme` function with the byte string "RaSTA" and
            `MD4_Type.FULL`. Expects a specific byte array as the result.
    """

    def test_get_checksumme1(self):
        """
        Test case for the `get_checksumme` function with an empty byte string and no checksum type.

        This test verifies that the `get_checksumme` function correctly returns an empty byte string
        when provided with an empty input and `MD4_Type.NONE` as the checksum type.

        Assertions:
            - The result of `get_checksumme(b"", MD4_Type.NONE)` should be an empty byte string (b"").
        """

        result = get_checksumme(b"", MD4_Type.NONE)
        assert result == b""

    def test_get_checksumme2(self):
        """
        Test case for the `get_checksumme` function.

        This test verifies that the `get_checksumme` function correctly computes
        the checksum for the given input data and checksum type.

        Test Scenario:
        - Input data: b"RaSTA"
        - Checksum type: MD4_Type.LOWER_HALF
        - Expected result: bytearray(b"\xc3\x03\xf2\xd8K\x91\xd8\xa7")

        Assertions:
        - Ensures the computed checksum matches the expected result.
        """

        result = get_checksumme(b"RaSTA", MD4_Type.LOWER_HALF)
        assert result == bytearray(b"\xc3\x03\xf2\xd8K\x91\xd8\xa7")

    def test_get_checksumme3(self):
        """
        Test the `get_checksumme` function with the input "RaSTA" and the MD4_Type.FULL option.

        This test verifies that the `get_checksumme` function correctly computes the checksum
        for the given input data and checksum type. The expected result is compared against
        the actual output to ensure correctness.

        Assertions:
            - The result of `get_checksumme` should match the expected bytearray value.
        """

        result = get_checksumme(b"RaSTA", MD4_Type.FULL)
        assert result == bytearray(
            b"\xc3\x03\xf2\xd8K\x91\xd8\xa7-\x8a\n\x13;/\xdd\xdf"
        )
