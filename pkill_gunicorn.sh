#!/bin/bash
PIDFILE="/home/Ayiadomboakye/sakila-db-api/gunicorn.pid"

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    
    if [[ "$PID" =~ ^[0-9]+$ ]]; then
        if kill -0 "$PID" 2>/dev/null; then
            echo "Killing Gunicorn process (PID: $PID)..."
            kill "$PID"
            sleep 1
            rm -f "$PIDFILE"
            echo "Gunicorn process terminated."
        else
            echo "No running process found for PID $PID. Removing stale PID file."
            rm -f "$PIDFILE"
        fi
    else
        echo "Invalid PID in file. Removing it."
        rm -f "$PIDFILE"
    fi
else
    echo "No Gunicorn PID file found. Nothing to kill."
fi

exit 0