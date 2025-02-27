FROM python:3.13

RUN apt-get update && apt-get install -y --no-install-recommends shellcheck

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  PATH="${PATH}:${HOME}/root/.mercado"

# Workaround for using different users
RUN git config --global --add safe.directory '*'

WORKDIR /app
COPY README.md Makefile poetry.lock pyproject.toml /app/
COPY hack/deps.sh /app/hack/deps.sh

RUN --mount=type=cache,mode=0777,target=$POETRY_CACHE_DIR \
    make deps
