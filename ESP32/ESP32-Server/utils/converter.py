"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
import binascii

def string_to_byte_array(string: str) -> bytearray:
    """Convert string to bytes

    Args:
        string (str):

    Returns:
        bytearray:
    """

    bytes_string = bytearray(string, "utf-8")

    return bytes_string


def int_to_2byte_array(number: int, byteorder: str = "little") -> bytearray:
    """converts an int to a 2 byte value, throws an Exception when the number is to big

    Args:
        number (int): the int number who gets converterd

    Returns:
        bytearray: the number as 2-byte bytearray
    """

    if number > 65535:
        raise ValueError("Number to big")

    array = bytearray(number.to_bytes(2, byteorder))
    return array


def int_to_4byte_array(number: int, byteorder: str = "little") -> bytearray:
    """converts an int to a 4 byte value, throws an Exception when the number is to big

    Args:
        number (int): the int number who gets converterd

    Returns:
        bytearray: the number as 4-byte bytearray
    """

    if number > 2147483646:
        raise ValueError("Number to big")

    array = bytearray(number.to_bytes(4, byteorder))
    return array


def convert_string_bytes_to_bytearray(string_with_bytes: str, type: int) -> bytearray:
    """converts the passed string into a byte array with the given type of the string

    Args:
        string_with_bytes (str):
        type (int): the type of the passed string

    Returns:
        bytearray: the converted data
    """

    if type == 1:
        test = string_with_bytes.split(", ")
        for idx, ele in enumerate(test):
            test[idx] = ele.replace("0x", "")

        for idx, ele in enumerate(test):
            if len(test[idx]) == 1:
                test[idx] = "0" + test[idx]

        string = " ".join(test)

        return bytearray(binascii.unhexlify(string.replace(' ', '')))
    elif type == 2:
        return bytearray(binascii.unhexlify(string_with_bytes.replace(' ', '')))
