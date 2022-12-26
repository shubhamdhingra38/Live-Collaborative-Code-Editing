#!/bin/bash

echo "Running migrations..."
python3 manage.py migrate

echo "Starting server..."
daphne core.asgi:application --port 8000 --bind 0.0.0.0 -v2
