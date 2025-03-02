"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from protocol.builder.builder_default_package import build_upload_data
from protocol.builder.builder_data_upload_package import build_data_upload_package_data_start
from protocol.parser.parser_default_package import parse_package
from utils.converter import int_to_2byte_array
from utils.build_helper import get_random_sequence_number, get_timestamp

data_upload_package = build_data_upload_package_data_start(
            int_to_2byte_array(1)
        )

sequence_number = get_random_sequence_number()
timestamp = get_timestamp()

print(data_upload_package.complete_data)

package = build_upload_data(
            10,
            20,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

print(len(package.complete_data))

parsed_package = parse_package(package.complete_data)

print(len(parsed_package.data))
