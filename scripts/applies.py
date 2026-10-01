#!/usr/bin/env python3
"""applies.py — which practices apply to a repo with these facts, in which order, and why.

The authority for selection and order (decision 0004 §5): the agent establishes the facts with evidence
(playbooks/which-practices-apply.md) or plans them (playbooks/bootstrap-new-repo.md), confirms them with Martin,
and this script turns them into the list. The agent's judgment goes into the facts and into the skip reasons, not
into re-reading the `applies-when` lines.

Usage:
  python3 scripts/applies.py llm_calls tools acts_on_world multi_tenant production personal_data regulated brownfield parallel_sessions long_tasks
  python3 scripts/applies.py llm_calls multi_tenant:planned acts_on_world:planned     # planned facts attach only day-0 practices
  python3 scripts/applies.py --explain <facts…>   # names the fact(s) that fired each practice
  python3 scripts/applies.py --shapes             # the four worked shapes of the playbook
  python3 scripts/applies.py --check              # exit 1 if a line fails to parse or the README table disagrees with a frontmatter
  python3 scripts/applies.py --json <facts…>      # machine-readable (used by make-router.py and the bootstrap)

Facts: words from practices/facts.md, optionally suffixed `:inferred` (default), `:planned` or `:asked`.
Grammar of applies-when / full-when: `always`, fact words, `and`, `or`, `not`, parentheses.
Order: practices/facts.md §Ordering — working-style in the README order, then capability practices (and the full
part of a practice with `full-when`) by stage (`when`: day-0 → first-user → at-scale) and, within a stage, by the triggering
fact: acts_on_world → personal_data / regulated → multi_tenant → production → the rest.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACT_PRIORITY = ["acts_on_world", "personal_data", "regulated", "multi_tenant", "production"]
WHEN_ORDER = {"day-0": 0, "first-user": 1, "at-scale": 2}

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


def frontmatter(name):
    path = os.path.join(ROOT, "practices", name, "README.md")
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in (m.group(1) if m else "").splitlines():
        mm = re.match(r"^([a-z-]+): *\"?([^\"#]*?)\"? *(?:#.*)?$", line)
        if mm: fm[mm.group(1)] = mm.group(2).strip()
    return fm


def variants(name):
    """{stack: status} from practices/<name>/variants/<stack>/README.md (field-tested copies, decision 0005 §7)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "practices", name, "variants", "*", "README.md"))):
        m = re.match(r"^---\n(.*?)\n---\n", open(f, encoding="utf-8").read(), re.S)
        st = re.search(r"^status: *([a-z-]+)", m.group(1), re.M) if m else None
        out[os.path.basename(os.path.dirname(f))] = st.group(1) if st else "?"
    return out


def practices():
    """Routed practices in README table order, with their frontmatter. The table is the routing gate (decision 0004 §6):
    a folder without a row is draft and unrouted."""
    out = []
    for line in open(os.path.join(ROOT, "practices", "README.md"), encoding="utf-8"):
        m = re.match(r"\| `([a-z0-9-]+)/` \| (working-style|capability) \| `([^`]+)`", line)
        if m:
            name = m.group(1); fm = frontmatter(name)
            out.append({"name": name, "kind": m.group(2), "table_applies": m.group(3), "applies": fm.get("applies-when", ""),
                        "full": fm.get("full-when"), "when": fm.get("when", "day-0"), "full_when_stage": fm.get("full-when-stage"),
                        "ref": fm.get("reference-status", "untested"), "status": fm.get("status", "draft"), "variants": variants(name)})
    return out


def tokens(expr):
    return re.findall(r"\(|\)|[a-z_]+", expr)


def evaluate(expr, facts, vocab):
    toks = tokens(expr)
    for t in toks:
        if t not in ("(", ")", "and", "or", "not", "always") and t not in vocab:
            raise ValueError(f"unknown fact word {t!r} in {expr!r}")
    py = " ".join("True" if t == "always" else t if t in ("(", ")", "and", "or", "not") else str(t in facts) for t in toks)
    return bool(eval(py, {"__builtins__": {}}, {}))  # only True/False/and/or/not/parens


def firing_facts(expr, facts):
    return [t for t in tokens(expr) if t in facts]


def rank(expr, facts):
    """Position in FACT_PRIORITY of the strongest fact that fired; len(FACT_PRIORITY) for the rest."""
    fired = firing_facts(expr, facts)
    return min((FACT_PRIORITY.index(f) for f in fired if f in FACT_PRIORITY), default=len(FACT_PRIORITY))


def parse_facts(args):
    inferred, planned = set(), set()
    for a in args:
        name, _, src = a.partition(":")
        if src not in ("", "inferred", "planned", "asked"):
            raise ValueError(f"bad fact source {src!r} in {a!r}: use fact, fact:inferred, fact:planned or fact:asked")
        (planned if src == "planned" else inferred).add(name)
    return inferred, planned


