# T19 – Zero-Trust GitHub Actions Workflows

## 🎯 Objective
Eliminate static secrets in CI/CD by implementing GitHub → AWS OIDC federation.

## 🛠️ Deliverables
- Configure AWS IAM role with trust policy for GitHub OIDC
- Deploy sample Lambda via GitHub Actions (no PATs or keys)
- Prove pipeline runs with zero static secrets
- Detect if anyone reintroduces secrets

## 🚀 Steps
1. Write Terraform in `infra/` to create IAM role + OIDC provider.
2. Add `scripts/configure_oidc.sh` to bootstrap trust policy.
3. Update `.github/workflows/ci.yml` to use OIDC → AWS.
4. Validate: remove all `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` from secrets.

## ✅ Validation
- Workflow passes and deploys Lambda.
- PR introducing static AWS creds fails.
