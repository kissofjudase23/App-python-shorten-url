#!/bin/bash
set -x

# check and create all tables
python3 -m shorten_url.storages.mysql.db

# start the web services
gunicorn -c ./configs/gunicorn_cfg.py "shorten_url:create_app()"