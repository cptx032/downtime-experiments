# migrate.py

from typing import List, Dict

import psycopg2
import sys
from psycopg2.extensions import connection as Con

op_code: str = sys.argv[1]

connection: Con = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)
with connection:
	cursor = connection.cursor()
	if op_code == "A18":
		cursor.execute("CREATE INDEX ON Tag ((name));")
		connection.commit()