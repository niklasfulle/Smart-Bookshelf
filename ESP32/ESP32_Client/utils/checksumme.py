"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from utils.md4 import MD4  # noqa: E402
from utils.constants import MD4_Type
from utils.converter import convert_string_bytes_to_bytearray


def get_checksumme(data: bytearray, type: MD4_Type) -> bytearray:
    """the function receives a byte array and the type of the desired checksum
    and then returns either no checksum, the lower half or the entire checksum

    Args:
        data (bytearray): the value from which the checksum is to be formed
        type (RASTA_SAFTEY_OPTION): The type of checksum

    Returns:
        bytearray: checksum
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
