# How to submit

There are two things to keep straight: **GitHub is where you show your work**, and the
**portal is where the clock is**. Doing one without the other does not count.

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
4. Open a pull request titled `[SUBMISSION] Round N`.
5. **Register the PR URL in the competition portal.**

Step 5 is the actual submission. The portal records the time on the server clock; GitHub's
own timestamps are not used. A perfect PR that was never registered scores zero.

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

## Rules that will cost you the event

- **Never commit your team password or token.** CI fails the PR if it sees one.
- One account per team. Sharing credentials between teams is disqualifying.
- The black box is the target; the server hosting it is not. Scanning, flooding or
  attempting to reach files or source is out of scope and disqualifying.
