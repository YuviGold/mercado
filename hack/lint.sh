#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

poetry check
poetry lock --check
poetry run ruff check .
find . -name '*.sh' -type f -not -path "./.git/*" -exec shellcheck {} +
git diff --shortstat --exit-code
