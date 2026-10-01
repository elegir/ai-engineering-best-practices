#!/usr/bin/env python3
"""check-practices.py — the two structural checks decision 0005 adds to kb-check.

Default: every routed practice (a folder with a row in practices/README.md) has the mandatory headings in order,
`reference-status` in its frontmatter, and a Verify section whose assertion lines parse as
  N. <assertion> — observer: script|agent|Martin — negative: <text> [— framework: beats|bends]
Lines before the first numbered assertion are free prose; a paragraph starting with "**Example commands"
ends the contract and is exempt; bullet lines ("- ") inside the contract are rejected (they were the old vibes).
A second, lexical net flags stack commands inside assertions.

--variants: every practices/<name>/variants/<stack>/README.md (or variants/<stack>.md with frontmatter) declares
status, verified-against and field-report, and verified-against is not older than the practice's last-reviewed.
Exit 1 on any problem; problems printed as "  - ...".
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "practices")
HEADINGS = ["Solves", "Applies when", "Does not apply when", "Files in this folder", "Reference implementation",
            "Stack-sensitive points", "Adapt", "Verify", "Sources", "Change log"]
ASSERT = re.compile(r"^\d+\. .+ — observer: (script|agent|Martin) — negative: .+?( — framework: (beats|bends))?$")
STACKY = re.compile(r"\b(npx|npm|pip|pip-audit|pytest|composer|vendor/bin|phpunit|pest|ruff|biome|playwright|python3)\b|src/|`/(context|ask-expert|audit|lesson|plan-ticket|develop-task|start-session|end-session)`")

def routed():
    for line in open(os.path.join(P, "README.md"), encoding="utf-8"):
        m = re.match(r"\| `([a-z0-9-]+)/` \|", line)
        if m: yield m.group(1)

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^([a-z-]+): *\"?([^\"\n#]*?)\"? *(?:#.*)?$", m.group(1), re.M)) if m else {}

def check_practice(name):
    probs = []
    path = os.path.join(P, name, "README.md")
    text = open(path, encoding="utf-8").read()
    fm = frontmatter(text)
    if fm.get("reference-status") not in ("untested", "field-tested", "reference"):
        probs.append(f"{name}: reference-status missing or not untested|field-tested|reference")
    heads = re.findall(r"^## (.+)$", text, re.M)
    idx = [heads.index(h) if h in heads else -1 for h in HEADINGS]
    missing = [h for h, i in zip(HEADINGS, idx) if i < 0]
    if missing: probs.append(f"{name}: missing section(s) {missing}")
    present = [i for i in idx if i >= 0]
    if present != sorted(present): probs.append(f"{name}: sections out of order (expected {HEADINGS})")
    m = re.search(r"^## Verify\n(.*?)(?=^## )", text, re.M | re.S)
    if not m: return probs
    body = m.group(1)
    contract = body.split("**Example commands")[0]
    n = 0
    for line in contract.splitlines():
        if re.match(r"^\d+\. ", line):
            n += 1
            if not ASSERT.match(line.rstrip()):
                probs.append(f"{name}: Verify line does not parse: {line[:70]}…")
            elif STACKY.search(line):
                probs.append(f"{name}: stack-specific command inside an assertion: {line[:70]}…")
        elif line.startswith("- "):
            probs.append(f"{name}: bullet inside the Verify contract (use a numbered assertion): {line[:60]}…")
    if n == 0: probs.append(f"{name}: Verify has no numbered assertion")
    return probs

def check_variants():
    probs = []
    for name in routed():
        pr = frontmatter(open(os.path.join(P, name, "README.md"), encoding="utf-8").read())
        vdir = os.path.join(P, name, "variants")
        if not os.path.isdir(vdir): continue
        for entry in sorted(os.listdir(vdir)):
            f = os.path.join(vdir, entry, "README.md") if os.path.isdir(os.path.join(vdir, entry)) else os.path.join(vdir, entry)
            if not f.endswith(".md") or not os.path.exists(f): continue
            fm = frontmatter(open(f, encoding="utf-8").read())
            if not fm: continue  # legacy stack-notes without frontmatter are notes, not variants
            rel = os.path.relpath(f, ROOT)
            for k in ("status", "verified-against", "field-report"):
                if k not in fm: probs.append(f"{rel}: missing {k}")
            if fm.get("status") not in (None, "field-tested", "reference"):
                probs.append(f"{rel}: status must be field-tested|reference")
            if fm.get("verified-against") and pr.get("last-reviewed") and fm["verified-against"] < pr["last-reviewed"]:
                probs.append(f"{rel}: verified-against {fm['verified-against']} is older than the practice's last-reviewed {pr['last-reviewed']} — re-verify or mark stale")
    return probs

if __name__ == "__main__":
    probs = check_variants() if "--variants" in sys.argv else [p for n in routed() for p in check_practice(n)]
    for p in probs: print("  -", p)
    sys.exit(1 if probs else 0)
