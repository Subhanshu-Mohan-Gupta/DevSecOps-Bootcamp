#!/usr/bin/env python3

import json, os, subprocess, textwrap, openai
from github import Github

openai.api_key = os.environ["OPENAI_API_KEY"]
gh       = Github(os.environ["GH_TOKEN"])
REPO     = os.environ["GITHUB_REPOSITORY"]
PR_NUM   = int(os.getenv("PR", "0"))  # passed via --pr

def run(cmd): return subprocess.check_output(cmd, shell=True, text=True)

def load_rubric():
    with open("shared/templates/rubric.md", "r", encoding="utf-8") as f:
        return f.read()

def diff_for(folder):
    return run(f"git diff origin/main...HEAD -- {folder}")

def ai_review(rubric, diff):
    prompt = textwrap.dedent(f"""
    You are a DevSecOps mentor. Use the rubric below to score the submission
    (1-4 per criterion) and provide concise feedback.

    ===== RUBRIC =====
    {rubric}
    ===== CODE DIFF (git) =====
    {diff}
    """)
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

def comment_on_pr(body):
    repo = gh.get_repo(REPO)
    pr   = repo.get_pull(PR_NUM)
    pr.create_issue_comment(body)

if __name__ == "__main__":
    import argparse, ast
    ap = argparse.ArgumentParser()
    ap.add_argument("--folders", required=True)
    ap.add_argument("--pr", required=True)
    args = ap.parse_args()
    folders = ast.literal_eval(args.folders)  # JSON array

    rubric = load_rubric()
    for folder in folders:
        diff  = diff_for(folder)
        if diff.strip():
            feedback = ai_review(rubric, diff)
            comment_on_pr(f"### 📝 AI Rubric Evaluation for **{folder}**\n{feedback}")
