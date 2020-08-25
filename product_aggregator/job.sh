#!/bin/sh
service cron start
python /app/manage.py runserver 0.0.0.0:8000