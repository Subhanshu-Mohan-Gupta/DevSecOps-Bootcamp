#!/usr/bin/env python3

import os, sys, subprocess, textwrap, ast, re
from pathlib import Path

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set – skipping AI rubric evaluation.")
    sys.exit(0)

import openai
from github import Github

openai.api_key = os.getenv("OPENAI_API_KEY")
gh = Github(os.getenv("GH_TOKEN"))

REPO    = os.getenv("GITHUB_REPOSITORY")
PR_NUM  = int(sys.argv[sys.argv.index("--pr") + 1])
FOLDERS = ast.literal_eval(sys.argv[sys.argv.index("--folders") + 1])

BASE_SHA = os.getenv("BASE_SHA")
HEAD_SHA = os.getenv("HEAD_SHA")

RUBRIC_PATH = Path("shared/templates/rubric.md")

def git_diff(folder: str) -> str:
    return subprocess.check_output(
        ["git", "diff", BASE_SHA, HEAD_SHA, "--", folder],
        text=True,
        stderr=subprocess.STDOUT,
    ) or "<no diff>"

def load_rubric() -> str:
    return RUBRIC_PATH.read_text(encoding="utf-8")

def ai_review(rubric: str, diff: str) -> str:
    prompt = textwrap.dedent(f"""
    You are a senior DevSecOps mentor. Evaluate the submission using the rubric
    (score 1–4 per criterion) and provide concise feedback.

    ### RUBRIC
    {rubric}

    ### CODE DIFF
    {diff}
    """)
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def comment_on_pr(body: str):
    gh.get_repo(REPO).get_pull(PR_NUM).create_issue_comment(body)

DATE_ROW_REGEX = re.compile(r"^\|\s*Date\s*\|.*\|$", re.IGNORECASE)

def main() -> None:
    rubric = load_rubric()

    for folder in FOLDERS:
        diff = git_diff(folder)
        if diff.strip() == "<no diff>":
            continue

        feedback = ai_review(rubric, diff)

        feedback = "\n".join(
            line for line in feedback.splitlines()
            if not DATE_ROW_REGEX.match(line.strip())
        )

        body = f"### 📝 AI Rubric Evaluation for **{folder}**\n\n{feedback}"
        comment_on_pr(body)

if __name__ == "__main__":
    main()
