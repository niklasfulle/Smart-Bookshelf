"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
import gc

def parse_data_start_end(data: str, end: int, start: int) -> bytearray:
    """Gets a string array where an index represents a byte, furthermore an end and a start
    point which represent the range of the value

    Args:
        data (str): the string array
        end (int): endpoint of the value
        start (int): start of the value

    Returns:
        bytearray: returns the value as bytearray
    """
    string = ""
    for i in range(start, end, 1):
        if i > end:
            string += data[i] + " "
        else:
            string += data[i]

    gc.collect()
    return bytearray.fromhex(string)
