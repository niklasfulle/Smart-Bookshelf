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
    """
    Processes tasks from the "tasks" table in the database.
    This function retrieves all tasks from the "tasks" table, orders them by
    their creation time in ascending order, and assigns the first task to the
    `_task` attribute of the provided `_connection` object. After processing
    the first task, it deletes the task from the database.
    Args:
        postgres: The PostgreSQL database connection object used to commit changes.
        cursor: The database cursor used to execute SQL queries.
        _connection (connection): An object that contains a `_task` attribute
            to store the first task retrieved from the database.
    Returns:
        None
    """

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
    """
    Handles various tasks based on the type of task assigned to the connection.
    Args:
        _connection (connection): The connection object containing task details and
                                  methods for communication.
    Task Types:
        - TASK_TYPES.SLEEP:
            Sends a sleep request to the client and pauses execution briefly.
        - TASK_TYPES.REBOOT:
            Sends a reboot request to the client and pauses execution briefly.
        - TASK_TYPES.CONFIG_SEND:
            Prepares the connection for sending configuration data by enabling
            data send mode and disabling data receive mode. Converts the task's
            data into a bytearray for transmission.
        - TASK_TYPES.CONFIG_REQUEST:
            Prepares the connection for receiving configuration data by enabling
            data receive mode and disabling data send mode.
        - TASK_TYPES.DATA_SEND_BOOK:
            Placeholder for handling book data sending tasks.
        - TASK_TYPES.DATA_SEND_BOOKS:
            Placeholder for handling multiple books data sending tasks.
        - TASK_TYPES.DATA_SEND_MODE:
            Placeholder for handling data send mode tasks.
        - TASK_TYPES.DATA_SEND_LIGHT_ON:
            Placeholder for handling tasks to send light-on commands.
        - TASK_TYPES.DATA_SEND_LIGHT_OFF:
            Placeholder for handling tasks to send light-off commands.
    Note:
        This function assumes that the `_connection` object has specific attributes
        and methods, such as `_task`, `send_message_to_client`, and others, which
        are used to perform the required operations.
    """

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

        data_split = _connection._task.data.split(", ")

        _connection.data_to_send = build_data_to_send_bytearray_arr(data_split[1])

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
