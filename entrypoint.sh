#!/bin/bash
echo 'Waiting for postgres...'

while ! nc -z $DB_HOSTNAME $DB_PORT; do
    sleep 0.1
done

echo 'Running migrations...'
python manage.py migrate
python manage.py loaddata api/fixtures/sources.json

exec "$@"