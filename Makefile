
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

clean_cache:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf && \
	rm -rf ./htmlcov

ut_dev: clean_cache
	pytest --pyargs -vvx --pdb ./shorten_url -c ./tests/pytest.ini

ut_redis:
	pytest --pyargs -vvx ./shorten_url -c ./tests/pytest.ini -m redis

ut_mysql:
	pytest --pyargs -vvx ./shorten_url -c ./tests/pytest.ini -m mysql

ut_usecase:
	pytest --pyargs -vvx ./shorten_url -c ./tests/pytest.ini -m use_cases

ut_user_usecase:
	pytest --pyargs -vvx ./shorten_url -c ./tests/pytest.ini -m user_usecases

ut_url_usecase:
	pytest --pyargs -vvx ./shorten_url -c ./tests/pytest.ini -m url_usecases

ut: clean_cache
	pytest --pyargs -v ./shorten_url -c ./tests/pytest.ini

ut_cov: clean_cache
	pytest --pyargs -c ./tests/pytest.ini --cov=./shorten_url --cov-config=./tests/pytest_conveage.ini --cov-report=html

login_shorten_url:
	docker exec -it $(service_name) bash

login_mysql:
	mysql -h 127.0.0.1 -P ${DB_PORT} -u${DB_ROOT_USER} -p${DB_ROOT_PASSWORD}

login_redis:
	redis-cli -h 127.0.0.1 -p ${CACHE_PORT}

flask_dev:
	env FLASK_APP='shorten_url:create_app()' FLASK_DEBUG=1 flask run --host=${APP_HOST} --port=${APP_PORT}

gunicorn_dev:
	gunicorn -w 1 -b ${APP_HOST}:${APP_PORT} -k gevent 'shorten_url:create_app()'
