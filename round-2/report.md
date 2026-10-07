# round-2 — Investigate

**Team:** BB-004  
**Queries used:** 177 / budget

## What we concluded

The combined Round 1 and Round 2 analysis indicates that the black-box score is strongly associated with several account-level variables, with the strongest observed relationships involving `account_age_days`, `months_active`, `trust_score`, and `utilisation`.

The strongest relationship with the output score is:

- `account_age_days` → `score`: **+0.816**
- `months_active` → `score`: **−0.807**
- `trust_score` → `score`: **−0.732**
- `utilisation` → `score`: **+0.657**

This suggests that the scoring function is not driven by a single feature. Instead, multiple account characteristics appear to contribute jointly to the final score.

The data also reveals substantial relationships between input variables themselves, particularly:

- `amount` ↔ `beneficiaries`: **+0.689**
- `months_active` ↔ `trust_score`: **+0.659**
- `account_age_days` ↔ `months_active`: **−0.622**
- `account_age_days` ↔ `amount`: **+0.604**

The decision distribution is highly imbalanced, with **158 APPROVE** observations and **19 DECLINE** observations. DECLINE observations generally have substantially lower scores and utilisation, while `months_active` and several other variables show noticeable differences between the two decision groups.

The evidence therefore points toward a **multi-variable and potentially nonlinear scoring mechanism**, rather than a simple independent contribution from each parameter.

---

## How we got there

### 1. Combined the available observations

We analyzed the available Round 1 controlled experiments together with the Round 2 observations.

The cleaned dataset contains:

- **R1:** 120 unique experiments
- **R2:** 160 unique experiments
- **Total:** 280 unique experiments

Repeated query IDs were removed so that repeated observations supplied as context were not treated as additional experiments.

---

### 2. Investigated relationships between numerical variables

Spearman correlation was used to identify both monotonic and potentially nonlinear relationships between variables.

The strongest relationships involving the output `score` were:

| Feature | Spearman correlation with score |
|---|---:|
| `account_age_days` | **+0.816** |
| `months_active` | **−0.807** |
| `trust_score` | **−0.732** |
| `utilisation` | **+0.657** |

These are considerably stronger than the relationships observed for many of the other variables.

The strongest relationships between input variables were:

| Feature pair | Spearman correlation |
|---|---:|
| `amount` ↔ `beneficiaries` | **+0.689** |
| `months_active` ↔ `trust_score` | **+0.659** |
| `account_age_days` ↔ `months_active` | **−0.622** |
| `account_age_days` ↔ `amount` | **+0.604** |

This indicates that some parameters are not independent of one another in the observed dataset.

---

### 3. Investigated APPROVE vs DECLINE

The dataset contains:

- **APPROVE:** 158
- **DECLINE:** 19

Therefore, approximately **89%** of observations are APPROVE and approximately **11%** are DECLINE.

The strongest differences between the two groups were observed in:

- `score`
- `utilisation`
- `amount`
- `recent_chargebacks`
- `months_active`
- `account_age_days`
- `beneficiaries`
- `account_balance`

The clearest separation was observed for `score`, `utilisation`, and `months_active`.

In general, DECLINE observations were associated with lower `score` and lower `utilisation`, while `months_active` and `recent_chargebacks` showed higher standardized values in the DECLINE group.

Because the DECLINE group contains only 19 observations, these group-level differences should not be treated as definitive causal rules.

---

### 4. Investigated multicollinearity

Variance Inflation Factor (VIF) was used to determine whether the numerical predictors contain substantial overlapping information.

The observed VIF values were:

| Feature | VIF |
|---|---:|
| `score` | **5.38** |
| `utilisation` | **3.85** |
| `account_age_days` | **3.21** |
| `amount` | 2.24 |
| `months_active` | 2.14 |
| `beneficiaries` | 2.07 |
| `recent_chargebacks` | 1.66 |
| `account_balance` | 1.62 |
| `trust_score` | 1.55 |
| `linked_cards` | 1.35 |

`score` has the highest VIF at **5.38**, indicating moderate multicollinearity.

