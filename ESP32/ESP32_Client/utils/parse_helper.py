"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from utils.converter import get_hex_string


def parse_data_start_end(data: str, end: int, start: int) -> bytearray:
    """
    Extracts a substring from the input string `data` between the specified `start`
    and `end` indices, converts it into a space-separated hexadecimal string, and
    returns it as a bytearray.
    Args:
        data (str): The input string containing hexadecimal characters.
        end (int): The ending index (exclusive) for the substring extraction.
        start (int): The starting index (inclusive) for the substring extraction.
    Returns:
        bytearray: A bytearray representation of the extracted hexadecimal string.
    Note:
        - The function appears to have a logical error in the condition `if i > end`,
          as `i` will never be greater than `end` due to the loop range. This condition
          may need to be reviewed and corrected.
    """

    string = ""
    for i in range(start, end, 1):
        if i > end:
            string += data[i] + " "
        else:
            string += data[i]

    return bytearray.fromhex(string)


def get_data_string_array(data: bytearray) -> str:
    """
    Converts the input data into a string array representation.
    Args:
        data (bytearray or str): The input data to be processed. It can either be a string or a bytearray.
    Returns:
        str: A string array representation of the input data. If the input is a string, it is split by spaces.
             If the input is a bytearray, it is converted to a hexadecimal string, split by commas, and
             stripped of the "0x" prefix.
    """

    string_split: str = ""

    if isinstance(data, str):
        string_split = data.split(" ")

    elif isinstance(data, bytearray):
        string = get_hex_string(data)
        string_split = string.split(", ")
        for idx, ele in enumerate(string_split):
            string_split[idx] = ele.replace("0x", "")

    return string_split
