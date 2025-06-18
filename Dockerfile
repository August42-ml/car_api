FROM python:3.12-slim

RUN pip install poetry==2.1.3

WORKDIR /app

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY src .


 