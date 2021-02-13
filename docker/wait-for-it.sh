#!/bin/sh

set -e

host="$1"
shift
port="$1"
shift
user="$1"
shift
password="$1"
shift
database="$1"
shift
cmd="$@"

echo "Waiting for postgresql"
until pg_isready -h"$host" -U"$user" -p"$port" -d"$database"
do
  echo -n "."
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd
