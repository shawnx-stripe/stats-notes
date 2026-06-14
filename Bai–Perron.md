---
title: Bai–Perron
aliases: [Bai-Perron, Bai–Perron test, multiple structural breaks, structural break test]
tags: [econometrics, time-series, structural-breaks, diagnostics]
updated: 2026-03-05
---

# Bai–Perron

> [!summary]
> Framework for detecting and dating multiple structural breaks in linear regression models. Sequential and global break-date estimation via dynamic programming; SupF, UDmax, and sequential tests for the number of breaks.

## When to use

Use when you suspect regime changes in a time series relationship but don't know the break dates or number of breaks. Common applications: policy regime changes, business cycle dating, structural shifts in demand elasticities. The method estimates break points by minimizing global SSR subject to a minimum segment length (typically 15% of sample).

## Python

```python
from statsmodels.sandbox.regression.structural_breaks import SupF
model = SupF(y, X, m=5, trim=0.15)  # test up to 5 breaks
print(model.test_results())  # SupF, UDmax, WDmax tests
```

> [!tip]
> Start with UDmax (equal-weighted) or WDmax (weighted) test to determine the number of breaks, then estimate break dates. Pre-whiten data if errors are serially correlated using HAC.

## Related notes

- [[Time Series (MOC)]]
- [[Markov switching]]
- [[ARIMA]]
