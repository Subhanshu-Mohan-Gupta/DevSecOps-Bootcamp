#!/usr/bin/env bash
set -euo pipefail
RAW_OUT="$1"
JSON_OUT="$2"

docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  --net host --pid host --cap-add audit_control \
  docker/docker-bench-security:latest > "${RAW_OUT}" 2>&1 || true

python - <<PY > "${JSON_OUT}"
import re, json
raw = open("${RAW_OUT}").read().splitlines()
results=[]
for line in raw:
    m = re.match(r'^\s*\[(?P<level>INFO|WARN|PASS|CRITICAL)\]\s*(?P<rest>.*)$', line)
    if m:
        results.append({"level": m.group("level"), "message": m.group("rest").strip()})
print(json.dumps({"results": results}, indent=2))
PY

