# Threshold Policy – Vulnerability Blocking in CI/CD

## Policy Statement
The CI/CD pipeline must fail if:
- Any vulnerability is detected with CVSS v3 score ≥ 7.0.
- OR any vulnerability has severity marked as CRITICAL.

## Tools
- **Trivy** for scanning dependencies and container images.
- **Semgrep** for static code analysis.
- **Docker Bench Security** for image hardening.

## Implementation
- Scan results stored as `trivy-report.json`.
- Enforced via `fail-on-threshold.sh` script:
```bash
#!/bin/bash
THRESHOLD=7.0
REPORT="trivy-report.json"

VIOLATIONS=$(jq --argjson threshold "$THRESHOLD" \
  '.Results[].Vulnerabilities[]? | select(.CVSS?.nvd?.V3Score >= $threshold) | .VulnerabilityID' \
  "$REPORT")

if [ -n "$VIOLATIONS" ]; then
    echo "❌ Vulnerabilities exceeding CVSS $THRESHOLD found:"
    echo "$VIOLATIONS"
    exit 1
else
    echo "✅ No vulnerabilities exceeding CVSS $THRESHOLD."
fi

