# round-4 — Reconstruct

Build a model that reproduces the hidden system's behaviour.

Your queries are your training set — including everything you already spent in Rounds 1
to 3. Teams that queried thoughtfully earlier have a better dataset now, which is the point.

Your submission is scored against data you never see, so what matters is generalisation,
not how well you fit the points you happen to have.

Anything you worked out in Round 2 about hidden transformations belongs in your feature
engineering here. A surrogate that ignores what you already discovered will underperform
one that uses it.

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. **Scored automatically.** |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py round-4
```

Then open a pull request titled `[SUBMISSION] Reconstruct` and **register the PR URL in the
competition portal before the deadline** — the portal's timestamp is what counts, not GitHub's.
