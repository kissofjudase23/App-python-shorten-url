#!/bin/bash
set -x

# check and create all tables
python3 -m shorten_url.storages.mysql.db

# start the web services
gunicorn -c ./deployments/gunicorn/gunicorn_shorten_url.py "shorten_url:create_app()"