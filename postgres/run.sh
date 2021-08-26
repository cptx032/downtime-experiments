#!/usr/bin/env bash

populations=(1 10 100)
operations=(A18 A2 A12 A21 A1 A6 A10 A8 A13 A20 A7 A4 A24 A16 A5)

for population in "${populations[@]}"
do
	for operation in "${operations[@]}"
	do
		echo $population $operation
		bash start_benchmark.sh $operation $population Tag
	done
done