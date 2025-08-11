#!/usr/bin/env python3
"""
Aggregate Semgrep, Trivy (deps + image), docker-bench JSON outputs into a single compliance JSON
and render a minimal HTML summary. Also annotate totals by severity for policy checking.
"""
import argparse, json, os, sys, datetime
from pathlib import Path
def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

parser = argparse.ArgumentParser()
parser.add_argument('--semgrep', required=True)
parser.add_argument('--trivy-deps', required=True)
parser.add_argument('--trivy-image', required=True)
parser.add_argument('--docker-bench', required=True)
parser.add_argument('--thresholds', required=True)
parser.add_argument('--out-dir', required=True)
args = parser.parse_args()

outdir = Path(args.out_dir); outdir.mkdir(parents=True, exist_ok=True)

sem = load_json(args.semgrep) or {}
trivy_deps = load_json(args.trivy_deps) or {}
trivy_image = load_json(args.trivy_image) or {}
docker_bench = load_json(args.docker_bench) or {}
thresholds = load_json(args.thresholds) or {}

report = {
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "semgrep": sem,
    "trivy_deps": trivy_deps,
    "trivy_image": trivy_image,
    "docker_bench": docker_bench,
    "summary": {}
}

# Build Trivy severity counts helper
def trivy_counts(trivy_json):
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"UNKNOWN":0}
    if not trivy_json:
        return counts
    # trivy JSON has 'Results' -> list -> 'Vulnerabilities' list
    for res in trivy_json.get("Results", []) :
        for vuln in (res.get("Vulnerabilities") or []):
            sev = vuln.get("Severity","UNKNOWN").upper()
            if sev not in counts: sev="UNKNOWN"
            counts[sev] = counts.get(sev,0)+1
    return counts

report["summary"]["trivy_deps_counts"] = trivy_counts(trivy_deps)
report["summary"]["trivy_image_counts"] = trivy_counts(trivy_image)

# Semgrep summary: count findings by severity
def semgrep_counts(sem):
    counts = {"ERROR":0,"WARNING":0,"INFO":0}
    findings = sem.get("results") or []
    for f in findings:
        level = f.get("extra",{}).get("severity","INFO").upper()
        counts[level] = counts.get(level,0)+1
    return counts

report["summary"]["semgrep_counts"] = semgrep_counts(sem)

# docker bench counts
def docker_bench_counts(db):
    counts={"PASS":0,"WARN":0,"INFO":0,"CRITICAL":0}
    for r in db.get("results",[]):
        lvl = r.get("level","INFO").upper()
        if lvl in counts:
            counts[lvl]+=1
    return counts

report["summary"]["docker_bench_counts"] = docker_bench_counts(docker_bench)

# Simple decision flags against thresholds (thresholds.json structure is expected)
violations = []
# Example thresholds: { "trivy": { "CRITICAL": 0, "HIGH": 5 }, "semgrep": { "ERROR":0 }, "docker_bench": { "CRITICAL": 0 } }
trivy_thresholds = thresholds.get("trivy", {})
for sev,allowed in trivy_thresholds.items():
    deps_count = report["summary"]["trivy_deps_counts"].get(sev,0)
    img_count = report["summary"]["trivy_image_counts"].get(sev,0)
    if deps_count > allowed:
        violations.append({"tool":"trivy-deps","severity":sev,"count":deps_count,"allowed":allowed})
    if img_count > allowed:
        violations.append({"tool":"trivy-image","severity":sev,"count":img_count,"allowed":allowed})

sem_thresh = thresholds.get("semgrep", {})
for sev,allowed in sem_thresh.items():
    cnt = report["summary"]["semgrep_counts"].get(sev,0)
    if cnt > allowed:
        violations.append({"tool":"semgrep","severity":sev,"count":cnt,"allowed":allowed})

db_thresh = thresholds.get("docker_bench", {})
for lvl,allowed in db_thresh.items():
    cnt = report["summary"]["docker_bench_counts"].get(lvl,0)
    if cnt > allowed:
        violations.append({"tool":"docker_bench","level":lvl,"count":cnt,"allowed":allowed})

report["violations"] = violations
report_path = outdir / "compliance_report.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

# Create a very small HTML summary
html = f"""<html>
<head><title>Compliance Report</title></head>
<body>
<h1>Compliance Report</h1>
<p>Generated at: {report['generated_at']}</p>
<h2>Summary</h2>
<pre>{json.dumps(report['summary'], indent=2)}</pre>
<h2>Violations</h2>
<pre>{json.dumps(report['violations'], indent=2)}</pre>
</body></html>
"""
with open(outdir / "compliance_report.html","w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote report to {report_path}")
if violations:
    print("Policy violations detected.")
else:
    print("No policy violations detected.")

