---
title: Diebold–Mariano Test
aliases: [Diebold-Mariano test, Diebold–Mariano test, DM test]
tags: [time-series, forecasting, diagnostics]
updated: 2026-03-05
---

# Diebold–Mariano Test

> [!summary]
> Test for equal predictive accuracy between two forecast methods. Robust to non-Gaussian, non-zero-mean, serially correlated, and contemporaneously correlated forecast errors. Modified version (Harvey, Leybourne & Newbold) improves small-sample size.

## Test statistic

Define loss differential $d_t = L(e_{1t}) - L(e_{2t})$ where $L(\cdot)$ is a loss function (e.g., squared or absolute error). Under null of equal accuracy, $\mathbb{E}[d_t] = 0$. Test:

$$\text{DM} = \frac{\bar{d}}{\sqrt{\hat{V}(\bar{d})/h}} \xrightarrow{d} N(0,1)$$

where $\hat{V}$ uses HAC to account for serial correlation in $d_t$ and $h$ is the forecast horizon.

## Python

```python
from scipy.stats import norm
d = loss1 - loss2  # forecast loss differences
dm_stat = d.mean() / (d.std() / np.sqrt(len(d)))
p_value = 2 * norm.cdf(-abs(dm_stat))
```

## Related notes

- [[MASE]]
- [[Time Series (MOC)]]
- [[cross-validation]]
