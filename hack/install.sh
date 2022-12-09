#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

pip install --force-reinstall ./dist/mercado-*.whl
