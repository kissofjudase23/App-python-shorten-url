
include .env

.PHONY: build up down start restart stop tty redis mysql shorten_url gunicorn_dev

service_name=py-shorten-url
compose_file=./deployments/docker-compose.yml

build:
	env DOCKER_BUILDKIT=1 docker-compose -f $(compose_file) -p $(service_name) build

up:
	docker-compose -f $(compose_file) -p $(service_name) up -d

down:
	docker-compose -f $(compose_file) -p $(service_name) down

start:
	docker-compose -f $(compose_file) -p $(service_name) down

restart:
	docker-compose -f $(compose_file) -p $(service_name) restart

stop:
	docker-compose -f $(compose_file) -p $(service_name) down

shorten_url:
	docker exec -it $(service_name) bash

mysql:
	mysql -h 127.0.0.1 -P ${DB_PORT} -u${DB_ROOT_USER} -p${DB_ROOT_PASSWORD}

redis:
	redis-cli -h 127.0.0.1 -p ${CACHE_PORT}

flask_dev:
	env FLASK_APP='shorten_url:create_app()' FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=${APP_PORT}

gunicorn_dev:
	gunicorn -w 1 -b 0.0.0.0:${APP_PORT} -k gevent 'shorten_url:create_app()'
