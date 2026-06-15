---
title: block bootstrap
aliases: [moving block bootstrap, stationary bootstrap]
tags: [bootstrap, time-series, dependence]
updated: 2026-06-16
---

# block bootstrap

> [!summary] Quick definition
> Block bootstrap methods resample contiguous blocks to preserve serial or spatial dependence within blocks.

## When it matters

Use block bootstrap for time series or ordered data where iid resampling would break dependence. Block length controls the bias-variance tradeoff: short blocks understate dependence, while long blocks reduce effective resamples.

## Related notes

- [[bootstrap]]
- [[Time Series (MOC)]]
- [[Newey–West]]
