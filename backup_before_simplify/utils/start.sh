#!/bin/bash

# Production startup script
set -e

echo "Starting Job Scheduler API..."

# Wait for database to be ready
echo "Waiting for database..."
python -c "
import time
import psycopg2
from config import settings

while True:
    try:
        conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db
        )
        conn.close()
        print('Database is ready!')
        break
    except psycopg2.OperationalError:
        print('Database not ready, waiting...')
        time.sleep(2)
"

# Wait for Redis to be ready
echo "Waiting for Redis..."
python -c "
import time
from redis_config import redis_manager

while True:
    try:
        if redis_manager.health_check():
            print('Redis is ready!')
            break
        else:
            print('Redis not ready, waiting...')
            time.sleep(2)
    except Exception:
        print('Redis not ready, waiting...')
        time.sleep(2)
"

# Run database migrations (if using Alembic)
# alembic upgrade head

# Start the application
echo "Starting application..."
exec gunicorn app:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-logfile - \
    --error-logfile - \
    --log-level info
