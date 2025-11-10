#!/bin/bash
pkill gunicorn || true
pwd
git pull 
source .venv/bin/activate 
gunicorn -D -b 0.0.0.0:8000 app:app

exit 0