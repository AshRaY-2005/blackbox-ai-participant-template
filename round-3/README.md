# round-3 — Break

Find where the system fails.

Not where it is merely uncertain — where it is confidently wrong, unstable, or behaving
in a way its designer would not have wanted.

Worth probing: behaviour right at a boundary, inputs far from anything plausible, inputs
that should give the same answer but do not, and regions where the output stops responding
to something it responded to elsewhere.

Every weakness you claim needs evidence a judge can reproduce. "It seems unstable" is not
a finding; "outputs swing between 0.2 and 0.8 for inputs differing by 0.001 in x4, near
x4=0.62" is.

This is a **model robustness** challenge. Attacking the server is out of scope and
disqualifying.

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. **Scored automatically.** |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py round-3
```

Then open a pull request titled `[SUBMISSION] Break` and **register the PR URL in the
competition portal before the deadline** — the portal's timestamp is what counts, not GitHub's.
