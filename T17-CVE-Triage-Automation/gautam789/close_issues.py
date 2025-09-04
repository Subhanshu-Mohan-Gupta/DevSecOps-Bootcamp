import requests
import os

# ==============================
# Jira Configuration
# ==============================
JIRA_URL = os.environ.get("JIRA_URL")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
PROJECT_KEY = os.environ.get("PROJECT_KEY")
DONE_TRANSITION_ID = os.environ.get("DONE_TRANSITION_ID")

if not JIRA_API_TOKEN:
    raise ValueError("Error: JIRA_API_TOKEN is not set. Please check your GitHub Actions secrets.")


# ==============================
# Fetch Open Issues
# ==============================
def get_open_issues():
    """Fetch all Jira issues in the project that are NOT Done."""
    print("[INFO] Fetching open issues...")
    url = f"{JIRA_URL}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    params = {
        "jql": f"project = {PROJECT_KEY} AND status != Done",
        "fields": "key"
    }

    response = requests.get(url, headers=headers, params=params, auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch open issues: {response.status_code}, {response.text}")
        return []

    issues = response.json().get("issues", [])
    open_issues = [issue["key"] for issue in issues]

    print(f"[INFO] Found {len(open_issues)} open issues: {open_issues}")
    return open_issues

# ==============================
# Close an Issue
# ==============================
def close_jira_issue(issue_key):
    """Close a Jira issue by moving it to 'Done'."""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "transition": {
            "id": DONE_TRANSITION_ID
        }
    }

    response = requests.post(url, headers=headers, json=payload, auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    if response.status_code == 204:
        print(f"[INFO] Issue {issue_key} successfully moved to Done.")
    else:
        print(f"[ERROR] Failed to close {issue_key}. Response: {response.status_code}, {response.text}")

# ==============================
# Main Automation
# ==============================
def auto_close_all_issues():
    """Automatically close all open Jira issues for the specified project."""
    open_issues = get_open_issues()

    if not open_issues:
        print("[INFO] No open issues found. Nothing to close.")
        return

    for issue_key in open_issues:
        close_jira_issue(issue_key)

    print(f"[INFO] Process completed. {len(open_issues)} issues closed.")

# ==============================
# Entry Point
# ==============================
if __name__ == "__main__":
    auto_close_all_issues()
