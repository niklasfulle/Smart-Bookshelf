"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from utils.send_data import build_data_to_send_bytearray_arr
from datatype.task import task


class TestBookshelf:
    """
    TestBookshelf is a test suite for verifying the functionality of the `build_data_to_send_bytearray_arr` function.
    Methods:
        test_build_data_to_send_bytearray_arr1:
            Tests the function with a short string input and verifies the resulting bytearray structure and content.
        test_build_data_to_send_bytearray_arr2:
            Tests the function with a moderately long string input and verifies the resulting bytearray structure and content.
        test_build_data_to_send_bytearray_arr3:
            Tests the function with a long string input that requires splitting into multiple bytearrays and verifies the structure and content of each segment.
        test_build_data_to_send_bytearray_arr4:
            Tests the function with an even longer string input that spans multiple bytearrays and verifies the structure and content of each segment.
    """

    def test_build_data_to_send_bytearray_arr1(self):
        """
        Test case for the `build_data_to_send_bytearray_arr` function.
        This test verifies that the function correctly builds a list of bytearrays
        from the provided task data. Specifically, it checks:
        - The length of the resulting list is 1.
        - The length of the first bytearray in the list is 12.
        - The content of the first bytearray matches the expected value.
        Test Data:
        - Task data: ("1", "CONFIG_SEND", "40000", "test")
        - Expected bytearray: b"test\xdb4mi\x1dz\xccM"
        Assertions:
        - The length of the result list is 1.
        - The length of the first bytearray in the result list is 12.
        - The first bytearray in the result list matches the expected value.
        """
        task_data = (
            "1",
            "CONFIG_SEND",
            "40000",
            "test",
        )

        _task = task(task_data[0], task_data[1], task_data[2], task_data[3])

        result = build_data_to_send_bytearray_arr(_task.data)

        assert len(result) == 1
        assert len(result[0]) == 12
        assert result[0] == bytearray(b"test\xdb4mi\x1dz\xccM")

    def test_build_data_to_send_bytearray_arr2(self):
        """
        Test case for the `build_data_to_send_bytearray_arr` function.
        This test verifies that the function correctly processes task data into a
        list containing a single bytearray with the expected length and content.
        Test Steps:
        1. Define task data as a tuple containing task ID, task type, task size,
           and task payload.
        2. Create a `task` object using the provided task data.
        3. Call `build_data_to_send_bytearray_arr` with the task's data.
        4. Assert that the resulting list contains exactly one bytearray.
        5. Assert that the length of the bytearray is 46 bytes.
        6. Assert that the bytearray matches the expected content.
        Expected Result:
        - The function should return a list containing a single bytearray with
          the correct length and content.
        """
        task_data = (
            "1",
            "CONFIG_SEND",
            "40000",
            "testdpoawhjdpawohdapdihlawkdiapwdhapwi",
        )

        _task = task(task_data[0], task_data[1], task_data[2], task_data[3])

        result = build_data_to_send_bytearray_arr(_task.data)

        assert len(result) == 1
        assert len(result[0]) == 46
        assert result[0] == bytearray(
            b"testdpoawhjdpawohdapdihlawkdiapwdhapwi\xbdl\xef\x8b\xf5\x85\x06\x8d"
        )

    def test_build_data_to_send_bytearray_arr3(self):
        """
        Test case for the `build_data_to_send_bytearray_arr` function.
        This test verifies that the function correctly splits a large string into
        multiple bytearrays of specified lengths and ensures the resulting bytearrays
        match the expected values.
        Test Scenario:
        - A task object is created with specific data.
        - The `build_data_to_send_bytearray_arr` function is called with the task's data.
        - The resulting bytearrays are validated for:
            - Correct number of bytearrays.
            - Correct lengths of each bytearray.
            - Correct content of each bytearray.
        Assertions:
        - The result contains exactly 3 bytearrays.
        - The lengths of the bytearrays are 88, 88, and 29 respectively.
        - The content of each bytearray matches the expected byte sequences.
        """

        task_data = (
            "1",
            "CONFIG_SEND",
            "40000",
            "testdpoawhjdpawohdapdihlawkdicaüpjfeüfosjeofpsefjpofjsepofespofpsofposehfposhefpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsnfspeoifbensifpiseapwdhapwi",
        )

        _task = task(task_data[0], task_data[1], task_data[2], task_data[3])

        result = build_data_to_send_bytearray_arr(_task.data)

        assert len(result) == 3
        assert len(result[0]) == 88
        assert len(result[1]) == 88
        assert len(result[2]) == 29
        assert result[0] == bytearray(
            bytearray(
                b"testdpoawhjdpawohdapdihlawkdica\xc3\xbcpjfe\xc3\xbcfosjeofpsefjpofjsepofespofpsofposehfposhe\x16D\x9d\x0b\xdd+I["
            )
        )
        assert result[1] == bytearray(
            b'fpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsnfspeo\xa8"\xc4X\xb6\x08\xe8\x1b'
        )
        assert result[2] == bytearray(b"ifbensifpiseapwdhapwiA '\xc4by}7")

    def test_build_data_to_send_bytearray_arr4(self):
        """
        Test the `build_data_to_send_bytearray_arr` function with a specific task data input.
        This test verifies that the function correctly splits a large string into multiple
        bytearray chunks of specified lengths and ensures the resulting bytearrays match
        the expected values.
        Test Steps:
        1. Create a `task` object with predefined data.
        2. Call the `build_data_to_send_bytearray_arr` function with the task's data.
        3. Assert that the resulting list contains exactly 5 bytearrays.
        4. Verify the length of each bytearray in the result.
        5. Compare each bytearray in the result with the expected bytearray values.
        Assertions:
        - The result contains 5 bytearrays.
        - The lengths of the bytearrays are as follows:
            - First 4 bytearrays: 88 bytes each.
            - Fifth bytearray: 23 bytes.
        - Each bytearray matches the expected bytearray value.
        Purpose:
        Ensure that the `build_data_to_send_bytearray_arr` function handles large input
        strings correctly by splitting them into bytearrays of appropriate sizes and
        content.
        """

        task_data = (
            "1",
            "CONFIG_SEND",
            "40000",
            "testdpoawhjdpawohdapdihlawkdicaüpjfeüfosjeofpsefjofjsepofespofpsofposehfposhefpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsntestdpoawhjdpawohdapdihlawkdicaüpjfeüfosjeofpsefjpofjsepofespofpsofposehfposhefpsnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsnfspeoifbensifpiseapwdhapwi",
        )

        _task = task(task_data[0], task_data[1], task_data[2], task_data[3])

        result = build_data_to_send_bytearray_arr(_task.data)

        assert len(result) == 5
        assert len(result[0]) == 88
        assert len(result[1]) == 88
        assert len(result[2]) == 88
        assert len(result[3]) == 88
        assert len(result[4]) == 23
        assert result[0] == bytearray(
            bytearray(
                b"testdpoawhjdpawohdapdihlawkdica\xc3\xbcpjfe\xc3\xbcfosjeofpsefjofjsepofespofpsofposehfposhef\xb7f\xad\xfb\xe1O*E"
            )
        )
        assert result[1] == bytearray(
            b"psnpfohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsntestdpx<\x11`\x81\xe6t\x13"
        )

        assert result[2] == bytearray(
            b"oawhjdpawohdapdihlawkdica\xc3\xbcpjfe\xc3\xbcfosjeofpsefjpofjsepofespofpsofposehfposhefpsnpf\xd6\xc95%\x86\xaf\xf2\xef"
        )

        assert result[3] == bytearray(
            b"ohepsfnsioefnpefnhesofinspeifnsepifnseonsefpisencpseifhnsipfsnehfipsnfspeoifbensX5\x99\x8f\x85\xcbJ#"
        )

        assert result[4] == bytearray(b"ifpiseapwdhapwi\x9f\xaa\xb57\x9f\xf7J\xa3")
