"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719
from protocol.builder.builder_default_package import build_connection_request
from protocol.parser.parser_default_package import parse_package

package = build_connection_request(10, 20, 0, 0, 0, 0)

parsed_package = parse_package(package.complete_data)
