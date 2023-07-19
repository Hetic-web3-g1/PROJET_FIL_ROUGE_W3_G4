# Saline Academy Backend

## Prerequisites

- `git clone` the repo using SSH
- install `pyenv`
- install `poetry`, see instructions [here](https://python-poetry.org/docs/#installation)
- create `development.env` file in the root of the project (More info further down)

### Pyenv debug

If the version of python (via `python -V`) is the the same of the version selected with pyenv (via `pyenv local`), check that the path of your python runtime is set to pyenv's shims directory (via `which python`).

### Env file Structure

```TOML
DATABASE_HOST = "postgres"
POSTGRES_USER = "changeme"
POSTGRES_PASSWORD = "changeme"
POSTGRES_HOSTNAME = "db-postgres"
POSTGRES_PORT = "5432"
POSTGRES_DB = "db_saline_royale"

# S3
SCALITY_ACCESS_KEY_ID=changeme
SCALITY_SECRET_ACCESS_KEY=changeme
S3_HOSTNAME=changeme
S3_PORT=changeme
BUCKET_NAME=changeme

# Hash keys
RESET_TOKEN_KEY="changeme"
JWT_PRIVATE_KEY="changeme"

# External keys
SENDGRID_API_KEY="changeme"

```

## Install

```shell
pyenv install
poetry install
```

This will install the python version for the project and create a python virtual environment and install all the dependencies.

## Run

Run the database with docker

```shell
docker run -d \
     --name saline-postgres \
     -e POSTGRES_PASSWORD=pgpassword \
     -e POSTGRES_USER=pguser \
     -e POSTGRES_DB=pgdb \
     -v saline-db:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:15.3
```

Run with VSCode debugger bu the running the configuration `Python: Saline Backend`, check that the python virtual environment is selected in the bottom right corner of VSCode.

## Migrations

```shell
alembic revision --autogenerate -m "<MESSAGE>"
alembic upgrade head
```
