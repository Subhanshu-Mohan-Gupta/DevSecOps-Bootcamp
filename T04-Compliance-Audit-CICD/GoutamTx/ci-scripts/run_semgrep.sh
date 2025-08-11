#!/usr/bin/env bash
set -euo pipefail
OUT="$1"
semgrep --config auto --json --output "${OUT}" || true

