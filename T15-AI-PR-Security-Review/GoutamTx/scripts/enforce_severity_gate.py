#!/usr/bin/env python3
import sys
import json
import os

SEVERITY_ORDER = ["low", "medium", "high", "critical"]

def safe_path(path_arg: str, base_dir: str = "reports") -> str:
    """Ensure the file path stays inside base_dir."""
    full_path = os.path.abspath(path_arg)
    if not full_path.startswith(os.path.abspath(base_dir)):
        raise ValueError(f"Unsafe path detected: {path_arg}")
    return full_path

def main():
    if len(sys.argv) < 3:
        print("Usage: python enforce_severity_gate.py <report.json> <threshold>")
        sys.exit(1)

    report_file = safe_path(sys.argv[1])
    threshold = sys.argv[2].lower()

    if threshold not in SEVERITY_ORDER:
        print(f"Invalid threshold: {threshold}. Choose from {SEVERITY_ORDER}")
        sys.exit(1)

    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract issues
    issues = data.get("issues", [])
    threshold_index = SEVERITY_ORDER.index(threshold)

    violations = [
        issue for issue in issues
        if SEVERITY_ORDER.index(issue.get("severity", "low")) >= threshold_index
    ]

    if violations:
        print(f"❌ Severity gate failed. Found {len(violations)} issues >= {threshold}")
        sys.exit(1)
    else:
        print(f"✅ No issues found above threshold '{threshold}'")

if __name__ == "__main__":
    main()
