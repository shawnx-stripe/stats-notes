---
title: Johansen
aliases: [Johansen, Johansen test, Johansen cointegration test, trace test, maximum eigenvalue test]
tags: [econometrics, time-series, cointegration]
updated: 2026-03-05
---

# Johansen

> [!summary]
> System-based cointegration test using VAR representation. Determines the number of cointegrating vectors via trace and maximum eigenvalue statistics. More general than [[Engle–Granger]]; handles multiple cointegrating relationships.

## Test Statistics

Consider a [[VECM]] with $k$ variables and $r$ cointegrating vectors ($0 \leq r < k$):

**Trace test**: $H_0: r \leq r_0$ vs. $H_a: r > r_0$
$$
\text{LR}_{\text{trace}}(r_0) = -T \sum_{i=r_0+1}^k \ln(1 - \hat{\lambda}_i)
$$

**Maximum eigenvalue test**: $H_0: r = r_0$ vs. $H_a: r = r_0 + 1$
$$
\text{LR}_{\text{max}}(r_0) = -T \ln(1 - \hat{\lambda}_{r_0+1})
$$

where $\hat{\lambda}_i$ are the ordered eigenvalues from the reduced rank regression.

## Code

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen

# Test cointegration (trace and max eigenvalue)
result = coint_johansen(df[['y1', 'y2', 'y3']], det_order=0, k_ar_diff=1)
print(result.lr1)  # trace statistic
print(result.cvt)  # critical values
```

## Related notes

- [[cointegration]]
- [[Engle–Granger]]
- [[VECM]]
- [[VAR]]
- [[Time Series (MOC)]]
