"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301,W0621,W0602
import math
from utils.checksumme import get_checksumme
from utils.constants import MD4_Type
from connection.connection import connection


def build_data_to_send_bytearray_arr(data: str) -> list:
    """
    Splits a given string into chunks of up to 80 bytes, appends a checksum to each chunk,
    and returns a list of bytearrays.
    Args:
        data (str): The input string to be split and processed.
    Returns:
        list: A list of bytearrays, where each bytearray represents a chunk of the input
        string with an appended checksum.
    Notes:
        - The function uses UTF-8 encoding to convert the input string into a bytearray.
        - If the input string is less than or equal to 80 bytes, it is processed as a single chunk.
        - For input strings longer than 80 bytes, the function splits the data into chunks of
          80 bytes, calculates a checksum for each chunk, and appends the checksum to the chunk.
        - The checksum is calculated using the `get_checksumme` function with the `MD4_Type.LOWER_HALF` type.
    """

    data_bytearray: bytearray = bytearray(data.encode("utf-8"))
    data_arr: list = []

    if len(data_bytearray) <= 80:
        data_arr.append(
            data_bytearray + get_checksumme(data_bytearray.copy(), MD4_Type.LOWER_HALF)
        )
    elif len(data_bytearray) > 80:
        data_packages_count: int = math.floor(len(data) / 80) + 1

        for i in range(0, data_packages_count, 1):
            if i == 0:
                data_arr.append(
                    data_bytearray[0:80]
                    + get_checksumme(data_bytearray[0:80].copy(), MD4_Type.LOWER_HALF)
                )
            elif i is data_packages_count - 1:
                first = i * 80
                second = len(data_bytearray)
                data_arr.append(
                    data_bytearray[first:second]
                    + get_checksumme(
                        data_bytearray[first:second].copy(), MD4_Type.LOWER_HALF
                    )
                )
            else:
                first = i * 80
                second = (i + 1) * 80
                data_arr.append(
                    data_bytearray[first:second]
                    + get_checksumme(
                        data_bytearray[first:second].copy(), MD4_Type.LOWER_HALF
                    )
                )

    return data_arr


def handle_data_reveiv_mode(_connection: connection) -> None:
    print(_connection.data_reveiv_mode)


def handle_data_send_mode(_connection: connection) -> None:
    print(_connection.data_send_mode)
