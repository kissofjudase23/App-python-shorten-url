
.PHONY: build up down start restart stop redis mysql shorten_url gunicorn_dev

service_name=py-shorten-url
compose_file=./deployments/docker-compose.yml
pytest_cfg=./configs/pytest.ini

# Set up editor env
# pyenv version 3.8.5
# pipenv shell
# pip install -r requirements.txt

build:
	docker-compose -f $(compose_file) -p $(service_name) build

clean_cache:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf && \
	rm -rf ./htmlcov

test: clean_cache
	pytest --pyargs -v ./shorten_url -c $(pytest_cfg)

ut_cov: clean_cache
	pytest --pyargs -c $(pytest_cfg) --cov=./shorten_url --cov-config=./configs/pytest_conveage.ini --cov-report=html

lint:
	flake8 ./shorten_url

black:
	python -m black shorten_url

up:
	docker-compose -f $(compose_file) -p $(service_name) --env-file  up  up -d

down:
	docker-compose -f $(compose_file) -p $(service_name) down

downv:
	docker-compose -f $(compose_file) -p $(service_name) down --volumes

start:
	docker-compose -f $(compose_file) -p $(service_name) start

restart:
	docker-compose -f $(compose_file) -p $(service_name) restart

stop:
	docker-compose -f $(compose_file) -p $(service_name) stop

clean:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf && \
	rm -rf ./htmlcov

ut_dev: clean_cache
	pytest --pyargs -v ./shorten_url -c ./tests/pytest.ini

ut_redis:
	pytest --pyargs -vvx ./shorten_url -c $(pytest_cfg) -m redis

ut_mysql:
	pytest --pyargs -vvx ./shorten_url -c $(pytest_cfg) -m mysql

ut_usecase:
	pytest --pyargs -vvx ./shorten_url -c $(pytest_cfg) -m use_cases

ut_user_usecase:
	pytest --pyargs -vvx ./shorten_url -c $(pytest_cfg) -m user_usecases

ut_url_usecase:
	pytest --pyargs -vvx ./shorten_url -c $(pytest_cfg) -m url_usecases

login:
	docker exec -it $(service_name) bash

login_mysql:
	mysql -h 127.0.0.1 -P 3306 -uroot -pq

login_redis:
	redis-cli -h 127.0.0.1 -p 6379

flask_dev:
	env FLASK_APP='shorten_url:create_app()' FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=8080

gunicorn_dev:
	gunicorn -w 1 -b 0.0.0.0:8080 -k gevent 'shorten_url:create_app()'
