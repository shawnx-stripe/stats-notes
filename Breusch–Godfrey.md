---
title: Breusch–Godfrey
aliases: [Breusch-Godfrey, Breusch–Godfrey test, LM test for serial correlation]
tags: [econometrics, diagnostics, time-series]
updated: 2026-03-05
---

# Breusch–Godfrey

> [!summary]
> Lagrange multiplier test for serial correlation (up to order $p$) in regression residuals. More general than [[Durbin–Watson]]; valid with lagged dependent variables and other regressors.

## Test procedure

1. Estimate original regression and save residuals $\hat{\varepsilon}_t$
2. Regress $\hat{\varepsilon}_t$ on original regressors plus $\hat{\varepsilon}_{t-1}, \ldots, \hat{\varepsilon}_{t-p}$
3. Test statistic: $(n-p)R^2 \sim \chi^2_p$ under null of no serial correlation

The test is asymptotically equivalent to a Wald test but computationally simpler. Unlike Durbin–Watson, it tests general AR($p$) alternatives and remains valid with stochastic regressors.

## Stata

```stata
reg y x1 x2 L.y
estat bgodfrey, lags(1/4)  // test AR(1) through AR(4)
```

> [!tip]
> If the test rejects, use [[Newey–West]] HAC standard errors or model the serial correlation explicitly via GLS or AR errors.

## Related notes

- [[Durbin–Watson]]
- [[Newey–West]]
- [[Econometrics (MOC)]]
