FROM python:3.11 AS test

# Set the working directory in the container
WORKDIR /app

RUN apt-get update

# Installation poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the pyproject.toml file to the container
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-interaction

# Set environment variables
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Declare the environment as development

WORKDIR /app


# # ------------------------------------------------------------------------

FROM test AS development
# Start the FastAPI app with auto-reload
CMD poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 4000 --reload

# # ------------------------------------------------------------------------

# Production stage
FROM python:3.11 AS production

# Set the working directory in the container
WORKDIR /app

RUN apt-get update

# Installation poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy the pyproject.toml file to the container
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-interaction

COPY . .

# Set environment variables
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Start the FastAPI app with no auto-reload
CMD poetry run alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 4000
