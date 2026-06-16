---
title: Time Series (MOC)
aliases: [Time Series, time series, Time-series hub, Forecasting (MOC)]
tags: [moc, time-series, forecasting, econometrics, modeling, diagnostics]
updated: 2025-09-17
---

# Time Series (MOC)

> [!summary] Scope
> Univariate and multivariate time-series analysis: modeling, forecasting, inference, diagnostics, structural breaks, volatility, seasonal adjustment, and evaluation.

---

## Quick start

> [!tip] One-page workflow
> 1) Explore and transform: visualize levels/changes; handle [[seasonality]], outliers, missingness; consider log/Box–Cox/differencing
> 2) Test/stationarity: unit roots ([[ADF test]] · [[PP test]] · [[KPSS test]]); decide ARIMA vs. trend/ECM
> 3) Pick model: [[ARIMA|ARMA/ARIMA/SARIMA]] · [[ETS]] · [[Prophet]] · [[Kalman filter|State-space/Kalman filter]] · [[TBATS]]; for multivariate: [[VAR|VAR/SVAR]] · [[VECM]]
> 4) Include exogenous effects if needed: ARIMAX/transfer function/[[ARDL]]/MIDAS
> 5) Cross-validate: rolling-origin; tune horizons and hyperparameters
> 6) Diagnose: residual whiteness, Ljung–Box, ARCH tests; stability/breaks ([[Bai–Perron]])
> 7) Forecast and evaluate: holdouts; [[Diebold–Mariano test]]; MAE/RMSE/[[MASE]]; combine forecasts
> 8) Document: transformations, calendar effects, evaluation protocol, and uncertainty intervals

---

## Core tasks

- Data preparation
  - Calendar effects: trading-days, holidays, moving holidays (Easter, Lunar New Year); [[seasonality]]; DST/time zones
  - Transformations: log, Box–Cox, demeaning/detrending, differencing; missing-data imputation (Kalman smoothing)
  - Outliers/anomalies: additive, level shifts, ramps; robust methods or explicit intervention dummies
- Stationarity and integration
  - Unit-root tests: [[ADF test]] · [[PP test]] · [[KPSS test]]; future notes: DF-GLS and break-robust tests such as Zivot-Andrews
  - Differencing and [[seasonal differencing]]; future note: fractional differencing

---

## Univariate models

- Classical families
  - [[ARIMA|ARMA/ARIMA/SARIMA]]: Box–Jenkins; seasonal components; identification via ACF/PACF; information criteria
  - [[ETS]] (Error–Trend–Seasonal): exponential smoothing with trend/seasonal states; automatic selection
  - [[TBATS]]: multiple/long seasonality, Box–Cox, ARMA errors
  - [[Prophet]]: additive trend/seasonality/holidays; robust defaults
  - [[Kalman filter|State-space/Kalman filter]]: local level/trend/seasonal; unobserved components (UCM)
- Exogenous regressors
  - ARIMAX / dynamic regression / transfer-function models
  - Distributed lags: [[ARDL]] (bounds testing), ADL with ECM representation

---

## Multivariate models

- VAR/VECM/SVAR
  - [[VAR|VAR/SVAR]]: lag selection, stability, Granger causality; identification via Cholesky, long-run, or sign restrictions
  - [[VECM]] and cointegration: [[Engle–Granger]] · [[Johansen]] · [[ARDL]] bounds; error-correction forms and impulse responses
- Structural analysis
  - IRFs, FEVDs; GIRFs; identification strategies (short-run/long-run/sign/IV-Proxy)
  - [[Local projections (Jordà)]] for IRFs with robust SEs and flexible controls
- Mixed-frequency and nowcasting
  - MIDAS (Almon/U-MIDAS), dynamic factor models (DFM), state-space nowcasting

---

## Volatility and high frequency

- ARCH/GARCH family
  - [[GARCH|ARCH/GARCH]] · EGARCH · GJR-GARCH; fat tails (t-innovations); long memory (FIGARCH)
  - Multivariate: DCC-GARCH, BEKK
- Realized measures
  - Realized volatility; HAR-RV; microstructure noise considerations
- Risk measures
  - VaR/ES backtesting; Kupiec/Christoffersen tests

---

## Seasonality and decomposition

- Seasonal adjustment
  - STL decomposition; X-13ARIMA-SEATS; TRAMO-SEATS
- Multiple/complex seasonality
  - [[TBATS]]; Fourier terms; temporal hierarchies

---

## Structural breaks and regimes

- Break detection
  - [[Bai–Perron]] multiple structural breaks; Quandt-Andrews/Chow tests
- Regime switching
  - [[Markov switching]] and threshold models (TAR/SETAR)

---

## Frequency- and trend-based methods

- Filters and spectra
  - HP filter (with caveats) · [[Baxter–King filter]] · [[Christiano–Fitzgerald filter]]
  - Spectral analysis: periodogram, spectral density, coherence

---

## Forecasting

