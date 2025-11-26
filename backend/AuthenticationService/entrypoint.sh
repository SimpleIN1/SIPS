#!/bin/sh

if [ "$MIGRATIONS" =  "1" ]
then
  /usr/src/app/venv/bin/python manage.py makemigrations
  /usr/src/app/venv/bin/python manage.py migrate
fi

exec "$@"