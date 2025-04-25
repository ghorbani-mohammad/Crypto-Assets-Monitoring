#!/bin/sh

# Remove PID file if it exists
if [ -f /tmp/celeryd.pid ]; then
  echo "Removing stale PID file..."
  rm /tmp/celeryd.pid
fi

# Change to the correct working directory
cd /app/crypto_assets

# Start Celery Beat
celery -A crypto_assets beat -l info --pidfile=/tmp/celeryd.pid
