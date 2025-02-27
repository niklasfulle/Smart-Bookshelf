"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from data_package import data_package
from utils.parse_helpers import parse_data_start_end

def parse_data_package (
    data: bytearray
) -> data_package:
    """
        - 
    """
    message_type: bytearray = parse_data_start_end(data, 4, 2)
    package_data: bytearray = parse_data_start_end(data, len(data), 4)

    return data_package(message_type, package_data)
