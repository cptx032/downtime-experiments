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
    # create index
    if op_code == "A18":
        cursor.execute("CREATE INDEX ON Tag ((name));")
        connection.commit()
    # add column
    elif op_code == "A2":
        cursor.execute("ALTER TABLE Tag ADD COLUMN new_column int default 0;")
        connection.commit()
    # add fk
    elif op_code == "A12":
        cursor.execute("ALTER TABLE Tag ADD CONSTRAINT subtag_id_fk FOREIGN KEY(subtag_id) REFERENCES Subtag(id) ON DELETE CASCADE;")
        connection.commit()
