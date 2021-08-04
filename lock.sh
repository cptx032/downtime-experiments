#!/usr/bin/env bash

export READ_LOG_PATH="./read-log-$2.txt"
export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

start_server() {
	# no reload is to avoid stop server when doing git checkout
	# once this not happens when using supervisor + gunicorn
	# at the same time, the "no reload" option make possible to kill
	# the django server with only the PDI, because Django normally creates
	# many subprocess
    $PY_EXE ./manage.py runserver --noreload &
    export SERVER_PID=$!
    echo Sleeping 5s
    sleep 5
}
stop_server() {
    kill -9 $SERVER_PID
}

start_read_client() {
	$PY_EXE ./read-client.py $READ_LOG_PATH &
    export READ_CLIENT_PID=$!
    sleep 1
}
stop_read_client() {
	kill -9 $READ_CLIENT_PID
}


git checkout main
echo "Setting up database"
sudo -u postgres psql -c "drop database downtimes;"
sudo -u postgres psql -c "create database downtimes;"

echo "Initial Migration"
$PY_EXE ./manage.py migrate

echo Populating
$PY_EXE ./manage.py populate $2

echo Starting Server
start_server

echo "Checkout branch"
git checkout $1
start_read_client
# 10s of normal execution
sleep $NORMAL_AVG_RESPONSE_WINDOW
echo "START MIGRATION"
echo "START MIGRATION" >> $READ_LOG_PATH
$PY_EXE ./manage.py migrate
echo "END MIGRATION"
echo "END MIGRATION" >> $READ_LOG_PATH

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_server
stop_read_client
