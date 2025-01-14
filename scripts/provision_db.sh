#!/usr/bin/env sh

SCRIPT_DIR=$(realpath $(dirname $0))
DATA_DIR=$SCRIPT_DIR/dev_data

. $SCRIPT_DIR/../.env

query="INSERT INTO vocabulary (english, korean, level) VALUES"
exec < $DATA_DIR/vocabulary.csv
read header
while IFS=";" read -r english korean level
do
    query="${query} ('${english}', '${korean}', ${level}),"
done 

query=${query%?}";"

echo $query

PGPASSWORD=$KV_PG_PASS psql -v -U $KV_PG_USER -d kovoc -p 5432 -h localhost -c "$query"
