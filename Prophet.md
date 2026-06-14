---
title: Prophet
aliases: [Facebook Prophet, prophet, additive time-series model]
tags: [time-series, forecasting, decomposition, holidays, changepoints, seasonality, regression]
updated: 2025-09-17
---

# Prophet

> [!summary] Quick definition
> Prophet is an additive time-series model and library (Python/R) for automatic forecasting with trend, multiple seasonalities, and holiday effects:
> $$
> y(t) = g(t) + s(t) + h(t) + \varepsilon_t
> $$
> - g(t): piecewise linear or logistic growth trend with changepoints  
> - s(t): seasonal components (weekly/annual, arbitrary via Fourier)  
> - h(t): holiday/event effects (calendar regressors)  
> - ε_t: error term (Gaussian by default)

- Strengths: robust defaults, built-in holidays, missing/outlier tolerance, fast fitting, interpretable components.
- Good for: business time series with strong seasonality/holidays and regime shifts, medium/long horizons.

---

## When to use Prophet (and when not)

> [!tip] Use when
> - Clear calendar effects (weekly/annual) and known holidays matter
> - Multiple seasonalities (daily/weekly/annual) and occasional changepoints
> - Need quick, interpretable baselines with sane defaults

> [!warning] Consider alternatives when
> - Very short series (few dozen points) or tiny samples
> - Complex dynamics (ARMA errors, rich autocorrelation) dominate over calendar effects
> - Multiple related series with shared structure (consider hierarchical/multivariate models)
> - High-frequency data with strong short-lag correlation (ARIMA/ETS/TBATS/State-space may fit better)

See also: [[Time Series (MOC)]], [[seasonality]].

---

## Model components

- Trend g(t)
  - Piecewise linear trend with automatically selected changepoints
  - Logistic/saturating growth with capacity cap (and optional floor)
  - Hyperparameters:
    - n_changepoints (default 25 within first 80% of history)
    - changepoint_range (fraction of history for changepoints, default 0.8)
    - changepoint_prior_scale (smoothness; larger → more flexible trend)

- Seasonality s(t)
  - Fourier series representation for periodic effects
  - Weekly, yearly built-in; can add custom seasonalities (e.g., monthly, hourly)
  - seasonality_mode: 'additive' (default) or 'multiplicative'
  - seasonality_prior_scale controls seasonality strength

- Holidays h(t)
  - Indicator regressors for specific dates, with optional window effects (± days)
  - Built-in country calendars via add_country_holidays
  - holidays_prior_scale controls shrinkage of holiday effects

- Extra regressors
  - User-supplied covariates (additive or multiplicative; continuous or binary)
  - Must be known in the future (no leakage); provide future values in the forecast frame

- Uncertainty
  - interval_width for prediction intervals (default 0.8)
  - mcmc_samples > 0 for full Bayesian uncertainty (slower)

---

## Core formulas (additive mode)

- Piecewise linear trend with changepoints τ_j:
$$
g(t) = \left(k + \sum_{j=1}^S \delta_j \mathbf{1}\{t\ge \tau_j\}\right)t + \left(m + \sum_{j=1}^S -\delta_j \tau_j \mathbf{1}\{t\ge \tau_j\}\right),
$$
with sparsity on δ via prior scale.

- Seasonality via Fourier terms (period P, order K):
$$
s_P(t) = \sum_{k=1}^{K}\left(a_k \cos\!\frac{2\pi k t}{P} + b_k \sin\!\frac{2\pi k t}{P}\right).
$$

- Logistic growth (with capacity cap and optional floor f):
$$
g(t) = \frac{C(t)}{1 + \exp\big(-k(t - m)\big)},\quad C(t)=\text{cap}(t).
$$

---

## Workflow and hyperparameters

> [!check] Typical steps
> - [ ] Clean timestamps; handle missing values; choose frequency; handle outliers
> - [ ] Decide trend (linear vs logistic with cap/floor)
> - [ ] Add built-in or custom holidays; set prior scales
> - [ ] Add extra regressors if known in future
> - [ ] Tune changepoint_prior_scale, seasonality_prior_scale via time-series CV
> - [ ] Validate with rolling-origin cross-validation and coverage diagnostics

> [!tip] Tuning
> - changepoint_prior_scale: 0.01 (smooth) → 0.5+ (wiggly)
> - seasonality_prior_scale: 1–10 typical
> - n_changepoints: increase with long histories; reduce for short series
> - seasonality_mode: multiplicative if seasonal amplitude grows with level

---

## Python code (prophet)

