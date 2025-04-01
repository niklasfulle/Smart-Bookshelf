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
    -
    """

    def test_build_data_to_send_bytearray_arr1(self):
        """
        -
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
        -
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
        -
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
        -
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
