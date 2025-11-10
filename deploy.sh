#!/bin/bash
pkill gunicorn || true
cd ./sakila-db-api
git pull 
source .venv/bin/activate 
gunicorn -D -b 0.0.0.0:8000 app:app

exit 0