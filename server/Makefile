install:
	poetry install

run-local:
	poetry run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload --reload-dir . --log-config=log_config.ini --log-level=debug

build:
	poetry run docker compose -f docker-compose.yml build

start:
	poetry run docker compose -f docker-compose.yml up --force-recreate --remove-orphans

up:
	poetry run docker compose -f docker-compose.yml up --force-recreate --remove-orphans -d

stop:
	poetry run docker-compose -f docker-compose.yml stop

rm:
	poetry run docker-compose -f docker-compose.yml rm
	sudo rm -rf db

lint:
	poetry run flake8
	poetry run mypy -p src --cache-dir=/dev/null --config-file=pyproject.toml
	poetry run mypy -p tests --cache-dir=/dev/null --config-file=pyproject.toml
