#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

if [ ! -x "$(command -v uv)" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv sync --verbose --no-install-project
