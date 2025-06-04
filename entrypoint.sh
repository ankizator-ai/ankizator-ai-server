#!/bin/sh

if [ "$RUN_MIGRATIONS" = "true" ]; then
echo 'Running migrations...'
python manage.py migrate
python manage.py loaddata api/fixtures/collections.json
fi

exec "$@"