# Automated Compliance Auditing in CI/CD

## Objective
Add a CI pipeline stage that performs static code analysis, dependency scan, and image hardening check.

## Tools & Setup
- Semgrep
- Trivy
- Docker Bench Security

## Steps
1. Run Semgrep for static code analysis.
2. Scan dependencies and container image with Trivy.
3. Run docker-bench-security and aggregate results.
4. Fail pipeline on critical vulnerabilities.

## Deliverables
- Pipeline YAML
- Compliance report (JSON or HTML)
- Threshold policy (CVSS score, etc.)
