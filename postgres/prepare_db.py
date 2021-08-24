# prepare_db.py

from typing import List, Dict

import random
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
    with connection.cursor() as cursor:
        if op_code in ("A18", "A2"):
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
        #add fk
        elif op_code == "A12":
            cursor.execute("CREATE TABLE Subtag (name varchar(255), id serial primary key)")
            cursor.execute("CREATE TABLE Tag (name varchar(255), subtag_id integer)")
            cursor.executemany(
                "INSERT INTO Subtag (name) VALUES (%(name)s)", [
                    {"name":  get_random_string()}
                    for i in range(3)
                ]
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values: List[Dict[str, str]] = [
                    {
                        "name": get_random_string(),
                        "subtag_id": random.choice([1, 2, 3])
                    }
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, subtag_id) VALUES (%(name)s, %(subtag_id)s)", values
                )
                time.sleep(0.1)
