# round-1 — Observe

Establish the basic behaviour of your assigned system.

Useful ground to cover: which inputs move the output and which do not, roughly how
strongly, whether the relationship is monotone, and where any obvious thresholds sit.

Change one thing at a time and hold the rest fixed — but notice when that stops
explaining what you see. If varying inputs individually tells you almost nothing,
that is itself a finding worth recording.

**This is the first elimination round.**

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. **Scored automatically.** |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py round-1
```

Then open a pull request titled `[SUBMISSION] Round 1 — Observe`.

**The pull request is your submission.** Open it before the organisers end the
round — what it contains at that moment is what gets marked, and anything pushed
afterwards is not.
