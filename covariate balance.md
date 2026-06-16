---
title: Covariate Balance
aliases: [covariate balance, balance diagnostics, standardized differences]
tags: [causal-inference, diagnostics]
updated: 2026-03-05
---

# Covariate Balance

> [!summary]
> Assessment of whether covariate distributions are similar across treatment groups after matching/weighting. Measured via standardized mean differences, variance ratios, or omnibus tests. Balance is necessary (not sufficient) for unbiased causal estimates.

## Key diagnostics

**Standardized mean difference (SMD)** for a continuous covariate $X$:
$$
\text{SMD} = \frac{\bar{X}_1 - \bar{X}_0}{\sqrt{(s_1^2 + s_0^2)/2}}
$$
Rule of thumb: $|\text{SMD}| < 0.1$ indicates good balance.

**Variance ratio**: $\text{VR} = s_1^2 / s_0^2$. Should be close to 1; red flags if $\text{VR} < 0.5$ or $\text{VR} > 2$.

> [!warning]
> Balance does not guarantee unconfoundedness—only that measured covariates are similar. Unmeasured confounders remain a threat. Use sensitivity analyses (e.g., [[Rosenbaum sensitivity]]) to assess robustness.

## Minimal code snippets

```r
# R: compute SMD with cobalt
library(cobalt)
bal.tab(treatment ~ age + income + edu, data = df, weights = "ipw_wt")
love.plot(treatment ~ age + income + edu, data = df, weights = "ipw_wt", thresholds = c(smd = 0.1))
```

```python
# Python: manual SMD calculation
import numpy as np
def smd(x1, x0):
    return (x1.mean() - x0.mean()) / np.sqrt((x1.var() + x0.var()) / 2)

treated = df[df['treatment'] == 1]['age']
control = df[df['treatment'] == 0]['age']
print(f"SMD: {smd(treated, control):.3f}")
```

## Related notes

- [[propensity score]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[entropy balancing]]
