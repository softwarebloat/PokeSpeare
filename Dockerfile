FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN apt-get update && apt-get -y install curl

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
          ln -s $HOME/.poetry/bin/poetry /usr/bin/poetry && \
          poetry --version && \
          poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-interaction

COPY src/ ./

ENV PORT=8080