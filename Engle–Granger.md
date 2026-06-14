---
title: Engle–Granger
aliases: [Engle-Granger, Engle–Granger test, EG test, residual-based cointegration test]
tags: [econometrics, time-series, cointegration]
updated: 2026-03-05
---

# Engle–Granger

> [!summary]
> Two-step residual-based cointegration test: (1) estimate the cointegrating regression by OLS; (2) test the residuals for a unit root. Simple but limited to a single cointegrating vector; for multiple vectors use [[Johansen]].

## Procedure

1. Estimate $y_t = \alpha + \beta x_t + u_t$ by OLS (superconsistent if cointegrated)
2. Save residuals $\hat{u}_t$ and run [[ADF test]] on $\hat{u}_t$ (no constant or trend)
3. If $\hat{u}_t$ is stationary, conclude $y_t$ and $x_t$ are cointegrated with vector $[1, -\beta]$

Critical values differ from standard ADF (use MacKinnon tables) because $\hat{u}_t$ contains estimation error.

## Python

```python
from statsmodels.tsa.stattools import coint
score, pvalue, crit_values = coint(y, x)
print(f"EG test: {score:.2f}, p-value: {pvalue:.3f}")
# pvalue < 0.05 rejects null of no cointegration
```

> [!warning]
> EG assumes a *single* cointegrating relationship and is sensitive to which variable is normalized. Use [[Johansen]] for systems with multiple cointegrating vectors.

## Related notes

- [[cointegration]]
- [[Johansen]]
- [[VECM]]
- [[ADF test]]
- [[Time Series (MOC)]]
