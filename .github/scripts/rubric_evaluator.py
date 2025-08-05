#!/usr/bin/env python3

import os, sys, subprocess, json, textwrap, ast
from pathlib import Path

# -------- Graceful exit if secret is missing ----------
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set – skipping AI rubric evaluation.")
    sys.exit(0)

import openai
from github import Github

openai.api_key = os.getenv("OPENAI_API_KEY")
gh  = Github(os.getenv("GH_TOKEN"))

REPO = os.getenv("GITHUB_REPOSITORY")          # e.g. "Org/Repo"
PR_NUM = int(sys.argv[sys.argv.index("--pr") + 1]) if "--pr" in sys.argv else 0
FOLDERS = ast.literal_eval(sys.argv[sys.argv.index("--folders") + 1])

RUBRIC_PATH = Path("shared/templates/rubric.md")

def sh(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)

def load_rubric() -> str:
    return RUBRIC_PATH.read_text(encoding="utf-8")

def diff_for(folder: str) -> str:
    base_sha = os.getenv("GITHUB_EVENT_PULL_REQUEST_BASE_SHA") or os.getenv("GITHUB_BASE_SHA")
    # fallback: use git merge-base
    try:
        base_sha = base_sha or sh("git merge-base HEAD origin/main").strip()
    except subprocess.CalledProcessError:
        base_sha = "HEAD~1"
    return sh(f"git diff {base_sha} HEAD -- {folder}") or "<no diff>"

def ai_review(rubric: str, diff: str) -> str:
    prompt = textwrap.dedent(f"""
    You are a DevSecOps mentor. Use the rubric below to score the submission
    (1-4 per criterion) and provide concise suggestions for improvement.

    ### RUBRIC
    {rubric}

    ### CODE DIFF
    {diff}
    """)
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

def comment_on_pr(body: str):
    repo = gh.get_repo(REPO)
    pr   = repo.get_pull(PR_NUM)
    pr.create_issue_comment(body)

def main():
    rubric = load_rubric()
    for folder in FOLDERS:
        diff = diff_for(folder)
        if diff.strip() == "<no diff>":
            continue
        feedback = ai_review(rubric, diff)
        comment_on_pr(f"### 📝 AI Rubric Evaluation for **{folder}**\n\n{feedback}")

if __name__ == "__main__":
    main()
