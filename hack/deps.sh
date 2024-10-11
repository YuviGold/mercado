#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

if [ ! -x "$(command -v poetry)" ]; then
    python3 -m pip install "poetry==1.8.3"
    poetry config virtualenvs.create false
fi

poetry install --verbose --no-interaction --no-ansi
