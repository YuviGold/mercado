#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

./setup.py bdist_wheel
