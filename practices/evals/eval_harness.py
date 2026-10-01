"""eval_harness.py — the ONE place where tasks are run, graded, aggregated and where a judge is calibrated.

Copy to <repo>/evals/harness.py. Replace <<JUDGE_MODEL>> and <<JUDGE_CLIENT_IMPORT>>; point `make_env()` and
`run_agent()` at the product. Nothing else in the repo grades model output: a CI job and the production-sample
job both call this module, so the numbers they report are computed by the same code.

What this buys you (principles/14-evals-and-error-analysis.md):
  * tasks are DATA (JSONL: input, expected outcome or assertions, reference solution)   -> anyone can add one as a PR
  * every trial starts from a clean environment                                        -> no correlated failures from shared state
  * graders are BINARY and one per failure mode: code assertions where code can decide,
    an LLM judge otherwise, returning pass / fail / unknown with its reasoning FIRST     -> no 3.7-out-of-5 nobody can explain
  * k trials per task, reported as pass^k (all k succeed) AND the worst case             -> a mean cannot hide a failed run
  * a judge-calibration check against human labels on a held-out set printing TPR, TNR,
    Cohen's kappa and the confusion matrix, refusing to report agreement alone           -> "it agrees 75 %" is a smell, not a number
  * the judge model and the judge prompt version are recorded with every run            -> a changed judge is a changed instrument

Vocabulary (Anthropic, "Demystifying evals for AI agents", 2026-01-09): a TASK is inputs + success criteria; a TRIAL is one
attempt (run several); a GRADER scores one aspect; the TRANSCRIPT is the full record; the OUTCOME is the final state.
pass@k = at least one of k trials passes (rises with k); pass^k = all k pass (falls with k): 0.75 per trial over 3 is 0.42.
Calibration rule (Husain 2024; Yan 2024-08; Lucas 2026-07): a judge is a classifier — report TPR and TNR (or kappa) on a
HELD-OUT labelled split, never raw agreement, because a judge that always says "pass" agrees 90 % of the time on a set with
10 % failures. Pin the judge model and prompt once calibrated; re-calibrate when either changes.

Branches every demo run exercises (recorded in the practice's change log):
  code grader pass / fail; LLM judge pass / fail / unknown; a flaky task where pass@k = 1 and pass^k = 0 with the worst
  case printed; a broken task (reference solution fails -> flagged, not counted as agent failure); partial credit on a
  multi-part task; calibration: TPR, TNR, kappa and the 2x2 matrix computed by hand against a labelled set that includes
  an `unknown` verdict (counted as abstention, excluded from the matrix); the floor check that exits non-zero; a judge whose
  recorded model differs from the configured one (refused); a judge file with no calibration record, with placeholder
  values, reporting agreement only, with rates below the floors, or with a placeholder model id (each refused before any call).

Python idioms, not required (decision 0005 §3): dataclasses, the JSONL loader, the `Judge` protocol. Any stack satisfies
the contract by keeping tasks as data, trials isolated, verdicts binary-with-unknown, pass^k reported, and the
calibration record next to the judge prompt. Requires: Python 3.10+ and `pydantic` (for the judge's typed verdict only).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Literal, Protocol

try:
    from pydantic import BaseModel, ConfigDict, ValidationError
except ImportError:  # pragma: no cover — the harness still runs code graders; the judge needs pydantic
    BaseModel = object  # type: ignore
    ConfigDict = dict  # type: ignore
    ValidationError = ValueError  # type: ignore

JUDGE_MODEL = "<<JUDGE_MODEL>>"       # the pinned judge; eval-policy.md records why and since when
JUDGE_TEMPERATURE = 0.0               # deterministic as far as the provider allows; the calibration record assumes it
PASS_K_FLOOR = 1.0                    # regression suite: every task must pass all k trials (eval-policy.md may lower it per suite)
TPR_FLOOR = 0.80                      # calibration floors; eval-policy.md owns the numbers — these are the defaults it starts from
TNR_FLOOR = 0.80
KAPPA_FLOOR = 0.60                    # Yan (2024-08): 80 % agreement was kappa 0.62 — the floor is on kappa, not agreement

Verdict = Literal["pass", "fail", "unknown"]


# --- 1. Tasks are data --------------------------------------------------------------------------------------------
@dataclass
class Task:
    """One row of tasks.jsonl. `expected` is the outcome the grader checks (state or output); `assertions` are code
    graders; `judge` names the failure-mode judge file (one per failure mode); `reference` is a solution that must pass."""
    id: str
    input: str
    expected: dict[str, Any] = field(default_factory=dict)
    assertions: list[dict[str, Any]] = field(default_factory=list)
    judge: str | None = None
    reference: str | None = None
    parts: int = 1  # multi-part tasks give partial credit per part (Anthropic 2026-01); 1 = all or nothing


def load_tasks(path: str) -> list[Task]:
    tasks = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                tasks.append(Task(**json.loads(line)))
    return tasks


# --- 2. Isolated trials ------------------------------------------------------------------------------------------
def make_env(task: Task) -> dict[str, Any]:
    """A CLEAN environment per trial: fresh database, fresh temp dir, fresh fixtures. Shared state is how one trial's
    leftovers (files, git history, cached answers) leak into the next and correlate failures — Anthropic 2026-01 saw a model
    read 'the git history from previous trials'. Replace with the product's setup; must be cheap enough to run 5x per task."""
    return {"task_id": task.id, "state": {}}


