# T21 – Secrets Canarying & Exfiltration Detection

## 🎯 Objective
Deploy honeytokens (fake credentials) and detect unauthorized use.

## 🛠️ Deliverables
- Generate honeytoken AWS keys via script.
- Store in a non-critical location (repo, logs, env).
- Trigger CloudTrail alert if used.
- Document alerting pipeline.

## 🚀 Steps
1. Implement `scripts/generate_honeytoken.py` to create fake AWS creds.
2. Configure `cloudtrail/alert.yaml` to detect their use.
3. Add CI to ensure script runs and JSON format is valid.
4. Document setup + test.

## ✅ Validation
- Fake creds generated.
- CloudTrail detects use.
- Alert documented.
