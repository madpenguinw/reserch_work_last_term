FROM python:3.12.0-slim

RUN apt-get update && apt-get install -y git make && apt-get clean
RUN pip install --upgrade pip poetry --no-cache-dir

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

ENV PORT=8000

EXPOSE $PORT

ENTRYPOINT python -m server --host=0.0.0.0