def run_agent(task: Task, env: dict[str, Any]) -> str:
    """Call the product (the real agent, workflow or prompt). Returns the transcript or final output; the OUTCOME is read from
    `env['state']` by the graders. <<replace with the product's entry point>>"""
    raise NotImplementedError("point run_agent at the product; the demo injects its own")


# --- 3. Graders: code first, judge where code cannot decide -------------------------------------------------------
def code_grade(task: Task, output: str, env: dict[str, Any]) -> tuple[Verdict, str, int, int]:
    """Code graders: deterministic checks on the outcome (state) or the output. Each assertion is one failure mode.
    Supported kinds: equals / contains / regex / max_len on `output`, and state_equals on `env['state'][key]`.
    Returns (verdict, reason, failed_checks, total_checks) — the counts feed partial credit on multi-part tasks."""
    reasons = []
    for a in task.assertions:
        kind = a["kind"]
        if kind == "equals" and output.strip() != a["value"]:
            reasons.append(f"equals: expected {a['value']!r}, got {output.strip()!r}")
        elif kind == "contains" and a["value"] not in output:
            reasons.append(f"contains: {a['value']!r} missing")
        elif kind == "regex" and not re.search(a["value"], output):
            reasons.append(f"regex: {a['value']!r} did not match")
        elif kind == "max_len" and len(output) > a["value"]:
            reasons.append(f"max_len: {len(output)} > {a['value']}")
        elif kind == "state_equals" and env["state"].get(a["key"]) != a["value"]:
            reasons.append(f"state[{a['key']}]: expected {a['value']!r}, got {env['state'].get(a['key'])!r}")
    for key, value in task.expected.items():  # outcome check: the environment's final state, not what the agent SAID
        if env["state"].get(key) != value:
            reasons.append(f"outcome {key}: expected {value!r}, got {env['state'].get(key)!r}")
    total = len(task.assertions) + len(task.expected)
    return ("pass", "all code checks held", 0, total) if not reasons else ("fail", "; ".join(reasons), len(reasons), total)


class JudgeVerdict(BaseModel):  # type: ignore[misc]
    """Reasoning FIRST, then the verdict (Yan 2024-08: without reasoning the judge was 'just not usable'; Anthropic's
    docs page 'Define success criteria / build evaluations', read 2026-10-01: 'reason first… and then discard the
    reasoning'). `unknown` is the out (Anthropic's agents post, 2026-01: 'give the LLM a way out')."""
    model_config = ConfigDict(extra="forbid")
    reasoning: str
    verdict: Verdict


