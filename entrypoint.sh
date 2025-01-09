#!/bin/bash

echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready."

alembic revision --autogenerate -m "Added the initial migration"

alembic upgrade head

exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload