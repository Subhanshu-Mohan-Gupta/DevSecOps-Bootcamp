#!/usr/bin/env bash
set -euo pipefail
OUT="$1"
IMAGE="${2:-}"
docker pull "$IMAGE" || true
trivy image --quiet --format json --output "${OUT}" "$IMAGE" || true

