#!/usr/bin/env bash
set -euo pipefail
REPORT="$1"
THRESH="$2"
violations=$(jq '.violations | length' "$REPORT" 2>/dev/null || echo 0)
if [[ "$violations" -gt 0 ]]; then
  echo "Compliance policy violated: $violations items"
  jq '.violations' "$REPORT" || true
  exit 1
else
  echo "No violations; continuing."
fi

