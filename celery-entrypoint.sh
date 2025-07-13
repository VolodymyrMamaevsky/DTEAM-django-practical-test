#!/usr/bin/env bash

echo "Waiting for Django and Redis to be ready..."
sleep 10

echo "Starting Celery worker..."
exec celery -A CVProject worker --loglevel=info 