class Judge(Protocol):
    def __call__(self, prompt: str, output: str) -> str: ...  # returns the model's text; parsed into JudgeVerdict here


@dataclass
class JudgeSpec:
    """Parsed header of a judge prompt file (judge-prompt-template.md): the instrument's identity AND its calibration record.
    A judge with no record, a record with placeholders, a record reporting agreement only (no TPR+TNR and no kappa), or
    numbers below the floors is refused before a single call — README assertion 4's negatives, enforced here.
    `--calibrate` is the one path that loads a judge WITHOUT a record (it is producing one): `require_record=False`."""
    path: str
    failure_mode: str
    model: str
    version: str
    prompt: str
    calibrated: str = ""
    calibration_set: str = ""
    tpr: float | None = None
    tnr: float | None = None
    kappa: float | None = None

    @classmethod
    def load(cls, path: str, require_record: bool = True) -> "JudgeSpec":
        text = open(path, encoding="utf-8").read()
        keys = "model|version|failure-mode|calibrated|calibration-set|tpr|tnr|kappa"
        head = {m.group(1): m.group(2).strip() for m in re.finditer(rf"^({keys}): *(.+)$", text, re.M)}
        missing = [k for k in ("model", "version", "failure-mode") if k not in head]
        if missing:
            raise ValueError(f"{path}: judge header missing {missing} (see judge-prompt-template.md)")
        if head["model"].startswith("<<"):
            raise ValueError(f"{path}: judge model is still the placeholder {head['model']!r}")

        def num(k: str) -> float | None:
            v = head.get(k)
            if v is None or v.startswith("<<"):
                return None
            return float(v)

        spec = cls(path, head["failure-mode"], head["model"], head["version"], text,
                   calibrated=head.get("calibrated", ""), calibration_set=head.get("calibration-set", ""),
                   tpr=num("tpr"), tnr=num("tnr"), kappa=num("kappa"))
        if require_record:
            problems = []
            if not spec.calibrated or spec.calibrated.startswith("<<"):
                problems.append("no `calibrated` date")
            if not spec.calibration_set or spec.calibration_set.startswith("<<"):
                problems.append("no `calibration-set` (the held-out labelled file)")
            has_rates = spec.tpr is not None and spec.tnr is not None
            if not has_rates and spec.kappa is None:
                problems.append("no TPR+TNR and no kappa (agreement alone is not a calibration record)")
            if has_rates and (spec.tpr < TPR_FLOOR or spec.tnr < TNR_FLOOR):
                problems.append(f"TPR {spec.tpr} / TNR {spec.tnr} below the floors {TPR_FLOOR} / {TNR_FLOOR}")
            if spec.kappa is not None and spec.kappa < KAPPA_FLOOR:
                problems.append(f"kappa {spec.kappa} below the floor {KAPPA_FLOOR}")
            if problems:
                raise ValueError(f"{path}: judge refused — " + "; ".join(problems) + " (README assertion 4; run --calibrate)")
        return spec


def judge_grade(spec: JudgeSpec, judge: Judge, output: str, configured_model: str = JUDGE_MODEL) -> tuple[Verdict, str]:
    if spec.model != configured_model:
        raise RuntimeError(f"judge {spec.path} was calibrated on {spec.model!r} but the harness is configured for "
                           f"{configured_model!r}: recalibrate (practices/evals/README.md assertion 4)")
    raw = judge(spec.prompt, output)
    try:
        v = JudgeVerdict.model_validate_json(raw)
    except (ValidationError, ValueError) as e:
        return "unknown", f"judge output did not parse as {{reasoning, verdict}}: {str(e)[:80]}"
    return v.verdict, v.reasoning


