# 🚀 DevSecOps Bootcamp Repository

Welcome to the **DevSecOps Bootcamp**&nbsp; a hands-on training ground where you will harden code, pipelines, and infrastructure **one task at a time**. Everything you need is here: task folders, trackers, CI/CD guard-rails, and step-by-step guides.

---

## 📚 Quick-Glance Tracker

| ID  | Folder                               | Theme (🔑 focus)                    | Difficulty 
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
* **Git ≥ 2.30**  
* **Docker / Podman** for local container work  
* **Python 3.9+** (helper scripts)  
* A personal **GitHub account & SSH key**
* Personal accounts related to that task-specific tools (if required)
* AWS credentials (provided separately)

---

## 🧑‍🎓 Workflow (📖 read once)

1. **Fork** this repo (or create a feature branch in the org if instructed).
2. **Clone** your fork:
   ```bash
   git clone git@github.com:<your-user>/devsecops-bootcamp.git
   cd devsecops-bootcamp
````

3. **Pick a task** from the tracker.
4. **Create a feature branch** named `<your-github-username>/Txx`, e.g.

   ```bash
   git checkout -b <your-github-username>/T01
   ```
5. **Create your personal sub-folder inside the task directory**

   ```
   T01/
     └─ <your-github-username>/       # <— all your code, docs, screenshots and configs here
   ```

   > 📌 **Rule:** every contributor works only in
   > `Txx/<your-github-username>/…`
6. Open the task’s `README.md` for exact steps, implement, and commit regularly.
7. Run `python auto-progress-checker.py` from repo root anytime to spot missing files.
8. **Push** your branch and open a **Pull Request (PR)** to **`final-submission-4302`**.
9. CI/CD runs *only* the checks for the folders you touched. All required checks must be ✅ before merge.
10. Request mentor review; once approved and merged, move to the next task ▶️.

---

## ♻️ CI/CD & Status Checks — Under the Hood

1. **Per-task workflows** (`Txx/.github/workflows/ci.yml`) run linters, scans, and tests for that task.
2. The **root workflow** `/.github/workflows/validate-task.yml` detects which task folders changed and launches only those jobs (see excerpt below).

```yaml
name: Validate Task
on:
  pull_request:
    paths: [ 'T*/**' ]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      folders: ${{ steps.set.outputs.changed }}
    steps:
      - uses: actions/checkout@v3
      - id: set
        run: |
          CHANGED=$(git diff --name-only origin/main...HEAD \
                     | grep -oE '^T[0-9]{2}[^/]+' \
                     | sort -u \
                     | jq -R -s -c 'split("\n")[:-1]')
          echo "changed=$CHANGED" >> $GITHUB_OUTPUT

  task-ci:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        folder: ${{ fromJson(needs.detect-changes.outputs.folders) }}
    steps:
      - uses: actions/checkout@v3
      - name: Run Task CI
        run: |
          cd ${{ matrix.folder }}
          if [ -f .github/workflows/ci.sh ]; then
            bash .github/workflows/ci.sh
          else
            echo "No task CI script found" && exit 1
          fi
```

3. **Branch protection** marks `validate-task / task-ci` as *Required*. No green ✅, no merge.
4. Run the same scripts locally to avoid CI surprises.

---

## 📋 Progress & Grading

* **Self-check:** `auto-progress-checker.py` + CSV/Excel tracker
* **Mentor rubric:** `/shared/rubric.md`
* **Weekly sync:** will review PRs every Friday, get feedback, grab next assignment

---

## 🤝 Support

* **Discussions (NEW!)** – Head to the **GitHub → Discussions** tab to  
  * ask questions,  
  * propose new advanced tasks,  
  * or share lessons learned.  
  Global contributors are encouraged to jump in!
* **Teams channel:** `#4302-Arena` — post questions & screenshots
* **Templates & examples:** see `/shared/templates/` for starter code

Happy hardening & shipping secure software! 💪