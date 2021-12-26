#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export DELETE_TABLE_NAME=$3
export NUM_CLIENTS=$4

# array with delete clients PIDs
export DELETE_CLIENT_PIDS=()

if [ -z $NUM_CLIENTS ]
then
    export NUM_CLIENTS=1
fi

export DELETE_LOG_PATH="./delete-log-$OP_DB_CODE-$POPULATION_PARAM"

export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

setup_database() {
    echo "Setting up database"
    sudo -u postgres psql -c "drop database downtimes;"
    sudo -u postgres psql -c "create database downtimes;"
}

start_delete_client() {
    for i in `seq $NUM_CLIENTS`
    do
        # if we have more than one write-client so the log is suffixed with an ID
        export DELETELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            DELETELOG_SUFFIX="-${i}"
        fi
        $PY_EXE ./delete-client.py "${DELETE_LOG_PATH}${DELETELOG_SUFFIX}.txt" $DELETE_TABLE_NAME $POPULATION_PARAM &
        DELETE_CLIENT_PIDS+=($!)
    done
    sleep 1
    echo Delete Client Started!
}

stop_delete_client() {
    for client_pid in "${DELETE_CLIENT_PIDS[@]}"
    do
        kill -9 $client_pid
    done
    echo Delete Client Stopped!
}


create_empty_log_files() {
    echo Cleaning log file
    for i in `seq $NUM_CLIENTS`
    do
        export DELETELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            DELETELOG_SUFFIX="-${i}"
        fi
        echo "" > "${DELETE_LOG_PATH}${DELETELOG_SUFFIX}.txt"
    done
}


register_migration() {
    echo $1 $(date --iso-8601=ns)
    for i in `seq $NUM_CLIENTS`
    do
        export DELETELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            DELETELOG_SUFFIX="-${i}"
        fi
        echo $1 $(date --iso-8601=ns) >> "${DELETE_LOG_PATH}${DELETELOG_SUFFIX}.txt"
    done
}

setup_database

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

create_empty_log_files
start_delete_client
# while this script is stopped because this sleep the write-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW
register_migration "START MIGRATION"
$PY_EXE ./migrate.py $OP_DB_CODE
register_migration "END MIGRATION"

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_delete_client