# --- 4. k trials, pass^k, worst case -------------------------------------------------------------------------------
@dataclass
class TrialResult:
    verdict: Verdict
    credit: float          # 1.0 pass, 0.0 fail, fraction for partial credit on multi-part tasks
    reason: str
    transcript: str


@dataclass
class TaskReport:
    task_id: str
    trials: list[TrialResult]
    broken: bool = False   # the reference solution failed its own graders: a task problem, not an agent problem

    @property
    def pass_at_k(self) -> bool: return any(t.verdict == "pass" for t in self.trials)
    @property
    def pass_pow_k(self) -> bool: return all(t.verdict == "pass" for t in self.trials)
    @property
    def worst(self) -> TrialResult: return min(self.trials, key=lambda t: t.credit)
    @property
    def credit(self) -> float:
        """Mean partial credit over the trials — a diagnostic for multi-part tasks, NOT the reported number (pass^k is)."""
        return sum(t.credit for t in self.trials) / len(self.trials)


def grade(task: Task, output: str, env: dict[str, Any], judge: Judge | None, judges_dir: str,
          configured_model: str = JUDGE_MODEL) -> TrialResult:
    verdict, reason, failed, total = code_grade(task, output, env)
    credit = 1.0 if verdict == "pass" else 0.0
    if task.parts > 1 and verdict == "fail" and total:  # partial credit: fraction of checks that held (counted, not parsed)
        credit = (total - failed) / total
    if verdict == "pass" and task.judge and judge is not None:
        if BaseModel is object:  # pydantic missing: code graders ran; the judge cannot parse a typed verdict
            return TrialResult("unknown", 0.0, "judge skipped: pydantic not installed (code graders passed)", output)
        spec = JudgeSpec.load(os.path.join(judges_dir, task.judge))
        verdict, reason = judge_grade(spec, judge, output, configured_model)
        credit = 1.0 if verdict == "pass" else 0.0  # `unknown` is NOT a pass: it is counted and read by a human
    return TrialResult(verdict, credit, reason, output)


def run_suite(tasks: Iterable[Task], k: int, agent: Callable[[Task, dict[str, Any]], str], judge: Judge | None,
              judges_dir: str = "evals/judges", configured_model: str = JUDGE_MODEL) -> list[TaskReport]:
    reports = []
    for task in tasks:
        broken = False
        if task.reference is not None:  # the reference solution must pass the graders, or the task is broken
            env = make_env(task)
            env["state"].update(task.expected)  # a reference solution reaches the expected outcome by definition
            ref = grade(task, task.reference, env, judge, judges_dir, configured_model)
            broken = ref.verdict != "pass"
        trials = []
        for _ in range(k):
            env = make_env(task)        # clean per trial — never reuse `env`
            output = agent(task, env)
            trials.append(grade(task, output, env, judge, judges_dir, configured_model))
        reports.append(TaskReport(task.id, trials, broken))
    return reports


def print_report(reports: list[TaskReport], k: int, judge_models: dict[str, str]) -> bool:
    ok = True
    print(f"\n== suite: {len(reports)} tasks x {k} trials; judges: {judge_models or 'code only'}")
    print(f"{'task':<22}{'pass@k':>8}{'pass^k':>8}{'credit':>7}  worst case   (credit = mean partial credit, diagnostic only; pass^k is the number)")
    for r in reports:
        flag = "BROKEN TASK (reference solution fails its graders — fix the task, Anthropic 2026-01)" if r.broken else ""
        print(f"{r.task_id:<22}{str(r.pass_at_k):>8}{str(r.pass_pow_k):>8}{r.credit:>7.2f}  "
              f"{r.worst.verdict}: {r.worst.reason[:70]} {flag}")
        if r.broken:
            continue  # not counted against the agent, but reported loudly
        if not r.pass_pow_k:
            ok = False
    unknowns = sum(1 for r in reports for t in r.trials if t.verdict == "unknown")
    rate = sum(1 for r in reports if r.pass_pow_k and not r.broken) / max(1, sum(1 for r in reports if not r.broken))
    print(f"pass^k rate {rate:.2f} (floor {PASS_K_FLOOR}); unknown verdicts {unknowns} (each one is read by a human)")
    return ok and rate >= PASS_K_FLOOR


