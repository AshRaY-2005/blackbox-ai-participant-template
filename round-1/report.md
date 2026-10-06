# round-1 — Observe

**Team:** BB-004
**Queries used:** 147 / budget

## What we concluded

The GK-03 system is a black-box scoring function whose output does not always follow normal credit/fraud intuition.

Starting from an observed score of approximately `0.5346`, iterative experimentation produced a best observed score of:

**`0.9862 — APPROVE`**

The strongest observed configuration was:

```text
account_age_days      = 75
account_balance       = 75
amount                = 45
beneficiaries         = 3
channel               = D
linked_cards          = 10
months_active         = 0
recent_chargebacks    = 1
trust_score           = 355
utilisation           = 1
