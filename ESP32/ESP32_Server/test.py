import sys
import os
import psycopg2
from dotenv import load_dotenv

sys.path.append("../")
from utils.send_data import build_data_to_send_bytearray_arr
from datatype.task import task

load_dotenv()

postgres = psycopg2.connect(
    database=os.getenv("DATABASE"),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)

cursor = postgres.cursor()

cursor.execute('select * from "tasks" ORDER BY "createdAt" ASC')

tasks = cursor.fetchall()

_task = task(
    tasks[0][0],
    tasks[0][1],
    tasks[0][2],
    tasks[0][3],
)

print(tasks[0])

result = build_data_to_send_bytearray_arr(_task.data)

print(result[0])
print(result[1])
print(result[2])
print(result[3])
print(result[4])
