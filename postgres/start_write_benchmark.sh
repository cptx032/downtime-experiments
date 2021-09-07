#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export WRITE_TABLE_NAME=$3

export WRITE_LOG_PATH="./write-log-$OP_DB_CODE-$POPULATION_PARAM.txt"
export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

start_write_client() {
	$PY_EXE ./write-client.py $WRITE_LOG_PATH $WRITE_TABLE_NAME name $POPULATION_PARAM &
    export WRITE_CLIENT_PID=$!
    sleep 1
}
stop_write_client() {
	kill -9 $WRITE_CLIENT_PID
}


echo Cleaning log file
echo "" > $WRITE_LOG_PATH
echo "Setting up database"
sudo -u postgres psql -c "drop database downtimes;"
sudo -u postgres psql -c "create database downtimes;"

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

# after the checkout the application is still running the old version
start_write_client
echo Write Client Started!
# while this script is stopped because this sleep the write-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW
echo "START MIGRATION" $(date --iso-8601=ns)
echo "START MIGRATION" $(date --iso-8601=ns) >> $WRITE_LOG_PATH
$PY_EXE ./migrate.py $OP_DB_CODE
echo "END MIGRATION" $(date --iso-8601=ns)
echo "END MIGRATION" $(date --iso-8601=ns) >> $WRITE_LOG_PATH

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_write_client
