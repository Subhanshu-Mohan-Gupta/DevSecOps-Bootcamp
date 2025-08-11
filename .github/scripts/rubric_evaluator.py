#!/usr/bin/env python3

import os, sys, subprocess, textwrap, ast, re, time
from pathlib import Path
from typing import List, Tuple

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set – skipping AI rubric evaluation.")
    sys.exit(0)

import openai
from github import Github

MODEL = "gpt-4o-mini"         
MAX_TOTAL_CHARS = 60000
MAX_DIFF_CHARS = 45000
MIN_CHUNK_CHARS = 8000
SLEEP_BETWEEN_CALLS = 1.0
MAX_RETRIES = 5
BACKOFF_BASE = 1.5

ALLOWED_SUFFIXES = {
    ".tf", ".hcl", ".rego",
    ".yaml", ".yml", ".json", ".md",
    ".py", ".go", ".js", ".ts", ".sh",
    ".Dockerfile", "Dockerfile", ".tpl",
}

openai.api_key = os.getenv("OPENAI_API_KEY")
gh = Github(os.getenv("GH_TOKEN"))

REPO     = os.getenv("GITHUB_REPOSITORY")
PR_NUM   = int(sys.argv[sys.argv.index("--pr") + 1])
FOLDERS  = ast.literal_eval(sys.argv[sys.argv.index("--folders") + 1])

BASE_SHA = os.getenv("BASE_SHA")
HEAD_SHA = os.getenv("HEAD_SHA")

RUBRIC_PATH = Path("shared/templates/rubric.md")
DATE_ROW_REGEX = re.compile(r"^\|\s*Date\s*\|.*\|$", re.IGNORECASE)

def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)

def load_rubric() -> str:
    return RUBRIC_PATH.read_text(encoding="utf-8")

def list_changed_files(folder: str) -> List[str]:
    out = run(["git", "diff", "--name-only", BASE_SHA, HEAD_SHA, "--", folder])
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    allowed = []
    for f in files:
        suf = Path(f).suffix
        base = Path(f).name
        if suf in ALLOWED_SUFFIXES or base in ALLOWED_SUFFIXES:
            allowed.append(f)
    return allowed

def file_diff(path: str) -> str:
    return run(["git", "diff", "-U1", BASE_SHA, HEAD_SHA, "--", path])

def chunk_diffs(diffs: List[Tuple[str, str]], rubric_len: int) -> List[str]:
    """
    Pack file diffs into chunks <= MAX_DIFF_CHARS (accounting for rubric length).
    """
    budget = min(MAX_DIFF_CHARS, max(8000, MAX_TOTAL_CHARS - rubric_len - 8000))
    chunks, cur, cur_len = [], [], 0

    for fname, d in diffs:
        header = f"\n\n# FILE: {fname}\n"
        piece = header + d
        if cur_len + len(piece) > budget and cur:
            chunks.append("".join(cur))
            cur, cur_len = [], 0
        if len(piece) > budget:
            clip = max(2000, budget // 2)
            piece = header + (d[:clip] + "\n...\n" + d[-clip:])
        cur.append(piece)
        cur_len += len(piece)

    if cur:
        chunks.append("".join(cur))
    return chunks

def ai_review(model: str, rubric: str, diff_chunk: str) -> str:
    prompt = textwrap.dedent(f"""
    Act as a senior DevSecOps mentor. Evaluate the submission using the rubric
    (score 1–4 per criterion) and provide concise, actionable feedback.
    If information is missing, mark that criterion as N/A and state what is needed.

    ### RUBRIC
    {rubric}

    ### CODE DIFF (subset)
    {diff_chunk}
    """)
    resp = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def safe_ai_review(rubric: str, chunk: str) -> str:
    """
    Try to review the chunk; if too large, auto-shrink and retry.
    Also handles 429 rate limits with exponential backoff.
    """
    cur = chunk
    shrink_guard = 0
    while True:
        try:
            return ai_review(MODEL, rubric, cur)

        except openai.BadRequestError as e:
            msg = str(e)
            if "maximum context length" in msg or "context_length_exceeded" in msg:
                if len(cur) < MIN_CHUNK_CHARS or shrink_guard > 6:
                    return ("⚠️ Context too large even after shrinking. "
                            "Please split your PR into smaller pieces or limit file scope.")
                cur = cur[: len(cur) // 2]
                shrink_guard += 1
                continue
            raise

        except openai.RateLimitError:
            for i in range(1, MAX_RETRIES + 1):
                delay = (BACKOFF_BASE ** i)
                time.sleep(delay)
                try:
                    return ai_review(MODEL, rubric, cur)
                except openai.RateLimitError:
                    continue
            return "⚠️ Repeated rate limit errors. Please retry shortly."

        finally:
            time.sleep(SLEEP_BETWEEN_CALLS)

def strip_overall_eval_date_row(md: str) -> str:
    """Remove ONLY the '| Date | ... |' row from any markdown table."""
    return "\n".join(
        line for line in md.splitlines()
        if not DATE_ROW_REGEX.match(line.strip())
    )

def comment_on_pr(body: str):
    gh.get_repo(REPO).get_pull(PR_NUM).create_issue_comment(body)

def main() -> None:
    rubric = load_rubric()
    rubric_len = len(rubric)

    for folder in FOLDERS:
        files = list_changed_files(folder)
        if not files:
            comment_on_pr(
                f"### 📝 AI Rubric Evaluation for **{folder}**\n\n"
                f"_No reviewable changes detected (non-code or unsupported file types)._\n"
                f"**Tip:** Include Terraform/K8s manifests, policy files, scripts, or docs."
            )
            continue

        diffs = []
        for f in files:
            try:
                d = file_diff(f)
                if d.strip():
                    diffs.append((f, d))
            except subprocess.CalledProcessError:
                continue

        if not diffs:
            comment_on_pr(
                f"### 📝 AI Rubric Evaluation for **{folder}**\n\n"
                f"_Changed files detected but produced empty diffs._"
            )
            continue

        chunks = chunk_diffs(diffs, rubric_len)

        total = len(chunks)
        for idx, chunk in enumerate(chunks, 1):
            feedback = safe_ai_review(rubric, chunk)
            feedback = strip_overall_eval_date_row(feedback)
            header = f"### 📝 AI Rubric Evaluation for **{folder}** — Chunk {idx}/{total}\n\n"
            comment_on_pr(header + feedback)

if __name__ == "__main__":
    main()
