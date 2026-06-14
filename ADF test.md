---
title: ADF Test
aliases: [ADF test, augmented Dickey-Fuller test, Dickey-Fuller test, unit root test]
tags: [econometrics, time-series, diagnostics, stationarity]
updated: 2026-03-05
---

# ADF Test

> [!summary]
> Augmented Dickey–Fuller test for a unit root. Null: series has a unit root (non-stationary). Augments the basic DF regression with lagged differences to account for serial correlation.

## Test regression

The ADF test estimates one of three specifications:

$$\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^{p} \delta_i \Delta y_{t-i} + \varepsilon_t$$

where $\gamma = \rho - 1$. The null hypothesis is $H_0: \gamma = 0$ (unit root) vs. $H_1: \gamma < 0$ (stationary). The number of lags $p$ is chosen via information criteria (AIC/BIC) or sequential tests.

## Python

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(series, maxlag=None, regression='ct', autolag='AIC')
print(f"ADF statistic: {result[0]:.3f}, p-value: {result[1]:.3f}")
# regression: 'c' (constant), 'ct' (constant+trend), 'n' (no constant)
```

> [!tip]
> If ADF fails to reject (p > 0.05), consider first-differencing before modeling. Cross-check with KPSS test (null = stationary) to distinguish unit root from structural breaks.

## Related notes

- [[KPSS test]]
- [[PP test]]
- [[ARIMA]]
- [[Time Series (MOC)]]
