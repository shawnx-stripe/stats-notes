---
title: KPSS Test
aliases: [KPSS test, KPSS, Kwiatkowski-Phillips-Schmidt-Shin test]
tags: [econometrics, time-series, diagnostics, stationarity]
updated: 2026-03-05
---

# KPSS Test

> [!summary]
> Stationarity test with null hypothesis of level or trend stationarity (opposite of unit-root tests like [[ADF test]]). Useful as a confirmatory test alongside ADF; when both reject, evidence of fractional integration.

## Test Statistic

For level stationarity ($H_0: y_t = \alpha + r_t$ where $r_t$ is $I(0)$):

$$
\text{KPSS} = \frac{1}{T^2 \hat{\sigma}^2} \sum_{t=1}^T S_t^2
$$

where $S_t = \sum_{s=1}^t \hat{e}_s$ (partial sum of residuals from $y_t = \alpha + e_t$) and $\hat{\sigma}^2$ is a consistent variance estimate.

Rejection → evidence against stationarity (unit root present).

> [!tip] Combined Testing Strategy
> | ADF | KPSS | Interpretation |
> |-----|------|----------------|
> | Fail to reject | Fail to reject | Inconclusive |
> | Reject | Fail to reject | Stationary |
> | Fail to reject | Reject | Unit root |
> | Reject | Reject | Possible fractional integration |

## Code

```python
from statsmodels.tsa.stattools import kpss

stat, p_value, lags, crit = kpss(y, regression='c', nlags='auto')
print(f'KPSS statistic: {stat:.4f}, p-value: {p_value:.4f}')
```

## Related notes

- [[ADF test]]
- [[PP test]]
- [[Time Series (MOC)]]
- [[ARIMA]]
