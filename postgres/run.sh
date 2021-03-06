#!/usr/bin/env bash

populations=(10 100 1000)
operations=(A18 A2 A12 A21 A1 A6 A10 A8 A13 A20 A7 A4 A24 A16 A5)

# READ
for population in "${populations[@]}"
do
	for operation in "${operations[@]}"
	do
		echo read $population $operation
		bash start_read_benchmark.sh $operation $population Tag
		sleep 10
	done
done

# WRITE
for population in "${populations[@]}"
do
	for operation in "${operations[@]}"
	do
		echo write $population $operation
		bash start_write_benchmark.sh $operation $population Tag
		sleep 10
	done
done

# INSERT
for population in "${populations[@]}"
do
	for operation in "${operations[@]}"
	do
		echo insert $population $operation
		bash start_insert_benchmark.sh $operation $population Tag
		sleep 10
	done
done

# DELETE
for population in "${populations[@]}"
do
	for operation in "${operations[@]}"
	do
		echo delete $population $operation
		bash start_delete_benchmark.sh $operation $population Tag
		sleep 10
	done
done
