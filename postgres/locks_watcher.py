#!/usr/bin/env python

import psycopg2
import time
from datetime import datetime


sql: str = """
SELECT
	pg_stat_all_tables.relname,
	pg_locks.mode,
	pg_locks.granted,
	pg_stat_activity.query
FROM pg_locks
INNER JOIN pg_stat_all_tables
	ON pg_locks.relation=pg_stat_all_tables.relid
INNER JOIN pg_stat_activity
	ON pg_stat_activity.pid=pg_locks.pid
WHERE pg_stat_all_tables.relname='tag'
ORDER BY relation ASC;
"""

delay: float = 0.5  # half second

connection = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)

print("Table,Mode,Granted,Query")
with connection:
    while True:
        with connection.cursor() as cursor:
            start: str = datetime.now().isoformat()
            cursor.execute(sql)
            connection.commit()
            # print(f"{start}")
            for row in cursor.fetchall():
            	print(",".join([start] + [str(i) for i in row]))
            time.sleep(delay)