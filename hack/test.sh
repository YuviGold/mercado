#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -o xtrace

python3 -m pytest --log-cli-level="${LOGLEVEL:-info}" -s --verbose "${TEST:-tests}" -k "${TEST_FUNC:-}"
