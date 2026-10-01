#!/usr/bin/env python3
"""guard.py — the one hook script for Claude Code: protect files, block dangerous commands,
format + lint after edits, refuse to stop with red tests. Standard library only (Python >= 3.8).

Wire it in .claude/settings.json as  "<<PYTHON>> .claude/hooks/guard.py <event> || exit 2"
so that a missing interpreter BLOCKS (exit 2) instead of letting the action through — Claude Code treats any
other non-zero exit as a non-blocking error (decision 0005 §6 in the AI-engineering KB).

Events (first argument):
  pre-edit    PreToolUse  Write|Edit|MultiEdit   -> exit 2 if the file is protected
  pre-bash    PreToolUse  Bash                   -> exit 2 if the command matches a deny pattern
  post-edit   PostToolUse Write|Edit|MultiEdit   -> format, lint, return remaining violations as context
  stop        Stop                               -> block the stop while the fast test command fails
  --selftest  run by the entry-file startup routine; exit 0 = the guard is alive and configured

Config: .claude/hooks.json next to this folder (see hooks.json in the practice). The guard refuses to run —
exit 2, every event — while the config still contains an unreplaced <<PLACEHOLDER>>, so a half-adapted copy
cannot silently pass. Every unexpected error also exits 2: this script fails closed.
"""

import json, os, re, shlex, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(os.path.dirname(HERE), "hooks.json")  # .claude/hooks.json


def die(msg, code=2):
    sys.stderr.write("guard: " + msg + "\n")
    sys.exit(code)


def load_config():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        die(f"cannot read {CONFIG_PATH}: {e} (the guard fails closed)")
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError as e:
        die(f"{CONFIG_PATH} is not valid JSON: {e}")

    def walk(v):  # every string value outside "_comment"-style keys
        if isinstance(v, dict):
            return [
                x
                for k, val in v.items()
                if not str(k).startswith("_")
                for x in walk(val)
            ]
        if isinstance(v, list):
            return [x for val in v for x in walk(val)]
        return [v] if isinstance(v, str) else []

    left = [v for v in walk(cfg) if "<<" in v]
    if left:
        die(
            f"{CONFIG_PATH} still contains {len(left)} unreplaced placeholder(s), e.g. {left[0][:60]!r}; adapt it (practice hooks-and-guards, §Adapt) — every action is blocked until then"
        )
    for key in (
        "protected_paths",
        "deny_commands",
        "format",
        "lint",
        "stop_test_command",
    ):
        if key not in cfg:
            die(f"{CONFIG_PATH} is missing '{key}'")
    try:
        cfg["_protected"] = [re.compile(p) for p in cfg["protected_paths"]]
        cfg["_deny"] = [re.compile(p, re.I) for p in cfg["deny_commands"]]
    except re.error as e:
        die(f"bad regex in {CONFIG_PATH}: {e}")
    return cfg


def read_event():
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except json.JSONDecodeError as e:
        die(f"hook input is not JSON: {e}")


def tool_input(ev):
    return ev.get("tool_input") or {}


def pre_edit(cfg, ev):
    path = tool_input(ev).get("file_path") or ""
    if not path:
        return
    norm = path.replace("\\", "/")
    for rx in cfg["_protected"]:
        if rx.search(norm):
            die(
                f"BLOCKED: '{path}' is protected (pattern {rx.pattern!r}). Ask Martin to change it by hand and explain why."
            )


def pre_bash(cfg, ev):
    cmd = tool_input(ev).get("command") or ""
    if not cmd:
        return
    for rx in cfg["_deny"]:
        if rx.search(cmd):
            die(
                f"BLOCKED: command matches forbidden pattern {rx.pattern!r}. If it is really needed, stop and ask Martin to run it."
            )


def run(cmd, timeout):
    """Run a command string; returns (exit_code, combined_output). A missing tool is an error, not a pass."""
    try:
        p = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s: {cmd}"


