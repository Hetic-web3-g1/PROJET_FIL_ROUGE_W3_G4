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
DATABASE_URL = # database_url (format: "postgresql+psycopg2://scott:tiger@localhost:5432")
MAIN_DATABASE_NAME = # ""
LOGS_DATABASE_NAME = # ""

RESET_TOKEN_KEY = # ""
JWT_PRIVATE_KEY = # ""

MEILISEARCH_MASTERKEY = # ""
SENDGRIP_API_KEY = # ""
```

## Install

```shell
pyenv install
poetry install
```

This will install the pythoin version for the project and create a python virtual environment and install all the dependencies.

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
