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

## Amazon S3

Amazon S3 (Simple Storage Service) is a cloud-based object storage service provided by AWS. In our implementation, we use a third-party service called [Scality](https://www.scality.com/) hosted on docker.

Scality, which is hosted on Docker. Boto3, an AWS SDK for Python, is utilized to interact with the Scality service. You can find the boto3 documentation [here](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

### Storage Configuration

configure the Scality storage service, two files are required: the credentials file and the config file. The credentials file is used by boto3 to authenticate requests to the Scality service. The config file is used to set up the service with essential variables.

The important variables in the config file include:

- restEndpoints: the endpoint of the Scality service.
- SCALITY_ACCESS_KEY_ID and SCALITY_SECRET_ACCESS_KEY: the credentials necessary to authenticate requests. These credentials should be provided in both the config file and the project environment file.

### Connection

To connect to the Scality service, you need to create a boto3 client with the appropriate credentials and endpoint.

### Bucket

A bucket in the Scality service acts as a container for storing objects (files). You can create a bucket either through the config file or by using the boto3 client.

### Object

An object represents a file stored in a bucket. Objects in Scality are stored with various information and metadata, with the most important being the object key. The object key serves as a unique identifier for each object stored in a bucket. To enable querying of objects, the object key should be stored in our database.

Interacting with objects can be accomplished through various methods. To retrieve an object, a presigned URL is usually generated if the object is private, or a URL is constructed using the bucket name and object key. Object information (headers) can be obtained by querying the object key.

To upload an object, you need to provide the file and additional information such as the generated object key, the bucket, privacy settings (is_public), content type, metadata, etc.