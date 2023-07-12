# Saline Academy Backend

## Prerequisites

- `git clone` the repo using SSH
- install `pyenv`
- install `poetry`, see instructions [here](https://python-poetry.org/docs/#installation)
- create `development.env` file in the root of the project (More info further down)

### Pyenv debug

If the version of python (via `python -V`) is the the same of the version selected with pyenv (via `pyenv local`), check that the path of your python runtime is set to pyenv's shims directory (via `which python`).

### Env file Structure
.env
```TOML
# Databese
DATABASE_HOST = ""
POSTGRES_USER = ""
POSTGRES_PASSWORD = ""
POSTGRES_HOSTNAME = ""
POSTGRES_PORT = ""
POSTGRES_DB = ""

# S3
SCALITY_ACCESS_KEY_ID=
SCALITY_SECRET_ACCESS_KEY=
S3_HOSTNAME=
S3_PORT=
BUCKET_NAME=

# Hash keys
RESET_TOKEN_KEY=""
JWT_PRIVATE_KEY=""

# External keys
SENDGRID_API_KEY=""
# MEILISEARCH_MASTERKEY =""
```

s3-config/credentials
```TOML
[default]
aws_access_key_id=
aws_secret_access_key=
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
