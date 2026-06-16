---
title: ARIMA
aliases: [ARIMA, ARMA, SARIMA, autoregressive integrated moving average, Box-Jenkins]
tags: [time-series, forecasting, econometrics]
updated: 2026-03-05
---

# ARIMA

> [!summary]
> Autoregressive Integrated Moving Average model: combines autoregressive (AR), differencing (I), and moving average (MA) components. SARIMA adds seasonal terms. The Box–Jenkins methodology provides a systematic identification-estimation-diagnostic cycle.

---

## Model notation: ARIMA(p, d, q)

ARIMA models a time series $Y_t$ as:
$$
\Phi(L)(1-L)^d Y_t = \Theta(L) \varepsilon_t,
$$
where:
- $p$: autoregressive order (number of lags of $Y_t$)
- $d$: degree of differencing (number of times to difference to achieve stationarity)
- $q$: moving average order (number of lags of error terms)
- $\Phi(L) = 1 - \phi_1 L - \phi_2 L^2 - \cdots - \phi_p L^p$ (AR polynomial)
- $\Theta(L) = 1 + \theta_1 L + \theta_2 L^2 + \cdots + \theta_q L^q$ (MA polynomial)
- $L$ is the lag operator: $L Y_t = Y_{t-1}$
- $\varepsilon_t \sim \text{WN}(0, \sigma^2)$ (white noise)

**After differencing** $d$ times, denote $W_t = (1-L)^d Y_t$. Then fit ARMA(p,q):
$$
W_t = \phi_1 W_{t-1} + \cdots + \phi_p W_{t-p} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}.
$$

**Special cases**:
- ARIMA(p,0,0) = AR(p): $Y_t = \phi_1 Y_{t-1} + \cdots + \phi_p Y_{t-p} + \varepsilon_t$
- ARIMA(0,0,q) = MA(q): $Y_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$
- ARIMA(0,1,0) = random walk: $Y_t = Y_{t-1} + \varepsilon_t$
- ARIMA(0,1,1) with drift: $\Delta Y_t = \mu + \theta_1 \varepsilon_{t-1} + \varepsilon_t$ (common for many economic series)

---

## Seasonal ARIMA: SARIMA(p,d,q)(P,D,Q)$_s$

For series with seasonal period $s$ (e.g., 12 for monthly data), add seasonal AR/MA terms:
$$
\Phi(L) \Phi_s(L^s) (1-L)^d (1-L^s)^D Y_t = \Theta(L) \Theta_s(L^s) \varepsilon_t,
$$
where:
- $(P, D, Q)$: seasonal AR, differencing, MA orders
- $\Phi_s(L^s) = 1 - \Phi_1 L^s - \Phi_2 L^{2s} - \cdots - \Phi_P L^{Ps}$
- $\Theta_s(L^s) = 1 + \Theta_1 L^s + \cdots + \Theta_Q L^{Qs}$

Example: SARIMA(1,1,1)(1,1,1)$_{12}$ for monthly sales data.

---

## Identification: selecting p, d, q

**Box–Jenkins approach**:

1. **Check stationarity**:
   - Plot series and ACF
   - Apply [[ADF test]] (Augmented Dickey-Fuller) or KPSS test
   - If non-stationary: difference until stationary (determine $d$)

2. **Examine ACF and PACF** of differenced series:
   - **AR(p)**: PACF cuts off after lag $p$; ACF decays exponentially
   - **MA(q)**: ACF cuts off after lag $q$; PACF decays exponentially
   - **ARMA(p,q)**: both ACF and PACF decay (harder to identify by eye)

3. **Fit candidate models** and compare via information criteria (AIC, BIC)

**Automated selection**: `auto.arima()` in R or `auto_arima()` in Python searches over $(p,d,q)$ grid using AIC/BIC.

> [!tip] Practical starting points
> - ARIMA(1,1,1): simple and often adequate
> - ARIMA(0,1,1) with drift: exponential smoothing equivalent
> - Seasonal: start with SARIMA(1,1,1)(1,1,1)$_s$

---

## Estimation

**Maximum Likelihood Estimation (MLE)**:
- Assumes $\varepsilon_t \sim N(0,\sigma^2)$
- Optimize log-likelihood via Kalman filter or state-space methods
- Standard approach in `stats::arima()` (R), `statsmodels.tsa.arima.ARIMA` (Python)

**Conditional Sum of Squares (CSS)**:
- Minimize $\sum_{t=p+1}^{T} \hat\varepsilon_t^2$ conditional on initial values
- Faster but less efficient than MLE
- Used for initialization in some software

**Estimation output**:
- Coefficients $\hat\phi_1, \ldots, \hat\phi_p, \hat\theta_1, \ldots, \hat\theta_q$
- Standard errors (from information matrix)
- $\hat\sigma^2$ (residual variance)
- Log-likelihood, AIC, BIC

---

## Diagnostics

> [!check] Post-estimation checks
> - [ ] **Residual ACF/PACF**: should resemble white noise (no significant spikes)
> - [ ] **Ljung-Box test**: H0 = residuals are white noise; want p > 0.05
> - [ ] **Normality**: QQ-plot, Shapiro-Wilk (less critical for forecasting than for inference)
> - [ ] **ARCH effects**: if residuals show volatility clustering, consider GARCH
> - [ ] **Overfitting**: if many MA terms have large SEs, reduce $q$

