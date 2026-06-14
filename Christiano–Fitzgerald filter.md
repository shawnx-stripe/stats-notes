---
title: Christiano–Fitzgerald Filter
aliases: [Christiano-Fitzgerald filter, CF filter]
tags: [time-series, filters]
updated: 2026-03-05
---

# Christiano–Fitzgerald Filter

> [!summary]
> Asymmetric band-pass filter that can use the full sample (unlike [[Baxter–King filter]]). Approximates the ideal filter assuming the series follows a random walk; suitable for real-time and end-of-sample analysis.

## When to use

Use CF when you need filtered estimates at the endpoints of your sample (e.g., for current business cycle assessment). Unlike [[Baxter–King filter]], CF doesn't lose observations but relies on extrapolation under the random walk assumption. The filter optimally weights past and future observations based on their distance from time $t$, adapting the weights to the series properties.

## R

```r
library(mFilter)
filtered <- cffilter(y, pl=6, pu=32, drift=FALSE)  # 6-32 quarter band
plot(filtered$cycle)  # no endpoint loss
```

> [!warning]
> CF assumes the series is I(1). For I(0) or I(2) series, pre-filter appropriately or use [[Baxter–King filter]] with trimmed sample.

## Related notes

- [[Baxter–King filter]]
- [[HP filter]]
- [[Time Series (MOC)]]
