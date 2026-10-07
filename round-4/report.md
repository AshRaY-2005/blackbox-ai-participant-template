# round-4 — Reconstruct

**Team:** BB-004  
**Queries used:** 250 / budget

---

## What we concluded

We reconstructed the black-box scoring and decision behavior using a diverse set of observations rather than relying on an APPROVE-heavy query strategy.

The system is **multi-feature and non-linear**. No single feature or simple linear formula explains the observed scores.

Our final dataset contains **280 observations**:

- APPROVE: 207
- DECLINE: 73

A key strength of our approach was deliberately obtaining both decision outcomes. A heavily imbalanced strategy such as **95 APPROVE / 5 DECLINE out of 100 queries** can produce an artificially high accuracy because the model can favor the majority class without properly learning the DECLINE boundary.

Our data is not perfectly 50/50 balanced, but it provides substantially more information about the decision boundary. We further used **SMOTE only on the training data** to reduce the remaining class imbalance. The test set was kept untouched.

For score reconstruction, **CatBoost** performed best:

- R²: **0.8666**
- MAE: **0.0579**
- RMSE: **0.1030**

For decision prediction, **Logistic Regression + StandardScaler** achieved:

- ROC-AUC: **0.9772**
- Average Precision: **0.9568**

The results demonstrate strong predictive reconstruction, although the exact hidden formula and exact decision threshold remain unknown.

---

## How we got there

### 1. Query strategy

We used the 250-query budget to explore different configurations of:

- account age
- account balance
- amount
- beneficiaries
- channel
- linked cards
- months active
- recent chargebacks
- trust score
- utilisation

The objective was to observe different score and decision regions instead of repeatedly querying obvious APPROVE cases.

### 2. Data preparation

The final dataset contained 280 observations and 13 original columns.

For modeling, we removed the following columns to prevent target leakage:

```text
score
decision
id
```

The remaining 10 input features were used for reconstruction, with feature engineering producing 27 final features.

### 3. Controlled observations

The strongest observed relationships were:

| Relationship | Spearman |
|---|---|
| score ↔ account_age_days | +0.816 |
| score ↔ months_active | -0.807 |
| score ↔ trust_score | -0.732 |
| score ↔ utilisation | +0.657 |

Controlled experiments showed:

- Increasing account_age_days generally increased score.
- months_active showed a negative effect in controlled configurations.
- trust_score behaved non-linearly rather than monotonically.
- utilisation affected the score.
- Channel affected the score, but was weaker than the main numerical features.

The trust-score behavior was especially important: values around 345–355 produced very high scores in some controlled configurations, while substantially larger values could produce lower scores. This ruled out a simple "higher trust = higher score" assumption.

### 4. Model comparison

We compared linear models, tree ensembles, boosting methods, and a neural network.

| Model | R² | MAE | RMSE |
|---|---|---|---|
| CatBoost | 0.8666 | 0.0579 | 0.1030 |
| XGBoost | 0.8638 | 0.0588 | 0.1035 |
| HistGradient Boosting | 0.8478 | 0.0626 | 0.1097 |
| Gradient Boosting | 0.8416 | 0.0622 | 0.1115 |
| LightGBM | 0.8417 | 0.0626 | 0.1115 |
| ElasticNet | 0.8203 | 0.0758 | 0.1188 |
| Extra Trees | 0.8152 | 0.0717 | 0.1219 |
| Ridge | 0.8004 | 0.0755 | 0.1237 |
| Random Forest | 0.7955 | 0.0746 | 0.1280 |
| Linear Regression | 0.7845 | 0.0762 | 0.1283 |
| Neural Network | 0.6340 | 0.1059 | 0.1705 |

CatBoost and XGBoost clearly outperformed the linear and neural-network approaches.

### 5. Decision reconstruction

The original decision distribution was:

- APPROVE = 207
- DECLINE = 73

We used SMOTE to improve minority-class representation only after the train/test split:

```text
Dataset
   ↓
Train / Test Split
   ↓
SMOTE → Training only
   ↓
Model
   ↓
Untouched Test Set
```

The strongest individual classifier was **Logistic Regression + StandardScaler**:

- ROC-AUC = 0.9772
- Average Precision = 0.9568

This demonstrated that the collected observations contain strong information about the hidden decision boundary.

---

## What we ruled out

### 1. Majority-class prediction

We ruled out relying on an APPROVE-heavy dataset. A distribution such as 95 APPROVE / 5 DECLINE can produce high accuracy without properly learning DECLINE cases.

### 2. A single-feature rule

No individual feature explained the complete score or decision behavior.

### 3. A purely linear scoring function

Linear Regression achieved R² = 0.7845, while CatBoost achieved 0.8666, showing substantial non-linear structure.

### 4. Higher trust always means higher score

Controlled observations showed non-monotonic trust-score behavior.

### 5. Neural networks automatically perform better

The neural network achieved only 0.6340 R², substantially below CatBoost and XGBoost.

### 6. Raw dataset is perfectly balanced

We do not claim 50/50 balance. The actual distribution is 207 APPROVE / 73 DECLINE.

Our claim is that our query strategy produced a more decision-diverse dataset than an extremely approval-skewed strategy, with SMOTE used to address remaining training imbalance.

### 7. SMOTE on the test set

SMOTE was applied only to training data. The test set remained untouched.

### 8. Exact hidden formula has been recovered

We reconstructed the behavior accurately enough for strong prediction, but the exact internal mathematical formula has not been established.

---

## What we are still unsure about

- The exact hidden scoring formula.
- The exact interaction terms between features.
- The exact threshold/rule converting score into APPROVE or DECLINE.
- The exact transformation applied to trust_score.
- Behavior outside the feature ranges covered by our queries.
- Whether additional targeted queries would significantly improve the reconstruction.

---

## Final conclusion

Our reconstruction shows that the black-box system is multi-variable, non-linear, and strongly learnable from limited observations.

- The strongest score model is **CatBoost** — R² 0.8666, RMSE 0.1030.
- The strongest individual decision model is **Logistic Regression + StandardScaler** — ROC-AUC 0.9772.

Most importantly, our approach did not optimize only for a misleading majority-class accuracy. We used the query budget to obtain a more diverse set of APPROVE and DECLINE observations and then used training-only SMOTE to further address class imbalance.

The exact black-box formula remains unresolved, but the observed behavior can be reconstructed with strong predictive performance.
