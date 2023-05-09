#!/bin/bash
echo "Starting Rasa server..."
rasa run --enable-api &

echo "Starting Django server..."
python manage.py runserver
