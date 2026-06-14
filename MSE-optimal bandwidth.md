---
title: MSE-Optimal Bandwidth
aliases: [MSE-optimal bandwidth, optimal bandwidth selection]
tags: [econometrics, rdd, nonparametric]
updated: 2026-03-05
---

# MSE-Optimal Bandwidth

> [!summary]
> Bandwidth chosen to minimize mean squared error of the local polynomial estimator at the RDD cutoff. Balances squared bias (decreasing in bandwidth) and variance (increasing in bandwidth). Implemented in [[rdrobust]] following [[Calonico-Cattaneo-Titiunik]].

## Bias-Variance Trade-off

Local polynomial estimator at cutoff $c$ has:

$$
\text{MSE}(h) = \text{Bias}^2(h) + \text{Variance}(h)
$$

- **Bias**: Decreases with $h$ (more data, less extrapolation error); proportional to $h^{p+1}$ for polynomial degree $p$
- **Variance**: Increases with $h$ (noisier estimates); proportional to $1/(nh)$

**Optimal bandwidth**: $h^* \propto n^{-1/(2p+3)}$ (for local polynomial of degree $p$).

> [!tip]
> - **CCT implementation**: [[rdrobust]] computes MSE-optimal bandwidth with robust bias correction
> - **Sensitivity**: Report point estimates and confidence intervals for multiple bandwidths
> - **Coverage-optimal bandwidth**: Alternative that optimizes CI coverage rather than MSE (often larger)

## Code

```r
# R: rdrobust with MSE-optimal bandwidth
library(rdrobust)
rd <- rdrobust(y, running_var, c = cutoff, bwselect = "mserd")
summary(rd)
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[rdrobust]]
- [[Calonico-Cattaneo-Titiunik]]
- [[bandwidth selection]]
