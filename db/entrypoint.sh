#!/bin/sh
set -e

if [ -f /run/secrets/postgres_password ]; then
    export POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password)
fi
if [ -f /run/secrets/postgres_user ]; then
    export POSTGRES_USER=$(cat /run/secrets/postgres_user)
fi

exec docker-entrypoint.sh "$@"