All other variables have VIF values below 5, and no variable reaches the severe multicollinearity threshold of VIF > 10.

---

## What we ruled out

### 1. A single-feature explanation

The observed correlations do not support the idea that one parameter alone explains the output.

Although `account_age_days` has the strongest correlation with score, other variables such as `months_active`, `trust_score`, and `utilisation` also show strong relationships.

Therefore, the current evidence favors a multi-feature scoring mechanism.

---

### 2. Treating APPROVE/DECLINE as the complete scoring mechanism

The score contains considerably more information than the binary decision.

Many observations with APPROVE decisions have substantially different scores, indicating that the underlying system appears to produce a continuous score before or alongside the final decision.

Therefore, simply modelling the binary decision would discard useful information about the black-box function.

---

### 3. Assuming correlation represents causation

The correlation results alone cannot establish that changing a feature will necessarily increase or decrease the score.

For example, the strong positive relationship between `account_age_days` and score does not prove that increasing account age always increases score under every combination of other parameters.

The same applies to the negative relationship between `months_active` and score.

These relationships should therefore be treated as hypotheses for controlled black-box experiments rather than final causal conclusions.

---

### 4. Assuming all features are independent

The strong correlations between several input variables indicate that the parameters can move together in the observed data.

Examples include:

- `amount` ↔ `beneficiaries`: +0.689
- `months_active` ↔ `trust_score`: +0.659
- `account_age_days` ↔ `months_active`: −0.622

This means marginal correlations may partially reflect relationships between the predictors themselves.

---

## What we are still unsure about

The main unresolved question is **how these variables interact inside the black-box scoring function**.

In particular, we still need to determine:

1. Whether `account_age_days` has a genuinely causal positive effect on score when all other variables are held constant.

2. Whether the negative relationship between `months_active` and score is causal or is partly caused by its strong relationship with `account_age_days`.

3. Why `trust_score` has a strong negative association with score in the combined dataset, despite the controlled Round 1 experiments showing that the effect of trust-related values is not necessarily monotonic.

4. Whether `utilisation` has an independent positive effect or whether its relationship with score depends strongly on other parameters.

5. Whether the black-box system contains important **feature interactions**, thresholds, nonlinearities, or optimal parameter regions.

6. Whether combinations such as:
   - `account_age_days × months_active`
   - `account_age_days × trust_score`
   - `trust_score × utilisation`
   - `months_active × utilisation`
   
   produce substantially different scores than would be expected from the individual feature effects.

7. Whether the strong correlations observed in the randomized Round 2 data continue to hold under controlled one-variable-at-a-time experiments.

---

## Next Investigation

The next stage should focus on controlled experiments rather than additional passive correlation analysis.

The highest-priority experiments are:

### Experiment A — Account age

Hold all other parameters constant and vary:

`account_age_days`

across a controlled range.

### Experiment B — Months active

Hold all other parameters constant and vary:

`months_active`

across a controlled range.

### Experiment C — Trust score

Hold all other parameters constant and test multiple trust-score regions, including the region around the high-scoring values observed during Round 1.

### Experiment D — Utilisation

Hold all other parameters constant and vary:

`utilisation`

from low to high values.

### Experiment E — Feature interactions

After identifying the strongest individual effects, vary two parameters simultaneously to determine whether their effects are additive, conditional, or nonlinear.

The objective is to move from **correlation-based hypotheses** to **controlled causal evidence** about the black-box scoring function.

---

## Summary

Round 2 analysis identified a strong relationship between the output score and several account characteristics.

The strongest observed associations were:

- `account_age_days`: **+0.816**
- `months_active`: **−0.807**
- `trust_score`: **−0.732**
- `utilisation`: **+0.657**

The analysis also identified strong relationships between input variables, particularly `amount` and `beneficiaries`, indicating that the system may contain correlated or interacting dimensions.

The evidence currently supports the hypothesis that the black-box score is generated from multiple interacting variables rather than a simple one-feature rule.

However, correlation and VIF analysis alone cannot establish the exact scoring mechanism. The next phase will therefore prioritize controlled black-box experiments to isolate individual feature effects and identify nonlinearities and feature interactions.
