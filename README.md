# BLACKBOX AI 1.0 — team repository

**Reverse Engineer the Intelligence** · IEEE Student Branch, GCET · 6–7 October 2026

Every team forks this repository, works in its fork, and sends its pull requests and
issues **back here**. Judges read them here.

## The short version

1. **Fork** this repository (the *Fork* button, top right). One fork per team is enough;
   add your teammates to it as collaborators so everyone can push.
2. Work in your fork. Each round has its own folder.
3. **Issues** = your investigation — hypotheses, experiments, discoveries. Open them
   **on this repository**, not on your fork.
4. **A pull request** from your fork to this repository = your submission for a round,
   one per round.
5. **Start every title with your Team ID**: `[BB-014] Round 2 — Investigate`. It is how
   judges find your work among everyone else's.

Judges mark the commit your pull request is at when the organisers end the round.
Anything pushed after that is not marked.

> **Everything here is public** — your fork, your pull requests and your issues. Other
> teams can read them. Never commit your password or token.

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

Round 0 is not here — it is a quiz in the portal, and the portal marks it.

## Getting started

```bash
git clone https://github.com/<your-username>/blackbox-ai-participant-template
cd blackbox-ai-participant-template
python tools/validate.py
```

That should pass on a fresh clone of your fork. Then, once you have your credentials
from the registration desk:

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

**Checking your quota is free.** So is reading your challenge spec, and so is
`bb.export()` — which hands back every query your team has ever made, as rows.

That last one matters more than it sounds. In Round 4 your earlier queries **are**
your training set, and `export()` returns all of them: the ones a teammate ran on
another laptop, and the ones from a browser tab you closed two hours ago. You do not
have to build your own logging to survive Round 4 — though keeping your own notes
about *why* you ran each experiment is still on you, and it is what judges read.

**The names are labels.** Every box is a synthetic system dressed up as a lending
service, a triage desk, a fraud screen and so on, and it does not follow real-world
logic: a lending box may well approve more applicants with more defaults. Trust what your
queries show, not what the domain suggests. Any number within a field's range is
accepted, fractions included, even in fields that sound like counts.

**Your queries carry across rounds.** You keep the same black box from Round 1 through
Round 4, so the data you collect early becomes your training set in Round 4. Careless
querying now is expensive later.

**AI tools are allowed** — ChatGPT, Claude, Copilot, whatever you use. They can help you
write code, plot results and reason about what you observed. They cannot tell you what
your black box will output. That information exists only on the competition server.

**Evidence beats guessing.** A confident claim that turns out wrong costs more than an
uncertain one. Saying "we are not sure" is a legitimate and rewarded answer.

## Never commit

Your team password, your API token, or any `.env` file. Your fork is public: the moment
you push one, anyone can read it and spend your budget. The check on your pull request
fails if it finds one — if that happens, ask the registration desk for a new password.
