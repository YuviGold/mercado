FROM python:3.13

RUN apt-get update && apt-get install -y --no-install-recommends shellcheck

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  UV_CACHE_DIR=/tmp/uv_cache \
  PATH="${PATH}:${HOME}/root/.mercado"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Workaround for using different users
RUN git config --global --add safe.directory '*'

WORKDIR /app
COPY Makefile uv.lock pyproject.toml README.md /app/
COPY hack/deps.sh /app/hack/deps.sh

RUN --mount=type=cache,mode=0777,target=$UV_CACHE_DIR \
    make deps
