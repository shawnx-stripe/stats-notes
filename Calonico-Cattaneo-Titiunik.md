---
title: Calonico–Cattaneo–Titiunik
aliases: [Calonico-Cattaneo-Titiunik, Calonico–Cattaneo–Titiunik (CCT), CCT, CCT bandwidth, robust bias-corrected inference]
tags: [econometrics, rdd, inference]
updated: 2026-03-05
---

# Calonico–Cattaneo–Titiunik

> [!summary]
> Framework for robust bias-corrected inference in [[Regression Discontinuity Design (RDD)]]. Provides MSE-optimal bandwidth selection and honest confidence intervals that account for smoothing bias. Implemented in `rdrobust`.

## Key innovation

Standard RDD inference ignores bias from polynomial approximation, leading to under-coverage. CCT explicitly estimates and corrects for this bias using a higher-order pilot estimate, then constructs robust confidence intervals. The MSE-optimal bandwidth minimizes $\text{Bias}^2 + \text{Variance}$, but CCT recommends the CER-optimal bandwidth for coverage-corrected inference.

## R / Stata

```r
library(rdrobust)
result <- rdrobust(y, running_var, c = 0, kernel = "triangular")
summary(result)  # bias-corrected CI, optimal bandwidth
```

```stata
rdrobust y running_var, c(0) all  // reports conventional + robust CI
```

> [!tip]
> Always report both conventional and robust CIs. If they differ substantially, bias is important. Use `rdbwselect` to explore alternative bandwidth selectors.

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[rdrobust]]
- [[rddensity]]
- [[bandwidth selection]]
- [[MSE-optimal bandwidth]]
