---
title: Common Support
aliases: [common support, overlap condition, common support condition]
tags: [causal-inference, identification, assumptions]
updated: 2026-03-05
---

# Common Support

> [!summary]
> Requirement that for every covariate value, both treated and untreated units exist: $0 < P(D=1 \mid X=x) < 1$. Also called the overlap or positivity condition. Violation leads to extrapolation bias in matching/weighting estimators.

## Formal statement

$$
0 < e(x) = P(D=1 \mid X=x) < 1 \quad \forall x \in \operatorname{supp}(X)
$$

Without common support, we cannot observe both potential outcomes for some covariate values; causal effects are not identified from the data.

## Violations and remedies

| Situation | Problem | Solution |
|-----------|---------|----------|
| No controls with $X=x$ | No counterfactual for treated units at $x$ | Trim treated units outside common support |
| No treated with $X=x$ | No counterfactual for control units at $x$ | Trim control units or redefine estimand |
| Propensity score near 0 or 1 | Extreme weights in IPW | Use overlap weights or trimming |

> [!warning]
> Trimming changes the estimand from ATE to ATE on the common support region. Always report how many units are trimmed and check sensitivity.

## Python diagnostic

```python
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Estimate propensity scores
ps_model = LogisticRegression().fit(X, D)
ps = ps_model.predict_proba(X)[:, 1]

# Plot propensity score distributions by treatment group
plt.hist(ps[D==1], bins=30, alpha=0.5, label='Treated')
plt.hist(ps[D==0], bins=30, alpha=0.5, label='Control')
plt.axvline(0.1, color='r', linestyle='--', label='Trimming threshold')
plt.axvline(0.9, color='r', linestyle='--')
plt.legend()
plt.show()
# Common support: region where both histograms overlap
```

## Related notes

- [[Overlap]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[matching]]
- [[Identification Strategies (MOC)]]
