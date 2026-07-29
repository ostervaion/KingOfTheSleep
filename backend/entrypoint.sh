#!/bin/sh
set -e

if [ -f /run/secrets/postgres_password ]; then
    export POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password)
fi
if [ -f /run/secrets/postgres_user ]; then
    export POSTGRES_USER=$(cat /run/secrets/postgres_user)
fi
if [ -f /run/secrets/secret_key ]; then
    export SECRET_KEY=$(cat /run/secrets/secret_key)
fi

exec "$@"