#!/usr/bin/env python3
"""applies.py — which practices does practices/README.md say apply to a repo with these facts?

A helper and a consistency check, not the authority: the agent still infers the facts with evidence,
confirms them with Martin and writes a repo-specific reason for every skipped practice
(playbooks/which-practices-apply.md). This script only evaluates the `applies-when` lines mechanically,
so that the worked examples in the playbook cannot drift from the practices again (they did between
2026-09-26 and 2026-09-30, when three practices and two facts were added).

Usage:
  python3 scripts/applies.py llm_calls tools acts_on_world multi_tenant production personal_data regulated brownfield parallel_sessions long_tasks
  python3 scripts/applies.py --shapes          # evaluate the four worked shapes used in the playbook
  python3 scripts/applies.py --check           # exit 1 if any applies-when line fails to parse (used by kb-check.sh)

Grammar of applies-when: `always`, fact words from practices/facts.md, `and`, `or`, `not`, parentheses.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHAPES = {
    "A multi-tenant agent SaaS acting on the world (AI SDR)": "llm_calls exposes_tools acts_on_world multi_tenant production personal_data regulated brownfield parallel_sessions long_tasks",
    "B scheduled LLM publishing pipeline (Content Central)": "llm_calls acts_on_world production brownfield",
    "C content/marketing site, no LLM at runtime": "production brownfield",
    "D payments/fintech, LLM facts as found": "regulated personal_data production multi_tenant brownfield",
}

def facts_vocabulary():
    words = set()
    for line in open(os.path.join(ROOT, "practices", "facts.md"), encoding="utf-8"):
        m = re.match(r"\| `([a-z_]+)` \|", line)
        if m: words.add(m.group(1))
    return words

def practices():
    """(name, kind, applies-when) from practices/README.md, in table order."""
    out = []
    for line in open(os.path.join(ROOT, "practices", "README.md"), encoding="utf-8"):
        m = re.match(r"\| `([a-z0-9-]+)/` \| (working-style|capability) \| `([^`]+)` \|", line)
        if m: out.append(m.groups())
    return out

def evaluate(expr, facts, vocab):
    tokens = re.findall(r"\(|\)|[a-z_]+", expr)
    for t in tokens:
        if t not in ("(", ")", "and", "or", "not", "always") and t not in vocab:
            raise ValueError(f"unknown fact word {t!r} in {expr!r}")
    py = " ".join("True" if t == "always" else t if t in ("(", ")", "and", "or", "not") else str(t in facts) for t in tokens)
    return bool(eval(py, {"__builtins__": {}}, {}))  # expression contains only True/False/and/or/not/parens

def main():
    args = sys.argv[1:]
    vocab = facts_vocabulary(); plist = practices()
    if "--check" in args:
        bad = 0
        for name, kind, expr in plist:
            try: evaluate(expr, set(), vocab)
            except Exception as e: print(f"  - {name}: {e}"); bad += 1
        sys.exit(1 if bad else 0)
    shapes = SHAPES if "--shapes" in args else {"given facts": " ".join(args)}
    for title, fstr in shapes.items():
        facts = set(fstr.split())
        unknown = facts - vocab
        if unknown: print(f"unknown facts: {sorted(unknown)}"); sys.exit(1)
        applies = [(n, k) for n, k, e in plist if evaluate(e, facts, vocab)]
        skipped = [(n, e) for n, k, e in plist if not evaluate(e, facts, vocab)]
        print(f"\n## {title}\nfacts: {' '.join(sorted(facts))}")
        print("applies (working-style): " + ", ".join(n for n, k in applies if k == "working-style"))
        print("applies (capability):    " + (", ".join(n for n, k in applies if k == "capability") or "—"))
        print("skipped:                 " + (", ".join(f"{n} [{e}]" for n, e in skipped) or "—"))

if __name__ == "__main__":
    main()
