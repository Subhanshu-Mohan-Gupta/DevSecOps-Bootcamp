# 🚀 DevSecOps Bootcamp Repository

Welcome to the **DevSecOps Bootcamp**&nbsp;- a hands-on training ground where you harden code, pipelines, and infrastructure **one task at a time**.  
Everything you need is here: task folders, trackers, CI/CD guard-rails, **data-driven PR evaluations**, and step-by-step guides.

---

## 📚 Quick-Glance Tracker

| ID  | Folder                               | Theme (🔑 focus)                   | Difficulty
|-----|--------------------------------------|-------------------------------------|-----------
| T01 | `T01-Enforce-IaC-Policies`           | Terraform + OPA / Sentinel          | ⚙️⚙️⚙️⚙️
| T02 | `T02-K8s-Runtime-Threat-Detection`   | Falco / Tracee, eBPF                | ⚙️⚙️⚙️⚙️
| T03 | `T03-Secrets-Management-Rotation`    | Vault, CSI driver, rotation scripts | ⚙️⚙️⚙️⚙️
| T04 | `T04-Compliance-Audit-CICD`          | Semgrep, Trivy, Docker Bench        | ⚙️⚙️⚙️⚙️
| T06 | `T06-Chaos-Security-Testing`         | Chaos Toolkit / LitmusChaos         | ⚙️⚙️⚙️⚙️⚙️
| T13 | `T13-Secure-Supply-Chain`            | SLSA, Cosign, in-toto               | ⚙️⚙️⚙️⚙️
| T14 | `T14-Threat-Modeling-Code`           | ThreatSpec, PlantUML                | ⚙️⚙️⚙️
| T15 | `T15-AI-PR-Security-Review`          | DeepCode / Snyk Code                | ⚙️⚙️⚙️⚙️
| T16 | `T16-Cloud-Honeypot`                 | DVWA + Falco + ELK                  | ⚙️⚙️⚙️⚙️⚙️
| T17 | `T17-CVE-Triage-Automation`          | SBOM + Grype + Jira                 | ⚙️⚙️⚙️⚙️
| T18 | `T18-Kubernetes-Policy-Enforcement`  | Kyverno Policy-as-Code              | ⚙️⚙️⚙️⚙️

---

## 🛠️ Environment Prerequisites

- **Git ≥ 2.30**
- **Docker / Podman** for local container work
- **Python 3.9+** (helper scripts)
- A personal **GitHub account & SSH key**
- Tool accounts required by your task (e.g., Vault, Snyk, Jira, etc.)
- Cloud creds (e.g., AWS) if the task calls for them

---

## 🧑‍🎓 Workflow (📖 read once)

1. **Fork** this repo (or create a feature branch in the org if instructed).
2. **Clone** your fork:
   ```bash
   git clone git@github.com:<your-user>/devsecops-bootcamp.git
   cd devsecops-bootcamp
   ````

3. **Pick a task** from the tracker.
4. **Create a feature branch** named `<your-github-username>/Txx`, e.g.:

   ```bash
   git checkout -b <your-github-username>/T01
   ```
5. **Create your personal sub-folder inside the task directory** (keeps merges conflict-free):

   ```
   T01/
     └─ <your-github-username>/      # all your code, docs, screenshots, configs
   T13/
     └─ <your-github-username>/      # same pattern for every task
   ```

   > 📌 **Rule:** work only in `Txx/<your-github-username>/…`
6. Open the task’s `README.md` for exact steps, implement, and commit regularly.
7. Run `python auto-progress-checker.py` from repo root anytime to spot missing files.
8. **Push** your branch and open a **Pull Request (PR)** to **`final-submission-4302`**.
9. CI/CD runs *only* the checks for the folders you changed. All required checks must be ✅ before merge.
10. Request mentor review; once approved and merged, move to the next task ▶️.

---

## ♻️ CI/CD & Status Checks

We run **two complementary pipelines** on every PR:

### 1) Task CI (per-folder)

* **Where:** `/.github/workflows/validate-task.yml`
* **What:** Executes each task’s own checks from `Txx/.github/workflows/ci.yml` (linters, scans, tests).
* **Gate:** Branch protection requires these checks to pass.

### 2) PR Evaluation (Static + AI Rubric) — **New**

* **Where:** `/.github/workflows/pr-evaluation.yml`

* **What happens:**

  1. **Static checks (safe, deterministic):**
     Inventories files you changed and compares them to per-task expectations (`_expectations.yml`). No secrets, no code execution.
  2. **AI rubric review (data-driven):**
     Uses the **task rubric** + **static evidence** + **diffs** to generate consolidated scores & feedback.
     The model is configurable via repo variable `OPENAI_MODEL` (default: `gpt-4o-mini`).

* **Output:** A comment on your PR like:
  `📝 AI Rubric Evaluation for T03-Secrets-Management-Rotation (Consolidated)`
  with a table of scores (General + Task-Specific) and actionable notes.

> 🔒 **Security note:** The evaluator **does not execute your code**. It only reads files, diffs, and configuration.

---

## 📦 Expectations-as-Code (how PRs are evaluated)

Each task folder contains an **`_expectations.yml`** that defines what “done” looks like (required files, allowed file types, and key concepts). Example:

```yaml
# T03-Secrets-Management-Rotation/_expectations.yml
task_id: T03
required_files:
  - "README.md"
  - ".github/workflows/ci.yml"
  - "vault/**/*.hcl"
  - "k8s/**/*.yaml"
  - "scripts/rotate*.py"
