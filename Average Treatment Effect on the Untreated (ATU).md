---
title: Average Treatment Effect on the Untreated (ATU)
aliases: [ATU, average treatment effect on the untreated, ATE on untreated]
tags: [causal-inference, treatment-effects]
updated: 2026-03-05
---

# Average Treatment Effect on the Untreated (ATU)

> [!summary]
> Average Treatment Effect on the Untreated: $\text{ATU} = \mathbb{E}[Y(1)-Y(0) \mid D=0]$. Relevant for policy expansion — the expected benefit of treating those currently untreated.

## When to use

ATU answers: "What would happen if we expanded treatment to the control group?" Critical for policy decisions when considering universal rollout after an experiment. Under [[Unconfoundedness|unconfoundedness]], ATU can be identified via propensity score methods with weights $\frac{p(X)}{1-p(X)}$ applied to the treated group. In RCTs, ATU = ATE = ATT due to randomization, but with selection, ATU may differ substantially from [[Average Treatment Effect on the Treated (ATT)|ATT]].

## Python

```python
from sklearn.ensemble import GradientBoostingRegressor
ps = GradientBoostingRegressor().fit(X, D).predict_proba(X)[:, 1]
weights = ps / (1 - ps)
atu = np.average(y[D==1] - y[D==0].mean(), weights=weights[D==1])
```

## Related notes

- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[potential outcomes]]