# --- 5. Calibration: the judge is a classifier --------------------------------------------------------------------
@dataclass
class Calibration:
    tp: int = 0; tn: int = 0; fp: int = 0; fn: int = 0; unknown: int = 0
    # positive class = "fail" (the failure mode IS present): a judge exists to catch failures, so TPR is "of the real
    # failures, how many did it catch" and TNR is "of the good outputs, how many did it leave alone".

    @property
    def n(self) -> int: return self.tp + self.tn + self.fp + self.fn
    @property
    def tpr(self) -> float: return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else float("nan")
    @property
    def tnr(self) -> float: return self.tn / (self.tn + self.fp) if (self.tn + self.fp) else float("nan")
    @property
    def agreement(self) -> float: return (self.tp + self.tn) / self.n if self.n else float("nan")

    @property
    def kappa(self) -> float:
        """Cohen's kappa by hand: (p_o - p_e) / (1 - p_e), p_e from the marginals. No library needed."""
        if not self.n:
            return float("nan")
        p_o = self.agreement
        judge_fail = (self.tp + self.fp) / self.n
        human_fail = (self.tp + self.fn) / self.n
        p_e = judge_fail * human_fail + (1 - judge_fail) * (1 - human_fail)
        return 1.0 if p_e == 1.0 else (p_o - p_e) / (1 - p_e)


def calibrate(spec: JudgeSpec, judge: Judge, labelled: Iterable[dict[str, Any]], configured_model: str = JUDGE_MODEL) -> Calibration:
    """`labelled` rows: {"id", "output", "label": "pass"|"fail"} — the HELD-OUT split the judge prompt was never tuned on
    (Lucas 2026-07: 'we were using training data inside this split'). Balanced sets only (Husain 2024)."""
    c = Calibration()
    for row in labelled:
        verdict, _ = judge_grade(spec, judge, row["output"], configured_model)
        human_fail = row["label"] == "fail"
        if verdict == "unknown":
            c.unknown += 1
        elif verdict == "fail" and human_fail: c.tp += 1
        elif verdict == "pass" and not human_fail: c.tn += 1
        elif verdict == "fail" and not human_fail: c.fp += 1
        else: c.fn += 1
    return c


def print_calibration(spec: JudgeSpec, c: Calibration) -> bool:
    print(f"\n== calibration: judge {spec.failure_mode!r} v{spec.version} on {spec.model} — {c.n} labelled, {c.unknown} unknown")
    print("                 human: fail   human: pass")
    print(f"judge: fail   {c.tp:>12}   {c.fp:>11}    <- FP = good outputs the judge rejects")
    print(f"judge: pass   {c.fn:>12}   {c.tn:>11}    <- FN = real failures the judge misses")
    print(f"TPR (recall of failures) {c.tpr:.2f}  TNR (recall of good) {c.tnr:.2f}  kappa {c.kappa:.2f}  "
          f"(raw agreement {c.agreement:.2f} — reported, never the decision)")
    ok = c.tpr >= TPR_FLOOR and c.tnr >= TNR_FLOOR and c.kappa >= KAPPA_FLOOR
    print("calibration", "OK" if ok else f"BELOW FLOOR (TPR>={TPR_FLOOR}, TNR>={TNR_FLOOR}, kappa>={KAPPA_FLOOR}) — fix the prompt or the labels; do not ship this judge")
    return ok


