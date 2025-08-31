#!/usr/bin/env bash
set -euo pipefail
mkdir -p threatmodel
if [ ! -f threatmodel/threatmodel.json ]; then
  echo "Run 'threatspec run' first to produce threatmodel/threatmodel.json"
  exit 1
fi
cp threatmodel/threatmodel.json threatmodel/baseline.json
echo "Initialized threatmodel/baseline.json"

