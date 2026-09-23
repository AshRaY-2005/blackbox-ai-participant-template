# round-4 — Reconstruct

Build a model that reproduces the hidden system's behaviour.

Your queries are your training set — including everything you already spent in Rounds 1
to 3. Teams that queried thoughtfully earlier have a better dataset now, which is the point.
`bb.export()` returns every query your team has made, from every laptop.

Anything you worked out in Round 2 about hidden transformations belongs in your feature
engineering here. A surrogate that ignores what you already discovered will underperform
one that uses it — and so will one that only fits the points you happen to have.

## What judges look for

- **Modelling** — the surrogate you chose follows from what you learned about the system.
- **Features** — it encodes what earlier rounds discovered, not just the raw inputs.
- **Generalisation** — you checked it on queries it was not trained on, and you say
  where your data is thin.
- **Data** — you turned your query budget into a usable dataset, and spent this round's
  budget where your model was least sure.

## What to submit

| File | Purpose |
|---|---|
| `surrogate.py` (or a notebook in `experiments/`) | Your reconstruction. Ideally a `predict(rows)` a judge can run on a few rows. |
| `report.md` | How you built it, what it encodes, how you validated it, and where it is weak. |
| `experiments/` | Your training data (`bb.export()`) and scripts |
| `plots/` | Anything visual that supports the report |
| `findings.json` | Anything new you established this round. Optional here. |

Validate before you open the PR:

```bash
python tools/validate.py round-4
```

Then open a pull request **from your fork to this repository**, titled
`[BB-XXX] Round 4 — Reconstruct` with your own Team ID in place of `BB-XXX`.

**The pull request is your submission.** Open it before the organisers end the round.
Judges mark the commit it is at when the round ends; anything pushed afterwards is not
marked.
