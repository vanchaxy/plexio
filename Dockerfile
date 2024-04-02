FROM node:18.2.0-alpine as build

WORKDIR /app

COPY frontend/package.json .

RUN npm install

COPY frontend .

RUN npm run build

FROM unit:1.32.1-python3.11

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY plexio plexio

RUN pip install -e . --no-cache-dir

COPY --from=build /app/build frontend

COPY unit-nginx-config.json /docker-entrypoint.d/config.json
