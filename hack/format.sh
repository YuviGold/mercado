#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

uv run ruff format .
uv run ruff check --fix-only .
