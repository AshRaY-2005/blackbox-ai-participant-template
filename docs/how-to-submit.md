# How to submit

**GitHub is where you show your work, and a pull request is your submission.** Rounds
end when the organisers end them, and what your pull request contains at that moment is
what gets marked.

## During a round

1. Open a **Hypothesis** issue before you spend queries testing something.
2. Run the experiment. Open an **Experiment** issue with what you expected and what you got.
3. When something is established, open a **Discovery** issue with the evidence.

You do not need an issue for every query. You do need them for the reasoning you want
credit for — the issues are how judges see how you thought, and they are the main
evidence in the technical defence if you reach the final.

Rejected hypotheses are worth as much as confirmed ones. Do not delete them.

## At the end of a round

1. Fill in `round-N/findings.json` — these are the claims that get **scored automatically**.
2. Write `round-N/report.md` — the reasoning behind them.
3. Validate:
   ```bash
   python tools/validate.py round-N
   ```
4. Open a pull request titled `[SUBMISSION] Round N — Name`, for example
   `[SUBMISSION] Round 2 — Investigate` or `[SUBMISSION] Final — The Unknown`.

That pull request is the submission — there is nothing else to register. Open it before the
organisers end the round: when they do, each team's pull request is frozen as it stands and
marked. Anything pushed afterwards is not seen. Make sure your repository is registered on the
portal (**Your repository**) — that is how the organisers find it.

## How findings are marked

Each round is marked on what **that round** is about. Round 1 on how the system behaves,
Round 2 on the structure underneath, Round 3 on where it breaks. The Final is marked on
everything about the Final's system.

So put your findings for *this* round in this round's `findings.json`. Repeating something
you established in an earlier round is harmless — it is neither credited again nor
penalised — so you do not need to decide whether to carry old claims forward.

## findings.json

`report.md` is prose and a human reads it. `findings.json` is a list of typed claims and a
scorer reads it. Each claim needs a type, a confidence, and evidence.

```json
{
  "round": "round-2",
  "team": "BB-017",
  "queries_used": 118,
  "claims": [
    {
      "type": "threshold",
      "feature": "x4",
      "value": 0.62,
      "tolerance": 0.02,
      "confidence": 0.9,
      "evidence": {
        "query_ids": ["a41f", "a42b", "a43c"],
        "summary": "Swept x4 from 0.55 to 0.70 in steps of 0.01 with all other inputs fixed at their midpoints. Output falls from 0.81 to 0.19 between 0.61 and 0.63."
      }
    },
    {
      "type": "ignored_feature",
      "feature": "x7",
      "confidence": 0.75,
      "evidence": {
        "query_ids": ["b10a", "b10b"],
        "summary": "Varied x7 across its full range at three different settings of the other inputs. Output identical to 6 decimal places in all cases."
      }
    }
  ]
}
```

**On confidence:** it is a real number and it is used. A confident wrong claim costs you
more than an uncertain one. If you are not sure, say so — that is rewarded, not punished.

## Claim types

| Type | Use it for | Also needs |
|---|---|---|
| `feature_effect` | An input that moves the output | `feature`, `direction` |
| `ignored_feature` | An input that does nothing | `feature` |
| `threshold` | A value where behaviour changes sharply | `feature`, `value` |
| `interaction` | Two inputs that matter together | `features` |
| `derived_feature` | Inputs combined before the model sees them | `features`, `form` |
| `decision_rule` | A rule sitting on top of the model | `category`, `feature`, `value`, `outcome` |
| `failure_region` | Where the system is confidently wrong | `category`, `feature`, `observed` |

Four fields take fixed vocabularies, because prose cannot be scored automatically:

| Field | Allowed values |
|---|---|
| `direction` | `increases` `decreases` `non_monotonic` `none` |
| `form` | `ratio` `product` `difference` `sum` `binned` `other` |
| `outcome` | `approve` `decline` `override` `no_change` |
| `observed` | `constant` `inverted` `unstable` `extrapolated` `saturated` |

A rule you noticed as *"applicants in region C under 25 always get declined"* is submitted as:

```json
{
  "type": "decision_rule",
  "category": "C", "feature": "age", "value": 25, "outcome": "decline",
  "confidence": 0.85,
  "evidence": { "query_ids": ["c01", "c02"], "summary": "..." }
}
```

## Getting your data back

Three endpoints cost nothing and do not touch your budget:

```python
bb.quota()        # limit / used / remaining
bb.challenge()    # your system's input and output schema
bb.export()       # every query your team has made, as flat rows
```

`export()` is the one to remember. Round 4 asks you to reconstruct the system from
your own observations, and this returns all of them — across teammates, across
laptops, across closed browser tabs. In Round 4, `bb.round4_test()` downloads the rows
you are marked on; see `round-4/README.md`.

```python
import pandas as pd
df = pd.DataFrame(bb.export())
df.to_csv("round-4/experiments/queries.csv", index=False)
```

## Rules that will cost you the event

- **Never commit your team password or token.** CI fails the PR if it sees one.
- One account per team. Sharing credentials between teams is disqualifying.
- The black box is the target; the server hosting it is not. Scanning, flooding or
  attempting to reach files or source is out of scope and disqualifying.
