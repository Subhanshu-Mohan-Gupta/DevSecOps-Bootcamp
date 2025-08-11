#!/usr/bin/env bash
set -euo pipefail
OUT="$1"
trivy fs --quiet --format json --output "${OUT}" . || true

