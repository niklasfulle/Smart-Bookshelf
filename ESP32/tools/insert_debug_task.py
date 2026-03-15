"""
Insert a debug task into the database.

Usage:
  python3 ESP32/tools/insert_debug_task.py --id ID --type TYPE --client CLIENT_ID [--data DATA]

The script reads DB connection settings from the same .env as the server,
inspects the "tasks" table for existing column names and inserts a row using
the best matching column names. It is intended for debugging only.
"""
import os
import sys
import argparse
import uuid

from dotenv import load_dotenv
import psycopg2


def infer_columns(cursor):
    cursor.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks';"
    )
    cols = [r[0] for r in cursor.fetchall()]
    return cols


def infer_column_types(cursor):
    cursor.execute(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'tasks';"
    )
    return {r[0]: r[1] for r in cursor.fetchall()}


def find_mapping(cols):
    # candidate mappings from logical name -> possible column names in DB
    candidates = {
        "id": ["id", "task_id", "uuid"],
        "type": ["type", "task_type"],
        "client": ["client_id", "clientid", "clientId", "client"],
        "data": ["data", "payload", "task_data"],
        "createdAt": ["createdat", "created_at", "createdAt"],
    }

    mapping = {}
    lower_cols = {c.lower(): c for c in cols}

    for logical, opts in candidates.items():
        for o in opts:
            if o.lower() in lower_cols:
                mapping[logical] = lower_cols[o.lower()]
                break

    return mapping


def insert_task(conn, cursor, mapping, values):
    # Build columns and values for INSERT from mapping and provided values
    cols = []
    vals = []
    # determine column types to avoid inserting string into integer id
    col_types = infer_column_types(cursor)

    for logical in ["id", "type", "client", "data"]:
        if logical in mapping and values.get(logical) is not None:
            dbcol = mapping[logical]
            # If the id column is integer, let DB assign default (skip it)
            if logical == "id" and col_types.get(dbcol, "") in ("integer", "bigint"):
                continue

            cols.append('"' + dbcol + '"')
            vals.append(values[logical])

    if not cols:
        raise RuntimeError("No suitable columns found in tasks table to insert into")

    placeholders = ", ".join(["%s"] * len(vals))
    sql = f"INSERT INTO \"tasks\" ({', '.join(cols)}) VALUES ({placeholders});"
    cursor.execute(sql, tuple(vals))
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Insert a debug task into DB")
    parser.add_argument("--id", help="task id (default: generated)")
    parser.add_argument("--type", required=True, help="task type (e.g. SLEEP)")
    parser.add_argument("--client", required=True, help="client id")
    parser.add_argument("--data", default=None, help="optional task data")

    args = parser.parse_args()

    load_dotenv()

    conn = psycopg2.connect(
        database=os.getenv("DATABASE"),
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )

    cur = conn.cursor()

    cols = infer_columns(cur)
    mapping = find_mapping(cols)

    task_id = args.id or str(uuid.uuid4())

    values = {"id": task_id, "type": args.type, "client": args.client, "data": args.data}

    print("Detected task table columns:", cols)
    print("Using mapping:", mapping)

    try:
        insert_task(conn, cur, mapping, values)
        print("Inserted task", task_id)
    except Exception as exc:
        print("Failed to insert task:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
