# Vulnerability Threshold Policy
- Fail pipeline if any vulnerability has CVSS score ≥ 7.0 (High or Critical)
- No `privileged` containers allowed
- Memory and CPU limits must be set on all containers
- Root filesystem must be mounted read-only