```python
# pip install prophet
from prophet import Prophet
import pandas as pd

# df must have columns: ds (datetime), y (numeric)
m = Prophet(
    growth='linear',               # or 'logistic'
    seasonality_mode='additive',   # or 'multiplicative'
    changepoint_prior_scale=0.1,
    seasonality_prior_scale=10.0,
    interval_width=0.95
)

# Holidays (built-in)
m.add_country_holidays(country_name='US')

# Custom seasonality (e.g., monthly ~ 30.5 days)
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)

# Extra regressor example (must be present in fit and future)
# df['promo'] = ...
m.add_regressor('promo')

m.fit(df)

# Create future dataframe
future = m.make_future_dataframe(periods=60, freq='D')  # 60 days ahead
# Add known future regressors/ caps if needed
# future['promo'] = ...
forecast = m.predict(future)

# Plot components
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
```

Logistic growth:

```python
df['cap'] = 100.0
df['floor'] = 0.0
m = Prophet(growth='logistic')
m.fit(df)
future = m.make_future_dataframe(periods=60, freq='D')
future['cap'] = 100.0
future['floor'] = 0.0
forecast = m.predict(future)
```

Cross-validation:

```python
from prophet.diagnostics import cross_validation, performance_metrics

df_cv = cross_validation(m, initial='365 days', period='30 days', horizon='90 days')
perf = performance_metrics(df_cv)
print(perf[['horizon','mae','rmse','mape','coverage']])
```

---

## R code (prophet)

```r
# install.packages("prophet")
library(prophet)

# df: columns ds (Date/POSIXct), y (numeric)
m <- prophet(growth = 'linear',
             seasonality.mode = 'additive',
             changepoint.prior.scale = 0.1,
             seasonality.prior.scale = 10)

# Holidays
m <- add_country_holidays(m, country_name = 'US')

# Custom seasonality
m <- add_seasonality(m, name='monthly', period=30.5, fourier.order=5)

# Extra regressor
# df$promo <- ...
m <- add_regressor(m, 'promo')

m <- fit.prophet(m, df)

future <- make_future_dataframe(m, periods = 60, freq = 'day')
# future$promo <- ...
forecast <- predict(m, future)

plot(m, forecast)
prophet_plot_components(m, forecast)
```

Cross-validation:

```r
library(prophet)
df.cv <- cross_validation(m, initial = 365, period = 30, horizon = 90, units = 'days')
perf  <- performance_metrics(df.cv)
perf[, c('horizon','mae','rmse','mape','coverage')]
```

---

## Diagnostics and evaluation

- Rolling-origin CV (initial, period, horizon) for realistic error estimates
- Metrics: MAE, RMSE, MAPE/SMAPE, [[MASE]]; interval coverage
- Component checks: trend reasonableness, seasonality shapes, holiday importance
- Residual autocorrelation: Prophet doesn’t model AR errors explicitly—consider adding regressors or switching to ARIMA/SSM if strong AR remains

---

## Handling practical issues

- Missing data: Prophet handles gaps; ensure correct frequency and no duplicated timestamps
- Outliers: model is robust, but consider capping/winsorizing extreme points
- Multi-seasonality: add multiple custom seasonalities (e.g., weekly + yearly + monthly + hourly)
- Event windows: use lower_window/upper_window around holidays; add customized event calendars
- Multiplicative effects: set seasonality_mode='multiplicative' if seasonal amplitude scales with level
- Known breaks: supply changepoints manually (m.changepoints = list of dates) or increase prior scale locally

---

## Comparisons

- vs ARIMA/ETS: Prophet emphasizes calendar/holidays and piecewise trend; ARIMA models serial correlation and can outperform when AR dynamics dominate
- vs TBATS: TBATS handles complex/multiple seasonalities well; Prophet simpler to use and interpret
- vs State-space (UCM/Kalman): SSMs more flexible (stochastic trend/seasonal), but require more setup

Often use Prophet as a baseline and compare via CV against ARIMA/ETS/SSM.

---

## Common pitfalls

> [!warning]
> - Overfitting trend with large changepoint_prior_scale; validate via CV  
> - Using extra regressors without known future values (leakage)  
> - Ignoring strong short-lag autocorrelation that Prophet won’t capture  
> - Multiplicative mode on zero/negative series without floor handling  
> - Not aligning time zones/holidays for global series

---

## Reporting essentials

- Data span/frequency; missing/outlier handling
- Model config: growth, changepoints (auto/manual), priors
- Seasonalities (built-in + custom), holidays used
- Extra regressors and their availability in the forecast horizon
- CV setup and performance metrics; forecast horizon and intervals
- Component plots and business interpretation; known risks/limitations

---

## Related notes

- [[Time Series (MOC)]]
- [[seasonality]] · X-13ARIMA-SEATS · [[TBATS]] · ARMA/ARIMA/SARIMA
- [[switchback experiment]] · [[geo experiment]] (holiday control, calendar effects)
- [[sequential testing]] (if forecasts gate decisions)

---