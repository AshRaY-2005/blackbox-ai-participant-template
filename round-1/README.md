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
| `findings.json` | Your claims, in structured form. Judges check each one. |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py round-1
```

Then open a pull request **from your fork to this repository**, titled
`[BB-XXX] Round 1 — Observe` with your own Team ID in place of `BB-XXX`.

**The pull request is your submission.** Open it before the organisers end the round.
Judges mark the commit it is at when the round ends; anything pushed afterwards is not
marked.
