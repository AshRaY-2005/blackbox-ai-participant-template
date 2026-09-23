# final — The Unknown

A fresh hidden system, the same one for every finalist.

Everything at once: investigate it, form hypotheses, design experiments that separate them,
find where it breaks, and reconstruct what you can — inside a fixed budget and a fixed
window.

Your submission is fixed when the organisers end the round, and judged after it.
Shortlisted teams then defend their reasoning to the judging panel, so keep your investigation trail readable
as you go: which experiment, why that one, what it ruled out.

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. Judges check each one. |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py final
```

Then open a pull request **from your fork to this repository**, titled
`[BB-XXX] Final — The Unknown` with your own Team ID in place of `BB-XXX`.

**The pull request is your submission.** Open it before the organisers end the round.
Judges mark the commit it is at when the round ends; anything pushed afterwards is not
marked.
