# migrate.py

import sys

import psycopg2
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
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT subtag_id_fk FOREIGN KEY(subtag_id) REFERENCES Subtag(id) ON DELETE CASCADE;"
        )
        connection.commit()
    # drop default value
    elif op_code == "A21":
        cursor.execute("ALTER TABLE Tag alter column number_col drop default;")
        connection.commit()
    # add table
    elif op_code == "A1":
        cursor.execute(
            "CREATE TABLE Subtag (subtag_id integer, constraint fk_ foreign key(subtag_id) references Tag(id) )"
        )
        connection.commit()
    # drop column
    elif op_code == "A6":
        cursor.execute("ALTER TABLE Tag DROP COLUMN other_name;")
        connection.commit()
    elif op_code == "A8":
        cursor.execute("ALTER TABLE Tag ALTER COLUMN name type varchar(255);")
        connection.commit()
    elif op_code == "A13":
        cursor.execute("ALTER TABLE Subtag drop constraint fk_;")
        connection.commit()
    elif op_code == "A20":
        cursor.execute(
            "ALTER TABLE Tag alter column other_column set default 'default value';"
        )
        connection.commit()
    elif op_code == "A7":
        cursor.execute("ALTER TABLE Tag rename name to new_column_name;")
        connection.commit()
    elif op_code == "A4":
        cursor.execute("DROP TABLE Subtag;")
        connection.commit()
    elif op_code == "A24":
        cursor.execute("ALTER TABLE Tag ALTER COLUMN name drop not null;")
        connection.commit()
    elif op_code == "A16":
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT my_constraint CHECK (number_col <= 1000);"
        )
        connection.commit()
    elif op_code == "A5":
        cursor.execute("ALTER TABLE Subtag RENAME TO NewTableName;")
        connection.commit()
