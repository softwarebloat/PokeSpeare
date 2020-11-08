# development
install-dependencies:
	poetry install

lint:
	poetry run flake8 src tests

unit-tests:
	poetry run pytest tests --cov-report term-missing --cov=src -m "not integration"

all-tests:
	poetry run pytest tests --cov-report term-missing --cov=src

dev:
	poetry run uvicorn src.main:app --port 8080 --reload


# docker
docker-build:
	docker build -t pokeapi .

docker-run:
	docker run -ti --name pokeapi-container -p 8080:8080 pokeapi

docker-rm:
	docker rm pokeapi-container