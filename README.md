# 🚀 DevSecOps Bootcamp Repository

Welcome to the **DevSecOps Bootcamp** &mdash; a hands‑on training ground where you will harden code, pipelines, and infrastructure **one task at a time**.  Everything you need to succeed is right here: task folders, trackers, CI/CD guard‑rails, and detailed step‑by‑step guidance.

---
## 📚 Quick‑Glance Tracker

| ID  | Folder                               | Theme (🔑 focus)                    | Difficulty 
|-----|--------------------------------------|-------------------------------------|------------
| T01 | `T01-Enforce-IaC-Policies`           | Terraform + OPA / Sentinel          | ⚙️⚙️⚙️⚙️ 
| T02 | `T02-K8s-Runtime-Threat-Detection`   | Falco / Tracee, eBPF                | ⚙️⚙️⚙️⚙️ 
| T03 | `T03-Secrets-Management-Rotation`    | Vault, CSI driver, rotation scripts | ⚙️⚙️⚙️⚙️ 
| T04 | `T04-Compliance-Audit-CICD`          | Semgrep, Trivy, Docker Bench        | ⚙️⚙️⚙️⚙️ 
| T06 | `T06-Chaos-Security-Testing`         | Chaos Toolkit / LitmusChaos         | ⚙️⚙️⚙️⚙️⚙️ 
| T13 | `T13-Secure-Supply-Chain`            | SLSA, Cosign, in‑toto               | ⚙️⚙️⚙️⚙️ 
| T14 | `T14-Threat-Modeling-Code`           | ThreatSpec, PlantUML                | ⚙️⚙️⚙️ 
| T15 | `T15-AI-PR-Security-Review`          | DeepCode / Snyk Code                | ⚙️⚙️⚙️⚙️ 
| T16 | `T16-Cloud-Honeypot`                 | DVWA + Falco + ELK                  | ⚙️⚙️⚙️⚙️⚙️ 
| T17 | `T17-CVE-Triage-Automation`          | SBOM + Grype + Jira                 | ⚙️⚙️⚙️⚙️ 
| T18 | `T18-Kubernetes-Policy-Enforcement`  | Kyverno Policy‑as‑Code              | ⚙️⚙️⚙️⚙️ 

---
## 🛠️ Environment Prerequisites
* **Git ≥ 2.30**  
* **Docker / Podman** for local container work  
* **Python 3.9+** (for helper scripts)  
* A personal **GitHub Account & SSH Key**  
* AWS account (credentials provided separately)

---
## 🧑‍🎓 Trainee Workflow (Read Once ✔️)

1. **Fork** this repository to your personal GitHub account. *(Company org members may create feature branches instead of forks if instructed.)*
2. **Clone** your fork locally:
   ```bash
   git clone git@github.com:<your‑user>/devsecops‑bootcamp.git && cd devsecops‑bootcamp
   ```
3. **Pick a task** from the tracker table above.
4. **Create a feature branch** following the naming convention:
   ```bash
   git checkout -b <github‑user>/T13
   ```
5. Navigate to the task folder (`cd T13-Secure-Supply-Chain`) and open its `README.md`.  Follow the instructions **exactly**.
6. Run `python ../auto-progress-checker.py` from repo root at any time to see what you might be missing.
7. **Commit often**, push your branch, and open a **Pull Request (PR)** back to **`final-submission-4302`**.
8. CI/CD will run **only the checks for the tasks you touched**. All _required_ checks must be green before the PR can be merged.
9. Once passed, request review from me. I will grade you with the rubric and merge.
10. Move on to your next task ▶️.

---
## ♻️ CI/CD & Status Checks — How It Works

1. **Per‑task workflows** (`Txx/.github/workflows/ci.yml`) perform task‑specific tests, scans, and validations.
2. A **root‑level workflow** `/.github/workflows/validate-task.yml` (excerpt below) detects which task folders changed in the PR and launches only those jobs:

```yaml
name: Validate Task

on:
  pull_request:
    paths: [ 'T*/**' ]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      paths: ${{ steps.set.outputs.changed }}
    steps:
      - uses: actions/checkout@v3
      - id: set
        run: |
          CHANGED=$(git diff --name-only origin/main...HEAD | grep -oE '^T[0-9]{2}[^/]+' | sort -u | jq -R -s -c 'split("\n")[:-1]')
          echo "changed=$CHANGED" >> $GITHUB_OUTPUT

  task-ci:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        folder: ${{ fromJson(needs.detect-changes.outputs.paths) }}
    steps:
      - uses: actions/checkout@v3
      - name: Re‑use Task Workflow
        run: |
          cd ${{ matrix.folder }}
          echo "▶ Running CI for ${{ matrix.folder }}"
          bash .github/workflows/ci.sh
```

3. **Branch protection rules** mark `validate-task / task-ci` as **Required**.  If any step fails, the PR stays in **“Checks Failing”** and cannot be merged.
4. Your mentors will only review PRs where all checks are ✅ green.

> **Tip 💡**: Run the same scripts locally before pushing to avoid CI failures.

---
## 📋 Progress & Grading
* **Self‑check**: `auto-progress-checker.py` (root) & table in the CSV/Excel tracker.
* **Mentor rubric**: see `/shared/rubric.md` *(also available in the canvas titled “DevSecOps Mentor Rubric”)*.
* **Weekly sync**: Each Friday you’ll demo your completed task(s) for feedback & next assignment.

---
## 🤝 Support
* **Teams channel** `#4302-Arena` – post questions & screenshots.
* **Docs & examples** – see `/shared/templates/` for starter code and CI templates.

Happy hardening & shipping secure software! 💪
