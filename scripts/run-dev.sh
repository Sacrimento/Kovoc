#!/usr/bin/env sh

uv pip sync requirements/requirements-dev.txt

docker stop postgresql
docker rm postgresql
docker run -itd -e POSTGRES_USER=kovoc -e POSTGRES_PASSWORD=xxxsecurexxx -p 5432:5432 --name postgresql postgres
alembic upgrade head

uvicorn kovoc.app:app --reload