**Model selection**:
- **AIC**: $-2 \log L + 2k$ (penalizes complexity; use for forecasting)
- **BIC**: $-2 \log L + k \log T$ (stronger penalty; use for parsimony)
- Lower AIC/BIC is better
- Out-of-sample forecast accuracy (RMSE, MAE) is ultimate test

---

## Forecasting

ARIMA produces optimal linear forecasts under MSFE criterion.

**h-step ahead forecast** $\hat Y_{T+h|T}$:
- Use recursion: plug in forecasts for future values
- Forecast SE grows with horizon $h$
- Prediction intervals: $\hat Y_{T+h|T} \pm z_{\alpha/2} \cdot \mathrm{se}(\hat Y_{T+h|T})$

**Example (ARIMA(1,1,1))**:
$$
\Delta Y_{T+1} = \hat\phi_1 \Delta Y_T + \hat\theta_1 \hat\varepsilon_T + \varepsilon_{T+1}.
$$
Then $\hat Y_{T+1|T} = Y_T + \hat\phi_1 \Delta Y_T + \hat\theta_1 \hat\varepsilon_T$.

**Forecast evaluation**:
- Rolling-origin cross-validation
- RMSE, MAE, MAPE on test set
- Compare with benchmark (naive, seasonal naive, exponential smoothing)

---

## Code snippets

> [!example] R: auto.arima

```r
library(forecast)

# Automatic model selection
fit <- auto.arima(y, seasonal = TRUE, stepwise = FALSE, approximation = FALSE)
summary(fit)

# Diagnostics
checkresiduals(fit)  # ACF + Ljung-Box + histogram

# Forecast 12 steps ahead
fc <- forecast(fit, h = 12)
plot(fc)
fc$mean  # point forecasts
fc$lower; fc$upper  # prediction intervals
```

> [!example] R: manual ARIMA specification

```r
library(forecast)

# ARIMA(1,1,1)
fit <- Arima(y, order = c(1, 1, 1))
summary(fit)

# SARIMA(1,1,1)(1,1,1)[12]
fit_seasonal <- Arima(y, order = c(1, 1, 1), seasonal = c(1, 1, 1))
summary(fit_seasonal)

# Ljung-Box test on residuals
Box.test(residuals(fit), lag = 20, type = "Ljung-Box")
```

> [!example] Python: statsmodels ARIMA

```python
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm

# Fit ARIMA(1,1,1)
model = ARIMA(y, order=(1, 1, 1))
fit = model.fit()
print(fit.summary())

# Diagnostics
fit.plot_diagnostics(figsize=(12, 8))

# Forecast 12 steps
forecast = fit.forecast(steps=12)
forecast_df = fit.get_forecast(steps=12).summary_frame()
print(forecast_df)  # includes confidence intervals
```

> [!example] Python: auto_arima (pmdarima)

```python
from pmdarima import auto_arima

# Automatic model selection
model = auto_arima(y, seasonal=True, m=12, stepwise=False,
                   suppress_warnings=True, error_action='ignore')
print(model.summary())

# Forecast
forecast, conf_int = model.predict(n_periods=12, return_conf_int=True)
```

> [!example] Stata: arima

```stata
* ARIMA(1,1,1)
arima y, arima(1,1,1)

* SARIMA(1,1,1)(1,1,1)12
arima y, arima(1,1,1) sarima(1,1,1,12)

* Forecast 12 periods
predict yhat, dynamic(tm(2024m1))

* Diagnostics
predict resid, residuals
ac resid
pac resid
wntestq resid  // Ljung-Box
```

---

## Relation to other models

- **Exponential smoothing (ETS)**: ARIMA(0,1,1) with drift ≡ simple exponential smoothing; ARIMA(0,1,1) + trend ≡ Holt's method. See [[ETS]]
- **Structural time series**: state-space formulation generalizes ARIMA; see [[TBATS]]
- **Prophet**: additive model with trend + seasonality + holidays; more flexible but less interpretable than ARIMA. See [[Prophet]]
- **GARCH**: models conditional heteroskedasticity; combine with ARIMA for volatility forecasting
- **VAR**: multivariate analog; see [[VAR]]

---

## Practical guidance

> [!tip] When to use ARIMA
> - Univariate time series with trend and/or seasonality
> - Stationary after differencing
> - Linear autocorrelation structure
> - Medium-term forecasting (not very long horizons)

> [!warning] Limitations
> - Assumes linear relationships; poor for highly nonlinear series
> - Sensitive to outliers and structural breaks
> - Differencing removes level information (reversible for forecasting)
> - Long-run forecasts revert to mean (flat with constant variance)
> - Does not incorporate covariates (use ARIMAX or dynamic regression)

> [!check] Best practices
> - Always plot the series and check stationarity before fitting
> - Use AIC/BIC for model selection; validate on holdout sample
> - Check residual diagnostics (ACF, Ljung-Box) to ensure adequate fit
> - Report model order $(p,d,q)$ and seasonal structure if applicable
> - Compare with simple benchmarks (seasonal naive, ETS)
> - For inference (not just forecasting), ensure residuals are well-behaved

---

## Related notes

- [[ETS]]
- [[TBATS]]
- [[Prophet]]
- [[ADF test]]
- [[Time Series (MOC)]]
- [[VAR]]
- [[Local projections (Jordà)]]
- [[Newey–West]]

---

## References

- Box, Jenkins, Reinsel, & Ljung, *Time Series Analysis: Forecasting and Control* (5th ed.)
- Hyndman & Athanasopoulos, *Forecasting: Principles and Practice* (fpp3.com)
- Brockwell & Davis, *Introduction to Time Series and Forecasting*
