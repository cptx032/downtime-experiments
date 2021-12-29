import argparse
import sys
import time

import psycopg2
from psycopg2.extensions import connection as Con

parser = argparse.ArgumentParser(description="Migrates the database schema")
parser.add_argument("op_code", type=str, help="DDL code")
args = parser.parse_args()

op_code: str = args.op_code

connection: Con = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)

# concurrent indexes cannot be created inside a transaction and the "with"
# keyword creates a transaction automatically, so A18n is created out of with
if op_code == "A18n":
    cursor = connection.cursor()
    connection.autocommit = True
    cursor.execute("CREATE INDEX CONCURRENTLY ON Tag ((name));")
    connection.commit()
    cursor.close()
    connection.close()
    sys.exit(0)
elif op_code == "A2n":
    default_value: int = 5
    cursor = connection.cursor()
    connection.autocommit = True
    cursor.execute("ALTER TABLE Tag ADD COLUMN new_column int DEFAULT NULL;")
    connection.commit()

    # in the insert situation we have the following problem:
    # while the script is looking for rows with new_column=null the insert
    # client is constantly inserting new rows, making the while loop infinite
    # this just can happen in a production environment. So we do:
    # - det as default value "null", in such way that postgres will lock
    # the table but, as we are using null as default value, this lock is very
    # fast in duration. After that, we change the default value to the real
    # default value, in this case, the value "5". This means that all the old
    # registers are null and the new registers will have the new default value
    # basically we defined a default value only for the new registers
    cursor.execute("ALTER TABLE Tag ALTER COLUMN new_column SET DEFAULT 5;")
    connection.commit()

    updated: int = -1
    count: int = 0
    while updated != 0:
        count += 1
        cursor.execute(
            "UPDATE Tag SET new_column=5 WHERE id IN (SELECT id FROM Tag WHERE new_column IS NULL LIMIT 50);"
        )
        connection.commit()
        updated = cursor.rowcount
        time.sleep(0.1)

    cursor.close()
    connection.close()
    sys.exit(0)
elif op_code == "A10n":
    cursor = connection.cursor()
    connection.autocommit = True
    cursor.execute(
        "CREATE UNIQUE INDEX CONCURRENTLY tag_unique_index ON Tag(other_name);"
    )
    connection.commit()

    cursor.execute(
        "ALTER TABLE Tag ADD CONSTRAINT tag_pk PRIMARY KEY USING INDEX tag_unique_index;"
    )
    connection.commit()
    cursor.close()
    connection.close()
    sys.exit(0)

with connection:
    cursor = connection.cursor()
    # create index
    if op_code == "A18":
        cursor.execute("CREATE INDEX ON Tag ((name));")
        connection.commit()
    elif op_code == "A2":
        cursor.execute("ALTER TABLE Tag ADD COLUMN new_column int default 0;")
        connection.commit()
    # add primary key
    elif op_code == "A10":
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT othernamepk PRIMARY KEY (other_name);"
        )
        connection.commit()
    # add fk
    elif op_code == "A12":
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT subtag_id_fk FOREIGN KEY(subtag_id) REFERENCES Subtag(id) ON DELETE CASCADE;"
        )
        connection.commit()
    elif op_code == "A12n":
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT subtag_id_fk FOREIGN KEY(subtag_id) REFERENCES Subtag(id) ON DELETE CASCADE NOT VALID;"
        )
        connection.commit()
        cursor.execute("ALTER TABLE Tag VALIDATE CONSTRAINT subtag_id_fk;")
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
        cursor.execute("ALTER TABLE Tag rename other_name to new_column_name;")
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
    elif op_code == "A16n":
        cursor.execute(
            "ALTER TABLE Tag ADD CONSTRAINT my_constraint CHECK (number_col <= 1000) NOT VALID;"
        )
        connection.commit()
        cursor.execute("ALTER TABLE Tag VALIDATE CONSTRAINT my_constraint;")
        connection.commit()
    elif op_code == "A5":
        cursor.execute("ALTER TABLE Subtag RENAME TO NewTableName;")
        connection.commit()
