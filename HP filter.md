---
title: HP Filter
aliases: [HP filter, Hodrick-Prescott filter, Hodrick–Prescott filter]
tags: [time-series, filters]
updated: 2026-03-05
---

# HP Filter

> [!summary]
> Hodrick–Prescott filter: decomposes a time series into trend and cyclical components by minimizing a penalized sum of squares. Widely used but criticized for spurious cycle generation, endpoint instability, and poor frequency-domain properties.

## Formula

Decompose $y_t = \tau_t + c_t$ (trend + cycle) by solving:

$$
\min_{\{\tau_t\}} \sum_{t=1}^T (y_t - \tau_t)^2 + \lambda \sum_{t=2}^{T-1} [(\tau_{t+1} - \tau_t) - (\tau_t - \tau_{t-1})]^2
$$

Standard $\lambda$ values: 100 (annual), 1600 (quarterly), 14400 (monthly).

> [!warning]
> - **Spurious cycles**: HP filter can induce oscillations not present in the data
> - **Endpoint problem**: unreliable estimates at the beginning/end of the sample
> - **Hamilton (2018) critique**: recommends using $y_{t+h} - y_t$ linear projection instead
> - Not recommended for trend-cycle decomposition in modern practice

## Code

```python
import statsmodels.api as sm

# Apply HP filter
cycle, trend = sm.tsa.filters.hpfilter(y, lamb=1600)
```

## Related notes

- [[Baxter–King filter]]
- Time Series–Fitzgerald filter
- [[Time Series (MOC)]]
