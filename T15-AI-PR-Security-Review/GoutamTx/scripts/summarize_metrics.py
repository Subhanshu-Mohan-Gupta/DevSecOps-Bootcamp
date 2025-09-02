#!/usr/bin/env python3
import sys
import json
import csv
import os
from datetime import datetime

def safe_path(path_arg: str, base_dir: str = "reports") -> str:
    """Ensure the file path stays inside base_dir."""
    full_path = os.path.abspath(path_arg)
    if not full_path.startswith(os.path.abspath(base_dir)):
        raise ValueError(f"Unsafe path detected: {path_arg}")
    return full_path

def count_severity(issues):
    counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for issue in issues:
        sev = issue.get("severity", "low").lower()
        if sev in counts:
            counts[sev] += 1
    return counts

def main():
    if len(sys.argv) < 4:
        print("Usage: python summarize_metrics.py <input.json> <summary.json> <trend.csv>")
        sys.exit(1)

    input_file = safe_path(sys.argv[1])
    summary_file = safe_path(sys.argv[2])
    trend_file = safe_path(sys.argv[3])

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    issues = data.get("issues", [])
    counts = count_severity(issues)

    summary = {
        "total_issues": sum(counts.values()),
        "by_severity": counts,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # Write summary JSON
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Append trend CSV with safe quoting
    timestamp = summary["timestamp"]
    with open(trend_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([timestamp, counts["low"], counts["medium"], counts["high"], counts["critical"]])

    print("✅ Metrics summarized successfully.")

if __name__ == "__main__":
    main()
