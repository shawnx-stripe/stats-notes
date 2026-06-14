---
title: Baxter–King Filter
aliases: [Baxter-King filter, Baxter–King, BK filter, band-pass filter]
tags: [time-series, filters]
updated: 2026-03-05
---

# Baxter–King Filter

> [!summary]
> Symmetric band-pass filter that isolates cyclical components of a time series within a specified frequency band. Approximates an ideal band-pass filter using a finite moving average; loses observations at endpoints.

## Key insight

BK extracts business cycle frequencies (e.g., 6–32 quarters) by applying symmetric weights to past and future observations. Unlike [[HP filter]], which only removes low frequencies, BK removes both high and low frequencies outside the target band. Loses $K$ observations at each end (typically $K=12$ for quarterly data), making it unsuitable for real-time forecasting.

## R

```r
library(mFilter)
filtered <- bkfilter(y, pl=6, pu=32, nfix=12)  # 6-32 quarter band
plot(filtered$cycle)  # cyclical component
```

> [!warning]
> The symmetric filter introduces phase shifts and is not causal. Use [[Christiano–Fitzgerald filter]] if you need end-of-sample estimates or real-time filtering.

## Related notes

- [[HP filter]]
- [[Christiano–Fitzgerald filter]]
- [[Time Series (MOC)]]
