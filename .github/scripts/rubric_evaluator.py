#!/usr/bin/env python3

import os, sys, subprocess, textwrap, ast
from pathlib import Path

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set – skipping AI rubric evaluation.")
    sys.exit(0)

import openai
from github import Github

openai.api_key = os.getenv("OPENAI_API_KEY")
gh   = Github(os.getenv("GH_TOKEN"))

REPO   = os.getenv("GITHUB_REPOSITORY")
PR_NUM = int(sys.argv[sys.argv.index("--pr") + 1])
FOLDERS = ast.literal_eval(sys.argv[sys.argv.index("--folders") + 1])

BASE_SHA = os.getenv("BASE_SHA")
HEAD_SHA = os.getenv("HEAD_SHA")

RUBRIC_PATH = Path("shared/templates/rubric.md")


def git_diff(folder: str) -> str:
    """Return diff limited to a folder between BASE_SHA and HEAD_SHA."""
    try:
        out = subprocess.check_output(
            ["git", "diff", BASE_SHA, HEAD_SHA, "--", folder],
            text=True,
            stderr=subprocess.STDOUT,
        )
        return out or "<no diff>"
    except subprocess.CalledProcessError as e:
        return f"<diff error>\n{e.output}"


def load_rubric() -> str:
    return RUBRIC_PATH.read_text(encoding="utf-8")


def ai_review(rubric: str, diff: str) -> str:
    prompt = textwrap.dedent(f"""
    Act as a senior DevSecOps mentor. Score the submission (1-4 per criterion)
    using the rubric, then give concise feedback.

    ### RUBRIC
    {rubric}

    ### CODE DIFF
    {diff}
    """)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def comment_on_pr(body: str):
    repo = gh.get_repo(REPO)
    pr   = repo.get_pull(PR_NUM)
    pr.create_issue_comment(body)


def main() -> None:
    rubric = load_rubric()
    for folder in FOLDERS:
        diff = git_diff(folder)
        if diff.strip() == "<no diff>":
            continue
        feedback = ai_review(rubric, diff)
        comment_on_pr(f"### 📝 AI Rubric Evaluation for **{folder}**\n\n{feedback}")


if __name__ == "__main__":
    main()
