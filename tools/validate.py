#!/usr/bin/env python3
"""Validate submission structure and findings.json.

Run it yourself before opening a PR:

    python tools/validate.py            # checks every round folder that has work in it
    python tools/validate.py round-2    # checks one round

Same script CI runs, so a green run here means a green run there.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROUNDS = ["round-1", "round-2", "round-3", "round-4", "final"]
CLAIM_TYPES = {
    "feature_effect", "ignored_feature", "threshold", "interaction",
    "derived_feature", "decision_rule", "failure_region",
}
# claim type -> fields that must be present beyond the common ones
REQUIRED_FIELDS = {
    "feature_effect": ["feature", "direction"],
    "ignored_feature": ["feature"],
    "threshold": ["feature", "value"],
    "interaction": ["features"],
    "derived_feature": ["features", "form"],
    "decision_rule": ["condition", "outcome"],
    "failure_region": ["condition", "observed"],
}

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


def check_round(name):
    d = ROOT / name
    findings = d / "findings.json"
    report = d / "report.md"

    if not findings.exists():
        err(name, "findings.json is missing")
        return
    try:
        data = json.loads(findings.read_text())
    except json.JSONDecodeError as e:
        err(f"{name}/findings.json", f"is not valid JSON — {e}")
        return

    for key in ("round", "team", "claims"):
        if key not in data:
            err(f"{name}/findings.json", f"missing required key '{key}'")
    if data.get("round") not in (None, name):
        err(f"{name}/findings.json", f"round is '{data.get('round')}', expected '{name}'")
    team = data.get("team", "")
    if not team or team.upper().startswith("BB-XXX"):
        err(f"{name}/findings.json", "team is still the placeholder — put your real team ID in")

    claims = data.get("claims", [])
    if not isinstance(claims, list) or not claims:
        err(f"{name}/findings.json", "claims must be a non-empty list")
        return

    for i, c in enumerate(claims):
        at = f"{name}/findings.json claim[{i}]"
        if not isinstance(c, dict):
            err(at, "must be an object")
            continue
        ctype = c.get("type")
        if ctype not in CLAIM_TYPES:
            err(at, f"type '{ctype}' is not one of {sorted(CLAIM_TYPES)}")
            continue
        conf = c.get("confidence")
        if not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
            err(at, "confidence must be a number between 0 and 1")
        ev = c.get("evidence")
        if not isinstance(ev, dict) or len(str(ev.get("summary", "")).strip()) < 10:
            err(at, "evidence.summary is missing or too short — an unevidenced claim scores nothing")
        elif not ev.get("query_ids"):
            warn(at, "no query_ids listed — judges cannot trace this back to your queries")
        for f in REQUIRED_FIELDS.get(ctype, []):
            if f not in c:
                err(at, f"type '{ctype}' requires field '{f}'")

    if not report.exists() or len(report.read_text().strip()) < 200:
        warn(name, "report.md is missing or very short — findings.json is scored, but the report is what judges read")


def has_work(name):
    d = ROOT / name
    if not d.exists():
        return False
    f = d / "findings.json"
    if not f.exists():
        return False
    try:
        return bool(json.loads(f.read_text()).get("claims"))
    except Exception:
        return True  # malformed but present — check it and report properly


targets = sys.argv[1:] or [r for r in ROUNDS if has_work(r)]
if not targets:
    print("No round has findings yet — nothing to validate.")
    sys.exit(0)

for t in targets:
    if t not in ROUNDS:
        err("args", f"'{t}' is not a round folder")
    else:
        check_round(t)

for w in warnings:
    print(f"warning  {w}")
for e in errors:
    print(f"ERROR    {e}")

print()
print(f"checked: {', '.join(targets)}")
if errors:
    print(f"FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)
print(f"PASSED — {len(warnings)} warning(s)")
