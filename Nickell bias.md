---
title: Nickell Bias
aliases: [Nickell bias, dynamic panel bias, incidental parameters bias]
tags: [econometrics, panel-data, dynamic-panels]
updated: 2026-03-05
---

# Nickell Bias

> [!summary]
> Inconsistency of the fixed-effects estimator in dynamic panels (with lagged dependent variable) when $T$ is small. The within-transformation creates correlation between the transformed lagged DV and the error. Remedy: [[Arellano–Bond]] or bias correction.

## Source of bias

$$
y_{it} = \rho y_{it-1} + x_{it}\beta + \alpha_i + \epsilon_{it}
$$

FE within-transformation: $\tilde{y}_{it} = y_{it} - \bar{y}_i$. Then $\tilde{y}_{it-1}$ depends on $\epsilon_{it-1}$, but $\bar{y}_i$ includes $\epsilon_{it}$, inducing correlation between the transformed lagged DV and the transformed error. Bias is $O(1/T)$; negligible for large $T$.

## Magnitude

For small $T$ (e.g., $T \leq 10$), the bias can be substantial, typically downward (toward zero). Rule of thumb: Nickell bias is serious when $T < 20$.

> [!warning]
> Do not use FE for dynamic panels with $T < 20$. Use [[Arellano–Bond]] difference GMM, [[System GMM]], or bias-corrected FE estimators instead.

## Python snippet (bias-corrected FE)

```python
from linearmodels.panel import PanelOLS
# Use bias-corrected dynamic panel estimators or GMM
# Standard FE will be biased in short panels with lagged DV
```

## Related notes

- [[Arellano–Bond]]
- [[two-way fixed effects]]
- [[Panel Data Methods (MOC)]]
