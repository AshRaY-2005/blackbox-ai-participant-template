# How to submit

**Everyone works in a fork of this repository and sends their work back to it.** Your
investigation goes in issues, and each round's submission is a pull request, both opened
**on this repository** (`ieee-blackbox-ai/blackbox-ai-participant-template`), where the
judges read them.

**Start every title with your Team ID** — `[BB-014] ...`. Hundreds of issues and pull
requests land here from every team; the ID is how judges find yours. A check labels each
one with its team and round, and comments if the ID is missing.

## Once, at the start

1. Sign in to GitHub and press **Fork** on this repository. One fork per team.
2. In your fork, **Settings → Collaborators → Add people**: add your teammates so all
   of you can push.
3. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/blackbox-ai-participant-template
   ```
4. Register your fork on the portal under **Submitting**, so judges can match your
   GitHub accounts to your team.

Your fork is public, like everything else here. Never commit your password or token.

## During a round

Open these **on this repository** (the *Issues* tab here, not on your fork):

1. A **Hypothesis** issue before you spend queries testing something.
2. An **Experiment** issue once you have run it: what you expected and what you got.
3. A **Discovery** issue when something is established, with the evidence.

Each form asks for your Team ID and the round. You do not need an issue for every query.
You do need them for the reasoning you want credit for — the issues are how judges see
how you thought, and they are the main evidence in the technical defence if you reach
the final.

Rejected hypotheses are worth as much as confirmed ones. Do not delete them.

## At the end of a round

1. Fill in `round-N/findings.json` — your claims. Judges check each one.
2. Write `round-N/report.md` — the reasoning behind them.
3. Validate:
   ```bash
   python tools/validate.py round-N
   ```
4. Commit on a branch for the round and push it to your fork:
   ```bash
   git switch -c round-2
   git add round-2
   git commit -m "Round 2"
   git push -u origin round-2
   ```
5. On GitHub, open a pull request **from that branch of your fork to `main` of this
   repository** (GitHub offers a *Compare & pull request* button after you push). Title
   it `[BB-014] Round 2 — Investigate`, with your own ID — or `[BB-014] Final — The Unknown`.

That pull request is the submission — there is nothing else to register. Open it before
the organisers end the round. When they do, judges mark the commit it is at; anything
pushed afterwards is not marked. One pull request per round: a pull request follows its
branch, so use a new branch for each round rather than piling every round onto one.

## How your work is marked

Judges mark every round from your pull request and your issues, against a short rubric
for that round — the evidence behind your claims, how you chose your experiments, how
honestly you state what you are unsure of, and how clearly someone else could follow it.
Each round's folder README says what that round is about.

Each round is marked on what **that round** is about: Round 1 on how the system behaves,
Round 2 on the structure underneath, Round 3 on where it breaks, Round 4 on your
reconstruction. So put this round's findings in this round's `findings.json`. Repeating
something from an earlier round does no harm and earns nothing new.

## findings.json

`report.md` is prose: the reasoning. `findings.json` is the list of claims it supports, in
a fixed shape so a judge can check fifty teams' claims side by side. Each claim needs a
type, a confidence, and evidence.

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

**On confidence:** it is a real number and judges read it. A confident wrong claim costs
you more than an uncertain one. If you are not sure, say so — that is rewarded, not punished.

## Claim types

| Type | Use it for | Also needs |
|---|---|---|
| `feature_effect` | An input that moves the output | `feature`, `direction` |
| `ignored_feature` | An input that does nothing | `feature` |
| `threshold` | A value where behaviour changes sharply | `feature`, `value` |
| `interaction` | Two inputs that matter together | `features` |
| `derived_feature` | Inputs combined before the model sees them | `features`, `form` |
| `decision_rule` | A rule sitting on top of the model | `category`, `feature`, `value`, `outcome` |
| `failure_region` | Where the system is confidently wrong | `feature`, `observed` (and `category` if it only happens in one) |

Four fields take fixed vocabularies, so two teams saying the same thing say it the same
way:

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
laptops, across closed browser tabs.

```python
import pandas as pd
df = pd.DataFrame(bb.export())
df.to_csv("round-4/experiments/queries.csv", index=False)
```

## Rules that will cost you the event

- **Never commit your team password or token.** Your fork is public; anyone can use it.
  The check on your pull request fails if it sees one.
- One account per team. Sharing credentials between teams is disqualifying.
- The black box is the target; the server hosting it is not. Scanning, flooding or
  attempting to reach files or source is out of scope and disqualifying.
