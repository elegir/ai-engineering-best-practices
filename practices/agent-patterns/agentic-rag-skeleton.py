"""agentic-rag-skeleton.py — agentic retrieval over a folder of markdown with three bounded tools.

Copy to <repo>/src/<feature>/agentic_rag.py. Set NOTES_DIR. Requires ripgrep (`rg`) in PATH
(brew install ripgrep / apt install ripgrep / choco install ripgrep) and the agent loop from
agent-loop-skeleton.py (imported as `run_agent` — adapt to your framework).

Why this shape (principles/21 §3.6): the same list / search / read primitives every coding agent uses
over a codebase work over any corpus; the loop lets the model retry a search that missed; the output
carries citations so downstream code and users can verify. Semantic RAG remains the better choice when
latency or cost dominate.

Production rules baked in: paths confined to NOTES_DIR; max results, max lines, max chars; errors
returned as text; relative paths to save tokens; ripgrep respects .gitignore and skips hidden files.
"""
from __future__ import annotations
import json, re, shutil, subprocess
from pathlib import Path

NOTES_DIR = Path("<<NOTES_DIR>>").resolve()   # e.g. Path(__file__).parent / "notes"
MAX_GREP_RESULTS = 40
MAX_READ_LINES = 200
MAX_LIST = 200

def _safe(rel: str) -> Path | None:
    p = (NOTES_DIR / rel).resolve()
    return p if p.is_relative_to(NOTES_DIR) else None

def list_files(pattern: str = "**/*.md") -> str:
    """List the documents available, one relative path per line (max 200).
    PATTERN is a glob relative to the notes folder, e.g. "runbooks/*.md". Use this first when you do
    not know the file names. Returns "error: ..." if the pattern is invalid."""
    try:
        paths = sorted(p.relative_to(NOTES_DIR).as_posix() for p in NOTES_DIR.glob(pattern) if p.is_file())
    except Exception as e:
        return f"error: invalid pattern: {e}"
    if not paths:
        return "error: no files match; try list_files('**/*.md')"
    return "\n".join(paths[:MAX_LIST]) + ("\n... (truncated)" if len(paths) > MAX_LIST else "")

def grep(pattern: str) -> str:
    """Search all documents for a regular expression (case-insensitive) and return matching lines as
    "path:line: text" (max 40). Use specific terms (names, ids, error codes) rather than whole questions;
    if nothing matches, try a shorter or alternative term. Returns "error: ..." if the regex is invalid."""
    try:
        re.compile(pattern)
    except re.error as e:
        return f"error: invalid regex: {e}"
    if shutil.which("rg") is None:
        return "error: ripgrep (rg) is not installed on this machine"
    try:
        proc = subprocess.run(
            ["rg", "--line-number", "--ignore-case", "--no-heading", "--color", "never",
             "--max-count", "20", "--glob", "*.md", "-e", pattern, "."],
            cwd=NOTES_DIR, capture_output=True, text=True, timeout=20,
        )
    except subprocess.TimeoutExpired:
        return "error: search timed out; use a more specific term"
    if proc.returncode == 1:
        return "error: no matches; try a shorter or different term"
    if proc.returncode not in (0, 1):
        return f"error: search failed: {proc.stderr.strip()[:200]}"
    lines = [l[2:] if l.startswith("./") else l for l in proc.stdout.splitlines()]
    return "\n".join(lines[:MAX_GREP_RESULTS]) + ("\n... (truncated)" if len(lines) > MAX_GREP_RESULTS else "")

def read_file(path: str, start_line: int = 1) -> str:
    """Read up to 200 lines of one document, starting at START_LINE (1-based), with line numbers.
    PATH is a relative path exactly as returned by list_files or grep. Call again with a later
    START_LINE to continue. Returns "error: ..." if the file is outside the notes folder or missing."""
    p = _safe(path)
    if p is None:
        return "error: path is outside the notes folder"
    if not p.is_file():
        return f"error: file not found: {path}"
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(1, int(start_line))
    chunk = lines[start - 1 : start - 1 + MAX_READ_LINES]
    out = "\n".join(f"{start + i}: {l}" for i, l in enumerate(chunk))
    if start - 1 + MAX_READ_LINES < len(lines):
        out += f"\n... (file continues; call read_file('{path}', {start + MAX_READ_LINES}))"
    return out

TOOLS = {"list_files": list_files, "grep": grep, "read_file": read_file}

SYSTEM_PROMPT = """You answer questions using only the documents available through your tools.
Search before answering; read the relevant file around each match; if a search misses, try another term.
Answer in this JSON shape and nothing else:
{"answer": "<plain English>", "citations": [{"file": "<relative path>", "line": <int>, "quote": "<exact text>"}]}
If the documents do not contain the answer, say so in "answer" and return an empty citations list."""

if __name__ == "__main__":
    import sys
    # Wire TOOLS and SYSTEM_PROMPT into agent-loop-skeleton.run_agent (or your framework), e.g.:
    #   from agent_loop import run_agent; print(run_agent(question, debug=True))
    print(json.dumps({"tools": list(TOOLS), "notes_dir": str(NOTES_DIR)}, indent=1))
    print("Wire these tools into your agent loop; see the module docstring.", file=sys.stderr)
