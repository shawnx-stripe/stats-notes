---
title: seasonal differencing
aliases: [seasonal difference, seasonal differencing operator]
tags: [time-series, seasonality]
updated: 2026-06-16
---

# seasonal differencing

> [!summary] Quick definition
> Seasonal differencing subtracts a value from the same season in a prior cycle, such as $Y_t - Y_{t-12}$ for monthly data.

## When it matters

It can remove seasonal unit roots or persistent seasonal patterns before modeling. Over-differencing can add noise, so check seasonality diagnostics and model residuals.

## Related notes

- [[Interrupted Time Series (ITS)]]
- [[seasonality]]
- [[ARIMA]]
