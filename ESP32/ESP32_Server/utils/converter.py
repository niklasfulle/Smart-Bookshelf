"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
import binascii


def string_to_byte_array(string: str) -> bytearray:
    """
    Converts a given string into a bytearray using UTF-8 encoding.
    Args:
        string (str): The input string to be converted.
    Returns:
        bytearray: The resulting bytearray representation of the input string.
    """

    bytes_string = bytearray(string, "utf-8")

    return bytes_string


def int_to_1byte_array(number: int, byteorder: str = "little") -> bytearray:
    """
    Converts an integer to a 1-byte array.
    Args:
        number (int): The integer to convert. Must be in the range 0-255.
        byteorder (str, optional): The byte order to use for conversion.
            Defaults to "little". Can be "little" or "big".
    Returns:
        bytearray: A 1-byte array representing the integer.
    Raises:
        ValueError: If the integer is greater than 255.
    """

    if number > 255:
        raise ValueError("Number to big")

    array = bytearray(number.to_bytes(1, byteorder))
    return array


def int_to_2byte_array(number: int, byteorder: str = "little") -> bytearray:
    """
    Converts an integer to a 2-byte array representation.
    Args:
        number (int): The integer to convert. Must be in the range 0-65535.
        byteorder (str): The byte order to use for the conversion.
                         Defaults to "little". Can be "little" or "big".
    Returns:
        bytearray: A 2-byte array representation of the input integer.
    Raises:
        ValueError: If the input integer is greater than 65535.
    """

    if number > 65535:
        raise ValueError("Number to big")

    array = bytearray(number.to_bytes(2, byteorder))
    return array


def int_to_4byte_array(number: int, byteorder: str = "little") -> bytearray:
    """
    Converts an integer into a 4-byte array representation.
    Args:
        number (int): The integer to convert. Must be less than or equal to 2147483646.
        byteorder (str): The byte order to use for the conversion. Defaults to "little".
                         Can be "little" for little-endian or "big" for big-endian.
    Returns:
        bytearray: A 4-byte array representing the integer.
    Raises:
        ValueError: If the number is greater than 2147483646.
    """

    if number > 2147483646:
        raise ValueError("Number to big")

    array = bytearray(number.to_bytes(4, byteorder))
    return array


def convert_string_bytes_to_bytearray(string_with_bytes: str, type: int) -> bytearray:
    """
    Converts a string representation of bytes into a bytearray.
    Args:
        string_with_bytes (str): The input string containing byte values.
            - For `type` 1: The string should contain comma-separated hexadecimal values (e.g., "0x1, 0x2, 0x3").
            - For `type` 2: The string should contain space-separated hexadecimal values (e.g., "01 02 03").
        type (int): Specifies the format of the input string.
            - 1: Input string is comma-separated with "0x" prefixes.
            - 2: Input string is space-separated without "0x" prefixes.
    Returns:
        bytearray: A bytearray object representing the converted bytes.
    Raises:
        ValueError: If the input string is not properly formatted or cannot be converted.
    """

    if type == 1:
        test = string_with_bytes.split(", ")
        for idx, ele in enumerate(test):
            test[idx] = ele.replace("0x", "")

        for idx, ele in enumerate(test):
            if len(test[idx]) == 1:
                test[idx] = "0" + test[idx]

        string = " ".join(test)

        return bytearray(binascii.unhexlify(string.replace(" ", "")))
    elif type == 2:
        return bytearray(binascii.unhexlify(string_with_bytes.replace(" ", "")))


def get_hex_string(byte_string: bytearray) -> str:
    """
    Converts a bytearray into a formatted hexadecimal string.
    This function takes a bytearray as input and returns a string where each byte
    is represented in hexadecimal format, separated by commas. Single-digit
    hexadecimal values are zero-padded to ensure a consistent two-character format.
    Args:
        byte_string (bytearray): The input bytearray to be converted.
    Returns:
        str: A string representation of the bytearray in hexadecimal format, with
             each byte separated by a comma.
    """

    hex_string = ", ".join(hex(b) for b in byte_string)
    hex_string = hex_string.replace("0x0", "0x00")

    split_string = hex_string.split(", ")

    for i in enumerate(split_string):
        if len(split_string[i[0]]) == 3:
            split_string2 = split_string[i[0]].split("x")
            element = split_string2[0] + "x0" + split_string2[1]
            split_string[i[0]] = element

    string = ", ".join(split_string)

    return string


def get_hex_string_arrs(byte_string: bytearray) -> list[str]:
    """
    Converts a bytearray into a list of formatted hexadecimal string representations.
    Args:
        byte_string (bytearray): The input bytearray to be converted.
    Returns:
        list[str]: A list of hexadecimal string representations of the input bytearray.
                   Each element is formatted as "0xXX", where "XX" is a two-character
                   hexadecimal value. Single-digit values are zero-padded.
    """

    hex_string = ", ".join(hex(b) for b in byte_string)
    hex_string = hex_string.replace("0x0", "0x00")

    split_string = hex_string.split(", ")

    for i in enumerate(split_string):
        if len(split_string[i[0]]) == 3:
            split_string2 = split_string[i[0]].split("x")
            element = split_string2[0] + "x0" + split_string2[1]
            split_string[i[0]] = element

    return split_string
