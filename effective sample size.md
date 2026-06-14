---
title: Effective Sample Size
aliases: [effective sample size, ESS]
tags: [econometrics, inference, weighting]
updated: 2026-03-05
---

# Effective Sample Size

> [!summary]
> The number of equally-weighted observations that would give the same precision as a weighted sample: $\text{ESS} = (\sum w_i)^2 / \sum w_i^2$. Diagnoses extreme weight concentration in [[Inverse Probability Weighting (IPW)|IPW]] and survey weighting.

## Formula and interpretation

$$
\text{ESS} = \frac{\left(\sum_{i=1}^n w_i\right)^2}{\sum_{i=1}^n w_i^2}
$$

For normalized weights $\tilde{w}_i = w_i / \sum_j w_j$:
$$
\text{ESS} = \frac{1}{\sum_{i=1}^n \tilde{w}_i^2}
$$

**Interpretation**: ESS is the number of observations if all had equal weight. $\text{ESS} / n$ measures efficiency loss from weighting.

> [!warning]
> ESS < 0.1n indicates severe weight concentration—a few observations dominate the weighted estimate. Consider trimming extreme propensity scores or using overlap weights instead of IPW.

## Minimal code snippets

```python
# Python: compute ESS from normalized weights
import numpy as np

w = df['ipw_weight'].values
w_norm = w / w.sum()
ess = 1 / (w_norm**2).sum()
print(f"ESS: {ess:.0f} / {len(w)} = {ess/len(w):.2%}")
```

```r
# R: ESS from unnormalized weights
w <- df$ipw_weight
ess <- sum(w)^2 / sum(w^2)
cat("Effective sample size:", round(ess), "out of", nrow(df), "\n")
```

## Related notes

- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Robust Methods (MOC)]]
- [[Standard Errors and Inference (MOC)]]
