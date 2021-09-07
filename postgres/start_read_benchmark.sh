#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export READ_TABLE_NAME=$3

export READ_LOG_PATH="./read-log-$OP_DB_CODE-$POPULATION_PARAM.txt"
export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

start_read_client() {
	$PY_EXE ./read-client.py $READ_LOG_PATH $READ_TABLE_NAME &
    export READ_CLIENT_PID=$!
    sleep 1
}
stop_read_client() {
	kill -9 $READ_CLIENT_PID
}


echo Cleaning log file
echo "" > $READ_LOG_PATH
echo "Setting up database"
sudo -u postgres psql -c "drop database downtimes;"
sudo -u postgres psql -c "create database downtimes;"

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

# after the checkout the application is still running the old version
start_read_client
echo Read Client Started!
# while this script is stopped because this sleep the read-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW
echo "START MIGRATION" $(date --iso-8601=ns)
echo "START MIGRATION" $(date --iso-8601=ns) >> $READ_LOG_PATH
$PY_EXE ./migrate.py $OP_DB_CODE
echo "END MIGRATION" $(date --iso-8601=ns)
echo "END MIGRATION" $(date --iso-8601=ns) >> $READ_LOG_PATH

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_read_client
