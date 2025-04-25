#!/bin/sh

# Remove PID file if it exists
if [ -f /tmp/celeryd.pid ]; then
  echo "Removing stale PID file..."
  rm /tmp/celeryd.pid
fi

# Start Celery Beat
celery -A crypto_assets beat -l info --pidfile=/tmp/celeryd.pid
