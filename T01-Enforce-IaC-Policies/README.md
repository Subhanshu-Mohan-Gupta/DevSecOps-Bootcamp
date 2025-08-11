# Enforce IaC Policies with Terraform and OPA

This project demonstrates how to enforce security and compliance policies on Infrastructure as Code (IaC) using Terraform, [Open Policy Agent (OPA)](https://www.openpolicyagent.org/), and [Conftest](https://www.conftest.dev/). It includes sample AWS resources, policy definitions in Rego, and a CI workflow for automated policy checks.

---

## Project Structure

```
.
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── policy/
│   ├── ec2_security.rego
│   └── s3_security.rego
└── terraform/
    ├── ec2.tf
    ├── outputs.tf
    ├── providers.tf
    ├── s3.tf
    └── variables.tf
```

### File/Folder Overview

- **README.md**  
  Project documentation and instructions.

- **.github/workflows/ci.yml**  
  GitHub Actions workflow for CI/CD. It runs Terraform commands and Conftest policy checks on every push or pull request.

- **policy/**  
  Contains OPA Rego policy files for security and compliance checks.
  - `ec2_security.rego`: Policies for EC2 instances (e.g., required tags, monitoring, encryption).
  - `s3_security.rego`: Policies for S3 buckets (e.g., public ACLs, versioning, required tags).

- **terraform/**  
  Terraform configuration for AWS resources.
  - `providers.tf`: Specifies the AWS provider and region.
  - `variables.tf`: Input variables for customizing the deployment.
  - `ec2.tf`: Defines EC2 instances with various compliance scenarios.
  - `s3.tf`: Defines S3 buckets with different ACLs, tags, and versioning settings.
  - `outputs.tf`: Outputs for created resources (EC2 instance IDs, S3 bucket names).

---

## How It Works

1. **Terraform Configuration**  
   The `terraform/` directory contains sample AWS resources, some intentionally non-compliant for demonstration.

2. **Policy Enforcement**  
   The `policy/` directory contains Rego policies that define security and compliance rules for EC2 and S3 resources.

3. **CI/CD Integration**  
   The [ci.yml](.github/workflows/ci.yml) workflow:
   - Initializes and validates Terraform.
   - Generates a Terraform plan in JSON format.
   - Runs Conftest to test the plan against the policies.
   - Uploads a policy report as a workflow artifact.

---

## Usage

### Prerequisites

- [Terraform](https://www.terraform.io/) >= 1.5.0
- [Conftest](https://www.conftest.dev/) >= 0.52.0
- AWS credentials configured (for actual deployment)

### Steps

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd T01-Enforce-IaC-Policies/terraform
   ```

2. **Initialize Terraform**
   ```sh
   terraform init
   ```

3. **Validate Terraform**
   ```sh
   terraform validate
   ```

4. **Create a Terraform plan**
   ```sh
   terraform plan -out=plan.tfplan
   terraform show -json plan.tfplan > plan.json
   ```

5. **Run Conftest policy checks**
   ```sh
   conftest test plan.json --policy ../policy/
   ```

6. **Review the output**
   - Any policy violations will be reported in the CLI and in the `policy-report.txt` artifact (if using CI).

---

## Policies Overview

### EC2 Policies ([policy/ec2_security.rego](policy/ec2_security.rego))
- Monitoring must be enabled.
- Only `t3.*` or `t4g.*` instance types allowed.
- Required tags: `Environment`, `Owner`, `Project`.
- Root volume must be encrypted.

### S3 Policies ([policy/s3_security.rego](policy/s3_security.rego))
- No public ACLs (`public-read`, `public-read-write`).
- Versioning must be enabled.
- Required tag: `Environment`.

---

## CI/CD

The workflow in [.github/workflows/ci.yml](.github/workflows/ci.yml) automates the above steps on every push or pull request, ensuring that all Terraform changes are compliant with the defined policies.

---