def record_run(path: str, reports: list[TaskReport], k: int, judge_models: dict[str, str]) -> None:
    """One JSON line per run: when, which judge model/version, pass^k per task. The datastore (Langfuse, LangSmith, a
    table) can hold the same rows; this file is the minimum that makes a run reproducible."""
    row = {"k": k, "judges": judge_models,
           "tasks": {r.task_id: {"pass_pow_k": r.pass_pow_k, "pass_at_k": r.pass_at_k, "broken": r.broken,
                                 "worst": r.worst.verdict} for r in reports}}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")


# --- 6. Offline demo: every branch, no network ---------------------------------------------------------------------
def _demo() -> int:
    import tempfile
    rng = random.Random(7)
    tmp = tempfile.mkdtemp(prefix="eval-demo-")
    judges_dir = os.path.join(tmp, "judges"); os.makedirs(judges_dir)
    judge_file = os.path.join(judges_dir, "handoff.md")
    with open(judge_file, "w", encoding="utf-8") as fh:
        fh.write("failure-mode: did not confirm the call transfer with the user\nmodel: fake-judge-1\nversion: 3\n"
                 "calibrated: 2026-10-01\ncalibration-set: evals/labels/handoff.jsonl\ntpr: 0.85\ntnr: 0.90\nkappa: 0.70\n\n"
                 "You are grading ONE failure mode…")
    stale_file = os.path.join(judges_dir, "stale.md")
    with open(stale_file, "w", encoding="utf-8") as fh:
        fh.write("failure-mode: stale\nmodel: some-other-model\nversion: 1\ncalibrated: 2026-10-01\n"
                 "calibration-set: x.jsonl\ntpr: 0.9\ntnr: 0.9\n\n…")
    bad_judges = {
        "no-record.md": "failure-mode: x\nmodel: fake-judge-1\nversion: 1\n\n…",
        "placeholders.md": "failure-mode: x\nmodel: fake-judge-1\nversion: 1\ncalibrated: <<YYYY-MM-DD>>\ncalibration-set: <<>>\ntpr: <<0.00>>\ntnr: <<0.00>>\n\n…",
        "agreement-only.md": "failure-mode: x\nmodel: fake-judge-1\nversion: 1\ncalibrated: 2026-10-01\ncalibration-set: x.jsonl\nagreement: 0.92\n\n…",
        "below-floor.md": "failure-mode: x\nmodel: fake-judge-1\nversion: 1\ncalibrated: 2026-10-01\ncalibration-set: x.jsonl\ntpr: 0.95\ntnr: 0.40\n\n…",
        "placeholder-model.md": "failure-mode: x\nmodel: <<JUDGE_MODEL>>\nversion: 1\ncalibrated: 2026-10-01\ncalibration-set: x.jsonl\nkappa: 0.8\n\n…",
    }
    for name, text in bad_judges.items():
        with open(os.path.join(judges_dir, name), "w", encoding="utf-8") as fh:
            fh.write(text)

    tasks = [
        Task("reservation_exists", "book a table for 2", expected={"reservation": True},
             assertions=[{"kind": "contains", "value": "booked"}], reference="booked: table for 2"),
        Task("flaky_date_format", "format today's date", assertions=[{"kind": "regex", "value": r"^\d{4}-\d{2}-\d{2}$"}],
             reference="2026-10-01"),
        Task("broken_task", "impossible expectation", expected={"x": 1}, assertions=[{"kind": "equals", "value": "A"}],
             reference="B"),  # reference solution fails its own grader -> flagged BROKEN, not an agent failure
        Task("handoff_confirmed", "transfer the call", assertions=[{"kind": "max_len", "value": 200}], judge="handoff.md",
             reference="I will transfer you now — is that okay? … Transferring."),
        Task("multi_part", "three checks", assertions=[{"kind": "contains", "value": "a"}, {"kind": "contains", "value": "b"},
                                                       {"kind": "contains", "value": "c"}], parts=3, reference="a b c"),
    ]

    calls = {"flaky": 0}

    def fake_agent(task: Task, env: dict[str, Any]) -> str:
        if task.id == "reservation_exists":
            env["state"]["reservation"] = True; return "Done — booked a table for 2."
        if task.id == "flaky_date_format":
            calls["flaky"] += 1
            return "October 1, 2026" if calls["flaky"] == 3 else "2026-10-01"   # 4 of 5 pass: pass@k = True, pass^k = False
        if task.id == "broken_task":
            return "A"
        if task.id == "handoff_confirmed":
            return rng.choice(["Transferring you now.", "Is it okay if I transfer you? … Transferring.", "???"])
        if task.id == "multi_part":
            return "a b"  # two of three parts -> partial credit 0.67
        return ""

    def fake_judge(prompt: str, output: str) -> str:  # in-memory stand-in for the model call; same contract
        if output == "???":
            return json.dumps({"reasoning": "the transcript is too short to tell", "verdict": "unknown"})
        if "okay" in output.lower() or "may i" in output.lower():
            return json.dumps({"reasoning": "the agent asked before transferring", "verdict": "pass"})
        if output == "not json":
            return "I think it passes"  # unparseable -> unknown branch
        return json.dumps({"reasoning": "no confirmation question before the transfer", "verdict": "fail"})

    k = 5
    reports = run_suite(tasks, k, fake_agent, fake_judge, judges_dir, configured_model="fake-judge-1")
    suite_ok = print_report(reports, k, {"handoff.md": "fake-judge-1 v3"})
    record_run(os.path.join(tmp, "runs.jsonl"), reports, k, {"handoff.md": "fake-judge-1 v3"})
    assert reports[0].pass_pow_k, "code grader + outcome check must pass"
    assert reports[1].pass_at_k and not reports[1].pass_pow_k, "the flaky task must show pass@k=True, pass^k=False"
    assert reports[2].broken, "the broken task must be flagged"
    assert any(t.verdict == "unknown" for t in reports[3].trials), "the judge's unknown out must appear"
    assert abs(reports[4].worst.credit - 2 / 3) < 1e-9 and abs(reports[4].credit - 2 / 3) < 1e-9, "partial credit on the multi-part task"
    print(f"suite verdict: {'OK' if suite_ok else 'FAIL (expected in the demo: the flaky task)'}")

    # unparseable judge output -> unknown (never a pass, never an exception)
    spec = JudgeSpec.load(judge_file)
    v, why = judge_grade(spec, fake_judge, "not json", configured_model="fake-judge-1")
    assert v == "unknown", why
    print(f"unparseable judge output -> {v}: {why[:60]}")

    # judges refused BEFORE any call: no record, placeholders, agreement only, below floor, placeholder model
    for name in bad_judges:
        try:
            JudgeSpec.load(os.path.join(judges_dir, name)); raise AssertionError(name)
        except ValueError as e:
            print(f"refused {name}: {str(e).split(' — ')[-1][:80]}")
    JudgeSpec.load(os.path.join(judges_dir, "no-record.md"), require_record=False)  # --calibrate may load it to produce the record

    # a judge whose header names a different model than the configured one is refused
    try:
        judge_grade(JudgeSpec.load(stale_file), fake_judge, "x", configured_model="fake-judge-1")
        raise AssertionError("stale judge must be refused")
    except RuntimeError as e:
        print(f"stale judge refused: {str(e)[:90]}…")

    # calibration by hand: 10 labelled rows -> 4 TP, 3 TN, 1 FP, 1 FN, 1 unknown
    labelled = [
        {"id": 1, "output": "Transferring you now.", "label": "fail"},            # TP
        {"id": 2, "output": "Transferring.", "label": "fail"},                    # TP
        {"id": 3, "output": "Hold on.", "label": "fail"},                         # TP
        {"id": 4, "output": "One moment.", "label": "fail"},                      # TP
        {"id": 5, "output": "Is it okay if I transfer you?", "label": "pass"},    # TN
        {"id": 6, "output": "May I transfer you to billing?", "label": "pass"},   # TN
        {"id": 7, "output": "Okay to transfer?", "label": "pass"},                # TN
        {"id": 8, "output": "Transferring, as you asked.", "label": "pass"},      # FP: human says fine, judge says fail
        {"id": 9, "output": "okay, transferring.", "label": "fail"},              # FN: 'okay' fools the judge
        {"id": 10, "output": "???", "label": "fail"},                             # unknown (abstention)
    ]
    c = calibrate(spec, fake_judge, labelled, configured_model="fake-judge-1")
    assert (c.tp, c.tn, c.fp, c.fn, c.unknown) == (4, 3, 1, 1, 1), (c.tp, c.tn, c.fp, c.fn, c.unknown)
    # by hand: n=9, p_o=7/9=0.778; judge_fail=5/9, human_fail=5/9 -> p_e=(25+16)/81=0.506; kappa=(0.778-0.506)/(0.494)=0.55
    assert abs(c.kappa - ((7 / 9) - 41 / 81) / (1 - 41 / 81)) < 1e-9
    cal_ok = print_calibration(spec, c)
    assert not cal_ok, "kappa 0.55 is below the 0.60 floor: the demo must show the refusal"

    # a judge that always says "pass" on a 10 %-failure set: agreement 0.90, TPR 0.00 — the smell Husain names
    always_pass = Calibration(tp=0, tn=90, fp=0, fn=10)
    print(f"\nalways-pass judge on a 10 %-failure set: agreement {always_pass.agreement:.2f}, TPR {always_pass.tpr:.2f}, "
          f"kappa {always_pass.kappa:.2f} -> agreement alone would have shipped it")
    assert always_pass.agreement == 0.9 and always_pass.tpr == 0.0 and always_pass.kappa == 0.0
    print("\ndemo: every documented branch exercised offline (no model call, no network)")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--tasks", help="tasks.jsonl")
    p.add_argument("--trials", type=int, default=5, help="k trials per task (>= 5; failure-modes row 12)")
    p.add_argument("--judges-dir", default="evals/judges")
    p.add_argument("--report", action="store_true", help="print the pass^k table and append to evals/runs.jsonl")
    p.add_argument("--calibrate", help="judge prompt file to calibrate")
    p.add_argument("--labels", help="held-out labelled JSONL for --calibrate")
    p.add_argument("--demo", action="store_true", help="offline run of every branch with a fake agent and judge")
    a = p.parse_args(argv)
    if a.demo:
        return _demo()
    judge = _real_judge()
    if a.calibrate:
        spec = JudgeSpec.load(a.calibrate, require_record=False)
        rows = [json.loads(l) for l in open(a.labels, encoding="utf-8") if l.strip()]
        return 0 if print_calibration(spec, calibrate(spec, judge, rows)) else 1
    if a.tasks:
        reports = run_suite(load_tasks(a.tasks), a.trials, run_agent, judge, a.judges_dir)
        judges = {t.judge: JudgeSpec.load(os.path.join(a.judges_dir, t.judge)).version for t in load_tasks(a.tasks) if t.judge}
        ok = print_report(reports, a.trials, judges)
        if a.report:
            record_run("evals/runs.jsonl", reports, a.trials, judges)
        return 0 if ok else 1
    p.print_help()
    return 2


def _real_judge() -> Judge:
    """The judge call goes through the repo's ONE LLM client (practices/llm-api-calls/) so it is logged and cost-capped.
    <<JUDGE_CLIENT_IMPORT>>: e.g. `from src.<package>.llm import client` and a call that returns the text of a
    structured response {reasoning, verdict} (practices/structured-outputs/structured_call.py gives the typed call)."""
    def _judge(prompt: str, output: str) -> str:
        raise NotImplementedError("wire the judge through the repo's LLM client module; see <<JUDGE_CLIENT_IMPORT>>")
    return _judge


if __name__ == "__main__":
    sys.exit(main())
