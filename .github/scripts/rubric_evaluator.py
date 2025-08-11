#!/usr/bin/env python3

import os, sys, subprocess, textwrap, ast, re, time, json
from pathlib import Path
from typing import List, Tuple, Dict, Any

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set – skipping AI rubric evaluation.")
    sys.exit(0)

import openai
from github import Github

MODEL = "gpt-4o-mini"
MAX_TOTAL_CHARS = 60000
MAX_DIFF_CHARS  = 45000
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

GENERAL_KEYS = ["technical_accuracy", "security_focus", "completeness", "documentation", "presentation"]
DATE_ROW_REGEX = re.compile(r"^\|\s*Date\s*\|.*\|$", re.IGNORECASE)

openai.api_key = os.getenv("OPENAI_API_KEY")
gh = Github(os.getenv("GH_TOKEN"))

REPO     = os.getenv("GITHUB_REPOSITORY")
PR_NUM   = int(sys.argv[sys.argv.index("--pr") + 1])
FOLDERS  = ast.literal_eval(sys.argv[sys.argv.index("--folders") + 1])

BASE_SHA = os.getenv("BASE_SHA")
HEAD_SHA = os.getenv("HEAD_SHA")

RUBRIC_PATH = Path("shared/templates/rubric.md")

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
    # -U1 minimizes context to shrink tokens
    return run(["git", "diff", "-U1", BASE_SHA, HEAD_SHA, "--", path])

def chunk_diffs(diffs: List[Tuple[str, str]], rubric_len: int) -> List[str]:
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

SCHEMA_EXAMPLE = {
  "format_version": "1",
  "task_id": "T03",
  "scores": {
    "technical_accuracy": 3,
    "security_focus": 3,
    "completeness": 2,
    "documentation": 3,
    "presentation": 3
  },
  "task_specific_total": 12,   # 0-20 for task-specific portion
  "notes": {
    "technical_accuracy": "e.g., Vault Agent injector works; rotation job rotates DB creds",
    "security_focus": "e.g., least privilege for Vault role; no plaintext secrets",
    "completeness": "what is missing / present",
    "documentation": "README clarity / diagrams",
    "presentation": "explanation quality"
  }
}

def build_json_prompt(rubric: str, diff_chunk: str, task_id: str) -> str:
    schema = json.dumps(SCHEMA_EXAMPLE, indent=2)
    return textwrap.dedent(f"""
    You are a senior DevSecOps mentor. Evaluate the submission using the rubric.
    IMPORTANT:
    - Output STRICT JSON ONLY (no markdown, no prose, no code fences).
    - Use this schema exactly (fill values appropriately):
    {schema}

    Rules:
    - 'scores' values must be integers 1..4 (N/A -> omit that key).
    - 'task_specific_total' is 0..20 (whole number). Do NOT exceed 20.
    - Do not include any extra keys.
    - If info is missing in this chunk, leave that criterion out of 'scores' and explain in notes.

    TASK_ID: {task_id}

    ### RUBRIC
    {rubric}

    ### CODE DIFF (subset)
    {diff_chunk}
    """)

def ai_review_json(rubric: str, diff_chunk: str, task_id: str) -> Dict[str, Any]:
    prompt = build_json_prompt(rubric, diff_chunk, task_id)
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = raw.strip().strip("`")
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)

