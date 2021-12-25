#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export WRITE_TABLE_NAME=$3
export NUM_CLIENTS=$4

# array with read clients PIDs
export INSERT_CLIENT_PIDS=()

if [ -z $NUM_CLIENTS ]
then
    export NUM_CLIENTS=1
fi

export INSERT_LOG_PATH="./insert-log-$OP_DB_CODE-$POPULATION_PARAM"

export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

setup_database() {
    echo "Setting up database"
    sudo -u postgres psql -c "drop database downtimes;"
    sudo -u postgres psql -c "create database downtimes;"
}

start_insert_client() {
    for i in `seq $NUM_CLIENTS`
    do
        # if we have more than one insert-client so the log is suffixed with an ID
        export INSERTLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            INSERTLOG_SUFFIX="-${i}"
        fi
        $PY_EXE ./insert-client.py "${INSERT_LOG_PATH}${INSERTLOG_SUFFIX}.txt" $WRITE_TABLE_NAME name &
        INSERT_CLIENT_PIDS+=($!)
    done
    sleep 1
    echo Insert Client Started!
}

stop_insert_client() {
    for client_pid in "${INSERT_CLIENT_PIDS[@]}"
    do
        kill -9 $client_pid
    done
    echo Insert Client Stopped!
}


create_empty_log_files() {
    echo Cleaning log file
    for i in `seq $NUM_CLIENTS`
    do
        export INSERTLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            INSERTLOG_SUFFIX="-${i}"
        fi
        echo "" > "${INSERT_LOG_PATH}${INSERTLOG_SUFFIX}.txt"
    done
}


register_migration() {
    echo $1 $(date --iso-8601=ns)
    for i in `seq $NUM_CLIENTS`
    do
        export INSERTLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            INSERTLOG_SUFFIX="-${i}"
        fi
        echo $1 $(date --iso-8601=ns) >> "${INSERT_LOG_PATH}${INSERTLOG_SUFFIX}.txt"
    done
}

setup_database

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

create_empty_log_files
start_insert_client
# while this script is stopped because this sleep the write-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW
register_migration "START MIGRATION"
$PY_EXE ./migrate.py $OP_DB_CODE
register_migration "END MIGRATION"

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_insert_client
