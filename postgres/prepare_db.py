# prepare_db.py

from typing import List, Dict

import psycopg2
import sys
from psycopg2.extensions import connection as Con
from django.utils.crypto import get_random_string
import time

op_code: str = sys.argv[1]
population: int = int(sys.argv[2])

connection: Con = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)
chunk_size: int = 10000
with connection:
	cursor = connection.cursor()
	if op_code == "A18":
		cursor.execute("CREATE TABLE Tag (name varchar(255))")
		for i in range(population):
			print("populating {}/{}".format(i + 1, population))
			values: List[Dict[str, str]] = [
				{"name": get_random_string()} for i in range(chunk_size)
			]
			cursor.executemany(
				"INSERT INTO Tag (name) VALUES (%(name)s)", values
			)
			time.sleep(0.1)
		connection.commit()
