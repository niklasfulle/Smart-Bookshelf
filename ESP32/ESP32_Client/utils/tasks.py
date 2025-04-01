"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301,W0621,W0602
import time

from connection.connection import connection
from utils.constants import TASK_TYPES
from utils.send_data import build_data_to_send_bytearray_arr
from datatype import task
from protocol.builder.builder_default_package import (
    build_sleep_request,
    build_reboot_request,
)


def check_tasks(postgres, cursor, _connection: connection) -> None:
    cursor.execute('select * from "tasks" ORDER BY "createdAt" ASC')

    tasks = cursor.fetchall()

    first_task: task
    if len(tasks) > 0:
        first_task = task(
            tasks[0][0],
            tasks[0][1],
            tasks[0][2],
            tasks[0][3],
        )
        _connection._task = first_task

        delete_sql = 'DELETE FROM "tasks" WHERE id = %s;'
        cursor.execute(delete_sql, (first_task.id,))
        postgres.commit()


def handle_tasks(_connection: connection) -> None:
    if _connection._task.type == TASK_TYPES.SLEEP:
        print("SLEEP")
        _connection.send_message_to_client(
            build_sleep_request(
                _connection.receiver_id_int,
                _connection.sender_id_int,
                _connection.last_send_package.sequence_number,
                _connection.last_received_package.sequence_number,
                0,
                _connection.last_received_package.timestamp,
            )
        )
        time.sleep(0.2)

    elif _connection._task.type == TASK_TYPES.REBOOT:
        print("REBOOT")
        _connection.send_message_to_client(
            build_reboot_request(
                _connection.receiver_id_int,
                _connection.sender_id_int,
                _connection.last_send_package.sequence_number,
                _connection.last_received_package.sequence_number,
                0,
                _connection.last_received_package.timestamp,
            )
        )
        time.sleep(0.2)

    elif _connection._task.type == TASK_TYPES.CONFIG_SEND:
        print("CONFIG_SEND")

        _connection.data_send_mode = True
        _connection.data_reveiv_mode = False

        _connection.data_to_send = build_data_to_send_bytearray_arr(
            _connection._task.data
        )

    elif _connection._task.type == TASK_TYPES.CONFIG_REQUEST:
        print("CONFIG_REQUEST")

        _connection.data_reveiv_mode = True
        _connection.data_send_mode = False

    elif _connection._task.type == TASK_TYPES.DATA_SEND_BOOK:
        print("DATA_SEND_BOOK")

    elif _connection._task.type == TASK_TYPES.DATA_SEND_BOOKS:
        print("DATA_SEND_BOOKS")

    elif _connection._task.type == TASK_TYPES.DATA_SEND_MODE:
        print("DATA_SEND_MODE")

    elif _connection._task.type == TASK_TYPES.DATA_SEND_LIGHT_ON:
        print("DATA_SEND_LIGHT_ON")

    elif _connection._task.type == TASK_TYPES.DATA_SEND_LIGHT_OFF:
        print("DATA_SEND_LIGHT_OFF")
