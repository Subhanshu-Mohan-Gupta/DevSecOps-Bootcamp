# T22 – Red vs Blue Chaos Pipeline

## 🎯 Objective
Simulate malicious insider actions (Red) and enforce defensive guardrails (Blue).

## 🛠️ Deliverables
- Red pipeline (`red.yml`) that tampers with scanning results.
- Blue pipeline (`blue.yml`) that detects tampering using checksums / signatures.
- Sigstore / Cosign used for artifact attestations.
- Document attack vs defense outcomes.

## 🚀 Steps
1. Implement `.github/workflows/red.yml` → simulate scanner bypass.
2. Implement `.github/workflows/blue.yml` → validate integrity.
3. Store generated attestation in `attestations/`.
4. Document “attack succeeded until defense blocked it.”

## ✅ Validation
- Red job produces tampered artifact.
- Blue job detects and blocks merge.
- Attestation JSON generated.
