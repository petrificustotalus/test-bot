# Use Python 3.12-alpine as the base image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

RUN apk add --no-cache curl
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-interaction --no-ansi

COPY . /code/

# The entry point ("main.py")
CMD ["python", "main.py"]