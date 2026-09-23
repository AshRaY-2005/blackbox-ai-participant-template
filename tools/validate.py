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
    "decision_rule": ["category", "feature", "value", "outcome"],
    # category only when the failure is confined to one; a boundary on a numeric input
    # (the effect reversing past some value) has none, and must not be forced to invent one
    "failure_region": ["feature", "observed"],
}
# Values that must come from a fixed vocabulary. Judges read every team's claims side by
# side, so "it goes up a lot" has to become direction="increases" to be comparable.
ENUM_FIELDS = {
    "direction": {"increases", "decreases", "non_monotonic", "none"},
    "form": {"ratio", "product", "difference", "sum", "binned", "other"},
    "outcome": {"approve", "decline", "override", "no_change"},
    "observed": {"constant", "inverted", "unstable", "extrapolated", "saturated"},
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

    if name == "round-4" and not has_findings(name):
        # findings are optional here: the surrogate and its report are the submission
        if not report.exists() or len(report.read_text().strip()) < 200:
            warn(name, "report.md is missing or very short — it is what judges read")
        return
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
        for f, allowed in ENUM_FIELDS.items():
            if f in c and str(c[f]).strip().lower() not in allowed:
                err(at, f"{f}='{c[f]}' is not one of {sorted(allowed)}")

    if not report.exists() or len(report.read_text().strip()) < 200:
        warn(name, "report.md is missing or very short — findings.json lists the claims, the report is where judges see why you believe them")


def has_work(name):
    """Has this round been started, or is it still the untouched starter file?

    A fresh clone must validate cleanly, so an unedited starter — placeholder team ID
    and the example claim still in place — counts as "not started" rather than as a
    broken submission. Touch either one and the round starts being checked.
    """
    return has_findings(name)


def has_findings(name):
    d = ROOT / name
    f = d / "findings.json"
    if not d.exists() or not f.exists():
        return False
    try:
        data = json.loads(f.read_text())
    except Exception:
        return True  # malformed but present — check it and report properly
    claims = data.get("claims") or []
    if not claims:
        return False
    untouched = (
        str(data.get("team", "")).upper().startswith("BB-XXX")
        and len(claims) == 1
        and "Replace this example claim" in str(
            claims[0].get("evidence", {}).get("summary", "")
        )
    )
    return not untouched


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
