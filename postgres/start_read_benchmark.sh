#!/usr/bin/env bash

export OP_DB_CODE=$1
export POPULATION_PARAM=$2
export READ_TABLE_NAME=$3
export NUM_CLIENTS=$4

# array with read clients PIDs
export READ_CLIENT_PIDS=()

if [ -z $NUM_CLIENTS ]
then
    export NUM_CLIENTS=1
fi

export READ_LOG_PATH="./read-log-$OP_DB_CODE-$POPULATION_PARAM"

export PY_EXE=$(which python)
# how many seconds we will look before and after migration
export NORMAL_AVG_RESPONSE_WINDOW=10


start_locks_watcher() {
    $PY_EXE ./locks_watcher.py > locks.csv &
    export LOCKS_WATCHER_PID=$!
}

stop_locks_watcher() {
    kill -9 $LOCKS_WATCHER_PID
}

setup_database() {
    echo "Setting up database"
    sudo -u postgres psql -c "drop database downtimes;"
    sudo -u postgres psql -c "create database downtimes;"
}

start_read_client() {
    for i in `seq $NUM_CLIENTS`
    do
        # if we have more than one read-client so the log is suffixed with an ID
        export READLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            READLOG_SUFFIX="-${i}"
        fi
        $PY_EXE ./read-client.py "${READ_LOG_PATH}${READLOG_SUFFIX}.txt" $READ_TABLE_NAME &
        READ_CLIENT_PIDS+=($!)
    done
    sleep 1
    echo Read Client Started!
}
stop_read_client() {
    for client_pid in "${READ_CLIENT_PIDS[@]}"
    do
        kill -9 $client_pid
    done
    echo Read Client Stopped!
}

create_empty_log_files() {
    echo Cleaning log file
    for i in `seq $NUM_CLIENTS`
    do
        export READLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            READLOG_SUFFIX="-${i}"
        fi
        echo "" > "${READ_LOG_PATH}${READLOG_SUFFIX}.txt"
    done
}

register_migration() {
    echo $1 $(date --iso-8601=ns)
    for i in `seq $NUM_CLIENTS`
    do
        export READLOG_SUFFIX=""
        if [ $NUM_CLIENTS -gt 1 ]
        then
            READLOG_SUFFIX="-${i}"
        fi
        echo $1 $(date --iso-8601=ns) >> "${READ_LOG_PATH}${READLOG_SUFFIX}.txt"
    done
}


setup_database

echo "Initial Migration"
$PY_EXE ./prepare_db.py $OP_DB_CODE $POPULATION_PARAM

create_empty_log_files
start_locks_watcher
start_read_client
# while this script is stopped because this sleep the read-application is
# still running in the background
sleep $NORMAL_AVG_RESPONSE_WINDOW

register_migration "START MIGRATION"
$PY_EXE ./migrate.py $OP_DB_CODE
register_migration "END MIGRATION"

echo "Getting metrics after migration"
sleep $NORMAL_AVG_RESPONSE_WINDOW
stop_read_client
stop_locks_watcher
