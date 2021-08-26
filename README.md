# how to run the postgres experiments
- `pip install psycopg2`
- create a postgres database named `downtimes` with `sudo -u postgres psql -c "CREATE DATABASE downtimes;"`
- run `./run.sh`

# Django project
- resolve o problema de:
	- que operações sempre vêm agregadas?

# downtime-experiments

## Operations to test
- A18 - Add index
	- two indexes are added if varchar: one normal for the column and another one for "LIKE" queries
- A2 - add column
	- not aggregated
- A12 - add fk
	- add column
	- create index (in the fk)
- A21 - drop column default value
	- none operations (the drop default was made in the creation of default)
- A1 - add table
	- add table
	- as many foreign keys in the table are created:
		- fk constraints
		- indexes in the fk columns
- A6 - drop column
	- drop column (all the dependencies are removed by the postgres, indexes, constraints)
- A10 - add pk
	- the primary key is together with table creation
	- the transformation of a column in primary key requires the drop of default ID column created by django
		- this means:
			- a drop
			- a column creation
			- a index creation
- A8 - change column data type
	- only the change data colun
- A13 - drop fk
	- onyl drop column
- A20 - add default value
	- none operations
- A7 - rename column
	- only the rename
- A4 - drop table
	- only drop table
- A24 - drop not null constraint
	- only drop
- A16 - add constraint
	- only constraint
- A5 - rename table
	- only rename
