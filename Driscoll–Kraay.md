---
title: Driscoll–Kraay
aliases: [Driscoll-Kraay, Driscoll–Kraay standard errors, Driscoll-Kraay standard errors, DK standard errors]
tags: [econometrics, inference, panel-data, standard-errors, time-series]
updated: 2026-03-05
---

# Driscoll–Kraay

> [!summary]
> Nonparametric covariance estimator for panel data that is robust to very general forms of cross-sectional and temporal dependence. Extends [[Newey–West]] to panels by averaging moment conditions across cross-sectional units before applying HAC.

## When to use

Use Driscoll–Kraay when you have a long panel ($T$ large relative to $N$) with potential correlation across both time and units. Unlike [[clustered standard errors]], DK handles both arbitrary within-unit serial correlation *and* arbitrary cross-sectional correlation. Particularly useful for macro panels (countries, states) where spatial spillovers and common shocks are plausible.

## Stata

```stata
xtscc y x1 x2, fe lag(3)  // FE with Driscoll-Kraay SEs, 3 lags
```

## Python

```python
from linearmodels.panel import PanelOLS
model = PanelOLS(y, X, entity_effects=True)
result = model.fit(cov_type='kernel', kernel='bartlett', bandwidth=3)
```

> [!tip]
> Choose lag truncation $L \approx T^{1/4}$ or use automatic selection. DK SEs are conservative with short $T$; [[clustered standard errors]] may be preferable for $T < 20$.

## Related notes

- [[Newey–West]]
- [[clustered standard errors]]
- [[Conley standard errors]]
- [[Panel Data Methods (MOC)]]
