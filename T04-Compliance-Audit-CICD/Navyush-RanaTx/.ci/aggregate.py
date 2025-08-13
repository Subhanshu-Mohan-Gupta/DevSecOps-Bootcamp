#!/usr/bin/env python3
"""
. ci/aggregate.py
Usage:
  python3 aggregate.py --semgrep semgrep.json --trivy-deps trivy-deps.json \
    --trivy-image trivy-image.json --docker-bench docker-bench.json \
    --policy policy.yaml --out compliance-report.json --html-out report.html
"""
import argparse, json, sys, os, yaml, datetime, html

def load_json(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path,'r',encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            # if invalid JSON, return raw text
            return {"_raw": open(path,'rb').read().decode('utf-8', errors='ignore')}

def severity_map_trivy(sev):
    # Trivy severities: CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN
    return sev.upper()

def severity_map_semgrep(s):
    # semgrep uses "severity": "ERROR"/"WARNING"/"INFO" sometimes; map to MEDIUM/HIGH
    s = (s or "").upper()
    if s in ("ERROR","HIGH"):
        return "HIGH"
    if s in ("WARNING","MEDIUM"):
        return "MEDIUM"
    if s in ("INFO","LOW"):
        return "LOW"
    return "UNKNOWN"

def summarize(trivy_json, kind="trivy"):
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"UNKNOWN":0}
    items = []
    # trivy JSON shape: list of results with Vulnerabilities lists OR for fs: .Results[].Vulnerabilities
    results = trivy_json.get("Results") or trivy_json.get("Vulnerabilities") or trivy_json.get("vulnerabilities") or []
    if isinstance(results, dict):
        results = [results]
    for res in results:
        vulns = res.get("Vulnerabilities") or []
        for v in vulns:
            sev = severity_map_trivy(v.get("Severity","UNKNOWN"))
            counts.setdefault(sev,0)
            counts[sev]+=1
            items.append({
                "id": v.get("VulnerabilityID") or v.get("Name"),
                "pkg": v.get("PkgName"),
                "installed": v.get("InstalledVersion"),
                "fixed": v.get("FixedVersion"),
                "severity": sev,
                "title": v.get("Title"),
                "data": v
            })
    return counts, items

def summarize_semgrep(j):
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"UNKNOWN":0}
    items = []
    for r in (j.get("results") or []):
        sev = severity_map_semgrep(r.get("severity"))
        counts.setdefault(sev,0)
        counts[sev]+=1
        items.append({
            "check_id": r.get("check_id"),
            "path": r.get("path"),
            "start": r.get("start"),
            "end": r.get("end"),
            "message": r.get("extra",{}).get("message"),
            "severity": sev,
            "data": r
        })
    return counts, items

def summarize_dockerbench(j):
    # docker-bench-security JSON format varies; simplest: count WARN/INFO/PASS/FAIL
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"UNKNOWN":0}
    items = []
    for entry in (j.get("tests") or j.get("controls") or []):
        # try multiple shapes
        title = entry.get("test_name") or entry.get("description") or entry.get("id")
        result = entry.get("result") or entry.get("status") or "WARN"
        # map FAIL -> CRITICAL, WARN -> MEDIUM
        if result.upper() in ("FAIL","ERROR"):
            counts["CRITICAL"] += 1
            sev="CRITICAL"
        elif result.upper() in ("WARN","WARNING"):
            counts["MEDIUM"] += 1
            sev="MEDIUM"
        elif result.upper() in ("PASS","INFO"):
            sev="LOW"
            counts["LOW"]+=1
        else:
            sev="UNKNOWN"
            counts["UNKNOWN"]+=1
        items.append({"title": title, "result": result, "severity": sev, "data": entry})
    return counts, items

def merge_counts(*counts):
    out = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"UNKNOWN":0}
    for c in counts:
        for k,v in c.items():
            out[k] = out.get(k,0) + v
    return out

