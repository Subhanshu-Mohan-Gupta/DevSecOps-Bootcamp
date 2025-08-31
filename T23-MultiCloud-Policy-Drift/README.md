# T23 – Multi-Cloud Policy Drift Guard

## 🎯 Objective
Detect IAM policy drift across AWS & GCP vs baseline.

## 🛠️ Deliverables
- Export AWS + GCP IAM policies.
- Define baseline YAML rules.
- Run OPA / Conftest to check drift.
- Fail pipeline on drift.

## 🚀 Steps
1. Store exported AWS policies in `aws_policies/`.
2. Store exported GCP policies in `gcp_policies/`.
3. Define baseline in `baseline/`.
4. CI runs Conftest against both.
5. Document drift detection examples.

## ✅ Validation
- Drift detected when baseline mismatch.
- CI fails appropriately.
