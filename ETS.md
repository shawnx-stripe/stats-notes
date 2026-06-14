---
title: ETS
aliases: [ETS, exponential smoothing, error-trend-seasonal, Holt-Winters]
tags: [time-series, forecasting]
updated: 2026-03-05
---

# ETS

> [!summary]
> Error–Trend–Seasonal state-space framework for exponential smoothing. Encompasses simple, Holt (trend), and Holt–Winters (trend + seasonal) methods with additive or multiplicative components. Automatic model selection via information criteria.

## Model taxonomy

ETS(Error, Trend, Seasonal) uses one-letter codes: A (additive), M (multiplicative), N (none). Examples:
- ETS(A,N,N): Simple exponential smoothing
- ETS(A,A,N): Holt's linear trend
- ETS(A,A,A): Additive Holt–Winters
- ETS(M,Ad,M): Multiplicative errors, damped trend, multiplicative seasonality

Automatic selection chooses among 30 models via AIC/BIC.

## Python

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
model = ExponentialSmoothing(y, seasonal='add', seasonal_periods=12)
fit = model.fit(optimized=True)
forecast = fit.forecast(steps=12)
```

> [!tip]
> ETS often outperforms ARIMA for short-term forecasts with strong seasonality. For long series with multiple seasonal patterns, use [[TBATS]].

## Related notes

- [[ARIMA]]
- [[TBATS]]
- [[Prophet]]
- [[Time Series (MOC)]]
