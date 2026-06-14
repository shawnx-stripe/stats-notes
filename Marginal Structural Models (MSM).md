---
title: Marginal Structural Models (MSM)
aliases: [Marginal Structural Models, MSM, marginal structural model]
tags: [causal-inference, longitudinal, weighting]
updated: 2026-03-05
---

# Marginal Structural Models (MSM)

> [!summary]
> Models for causal effects of time-varying treatments in the presence of time-varying confounders affected by prior treatment. Estimated via [[Inverse Probability Weighting (IPW)|IPW]] with stabilized weights to handle the bias from conditioning on post-treatment variables.

## Key insight

Standard regression conditioning on time-varying confounders induces collider bias when those confounders are affected by prior treatment. MSMs avoid this by modeling the marginal distribution of potential outcomes, using IPW to reweight the observed data to mimic a pseudo-population where treatment is independent of covariates at every time point.

## Stabilized weights

$$
SW_i(t) = \prod_{s=0}^{t} \frac{P(A_s = a_s \mid \bar{A}_{s-1} = \bar{a}_{s-1})}{P(A_s = a_s \mid \bar{L}_s, \bar{A}_{s-1} = \bar{a}_{s-1})}
$$

Numerator uses treatment history only; denominator adds time-varying covariates $\bar{L}_s$. Stabilized weights have mean near 1, reducing variance compared to unstabilized IPW.

## Python snippet

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

# At each time t, fit propensity score P(A_t | L_t, A_{t-1}, ...)
ps_model = LogisticRegression()
ps_model.fit(X_confounders_and_history, treatment_t)
ps_denom = ps_model.predict_proba(X_confounders_and_history)[:, 1]

# Fit numerator model P(A_t | A_{t-1}, ...)
ps_num_model = LogisticRegression()
ps_num_model.fit(X_history_only, treatment_t)
ps_num = ps_num_model.predict_proba(X_history_only)[:, 1]

# Compute stabilized weight at time t
sw_t = np.where(treatment_t == 1, ps_num / ps_denom, (1 - ps_num) / (1 - ps_denom))
# Cumulative product over time for final weight
```

## Related notes

- [[Inverse Probability Weighting (IPW)|IPW]]
- [[LTMLE]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Unconfoundedness]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
