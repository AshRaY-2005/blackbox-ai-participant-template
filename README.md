# BLACKBOX AI 1.0 — team repository

**Reverse Engineer the Intelligence** · IEEE Student Branch, GCET · 6–7 October 2026

This is your team's working repository. It is where you record how you investigated your
assigned black box, and where your official submissions come from.

> **Keep this repository private for the duration of the event.** Other teams must not be
> able to read your findings.

## The short version

- **Issues** = your investigation. Hypotheses, experiments, discoveries.
- **Pull requests** = your official submissions, one per round.
- **The portal** = where the deadline actually is. Register your PR URL there or it does not count.

Full instructions: [`docs/how-to-submit.md`](docs/how-to-submit.md)

## Layout

```
round-1/    Observe       findings.json · report.md · experiments/ · plots/
round-2/    Investigate
round-3/    Break
round-4/    Reconstruct
final/      The Unknown
src/        shared code, including a small API client
tools/      validate.py — run this before every PR
docs/       how to submit
```

Round 0 is not here — it is answered in the portal and scored automatically.

## Getting started

```bash
python tools/validate.py
```

That should pass on a fresh clone. Then, once you have your credentials from the
registration desk:

```python
from src.blackbox import Blackbox

bb = Blackbox("http://<server-address>", "BB-XXX", "<your-password>")
print(bb.challenge())   # what your assigned system looks like from outside
print(bb.quota())       # free — checking your budget does not cost a query

out = bb.query([
    {"x1": 0.5, "x2": 0.2, "x3": 0.9},
    {"x1": 0.6, "x2": 0.2, "x3": 0.9},
])
print(out)
```

The server address is given at the briefing. **One row is one query** — batching several
rows into a single request is faster, but costs exactly the same as sending them separately.

## Things worth knowing before you start

**Your query budget does not come back.** There is no timer that refills it, and logging
out does not reset it. When it is gone for a round, it is gone. Decide what an experiment
is worth before you run it.

**Checking your quota is free.** So is reading your challenge spec. Only `query()` costs.

**Your queries carry across rounds.** You keep the same black box from Round 1 through
Round 4, so the data you collect early becomes your training set in Round 4. Careless
querying now is expensive later.

**AI tools are allowed** — ChatGPT, Claude, Copilot, whatever you use. They can help you
write code, plot results and reason about what you observed. They cannot tell you what
your black box will output. That information exists only on the competition server.

**Evidence beats guessing.** A confident wrong claim in `findings.json` costs more than an
uncertain one. Saying "we are not sure" is a legitimate and rewarded answer.

## Never commit

Your team password, your API token, or any `.env` file. CI will fail your submission PR if
it finds one, and a leaked credential is your problem, not ours — anyone with it can spend
your budget.
