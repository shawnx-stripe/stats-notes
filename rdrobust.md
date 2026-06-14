---
title: rdrobust
aliases: [rdrobust, RD robust]
tags: [econometrics, rdd, software]
updated: 2026-03-05
---

# rdrobust

> [!summary]
> R/Stata package for robust RDD analysis implementing MSE-optimal bandwidth selection, local polynomial estimation, and robust bias-corrected inference following [[Calonico-Cattaneo-Titiunik]].

## Basic usage

```r
library(rdrobust)

# Automatic bandwidth, bias-corrected inference
out <- rdrobust(y = outcome, x = running_var, c = 0)
summary(out)

# Visualize RD plot
rdplot(y = outcome, x = running_var, c = 0, ci = 95)
```

## Key features

- **MSE-optimal bandwidth**: Data-driven selection balancing bias and variance
- **Bias correction**: Uses higher-order polynomial to correct for bias in the point estimate
- **Robust inference**: Adjusts standard errors for bias-correction
- **Covariates**: Includes pre-treatment $X$ to improve precision

> [!tip] Standard practice
> Always use `rdrobust` defaults for primary specification. Report the MSE-optimal bandwidth and show robustness to alternative bandwidths ($0.5h$, $2h$). Check sensitivity to polynomial order (though defaults usually work well).

## Stata equivalent

```stata
rdrobust outcome running_var, c(0) all
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[Calonico-Cattaneo-Titiunik]]
- [[rddensity]]
- [[bandwidth selection]]
