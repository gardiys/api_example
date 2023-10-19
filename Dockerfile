FROM python:3.11.6-slim as base

ARG ENVIRONMENT="production"
ARG NEXUS_LOGIN=""
ARG NEXUS_PASSWORD=""

ENV DEBIAN_FRONTEND=noninteractive \
  TZ=Europe/Moscow \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONPATH=/var/install/api/ \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# setting timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# System deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3-dev \
    libpq-dev \
    build-essential \
    curl \
    git \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && pip install "poetry==$POETRY_VERSION"

WORKDIR /var/install/api
# Copy only requirements, to cache them in docker layer
COPY ./pyproject.toml ./poetry.lock /var/install/api/

# Project initialization:
RUN echo "$ENVIRONMENT" \
    && poetry --version \
    # Generating requirements.txt
    && poetry export --without-hashes -f requirements.txt -o /var/install/requirements.txt \
    && poetry install \
        $(if [ "$ENVIRONMENT" = 'production' ]; then echo '--no-dev'; fi) \
        --no-interaction --no-ansi \
        # Do not install the root package (the current project)
        --no-root \
    # Cleaning poetry installation's cache for production:
    && if [ "$ENVIRONMENT" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

# Setting up proper permissions:
RUN groupadd -r web && useradd -d /var/install/api -r -g web web \
    && chown web:web -R /var/install/api

# Running as non-root user:
USER web

COPY ./src/ /var/install/api/

CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "3000"]
