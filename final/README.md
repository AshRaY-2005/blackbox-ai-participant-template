# final — The Unknown

A fresh hidden system, the same one for every finalist.

Everything at once: investigate it, form hypotheses, design experiments that separate them,
find where it breaks, and reconstruct what you can — inside a fixed budget and a fixed
window.

Your submission freezes at the deadline and is evaluated after the event. Shortlisted teams
then defend their reasoning to the judging panel, so keep your investigation trail readable
as you go: which experiment, why that one, what it ruled out.

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. **Scored automatically.** |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py final
```

Then open a pull request titled `[SUBMISSION] Final — The Unknown`.

**The pull request is your submission.** Open it before the organisers end the
round — what it contains at that moment is what gets marked, and anything pushed
afterwards is not.
