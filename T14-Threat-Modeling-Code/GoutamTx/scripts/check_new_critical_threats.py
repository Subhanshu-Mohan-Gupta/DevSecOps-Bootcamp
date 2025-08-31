#!/usr/bin/env python3
"""
Compare threatmodel/threatmodel.json to threatmodel/baseline.json and
fail with exit code 2 if new unmitigated critical exposures are found.
"""
import json, sys
from pathlib import Path

BASE = Path("threatmodel/baseline.json")
CURR = Path("threatmodel/threatmodel.json")

def load(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def collect_unmitigated_criticals(model):
    out = set()
    if not isinstance(model, dict):
        return out
    # Look for exposures/exposed lists
    ex_keys = [k for k in ("exposures","exposure","exposed") if k in model]
    exposures = []
    if ex_keys:
        for k in ex_keys:
            if isinstance(model[k], list):
                exposures.extend(model[k])
    else:
        # fallback traverse to find dicts with 'component' and 'threat' or 'exposes'
        def traverse(obj):
            if isinstance(obj, dict):
                if ('component' in obj or 'target' in obj) and ('threat' in obj or 'id' in obj or 'name' in obj):
                    exposures.append(obj)
                for v in obj.values():
                    traverse(v)
            elif isinstance(obj, list):
                for it in obj:
                    traverse(it)
        traverse(model)
    # gather mitigations and acceptances
    mitig = set()
    acc = set()
    for k in ("mitigations","mitigation"):
        for m in model.get(k, []) if isinstance(model.get(k, []), list) else []:
            comp = m.get("component") or m.get("target")
            thr = m.get("threat") or m.get("id") or m.get("name")
            if comp and thr:
                mitig.add((comp, thr))
    for k in ("acceptances","accepts","accepted"):
        for a in model.get(k, []) if isinstance(model.get(k, []), list) else []:
            comp = a.get("component") or a.get("target")
            thr = a.get("threat") or a.get("id") or a.get("name")
            if comp and thr:
                acc.add((comp, thr))

    for e in exposures:
        comp = e.get("component") or e.get("target") or e.get("resource")
        thr  = e.get("threat") or e.get("id") or e.get("name")
        meta = e.get("data") or e.get("meta") or {}
        impact = (meta.get("impact") or meta.get("severity") or "").lower() if isinstance(meta, dict) else ""
        if impact == "critical":
            key = (comp, thr)
            if key not in mitig and key not in acc:
                out.add(f"{comp}::{thr}")
    return out

base = load(BASE)
curr = load(CURR)

base_set = collect_unmitigated_criticals(base)
curr_set = collect_unmitigated_criticals(curr)

new = curr_set - base_set
if new:
    print("❌ New unmitigated CRITICAL threats detected:")
    for n in sorted(new):
        print("  -", n)
    sys.exit(2)
else:
    print("✅ No new unmitigated CRITICAL threats.")
    sys.exit(0)

