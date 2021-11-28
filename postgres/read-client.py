import argparse
import time
from datetime import datetime

import psycopg2

parser = argparse.ArgumentParser(
    description="It does a SELECT in a table at each 0.5 seconds"
)
parser.add_argument("log_file_name", type=str, help="log file name")
parser.add_argument("table", type=str, help="the table name")
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
                cursor.execute("SELECT * from {} LIMIT 100".format(args.table))
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
