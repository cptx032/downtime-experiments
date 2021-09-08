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
with connection:
    while True:
        with connection.cursor() as cursor:
            start: str = datetime.now().isoformat()
            success: bool = True
            error: str = ""
            try:
                sql = "UPDATE {table} SET {column}='{new_value}' WHERE id={id}".format(
                    table=args.table.strip(),
                    column=args.column.strip(),
                    new_value=get_random_string(),
                    id=random.choice(range(args.population * 10000)) + 1,
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
            time.sleep(delay)