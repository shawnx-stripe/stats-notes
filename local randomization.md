---
title: Local Randomization
aliases: [local randomization, local randomization framework]
tags: [econometrics, rdd, identification]
updated: 2026-03-05
---

# Local Randomization

> [!summary]
> Alternative framework for RDD inference that assumes treatment is as-if randomly assigned within a narrow window around the cutoff. Enables exact (Fisher) inference methods rather than large-sample local polynomial approaches.

## Identification assumption

Define a window $W = [c - w, c + w]$ around cutoff $c$. Within $W$:
$$
D_i \perp\!\!\perp (Y_i(0), Y_i(1), X_i) \quad \text{for } R_i \in W
$$
where $R_i$ is the running variable. This is **stronger** than continuity but permits exact finite-sample inference.

> [!tip]
> Local randomization is appropriate when:
> - Units cannot precisely manipulate the running variable within $W$
> - Covariates are balanced within $W$ ([[covariate balance]])
> - The window is narrow enough that potential outcomes are nearly constant

## Key advantage

Enables **randomization inference** (permutation tests) without large-sample approximations. Useful when:
- Sample size near cutoff is small
- Concerned about local polynomial bandwidth sensitivity
- Want exact p-values rather than asymptotic

## Minimal code snippets

```r
# R: local randomization with rdlocrand
library(rdlocrand)

# Select window using covariate balance
rdwinselect(R = df$running_var, X = df[, c("cov1", "cov2")], cutoff = 0)

# Randomization inference within chosen window
rdrandinf(Y = df$outcome, R = df$running_var, cutoff = 0, wl = -0.5, wr = 0.5)
```

```python
# Python: manual randomization inference (simplified)
import numpy as np

window = df[(df['running_var'] >= -0.5) & (df['running_var'] <= 0.5)]
obs_diff = window[window['D'] == 1]['Y'].mean() - window[window['D'] == 0]['Y'].mean()

# Permutation test
np.random.seed(42)
n_perm = 5000
perm_diffs = []
for _ in range(n_perm):
    perm_D = np.random.permutation(window['D'])
    perm_diffs.append(window.loc[perm_D == 1, 'Y'].mean() - window.loc[perm_D == 0, 'Y'].mean())

p_value = (np.abs(perm_diffs) >= np.abs(obs_diff)).mean()
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[randomization inference]]
- [[bandwidth selection]]
