# round-4 — Reconstruct

Build a model that reproduces the hidden system's behaviour.

Your queries are your training set — including everything you already spent in Rounds 1
to 3. Teams that queried thoughtfully earlier have a better dataset now, which is the point.

Your submission is scored against data you never see, so what matters is generalisation,
not how well you fit the points you happen to have.

Anything you worked out in Round 2 about hidden transformations belongs in your feature
engineering here. A surrogate that ignores what you already discovered will underperform
one that uses it.

## Your test set

While Round 4 is open, download your team's test set from the portal
(**Download test set**) or from Python:

```python
rows = bb.round4_test()           # also saves round-4/test.csv
```

It is rows your box has never been asked about, in the same column names you have been
querying all event. Downloading it is free and costs no queries. It is **your box
only** — another team's file is for a different system and is no use to you.

## What to submit

| File | Purpose |
|---|---|
| `predictions.csv` | For every test row, the probability your box returns `APPROVE`. **Scored automatically.** |
| `findings.json` | Anything new you established this round. Optional here. |
| `report.md` | How you built the surrogate and why. Read by judges. |
| `experiments/` | Your training data and scripts |
| `plots/` | Anything visual that supports the report |

`predictions.csv` has exactly two columns:

```csv
id,target
0,0.93
1,0.04
```

One row per test row, `target` between 0 and 1. It is marked by how well it ranks the
rows (AUC): a coin toss scores nothing and a perfect ranking scores everything, so what
matters is getting the *order* right — including the rows where something other than the
model decides.

Validate before you open the PR:

```bash
python tools/validate.py round-4
```

Then open a pull request titled `[SUBMISSION] Round 4 — Reconstruct`.

**The pull request is your submission.** Open it before the organisers end the
round — what it contains at that moment is what gets marked, and anything pushed
afterwards is not.