def safe_ai_review_json(rubric: str, chunk: str, task_id: str) -> Dict[str, Any]:
    cur = chunk
    shrink_guard = 0
    def backoff_call():
        for i in range(1, MAX_RETRIES + 1):
            try:
                return ai_review_json(rubric, cur, task_id)
            except openai.RateLimitError:
                time.sleep(BACKOFF_BASE ** i)
        return {"scores": {}, "task_specific_total": 0, "notes": {"error": "rate_limited"}}

    while True:
        try:
            return ai_review_json(rubric, cur, task_id)
        except openai.BadRequestError as e:
            msg = str(e)
            if "maximum context length" in msg or "context_length_exceeded" in msg:
                if len(cur) < MIN_CHUNK_CHARS or shrink_guard > 6:
                    return {"scores": {}, "task_specific_total": 0, "notes": {"error": "context_too_large"}}
                cur = cur[: len(cur) // 2]
                shrink_guard += 1
                continue
            else:
                return backoff_call()
        except openai.RateLimitError:
            return backoff_call()
        finally:
            time.sleep(SLEEP_BETWEEN_CALLS)

def strip_overall_eval_date_row(md: str) -> str:
    return "\n".join(
        line for line in md.splitlines()
        if not DATE_ROW_REGEX.match(line.strip())
    )

def comment_on_pr(body: str):
    gh.get_repo(REPO).get_pull(PR_NUM).create_issue_comment(body)

def aggregate_results(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    agg_scores = {k: 0 for k in GENERAL_KEYS}
    agg_notes: Dict[str, List[str]] = {k: [] for k in GENERAL_KEYS}
    task_total_max = 0

    for res in chunks:
        scores = res.get("scores", {}) or {}
        for k in GENERAL_KEYS:
            v = scores.get(k)
            if isinstance(v, (int, float)) and v > agg_scores[k]:
                agg_scores[k] = int(v)
        notes = res.get("notes", {}) or {}
        for k in GENERAL_KEYS:
            n = notes.get(k)
            if isinstance(n, str) and n and n not in agg_notes[k]:
                agg_notes[k].append(n)
        t = res.get("task_specific_total", 0) or 0
        if isinstance(t, (int, float)) and t > task_total_max:
            task_total_max = int(t)

    overall = sum(agg_scores.values()) + task_total_max
    return {"scores": agg_scores, "task_specific_total": task_total_max, "overall_total": overall, "notes": agg_notes}

def render_markdown(task_id: str, agg: Dict[str, Any]) -> str:
    s = agg["scores"]
    task_total = agg["task_specific_total"]
    overall = agg["overall_total"]
    notes = agg["notes"]

    table = [
        "| **General Criteria** | **Score (1-4)** |",
        "|---|---|",
        f"| Technical Accuracy | {s['technical_accuracy']} |",
        f"| Security Focus | {s['security_focus']} |",
        f"| Completeness | {s['completeness']} |",
        f"| Documentation | {s['documentation']} |",
        f"| Presentation | {s['presentation']} |",
        "",
        "| **Task-Specific** | **Score (0-20)** |",
        "|---|---|",
        f"| {task_id} | {task_total} |",
        "",
        "| **Overall Evaluation** | **Value** |",
        "|---|---|",
        f"| Total Score (General + Task-Specific) | {overall} / 40 |",
    ]
    bullets = ["", "#### Notes & Suggestions"]
    for k in GENERAL_KEYS:
        if notes[k]:
            bullets.append(f"- **{k.replace('_',' ').title()}**: " + " ".join(notes[k]))

    return "\n".join(table + bullets)

def main() -> None:
    rubric = load_rubric()
    rubric_len = len(rubric)

    for folder in FOLDERS:
        files = list_changed_files(folder)
        task_id = Path(folder).name.split("-")[0] if "-" in Path(folder).name else Path(folder).name

        if not files:
            comment_on_pr(
                f"### 📝 AI Rubric Evaluation for **{folder}**\n\n"
                f"_No reviewable changes detected (non-code or unsupported file types)._"
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
        chunk_results: List[Dict[str, Any]] = []

        for chunk in chunks:
            res = safe_ai_review_json(rubric, chunk, task_id)
            chunk_results.append(res)

        agg = aggregate_results(chunk_results)
        md = render_markdown(task_id, agg)
        md = strip_overall_eval_date_row(md)

        header = f"### 📝 AI Rubric Evaluation for **{folder}** (Consolidated)\n\n"
        comment_on_pr(header + md)

if __name__ == "__main__":
    main()
