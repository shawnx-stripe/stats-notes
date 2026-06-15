---
title: BCa bootstrap
aliases: [bias-corrected and accelerated bootstrap, BCa interval]
tags: [bootstrap, inference]
updated: 2026-06-16
---

# BCa bootstrap

> [!summary] Quick definition
> The BCa bootstrap adjusts percentile intervals for median bias and skewness using bias-correction and acceleration constants.

## When it matters

BCa intervals often improve coverage for skewed bootstrap distributions, but they require stable jackknife estimates and enough resamples. They are less appropriate when the statistic is highly nonsmooth or the bootstrap itself is inconsistent.

## Related notes

- [[bootstrap]]
- [[confidence intervals]]
- [[bias estimation]]
