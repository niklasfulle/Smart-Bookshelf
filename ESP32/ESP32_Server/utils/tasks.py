"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,C0301,W0621,W0602
import time

from connection.connection import connection
from utils.constants import TASK_TYPES
from utils.send_data import build_data_to_send_bytearray_arr
from datatype.task import task
from protocol.builder.builder_default_package import (
    build_sleep_request,
    build_reboot_request,
)
import os
import psycopg2
from dotenv import load_dotenv
import sys


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

    print("Checking for tasks...")

    # Open a dedicated DB connection for this thread to avoid sharing the
    # global `postgres` connection across threads which may block.
    load_dotenv()
    local_conn = None
    try:
        print("check_tasks: opening local DB connection")
        sys.stdout.flush()
        local_conn = psycopg2.connect(
            database=os.getenv("DATABASE"),
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )
        local_cursor = local_conn.cursor()
        print("check_tasks: executing select")
        sys.stdout.flush()
        local_cursor.execute('select * from "tasks" ORDER BY "createdAt" ASC')
        tasks = local_cursor.fetchall()
        print("check_tasks: fetched", len(tasks), "tasks")
        sys.stdout.flush()

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
            print("check_tasks: deleting task id", first_task.id)
            sys.stdout.flush()
            local_cursor.execute(delete_sql, (first_task.id,))
            local_conn.commit()
            print("check_tasks: delete committed")
            sys.stdout.flush()
    finally:
        if local_conn is not None:
            try:
                local_conn.close()
            except Exception:
                pass


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

    print(
        "handle_tasks: starting, task id:",
        getattr(_connection, "_task").id if _connection._task else None,
        "type:",
        getattr(_connection, "_task").type if _connection._task else None,
    )
    sys.stdout.flush()

    # normalize task type (accept 'SLEEP', 'task_sleep', etc.)
    task_type_raw = _connection._task.type if _connection._task else None
    task_type = task_type_raw.lower() if isinstance(task_type_raw, str) else None

    if task_type and task_type.endswith("sleep"):
        print("SLEEP")
        # determine duration from task data (accept JSON {"duration":N} or numeric string)
        duration = 0
        try:
            import json

            if _connection._task.data is not None:
                try:
                    parsed = json.loads(_connection._task.data)
                    if isinstance(parsed, dict) and "duration" in parsed:
                        duration = int(parsed["duration"])
                except Exception:
                    # not json, try numeric
                    try:
                        duration = int(str(_connection._task.data))
                    except Exception:
                        duration = 0
        except Exception:
            duration = 0

        _connection.send_message_to_client(
            build_sleep_request(
                _connection.receiver_id_int,
                _connection.sender_id_int,
                _connection.last_send_package.sequence_number,
                _connection.last_received_package.sequence_number,
                0,
                _connection.last_received_package.timestamp,
                duration,
            )
        )
        _connection._wait_for_task_response = True
        print("handle_tasks: sent SLEEP request, waiting for response")
        sys.stdout.flush()
        time.sleep(0.2)

    elif task_type and task_type.endswith("reboot"):
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
        _connection._wait_for_task_response = True
        print("handle_tasks: sent REBOOT request, waiting for response")
        sys.stdout.flush()
        time.sleep(0.2)

    elif task_type and task_type.endswith("config_send"):
        print("CONFIG_SEND")

        _connection.data_send_mode = True
        _connection.data_reveiv_mode = False

        _connection.data_to_send = build_data_to_send_bytearray_arr(
            _connection._task.data
        )

    elif task_type and task_type.endswith("config_request"):
        print("CONFIG_REQUEST")

        _connection.data_reveiv_mode = True
        _connection.data_send_mode = False

    elif task_type and task_type.endswith("data_send_book"):
        print("DATA_SEND_BOOK")

    elif task_type and task_type.endswith("data_send_books"):
        print("DATA_SEND_BOOKS")

    elif task_type and task_type.endswith("data_send_mode"):
        print("DATA_SEND_MODE")

    elif task_type and task_type.endswith("data_send_ligh_on"):
        print("DATA_SEND_LIGHT_ON")

    elif task_type and task_type.endswith("data_send_ligh_off"):
        print("DATA_SEND_LIGHT_OFF")
