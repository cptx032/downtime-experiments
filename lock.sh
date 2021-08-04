#!/usr/bin/env bash

export READ_LOG_PATH="./read-log.txt"
export PY_EXE=$(which python)

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

start_migration() {
	echo fixme
}


# fixme
# drop database
# create database
# git checkout $1
start_server
start_read_client
# 10s of normal execution
sleep 10
echo "START MIGRATION" >> $READ_LOG_PATH
start_migration
echo "END MIGRATION" >> $READ_LOG_PATH

stop_server
stop_read_client
