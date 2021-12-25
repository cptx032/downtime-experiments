import argparse
import random
import time
from datetime import datetime

import psycopg2
from django.utils.crypto import get_random_string

parser = argparse.ArgumentParser(
    description="It does a UPDATE in a table at each 0.5 seconds"
)
parser.add_argument("log_file_name", type=str, help="log file name")
parser.add_argument("table", type=str, help="the table name")
parser.add_argument("column", type=str, help="the column name")
parser.add_argument(
    "population", type=int, help="population argument used in prepare_db.py"
)
args = parser.parse_args()

delay: float = 0.5  # half second

connection = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)
deleted_ids = []


def random_value():
    return random.choice(range(args.population * 10000)) + 1


def get_random_id():
    possible_id = random_value()
    while possible_id in deleted_ids:
        possible_id = random_value()
    deleted_ids.append(possible_id)
    return possible_id

with connection:
    while True:
        with connection.cursor() as cursor:
            start: str = datetime.now().isoformat()
            success: bool = True
            error: str = ""
            try:
                sql = "DELETE FROM {table} WHERE id={id}".format(
                    table=args.table.strip(),
                    id=get_random_id(),
                )
                cursor.execute(sql)
                connection.commit()
            except Exception as e:
                success = False
                error = str(e)
            finally:
                end: str = datetime.now().isoformat()
                with open(args.log_file_name, "a") as log_file:
                    print(
                        "{start};{end};{success};{error}".format(
                            start=start,
                            end=end,
                            success=int(success),
                            error=error,
                        ),
                        file=log_file,
                    )
                    log_file.flush()
            time.sleep(delay)
