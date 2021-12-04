#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export WRITE_TABLE_NAME=$3
export NUM_CLIENTS=$4

# array with read clients PIDs
export WRITE_CLIENT_PIDS=()

if [ -z $NUM_CLIENTS ]
then
    export NUM_CLIENTS=1
fi

export WRITE_LOG_PATH="./write-log-$OP_DB_CODE-$POPULATION_PARAM"

export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10

setup_database() {
    echo "Setting up database"
    sudo -u postgres psql -c "drop database downtimes;"
    sudo -u postgres psql -c "create database downtimes;"
}

start_write_client() {
    for i in `seq $NUM_CLIENTS`
    do
        # if we have more than one write-client so the log is suffixed with an ID
        export WRITELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            WRITELOG_SUFFIX="-${i}"
        fi
        $PY_EXE ./write-client.py "${WRITE_LOG_PATH}${WRITELOG_SUFFIX}.txt" $WRITE_TABLE_NAME name $POPULATION_PARAM &
        WRITE_CLIENT_PIDS+=($!)
    done
    sleep 1
    echo Write Client Started!
}

stop_write_client() {
    for client_pid in "${WRITE_CLIENT_PIDS[@]}"
    do
        kill -9 $client_pid
    done
    echo Write Client Stopped!
}


create_empty_log_files() {
    echo Cleaning log file
    for i in `seq $NUM_CLIENTS`
    do
        export WRITELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            WRITELOG_SUFFIX="-${i}"
        fi
        echo "" > "${WRITE_LOG_PATH}${WRITELOG_SUFFIX}.txt"
    done
}


register_migration() {
    echo $1 $(date --iso-8601=ns)
    for i in `seq $NUM_CLIENTS`
    do
        export WRITELOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            WRITELOG_SUFFIX="-${i}"
        fi
        echo $1 $(date --iso-8601=ns) >> "${WRITE_LOG_PATH}${WRITELOG_SUFFIX}.txt"
    done
}

setup_database

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

create_empty_log_files
start_write_client
# while this script is stopped because this sleep the write-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW
register_migration "START MIGRATION"
$PY_EXE ./migrate.py $OP_DB_CODE
register_migration "END MIGRATION"

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_write_client