def load_policy(path):
    if not path or not os.path.exists(path):
        # default policy
        return {"fail_on": {"CRITICAL": 1, "HIGH": 5}, "cvss_threshold": 9.0}
    with open(path,'r',encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--semgrep'); p.add_argument('--trivy-deps'); p.add_argument('--trivy-image')
    p.add_argument('--docker-bench'); p.add_argument('--policy'); p.add_argument('--out'); p.add_argument('--html-out')
    args = p.parse_args()

    sem = load_json(args.semgrep) if args.semgrep else {}
    tr_deps = load_json(args.trivy_deps) if args.trivy_deps else {}
    tr_img = load_json(args.trivy_image) if args.trivy_image else {}
    db = load_json(args.docker_bench) if args.docker_bench else {}

    sem_counts, sem_items = summarize_semgrep(sem)
    tr_deps_counts, tr_deps_items = summarize(tr_deps, kind="trivy-deps")
    tr_img_counts, tr_img_items = summarize(tr_img, kind="trivy-image")
    db_counts, db_items = summarize_dockerbench(db)

    merged_counts = merge_counts(sem_counts, tr_deps_counts, tr_img_counts, db_counts)

    policy = load_policy(args.policy)
    failures = []
    # check count thresholds
    fail_on = policy.get("fail_on", {})
    for sev, threshold in fail_on.items():
        if merged_counts.get(sev,0) >= threshold:
            failures.append(f"severity {sev} count {merged_counts.get(sev)} >= threshold {threshold}")

    # optional CVSS threshold: scan trivy items for CVSS
    cvss_threshold = policy.get("cvss_threshold")
    if cvss_threshold:
        for it in (tr_deps_items + tr_img_items):
            # trivy stores CVSS in 'Cvss' or 'CVSS' fields inside 'Vulnerability'
            data = it.get("data", {})
            # try typical fields:
            cvss = None
            for key in ("Cvss", "CVSS", "cvss"):
                if key in data:
                    try:
                        # some shapes: {"nvd":{"V2":...}}
                        pass
                    except:
                        pass
            # Try to read score from data.get('CVSS', {}) fields:
            try:
                if isinstance(data.get("CVSS"), dict):
                    # attempt first available vector
                    for k,v in data["CVSS"].items():
                        score = v.get("Score") or v.get("score")
                        if score:
                            cvss = float(score)
                            break
                # some Trivy versions attach "VulnerabilityID" and "Score" directly:
                if cvss is None and data.get("Score"):
                    cvss = float(data.get("Score"))
            except Exception:
                cvss = None
            if cvss and cvss >= float(cvss_threshold):
                failures.append(f"vuln {it.get('id')} has CVSS {cvss} >= {cvss_threshold}")

    report = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "summary": merged_counts,
        "details": {
            "semgrep": {"counts": sem_counts, "items": sem_items},
            "trivy_deps": {"counts": tr_deps_counts, "items": tr_deps_items},
            "trivy_image": {"counts": tr_img_counts, "items": tr_img_items},
            "docker_bench": {"counts": db_counts, "items": db_items},
        },
        "policy": policy,
        "failures": failures,
        "passed": len(failures) == 0
    }

    with open(args.out or "compliance-report.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    # simple HTML report
    if args.html_out:
        html_snippets = []
        html_snippets.append(f"<h1>Compliance report</h1><p>Generated: {report['generated_at']}</p>")
        html_snippets.append("<h2>Summary</h2><ul>")
        for k,v in merged_counts.items():
            html_snippets.append(f"<li>{html.escape(k)}: {v}</li>")
        html_snippets.append("</ul>")

        if failures:
            html_snippets.append("<h2 style='color:red'>Policy Failures</h2><ul>")
            for fmsg in failures:
                html_snippets.append(f"<li>{html.escape(fmsg)}</li>")
            html_snippets.append("</ul>")
        else:
            html_snippets.append("<h2 style='color:green'>Passed</h2>")

        html_snippets.append("<h2>Details (Top findings)</h2>")
        # include top 20 items across all scanners
        combined_items = (tr_img_items + tr_deps_items + sem_items + db_items)[:50]
        html_snippets.append("<ol>")
        for it in combined_items:
            title = it.get("title") or it.get("id") or it.get("check_id") or it.get("title") or "item"
            sev = it.get("severity","UNKNOWN")
            html_snippets.append(f"<li><b>{html.escape(str(title))}</b> - {html.escape(sev)}</li>")
        html_snippets.append("</ol>")

        with open(args.html_out, "w", encoding='utf-8') as f:
            f.write("\n".join(html_snippets))

    if failures:
        print("Policy violations detected:")
        for fmsg in failures:
            print(" -", fmsg)
        sys.exit(2)
    print("No policy violations. All checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
