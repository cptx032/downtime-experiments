import time
from datetime import datetime
from typing import Dict
import sys
import psycopg2

delay: float = 0.5  # half second
# here we mimics the Django behavior in production: keeps an connection opened
connection = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)

with connection:
    cursor = connection.cursor()

    while True:
        start: str = datetime.now().isoformat()
        success: bool = True
        error: str = ""
        try:
            cursor.execute("SELECT * from {}".format(sys.argv[2]))
            cursor.fetchall()
        except Exception as e:
            success = False
            error = str(e)
        finally:
            end: str = datetime.now().isoformat()
            with open(sys.argv[1], 'a') as log_file:
                print(
                    "{start};{end};{success};{error}".format(
                        start=start, end=end, success=int(success), error=error
                    ),
                    file=log_file
                )
        time.sleep(delay)
