coverage-report:
	poetry run pytest tests --cov-report term-missing --cov=src -m "not integration" | grep TOTAL | egrep '\d+(?:\\.\\d+)?%' | awk '{print substr($$NF, 1, 2)}' > .tmp-report
	ls -a
	report=cat .tmp-report
	echo $report
	poetry run python scripts/coverage-shield.py generate echo $report > .cov-report.json
	rm .tmp-report


install-dependencies:
	poetry install

lint:
	poetry run flake8 src tests

unit-tests:
	poetry run pytest tests --cov-report term-missing --cov=src -m "not integration"

tests:
	poetry run pytest tests --cov-report term-missing --cov=src

dev:
	poetry run uvicorn src.main:app --port 8080 --reload