def post_edit(cfg, ev):
    path = tool_input(ev).get("file_path") or ""
    if not path or not os.path.isfile(path):
        return
    ext = os.path.splitext(path)[1].lower()
    fmt, lint = cfg["format"].get(ext), cfg["lint"].get(ext)
    if not fmt and not lint:
        return
    q = (
        f'"{path}"' if os.name == "nt" else shlex.quote(path)
    )  # cmd.exe does not understand POSIX quotes
    if fmt:
        run(fmt.replace("{file}", q), cfg.get("tool_timeout_seconds", 60))
    if lint:
        code, out = run(lint.replace("{file}", q), cfg.get("tool_timeout_seconds", 60))
        if code != 0:
            ctx = f"Lint violations remain in {path} after auto-format. Fix them now (do not disable rules):\n{out[-4000:]}"
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "additionalContext": ctx,
                        }
                    }
                )
            )


def stop(cfg, ev):
    if ev.get("stop_hook_active"):
        return  # already ran once for this stop; let the session end
    cmd = cfg["stop_test_command"]
    code, out = run(cmd, cfg.get("stop_timeout_seconds", 90))
    low = out.lower()
    if code == 127 or (
        code != 0
        and (
            "command not found" in low
            or "is not recognized as an internal or external command" in low
        )
    ):
        die(
            f"the stop test command could not run ({cmd!r}): {out.strip()[:200]} — fix the command in hooks.json; the session cannot end until the sensor works"
        )
    if code != 0:
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": "Tests are failing; you cannot declare the task done. Fix them, then stop again. Last lines:\n"
                    + "\n".join(out.splitlines()[-40:]),
                }
            )
        )


def selftest(cfg):
    problems = []
    # 1. every tool referenced in the config resolves on this machine
    for name, cmd in (
        list(cfg["format"].items())
        + list(cfg["lint"].items())
        + [("stop", cfg["stop_test_command"])]
    ):
        first = shlex.split(cmd.replace("{file}", "x"))[0] if cmd.strip() else ""
        if first and not (shutil.which(first) or os.path.exists(first)):
            problems.append(f"tool not found for {name!r}: {first}")
    # 2. the guard blocks what it must
    for rx, sample in (
        (cfg["_protected"], ".env"),
        (cfg["_protected"], "/repo/.env.production"),
        (cfg["_protected"], ".claude/hooks/guard.py"),
    ):
        if not any(r.search(sample) for r in rx):
            problems.append(f"protected_paths does not cover {sample!r}")
    for sample in (
        "git push --force origin main",
        "git commit -m x --no-verify",
        "rm -rf /",
    ):
        if not any(r.search(sample) for r in cfg["_deny"]):
            problems.append(f"deny_commands does not cover {sample!r}")
    if problems:
        for p in problems:
            sys.stderr.write("guard selftest: " + p + "\n")
        sys.exit(1)
    print(
        f"guard selftest OK — python {sys.version.split()[0]}, config {CONFIG_PATH}, {len(cfg['_protected'])} protected patterns, {len(cfg['_deny'])} deny patterns, stop command {cfg['stop_test_command']!r}"
    )


def main():
    if len(sys.argv) < 2:
        die("usage: guard.py pre-edit|pre-bash|post-edit|stop|--selftest")
    event = sys.argv[1]
    cfg = load_config()
    if event == "--selftest":
        return selftest(cfg)
    ev = read_event()
    try:
        {
            "pre-edit": pre_edit,
            "pre-bash": pre_bash,
            "post-edit": post_edit,
            "stop": stop,
        }[event](cfg, ev)
    except KeyError:
        die(f"unknown event {event!r}")
    except SystemExit:
        raise
    except Exception as e:  # anything unexpected blocks rather than passes
        die(f"internal error ({type(e).__name__}: {e}); failing closed")


if __name__ == "__main__":
    main()
