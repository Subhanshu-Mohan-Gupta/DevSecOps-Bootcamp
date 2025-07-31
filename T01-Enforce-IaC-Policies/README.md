# Task 1: Enforce Security Policies in Infrastructure-as-Code (IaC)

## Objective
Validate Terraform code against security policies (e.g., no public S3, encryption enabled) using policy-as-code tools like OPA or Sentinel.

## Tools & Setup
- Terraform
- Open Policy Agent (OPA) + Conftest or Sentinel

## Steps
1. Write Rego policies to enforce best practices.
2. Use `conftest test` or equivalent to scan .tf files.
3. Integrate the policy test in CI pipeline.
4. Block PRs/merges if violations are found.

## Deliverables
- Rego policy files
- CI output demonstrating enforcement
- Violation and pass report