required_concepts:
  - "vault"
  - "rotation"
  - "dynamic"
  - "csi"
allowed_extensions: [ .hcl, .yaml, .yml, .json, .md, .py, .sh ]
rubric_path: "../../shared/templates/rubric.md"
```

I’ve added tailored `_expectations.yml` to all shipped tasks:

* `T01-Enforce-IaC-Policies/_expectations.yml`
* `T02-K8s-Runtime-Threat-Detection/_expectations.yml`
* `T03-Secrets-Management-Rotation/_expectations.yml`
* `T04-Compliance-Audit-CICD/_expectations.yml`
* `T06-Chaos-Security-Testing/_expectations.yml`
* `T13-Secure-Supply-Chain/_expectations.yml`
* `T14-Threat-Modeling-Code/_expectations.yml`
* `T15-AI-PR-Security-Review/_expectations.yml`
* `T16-Cloud-Honeypot/_expectations.yml`
* `T17-CVE-Triage-Automation/_expectations.yml`
* `T18-Kubernetes-Policy-Enforcement/_expectations.yml`

A **default** is also available at `shared/templates/_expectations.yml` (used if a task doesn’t override it).

---

## 🧪 Interpreting PR Feedback

* **Static evidence** shows which required files were found/missing and which concepts were detected in your diffs.
* **Scores** are based on `/shared/templates/rubric.md` plus the evidence above.
* **Actionable notes** call out where to improve (e.g., add rotation job, sign image, tighten Kyverno rule).
* If feedback seems off:

  * Ensure all work is under `Txx/<your-github-username>/…`
  * Make sure file names/paths match the expectations (e.g., `README.md`, `ci.yml`, etc.)
  * Push a small update; the evaluation reruns automatically.

---

## 🔧 Maintainer Setup (already configured)

* **Secrets:** `OPENAI_API_KEY` (Settings → Secrets → Actions)
* **Variables (optional):** `OPENAI_MODEL` (e.g., `gpt-4o` / `gpt-4o-mini`)
* **Reviewer bot:** The workflow auto-adds `github-copilot[bot]` as a reviewer (if available).
* **Safety:** `pull_request_target` is used only to **read** files and post comments; static checks run with the PR head but do not execute arbitrary code.

---

## 📋 Progress & Grading

* **Self-check:** `auto-progress-checker.py` + CSV/Excel tracker
* **Mentor rubric:** `/shared/rubric.md`
* **Weekly sync:** PRs are reviewed every Friday; you’ll get feedback & the next assignment

---

## 🤝 Support & Community

* **Discussions (NEW!)** – Use the **GitHub → Discussions** tab to:

  * ask questions,
  * propose new advanced tasks,
  * share lessons learned.
    Global contributors are welcome!
* **Teams channel:** `#4302-Arena` — post quick questions & screenshots
* **Templates & examples:** see `/shared/templates/` for starter code and CI snippets

Happy hardening & shipping secure software! 💪
