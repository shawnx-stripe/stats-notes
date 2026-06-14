---
title: rddensity
aliases: [rddensity, manipulation density test]
tags: [econometrics, rdd, diagnostics, software]
updated: 2026-03-05
---

# rddensity

> [!summary]
> R/Stata package implementing density discontinuity tests for [[Regression Discontinuity Design (RDD)]]. Tests for bunching at the cutoff using local polynomial density estimation (Cattaneo, Jansson, Ma 2020). Modern alternative to the [[McCrary test]].

## Usage

```r
library(rddensity)

# Test for manipulation at cutoff
out <- rddensity(X = running_var, c = 0)
summary(out)

# Plot estimated densities
rdplotdensity(out, X = running_var)
```

## Interpretation

The null hypothesis is continuity of the density of the running variable at the cutoff:

$$
\lim_{x \uparrow c} f(x) = \lim_{x \downarrow c} f(x)
$$

Rejection indicates [[manipulation test|manipulation]]—units strategically sort around the threshold, threatening the local-as-random assumption of RDD.

> [!tip] Practical guidance
> Run this test before reporting RDD results. If rejected, consider robustness checks: exclude observations near the cutoff (donut-hole RDD), use a narrower bandwidth, or investigate which subgroups are manipulating.

## Related notes

- [[McCrary test]]
- [[manipulation test]]
- [[Regression Discontinuity Design (RDD)]]
- [[running variable]]
