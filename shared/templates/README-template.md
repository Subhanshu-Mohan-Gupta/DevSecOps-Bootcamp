# DevSecOps Mentor Rubric

A standardized guide for mentors evaluating trainee submissions in the **DevSecOps-Bootcamp** repo.

---

## Scoring Key

| Score | Meaning                    |
|-------|---------------------------|
| **1** | Needs Improvement         |
| **2** | Adequate                  |
| **3** | Good                      |
| **4** | Excellent / Industry-grade|

---

## 1. General Criteria  
*(applies to every task)*

| Category              | What mentors look for                                                        | Score (1-4) | Comments |
|-----------------------|------------------------------------------------------------------------------|-------------|----------|
| **Technical Accuracy**| Correct tool usage, follows best practices                                   |             |          |
| **Security Focus**    | Clear application of security principles; risk identified & mitigated        |             |          |
| **Completeness**      | All required deliverables provided and demonstrably working                  |             |          |
| **Documentation**     | README / run-books are clear, concise; diagrams or workflow visuals included |             |          |
| **Presentation**      | Trainee can articulate *what*, *why*, and *how* they built their solution    |             |          |

---

## 2. Task-Specific Criteria

> **Mentors:** Fill in only for the task(s) present in the PR.

| Task ID | Key Evaluation Points | Score (1-4) | Comments |
|---------|-----------------------|-------------|----------|
| **T01 – Enforce Security Policies in IaC** | • Rego/Sentinel rules cover S3, SG, at-rest encryption<br>• CI blocks non-compliant code<br>• Violation & pass reports attached | | |
| **T02 – Runtime Threat Detection in K8s** | • Falco/Tracee deployed as DaemonSet<br>• Custom rules detect `kubectl exec`, anomalous traffic<br>• Alerts forwarded to Slack/Alertmanager | | |
| **T03 – Secrets Management & Rotation** | • Vault (or cloud equivalent) running HA<br>• Dynamic secrets injected via CSI/sidecar<br>• Rotation script triggers rolling restart with zero downtime | | |
| **T04 – Automated Compliance Auditing** | • Semgrep, Trivy & Docker-Bench integrated in CI<br>• HTML/JSON report aggregated<br>• Pipeline fails on critical findings with clear thresholds | | |
| **T06 – Chaos-Driven Security Testing** | • Chaos experiment files present & safe to run<br>• Detection and remediation validated automatically<br>• Pass/fail summary report included | | |
| **T13 – Secure Software Supply Chain** | • GPG commit signatures enforced<br>• Container images signed with Cosign<br>• SLSA provenance documented & verifiable | | |
| **T14 – Threat Modeling as Code** | • ThreatSpec/IriusRisk annotations meaningful<br>• Diagram auto-generated in CI<br>• High-severity threats mitigated | | |
| **T15 – AI-Powered PR Review** | • AI scanner runs on every PR<br>• Actionable comments, minimal noise<br>• False-positive analysis included | | |
| **T16 – Cloud Honeypot** | • Honeypot isolated (network & creds)<br>• Logs shipped to ELK/Loki<br>• Insights fed back into detection rules | | |
| **T17 – CVE Triage Automation** | • SBOM generated with Syft<br>• Grype scan + VEX filtering<br>• Jira tickets auto-created/closed accurately | | |
| **T18 – Kubernetes Policy-as-Code** | • Kyverno policies cover privilege, FS, labels<br>• Non-compliant workloads blocked<br>• Validation reports stored as artifacts | | |

---

## 3. Overall Evaluation

| Metric | Value |
|--------|-------|
| **Total Score (General + Task-Specific)** | **__/40** (adjust max if fewer tasks) |
| **Mentor Name** | |
| **Trainee Name** | |
| **Date** | |

---