- Evaluation and selection
  - Metrics: MAE, RMSE, sMAPE, [[MASE]]; Mincer–Zarnowitz regression; [[Diebold–Mariano test]]
  - Cross-validation: rolling/expanding origin; blocked CV; nested evaluation for hyperparameters
- Forecast combinations and hierarchies
  - Simple averages to weighted/stacking; reconciliation such as MinT for aggregation constraints
  - Temporal hierarchies and hierarchical/grouped time-series
- Intermittent demand
  - Croston/SBA/TSB methods

---

## Inference and robust SEs

- HAC and dependence
  - [[Newey–West]] · Andrews automatic bandwidth; prewhitening
  - Long-run variance; [[Driscoll–Kraay]] (panel cross-sectional dependence)
- Model diagnostics
  - Residual whiteness (Ljung–Box), normality, ARCH effects (Engle test), stability tests (CUSUM/SUP-F), leverage/outliers

---

## Panel time series

- Cross-sectional/time dependence
  - [[Driscoll–Kraay]] · Pesaran CD test; CCE/Pesaran
- Dynamic panels
  - [[Arellano–Bond]] · [[System GMM]]
- Panel VAR/ECM
  - Panel VAR, pooled mean group/mean group

---

## ML for time series

- Feature-based regressors
  - Lags, rolling statistics, Fourier terms; tree ensembles (RF/GBM), linear penalized ([[regularization|Lasso/ridge/elastic net]])
- Sequence models
  - RNN/LSTM/GRU; temporal CNNs; transformers
- Cross-validation and leakage
  - Time-aware train/validate splits; forecast-origin backtests; leakage avoidance (no peeking into future)

---

## Data issues and best practices

- Missing data: Kalman smoothing and imputation; careful with multi-seasonal gaps
- Real-time data/revisions: pseudo-out-of-sample with vintages
- Time zones/DST: align timestamps; business calendars
- Reproducibility: code notebooks, seeds, environment, versioned data

---

## Checklists

> [!check] Modeling checklist
> - [ ] Visualize series (levels/diffs), ACF/PACF, seasonal subseries
> - [ ] Choose transformations (log/Box–Cox), differencing orders (incl. seasonal)
> - [ ] Unit-root tests and break diagnostics
> - [ ] Candidate models (ARIMA/ETS/SSM) vs. multivariate (VAR/VECM)
> - [ ] Include exogenous regressors/holidays if needed
> - [ ] Backtest via rolling-origin; compare with baseline benchmarks (Naive/Seasonal Naive)
> - [ ] Diagnose residuals; stability and ARCH tests
> - [ ] Report intervals, evaluation metrics, and forecast combinations

> [!check] Multivariate/structural checklist
> - [ ] Cointegration tests and rank selection
> - [ ] Identification strategy (Cholesky/long-run/sign/IV) documented
> - [ ] IRFs/FEVDs with CIs (bootstrap or asymptotic)
> - [ ] Robustness: ordering sensitivity, sign-restriction priors, alternative lags
> - [ ] Local projections as robustness to VAR misspecification

---

## Reporting essentials

- Data frequency, span, transformations, seasonal/holiday handling
- Stationarity and differencing decisions; cointegration evidence if multivariate
- Model specification and selection (IC/CV); exogenous regressors and interventions
- Diagnostics and stability/break tests; residual checks
- Forecast protocol (origin, horizon, metrics, confidence intervals)
- Reproducibility (software, versions, seeds, code/data availability)

---

## Reading list

- Forecasting: Hyndman & Athanasopoulos, Box–Jenkins, Durbin & Koopman (state space)
- Multivariate: Lütkepohl (VAR/VECM), Hamilton (time series)
- Volatility: Engle & Bollerslev (ARCH/GARCH)
- Breaks/regimes: Bai & Perron; Hamilton (Markov switching)

---

## Index of topics (A–Z)

- [[ADF test]] · [[ARDL]] · [[Arellano–Bond]] · [[GARCH|ARCH/GARCH]] · [[ARIMA|ARMA/ARIMA/SARIMA]] · [[Bai–Perron]] · [[Baxter–King filter]]
- Box-Cox · [[Christiano–Fitzgerald filter]] · [[cointegration]] · CUSUM
- [[Diebold–Mariano test]] · [[Driscoll–Kraay]] · [[Engle–Granger]] · [[ETS]] · [[Granger causality]]
- [[HP filter]] · [[Johansen]] · [[Kalman filter|Kalman filter/state-space]] · [[KPSS test]] · [[Local projections (Jordà)]]
- MAE · [[MASE]] · MIDAS · MinT · [[Newey–West]]
- periodogram · [[Prophet]] · [[PP test]] · [[RESET test]]
- [[seasonality]] · spectral density · [[Kalman filter|State-space/Kalman filter]] · [[TBATS]] · Temporal hierarchies
- [[VAR|VAR/SVAR]] · [[VECM]] · X-13ARIMA-SEATS

---

## Related hubs

- [[Econometrics (MOC)]]
- [[Causal Inference (MOC)]]
- [[ML for Econometrics (MOC)]]
