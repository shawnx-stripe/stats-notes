---
title: ARDL
aliases: [ARDL, autoregressive distributed lag, ARDL bounds test]
tags: [econometrics, time-series, cointegration]
updated: 2026-03-05
---

# ARDL

> [!summary]
> Autoregressive Distributed Lag model: includes lags of both the dependent variable and regressors. The ARDL bounds test (Pesaran, Shin & Smith 2001) tests for cointegration without requiring all series to be I(1).

## Model specification

$$y_t = \alpha + \sum_{i=1}^{p} \phi_i y_{t-i} + \sum_{j=0}^{q} \beta_j x_{t-j} + \varepsilon_t$$

The ARDL bounds test reformulates this in error-correction form and tests whether $y_t$ and $x_t$ are cointegrated. Key advantage: works with mixed I(0)/I(1) series, avoiding unit root pre-testing.

## R

```r
library(ARDL)
model <- auto_ardl(y ~ x, data = df, max_order = c(4, 4))
bounds_test(model)  # H0: no cointegration
```

> [!tip]
> The bounds test is valid even when regressors are endogenous, as long as errors are serially uncorrelated. Use information criteria to select lag orders.

## Related notes

- [[cointegration]]
- [[VECM]]
- [[VAR]]
- [[Time Series (MOC)]]
