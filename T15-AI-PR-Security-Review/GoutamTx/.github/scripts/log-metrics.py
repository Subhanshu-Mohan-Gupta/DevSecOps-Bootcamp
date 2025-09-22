#!/usr/bin/env python3
import json
import argparse
import datetime
import os

def log_security_metrics(pr_number, total_issues, high_issues, critical_issues, commit_sha):
    """Log security scan metrics for tracking and analysis"""
    
    metrics = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'pr_number': pr_number,
        'commit_sha': commit_sha,
        'scan_results': {
            'total_issues': int(total_issues),
            'high_issues': int(high_issues),
            'critical_issues': int(critical_issues),
            'scan_engine': 'snyk-code'
        },
        'security_gate': {
            'passed': int(high_issues) == 0 and int(critical_issues) == 0,
            'blocking_issues': int(high_issues) + int(critical_issues)
        },
        'false_positive_tracking': {
            'enabled': True,
            'review_pending': int(total_issues) > 0
        }
    }
    
    # Log to file for persistence
    log_file = f"security-metrics-{pr_number}.json"
    with open(log_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Log to GitHub Actions output
    print(f"::notice title=Security Metrics::Logged metrics for PR #{pr_number}")
    print(f"Total Issues: {total_issues}, High: {high_issues}, Critical: {critical_issues}")
    
    # Create metrics summary for artifact upload
    with open('metrics-summary.txt', 'w') as f:
        f.write(f"Security Scan Metrics - PR #{pr_number}\n")
        f.write(f"Timestamp: {metrics['timestamp']}\n")
        f.write(f"Total Issues: {total_issues}\n")
        f.write(f"High Severity: {high_issues}\n")
        f.write(f"Critical Severity: {critical_issues}\n")
        f.write(f"Security Gate: {'PASS' if metrics['security_gate']['passed'] else 'FAIL'}\n")
        f.write(f"Commit SHA: {commit_sha}\n")
        f.write(f"False Positive Tracking: Enabled\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr-number', required=True)
    parser.add_argument('--total-issues', required=True)
    parser.add_argument('--high-issues', required=True)
    parser.add_argument('--critical-issues', required=True)
    parser.add_argument('--commit-sha', required=True)
    
    args = parser.parse_args()
    
    log_security_metrics(
        args.pr_number,
        args.total_issues,
        args.high_issues,
        args.critical_issues,
        args.commit_sha
    )

