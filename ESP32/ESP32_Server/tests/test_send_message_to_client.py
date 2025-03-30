"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902,C0413,C0301,E0211
import sys

sys.path.append("../")
from datatype.book import book
from utils.json_data_reader import json_data_reader
from utils.build_helper import get_random_sequence_number, get_timestamp
from utils.converter import int_to_1byte_array, int_to_2byte_array
from hardware.bookshelf import bookshelf
from connection.connection import connection
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
from protocol.builder.builder_data_package import (
    build_data_package_book,
    build_data_package_books,
    build_data_package_light_off,
    build_data_package_light_on,
    build_data_package_mode,
)
from protocol.builder.builder_data_upload_package import (
    build_data_upload_package_data,
    build_data_upload_package_data_start,
    build_data_upload_package_data_end,
    build_data_upload_package_data_cancel,
    build_data_upload_package_data_error,
)
from protocol.constants.constants import DISC_REASON, STATUS


class TestSendMessageClient:
    """
    -
    """

    client_config: str = '{"id": 10,"name": "Client_0","connection": { "ip": "127.0.0.1", "port": 40002 },"server": {"id": 20,"name": "Server","ip": "127.0.0.1","port": 50002}}'
    bookshelf_config: str = '{"name": "bookshelf_Name1", "shelving_units": [{ "order": 1, "length": 50 },{ "order": 2, "length": 50 },{ "order": 3, "length": 50 },{ "order": 4, "length": 50 },{ "order": 5, "length": 50 },{ "order": 6, "length": 50 },{ "order": 7, "length": 50 },{ "order": 8, "length": 50 }]}'
    file1: str = '{"protocol_version_major": 1,"protocol_version_minor": 0,"client_version_major": 1,"client_version_minor": 0,"bookshelf_version_major": 1,"bookshelf_version_minor": 0}'

    ip = json_data_reader(client_config, ["connection", "ip"], 2)
    bookshelf_name = json_data_reader(bookshelf_config, ["name"], 2)
    shelving_units = json_data_reader(bookshelf_config, ["shelving_units"], 2)

    bookshelf_object: bookshelf = bookshelf(bookshelf_name, ip, shelving_units)

    client_ip = json_data_reader(client_config, ["connection", "ip"], 2)
    client_port = json_data_reader(client_config, ["connection", "port"], 2)
    server_ip = json_data_reader(client_config, ["server", "ip"], 2)
    server_port = json_data_reader(client_config, ["server", "port"], 2)
    sender_id = json_data_reader(client_config, ["id"], 2)
    receiver_id = json_data_reader(client_config, ["server", "id"], 2)

    connection_object: connection = connection(
        (client_ip, client_port),
        (server_ip, server_port),
        receiver_id,
        sender_id,
        bookshelf_object,
    )

    def test_send_connection_request(self):
        """
        -
        """
        package = build_connection_request(self.sender_id, self.receiver_id, 0, 0, 0, 0)
        self.connection_object.send_message_to_client(package)

    def test_send_connection_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        package = build_connection_response(
            self.sender_id, self.receiver_id, 0, sequence_number, 0, 0
        )
        self.connection_object.send_message_to_client(package)

    def test_send_connection_approve(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_connection_approve(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_version_request(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_version_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_version_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["protocol_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["protocol_version_minor"], 2)
                )
            ),
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["client_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["client_version_minor"], 2)
                )
            ),
            (
                int_to_1byte_array(
                    json_data_reader(self.file1, ["bookshelf_version_major"], 2)
                )
                + int_to_1byte_array(
                    json_data_reader(self.file1, ["bookshelf_version_minor"], 2)
                )
            ),
        )
        self.connection_object.send_message_to_client(package)

    def test_send_status_request(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_status_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_status_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(STATUS.RUNNING),
        )
        self.connection_object.send_message_to_client(package)

    def test_send_disconnection_request(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.USERREQUEST),
        )
        self.connection_object.send_message_to_client(package)

    def test_send_disconnection_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_disconnection_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            int_to_2byte_array(DISC_REASON.USERREQUEST),
        )
        self.connection_object.send_message_to_client(package)

    def test_send_sleep_request(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_sleep_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_sleep_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_reboot_request(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_request(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_reboot_response(self):
        """
        -
        """
        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_reboot_response(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
        )
        self.connection_object.send_message_to_client(package)

    def test_send_data_package_light_on(self):
        """
        -
        """
        data_package = build_data_package_light_on()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_light_off(self):
        """
        -
        """
        data_package = build_data_package_light_off()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_book(self):
        """
        -
        """
        data_package = build_data_package_book(book(1, 12).data)

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_books(self):
        """
        -
        """
        data_package = build_data_package_books(
            data=(book(1, 12).data + book(3, 2).data)
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_package_mode(self):
        """
        -
        """
        data_package = build_data_package_mode(int_to_2byte_array(1))

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data(self):
        """
        -
        """
        data_upload_package = build_data_upload_package_data(
            int_to_2byte_array(1),
            bytearray(
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_start(self):
        """
        -
        """
        data_upload_package = build_data_upload_package_data_start(
            bytearray(b"\x00\x00")
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_end(self):
        """
        -
        """
        data_upload_package = build_data_upload_package_data_end()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_error(self):
        """
        -
        """
        data_upload_package = build_data_upload_package_data_error(
            bytearray(b"\x00\x00")
        )

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)

    def test_send_data_upload_package_data_cancel(self):
        """
        -
        """
        data_upload_package = build_data_upload_package_data_cancel()

        sequence_number = get_random_sequence_number()
        timestamp = get_timestamp()
        package = build_upload_data(
            self.sender_id,
            self.receiver_id,
            sequence_number,
            sequence_number,
            timestamp,
            timestamp,
            data_upload_package.complete_data,
        )

        self.connection_object.send_message_to_client(package)
