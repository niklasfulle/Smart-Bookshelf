"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719
from data_upload_package import data_upload_package
from ESP32.ESP32_Server.utils.parse_helper import parse_data_start_end

def parse_data_upload_package (
    data: bytearray
) -> data_upload_package:
    """
        - 
    """
    message_type: bytearray = parse_data_start_end(data, 4, 2)
    upload_package_data: bytearray = parse_data_start_end(data, len(data), 4)

    return data_upload_package(message_type, upload_package_data)
