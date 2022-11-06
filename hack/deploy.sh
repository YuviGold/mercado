#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

# python -m twine upload --verbose dist/*
poetry publish
