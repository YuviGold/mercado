#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

poetry run ruff format .
poetry run ruff check --fix-only .
