"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301
import sys

sys.path.append("../")
from protocol.builder.builder_default_package import (
    build_connection_request,
    build_connection_response,
    build_connection_approve,
    build_version_request,
    build_version_response,
    build_status_request,
    build_status_response,
    build_disconnection_request,
    build_disconnection_response,
    build_sleep_request,
    build_sleep_response,
    build_reboot_request,
    build_reboot_response,
    build_data,
    build_upload_data,
)
from utils.build_helper import get_timestamp, get_random_sequence_number, increment_sequence_number

from protocol.parser.parser_default_package import parse_package
class TestParseDefaultPackage:
    """
    -
    """
    
    def test_parse_connection_request(self) -> None:
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_request(
            10, 20, sequence_number, sequence_number, timestamp, timestamp
        )

        parsed_package = parse_package(package.complete_data)

        assert int.from_bytes(parsed_package.lenght, "little") == 36
        assert int.from_bytes(parsed_package.receiver_id, "little") == 10
        assert int.from_bytes(parsed_package.sender_id, "little") == 20
        assert parsed_package.sequence_number == increment_sequence_number(sequence_number)
        assert parsed_package.confirmed_sequence_number == sequence_number
        assert parsed_package.timestamp == timestamp
        assert parsed_package.confirmed_timestamp == timestamp
