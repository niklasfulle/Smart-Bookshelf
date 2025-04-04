"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from utils.md4 import MD4  # noqa: E402
from utils.constants import MD4_Type
from utils.converter import convert_string_bytes_to_bytearray


def get_checksumme(data: bytearray, type: MD4_Type) -> bytearray:
    """
    Computes the checksum of the given data using the MD4 hashing algorithm.
    Args:
        data (bytearray): The input data for which the checksum is to be calculated.
        type (MD4_Type): Specifies the type of checksum to compute. It can be one of the following:
            - MD4_Type.LOWER_HALF: Computes the checksum using only the lower half of the MD4 hash.
            - MD4_Type.FULL: Computes the checksum using the full MD4 hash.
    Returns:
        bytearray: The computed checksum as a bytearray. Returns an empty bytearray (b"") if the type is invalid.
    """

    if type == MD4_Type.LOWER_HALF:
        md4 = MD4(data)
        md4_len = [
            md4.hexdigest()[i : i + 16] for i in range(0, len(md4.hexdigest()), 16)
        ]
        md4_hex_string = " ".join(
            md4_len[0][i : i + 2] for i in range(0, len(md4_len[0]), 2)
        )
        checksum = convert_string_bytes_to_bytearray(md4_hex_string, 2)
        return checksum

    if type == MD4_Type.FULL:
        md4 = MD4(data)
        md4_hex_string = " ".join(
            md4.hexdigest()[i : i + 2] for i in range(0, len(md4.hexdigest()), 2)
        )
        checksum = convert_string_bytes_to_bytearray(md4_hex_string, 2)
        return checksum

    return b""
