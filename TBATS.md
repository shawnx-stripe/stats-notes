---
title: TBATS
aliases: [TBATS, trigonometric seasonality, Box-Cox ARMA trend seasonal]
tags: [time-series, forecasting]
updated: 2026-03-05
---

# TBATS

> [!summary]
> Exponential smoothing state-space model with Box–Cox transformation, ARMA errors, Trend, and Seasonal components using trigonometric (Fourier) representation. Handles multiple and high-frequency seasonal periods.

## Model components

$$
y_t^{(\lambda)} = \ell_{t-1} + \phi b_{t-1} + \sum_{i=1}^M s_{t-m_i}^{(i)} + d_t
$$

where:
- $y_t^{(\lambda)}$ is the Box–Cox transformed series
- $\ell_t, b_t$ are level and trend
- $s_t^{(i)}$ are seasonal components represented as Fourier terms
- $d_t$ is ARMA($p,q$) error

Each seasonal component uses trigonometric basis functions, allowing for complex and long seasonal periods (e.g., daily + weekly + yearly).

## When to use

- Multiple seasonal patterns (e.g., hourly data with daily and weekly cycles)
- High-frequency seasonality (e.g., 168 periods for hourly weekly cycles)
- Data with non-constant variance (Box–Cox handles this)
- Standard [[ETS]] or [[ARIMA]] models are too restrictive

## R snippet

```r
library(forecast)
tbats_model <- tbats(ts_data, use.box.cox = TRUE, use.trend = TRUE)
forecast(tbats_model, h = 24)
```

> [!tip]
> TBATS is computationally intensive for very long series. For simpler seasonality, try [[ETS]] or [[Prophet]] first.

## Related notes

- [[ETS]]
- [[ARIMA]]
- [[Prophet]]
- [[seasonality]]
- [[Time Series (MOC)]]