def route(args, vocab, plist):
    inferred, planned = parse_facts(args)
    allf = inferred | planned
    unknown = allf - vocab
    if unknown: raise ValueError(f"unknown facts: {sorted(unknown)}")
    rows = []
    for p in plist:
        holds = evaluate(p["applies"], allf, vocab)
        holds_inferred = evaluate(p["applies"], inferred, vocab)
        entry = {"name": p["name"], "kind": p["kind"], "when": p["when"], "ref": p["ref"], "status": p["status"], "applies_when": p["applies"], "variants": p["variants"]}
        blank = not inferred  # a blank repo: nothing inferred yet
        if not holds:
            entry["verdict"] = "skipped"; entry["why"] = f"[{p['applies']}] does not hold"
        elif not holds_inferred and p["when"] != "day-0":
            entry["verdict"] = "deferred"; entry["why"] = f"fires only on planned facts {firing_facts(p['applies'], planned)}; when={p['when']} — attaches once inferred"
        elif blank and p["when"] != "day-0":
            entry["verdict"] = "deferred"; entry["why"] = f"blank repo; when={p['when']} — install once the product has users"
        else:
            entry["verdict"] = "applies"; entry["why"] = "always" if p["applies"] == "always" else "fired by " + ", ".join(firing_facts(p["applies"], allf))
            entry["rank"] = rank(p["applies"], allf)
        if p["full"]:
            fh = evaluate(p["full"], allf, vocab); fhi = evaluate(p["full"], inferred, vocab)
            if fh and (fhi or (p["full_when_stage"] or "day-0") == "day-0"):
                entry["full"] = {"verdict": "applies", "why": "full part fired by " + ", ".join(firing_facts(p["full"], allf)), "rank": rank(p["full"], allf), "when": p["full_when_stage"] or p["when"]}
            elif fh:
                entry["full"] = {"verdict": "deferred", "why": f"full part fires only on planned facts; when={p['full_when_stage']}", "when": p["full_when_stage"]}
            else:
                entry["full"] = {"verdict": "skipped", "why": f"full part [{p['full']}] does not hold"}
        rows.append(entry)
    ws = [r for r in rows if r["verdict"] == "applies" and r["kind"] == "working-style"]
    caps = [r for r in rows if r["verdict"] == "applies" and r["kind"] == "capability"]
    fulls = [dict(r, name=r["name"] + " (full)", rank=r["full"]["rank"], why=r["full"]["why"], when=r["full"]["when"]) for r in rows if r.get("full", {}).get("verdict") == "applies"]
    second = sorted(caps + fulls, key=lambda r: (WHEN_ORDER.get(r["when"], 9), r["rank"], [p["name"] for p in plist].index(r["name"].split(" ")[0])))
    deferred = [r for r in rows if r["verdict"] == "deferred"] + [dict(r, name=r["name"] + " (full)", why=r["full"]["why"]) for r in rows if r.get("full", {}).get("verdict") == "deferred"]
    skipped = [r for r in rows if r["verdict"] == "skipped"]
    return {"facts": {"inferred": sorted(inferred), "planned": sorted(planned)}, "order": [r["name"] for r in ws] + [r["name"] for r in second],
            "working_style": ws, "capability_and_full": second, "deferred": deferred, "skipped": skipped}


def tag(r):
    name = r["name"] + (" (core)" if r.get("full") and not r["name"].endswith("(full)") else "")
    v = ("; variants: " + ", ".join(f"{k}={s}" for k, s in r["variants"].items())) if r.get("variants") else ""
    return f"{name} [{r['when']}; ref {r['ref']}{v}" + ("" if r["status"] == "current" else f"; {r['status']}") + "]"


def print_route(title, res, explain):
    print(f"\n## {title}")
    print("facts: " + " ".join(res["facts"]["inferred"]) + (("  planned: " + " ".join(res["facts"]["planned"])) if res["facts"]["planned"] else ""))
    print("order:")
    for i, r in enumerate(res["working_style"] + res["capability_and_full"], 1):
        line = f"  {i:2}. {tag(r)}"
        if explain: line += f" — {r['why']}"
        print(line)
    if res["deferred"]:
        print("deferred (planned facts attach only day-0 practices):")
        for r in res["deferred"]: print(f"  - {r['name']} — {r['why']}")
    print("skipped:")
    for r in res["skipped"]: print(f"  - {r['name']} — {r['why']}")
    for r in res["working_style"] + res["capability_and_full"]:
        if r["ref"] == "untested" and r["kind"] == "capability":
            print(f"note: {r['name']} has no field-tested reference yet — implement from its contract (## Verify) with practices/prompt-library/implement-practice.md; see practices/adoptions.md")
            break


def check(vocab, plist):
    bad = 0
    for p in plist:
        for label, e in (("applies-when", p["applies"]), ("full-when", p["full"])):
            if e is None or e == "": continue
            try: evaluate(e, set(), vocab)
            except Exception as err: print(f"  - {p['name']} {label}: {err}"); bad += 1
        if p["table_applies"] != p["applies"]:
            print(f"  - {p['name']}: README table says `{p['table_applies']}` but frontmatter says `{p['applies']}`"); bad += 1
        if p["when"] not in ("day-0", "first-user", "at-scale"):
            print(f"  - {p['name']}: when must be day-0|first-user|at-scale (got {p['when']!r})"); bad += 1
    # the ordering rule in facts.md names the working-style order; it must match the README table order
    facts_md = open(os.path.join(ROOT, "practices", "facts.md"), encoding="utf-8").read()
    m = re.search(r"Working-style practices first: (.+?)\n", facts_md)
    if m:
        listed = re.findall(r"`([a-z0-9-]+)`", m.group(1))
        table = [p["name"] for p in plist if p["kind"] == "working-style"]
        if listed != table:
            print(f"  - practices/facts.md §Ordering lists {listed} but practices/README.md table order is {table}"); bad += 1
    return bad


def main():
    args = sys.argv[1:]
    vocab = facts_vocabulary(); plist = practices()
    if "--check" in args:
        sys.exit(1 if check(vocab, plist) else 0)
    explain = "--explain" in args; as_json = "--json" in args
    facts_args = [a for a in args if not a.startswith("--")]
    shapes = SHAPES if "--shapes" in args else {"given facts": " ".join(facts_args)}
    out = {}
    for title, fstr in shapes.items():
        try: res = route(fstr.split(), vocab, plist)
        except ValueError as e: print(e); sys.exit(1)
        out[title] = res
        if not as_json: print_route(title, res, explain)
    if as_json: print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
