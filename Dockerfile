FROM python:3.11-alpine

WORKDIR /app

COPY plexio plexio
COPY pyproject.toml pyproject.toml

RUN pip install -e . --no-cache-dir
CMD uvicorn plexio.main:app --host 0.0.0.0 --port 7777