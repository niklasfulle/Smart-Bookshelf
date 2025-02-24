"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719

from utils.build_helper import get_random_sequence_number, get_timestamp
from protocol.builder.builder_default_package import build_connection_request, build_connection_response

test = build_connection_request(10, 20, get_random_sequence_number(), 0, get_timestamp(), 0)

test.print_data()
