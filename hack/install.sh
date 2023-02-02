#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

python -m pip install --verbose --force-reinstall ./dist/mercado-*.whl
