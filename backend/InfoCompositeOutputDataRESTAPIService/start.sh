#!/bin/bash

/usr/src/app/venv/bin/gunicorn --timeout 600 --preload --workers 6 --bind 0.0.0.0:8000 api.app:app