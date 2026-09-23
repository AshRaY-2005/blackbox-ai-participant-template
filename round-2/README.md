# round-2 — Investigate

Go past surface behaviour into the pipeline.

By now several different explanations probably fit everything you have seen. The round
is not asking you to pick your favourite — it is asking you to design the query that
tells them apart. That is where the marks are.

Worth probing: inputs that are transformed before the model sees them, inputs that are
combined with each other, inputs that are silently dropped, and structure that only
appears when you vary two things at once.

Record the hypotheses you **rejected**. They count.

## What to submit

| File | Purpose |
|---|---|
| `findings.json` | Your claims, in structured form. **Scored automatically.** |
| `report.md` | The reasoning behind the claims. Read by judges. |
| `experiments/` | Scripts and query logs |
| `plots/` | Anything visual that supports a claim |

Validate before you open the PR:

```bash
python tools/validate.py round-2
```

Then open a pull request titled `[SUBMISSION] Round 2 — Investigate`.

**The pull request is your submission.** Open it before the organisers end the
round — what it contains at that moment is what gets marked, and anything pushed
afterwards is not.
