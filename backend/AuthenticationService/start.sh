#!/bin/sh


if [ "$DEBUG" = "1" ]
then
  /usr/src/app/venv/bin/python manage.py runserver 0.0.0.0:8000
else
  /usr/src/app/venv/bin/gunicorn --timeout 600 --preload --workers 6 --bind 0.0.0.0:8000 AccountProject.wsgi:application -e WSGI_FULL_INIT=1 -e WSGI_FULL_INIT_CLOSE_CONNECTIONS=1
fi