# prepare_db.py

import argparse
import random
import time
from typing import Dict, List

import psycopg2
from django.utils.crypto import get_random_string
from psycopg2.extensions import connection as Con

number_of_columns: int = 30
columns_names: List[str] = [
    "_" + get_random_string() for i in range(number_of_columns)
]
columns_definition: str = ", ".join(
    ["{} varchar(255)".format(i) for i in columns_names]
)
values_dict: Dict[str, str] = {
    k: "{0}{0}".format(get_random_string()) for k in columns_names
}
cols_separated_by_comma: str = ", ".join(columns_names)
percent_format: str = ", ".join(["%({})s".format(i) for i in columns_names])


parser = argparse.ArgumentParser(
    description="Prepare the database to the subsequent DDL commands"
)
parser.add_argument("op_code", type=str, help="ddl category code")
parser.add_argument("population", type=int, help="populate argument")
args = parser.parse_args()

op_code: str = args.op_code
population: int = args.population

connection: Con = psycopg2.connect(
    "dbname='downtimes' user='postgres' host='127.0.0.1' password='master'"
)
chunk_size: int = 10000
with connection:
    with connection.cursor() as cursor:
        if op_code in ("A18", "A18n", "A2", "A2n", "A1", "A8"):
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values: List[Dict[str, str]] = [
                    {"name": get_random_string(), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
        # drop column
        elif op_code in ("A6", "A7"):
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), other_name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {
                        "name": get_random_string(),
                        "other_name": get_random_string(),
                        **values_dict,
                    }
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
        # add fk
        elif op_code in ("A12", "A12n"):
            cursor.execute(
                "CREATE TABLE Subtag (name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), subtag_id integer, id serial primary key, {})".format(
                    columns_definition
                )
            )
            cursor.executemany(
                "INSERT INTO Subtag (name, {}) VALUES (%(name)s, {})".format(
                    cols_separated_by_comma, percent_format
                ),
                [
                    {"name": get_random_string(), **values_dict}
                    for i in range(3)
                ],
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {
                        "name": get_random_string(),
                        "subtag_id": str(random.choice([1, 2, 3])),
                        **values_dict,
                    }
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, subtag_id, {}) VALUES (%(name)s, %(subtag_id)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
        # drop default value
        elif op_code == "A21":
            cursor.execute(
                "CREATE TABLE Tag (number_col int default 0, name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {"name": str(random.choice(range(1000))), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
        elif op_code == "A13":
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            connection.commit()
            cursor.execute(
                "CREATE TABLE Subtag (subtag_id integer, {}, constraint fk_ foreign key(subtag_id) references Tag(id) )".format(
                    columns_definition
                )
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {"name": str(random.choice(range(1000))), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
        elif op_code == "A20":
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), other_column varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {"name": get_random_string(), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()

        elif op_code in ("A4", "A5"):
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), id serial primary key, {})".format(
                    columns_definition
                )
            )
            connection.commit()
            cursor.execute(
                "CREATE TABLE Subtag (subtag_id integer, {}, constraint fk_ foreign key(subtag_id) references Tag(id) )".format(
                    columns_definition
                )
            )
            connection.commit()
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {"name": str(random.choice(range(1000))), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                connection.commit()
                values = [
                    {
                        "subtag_id": str(random.choice(range(1, 1000))),
                        **values_dict,
                    }
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Subtag (subtag_id, {}) VALUES (%(subtag_id)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                connection.commit()
                time.sleep(0.1)
            connection.commit()
        # drop not null constraint
        elif op_code == "A24":
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255) not null, id serial primary key, {})".format(
                    columns_definition
                )
            )
            connection.commit()
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {"name": get_random_string(), **values_dict}
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, {}) VALUES (%(name)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
        # add constraint
        elif op_code in ("A16", "A16n"):
            cursor.execute(
                "CREATE TABLE Tag (name varchar(255), number_col integer, id serial primary key, {})".format(
                    columns_definition
                )
            )
            connection.commit()
            for i in range(population):
                print("populating {}/{}".format(i + 1, population))
                values = [
                    {
                        "name": get_random_string(),
                        "number_col": str(random.choice(range(1000))),
                        **values_dict,
                    }
                    for i in range(chunk_size)
                ]
                cursor.executemany(
                    "INSERT INTO Tag (name, number_col, {}) VALUES (%(name)s, %(number_col)s, {})".format(
                        cols_separated_by_comma, percent_format
                    ),
                    values,
                )
                time.sleep(0.1)
            connection.commit()
