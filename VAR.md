---
title: VAR
aliases: [VAR, vector autoregression, SVAR, structural VAR]
tags: [econometrics, time-series, multivariate]
updated: 2026-03-05
---

# VAR

> [!summary]
> Vector Autoregression: system of equations where each variable is regressed on its own lags and lags of all other variables. Structural VAR (SVAR) imposes identification restrictions to recover causal impulse responses.

---

## Model form

A VAR(p) model for $K$-dimensional time series $\mathbf{Y}_t = (Y_{1t}, \ldots, Y_{Kt})'$:
$$
\mathbf{Y}_t = \mathbf{c} + \mathbf{A}_1 \mathbf{Y}_{t-1} + \mathbf{A}_2 \mathbf{Y}_{t-2} + \cdots + \mathbf{A}_p \mathbf{Y}_{t-p} + \mathbf{u}_t,
$$
where:
- $\mathbf{c}$ is a $K \times 1$ vector of constants
- $\mathbf{A}_i$ are $K \times K$ coefficient matrices for lag $i$
- $\mathbf{u}_t$ is a $K \times 1$ vector of innovations with $\mathbb{E}[\mathbf{u}_t]=0$, $\mathrm{Cov}(\mathbf{u}_t) = \Sigma_u$
- Assumes stationarity: eigenvalues of companion matrix lie inside unit circle

**Compact form**:
$$
\mathbf{Y}_t = \mathbf{B} \mathbf{Z}_{t-1} + \mathbf{u}_t,
$$
where $\mathbf{Z}_{t-1} = (1, \mathbf{Y}_{t-1}', \mathbf{Y}_{t-2}', \ldots, \mathbf{Y}_{t-p}')'$ and $\mathbf{B} = [\mathbf{c}, \mathbf{A}_1, \ldots, \mathbf{A}_p]$.

**Example (VAR(1) with 2 variables)**:
$$
\begin{pmatrix} Y_{1t} \\ Y_{2t} \end{pmatrix} = \begin{pmatrix} c_1 \\ c_2 \end{pmatrix} + \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix} \begin{pmatrix} Y_{1,t-1} \\ Y_{2,t-1} \end{pmatrix} + \begin{pmatrix} u_{1t} \\ u_{2t} \end{pmatrix}.
$$

---

## Estimation

**Equation-by-equation OLS**:
- Each equation can be estimated by [[Ordinary Least Squares (OLS)|OLS]] independently
- All equations have the same regressors $(1, \mathbf{Y}_{t-1}', \ldots, \mathbf{Y}_{t-p}')$
- OLS is efficient (equivalent to GLS) under standard VAR assumptions
- Consistent estimates of $\mathbf{B}$ and $\Sigma_u$

**Estimation steps**:
1. Choose lag order $p$ (see below)
2. Estimate each equation by OLS
3. Collect residuals $\hat{\mathbf{u}}_t$ and estimate $\hat\Sigma_u = \frac{1}{T} \sum_{t} \hat{\mathbf{u}}_t \hat{\mathbf{u}}_t'$

**Standard errors**: Use [[Newey–West]] HAC if concerned about residual autocorrelation (rare if $p$ is adequate).

---

## Lag selection

Choose $p$ to balance fit and parsimony.

**Information criteria** (lower is better):
- **AIC**: $\log |\hat\Sigma_u| + \frac{2 K^2 p}{T}$
- **BIC**: $\log |\hat\Sigma_u| + \frac{K^2 p \log T}{T}$
- **HQ**: $\log |\hat\Sigma_u| + \frac{2 K^2 p \log \log T}{T}$

BIC penalizes complexity more heavily; often selects smaller $p$.

**Sequential testing**:
- Start with $p_{\max}$ (e.g., 12 for monthly data)
- Test down using likelihood ratio test: $\text{LR} = T(\log|\hat\Sigma_u(p)| - \log|\hat\Sigma_u(p+1)|) \sim \chi^2_{K^2}$

> [!tip] Practical advice
> - Use AIC/BIC for automatic selection
> - Check residual autocorrelation: if ACF shows spikes, increase $p$
> - For monthly/quarterly data, start with $p \in \{1, \ldots, 4\}$

---

## Granger causality tests

**Definition**: $Y_2$ Granger-causes $Y_1$ if lags of $Y_2$ improve prediction of $Y_1$ beyond lags of $Y_1$ alone.

**Test**: In equation for $Y_{1t}$, test $H_0: a_{12,1} = \cdots = a_{12,p} = 0$ (F-test or Wald test).

**Interpretation**:
- Rejection ⇒ $Y_2$ helps forecast $Y_1$ (not necessarily causal in structural sense)
- Bidirectional Granger causality (feedback) is common

See [[Granger causality]] for details.

---

## Impulse Response Functions (IRFs)

**IRF**: traces effect of a one-unit shock to innovation $u_{jt}$ on $Y_{kt}$ over time.

**Reduced-form VAR** shocks $\mathbf{u}_t$ are correlated (non-zero $\Sigma_u$). To isolate causal shocks, impose identification:

**Cholesky decomposition** (recursive identification):
- Order variables $(Y_1, \ldots, Y_K)$
- Cholesky factor $\Sigma_u = PP'$ gives orthogonal shocks $\mathbf{\varepsilon}_t = P^{-1} \mathbf{u}_t$
- $\varepsilon_{1t}$ affects all variables contemporaneously; $\varepsilon_{Kt}$ only affects $Y_K$ contemporaneously
- IRF depends on ordering (sensitivity check: reorder variables)

**Structural VAR (SVAR)**: impose economic restrictions (e.g., monetary policy shock does not affect output contemporaneously) to identify structural shocks.

**Cumulative IRF**: sum of IRF over horizons (e.g., total effect of shock on level of $Y$).

---

## Forecast Error Variance Decomposition (FEVD)

**FEVD**: decomposes h-step-ahead forecast error variance of $Y_{kt}$ into contributions from each shock $\varepsilon_j$.

Answers: "What fraction of variation in $Y_k$ is due to shocks to $Y_j$?"

Depends on identification (Cholesky or SVAR). Sum across shocks = 100% at each horizon.

---

## Stationarity and cointegration

- VAR assumes stationarity: if series are non-stationary (unit roots), spurious regressions may occur
- Test stationarity with [[ADF test]] for each series
- If series are I(1) but cointegrated, use [[VECM]] (Vector Error Correction Model) instead
- VECM = VAR in differences + error correction term capturing long-run equilibrium

---

## Code snippets

> [!example] R: VAR estimation with vars package

```r
library(vars)

# Prepare matrix/data.frame with K columns (one per variable)
data <- cbind(Y1, Y2, Y3)

# Lag selection
VARselect(data, lag.max = 8, type = "const")  # reports AIC/BIC/HQ

# Estimate VAR(2)
var_fit <- VAR(data, p = 2, type = "const")
summary(var_fit)

# Residual diagnostics
serial.test(var_fit, lags.pt = 10, type = "PT.asymptotic")  # Portmanteau test
normality.test(var_fit)
arch.test(var_fit)

# Granger causality: does Y2 Granger-cause Y1?
causality(var_fit, cause = "Y2")
```

> [!example] R: Impulse responses and FEVD

```r
# Compute IRFs (Cholesky identification, 10 periods)
irf_result <- irf(var_fit, impulse = "Y1", response = "Y2", n.ahead = 10,
                  ortho = TRUE, boot = TRUE, ci = 0.95)
plot(irf_result)

# Forecast error variance decomposition
fevd_result <- fevd(var_fit, n.ahead = 10)
plot(fevd_result)
```

> [!example] Python: statsmodels VAR

```python
from statsmodels.tsa.api import VAR
import pandas as pd

# Data: DataFrame with K columns
model = VAR(data)

# Lag selection
lag_order = model.select_order(maxlags=8)
print(lag_order.summary())

# Fit VAR(2)
results = model.fit(maxlags=2)
print(results.summary())

# Granger causality tests
granger = results.test_causality('Y1', 'Y2', kind='f')
print(granger.summary())

# IRFs (orthogonalized)
irf = results.irf(periods=10)
irf.plot(impulse='Y1', response='Y2')

# FEVD
fevd = results.fevd(periods=10)
fevd.plot()
```

> [!example] Stata: var and irf

```stata
* Estimate VAR(2)
var Y1 Y2 Y3, lags(1/2)

* Lag selection
varsoc Y1 Y2 Y3, maxlag(8)

* Granger causality: does Y2 Granger-cause Y1?
vargranger

* Create IRF results (Cholesky)
irf create var_irf, step(10) set(myirf) replace

* Plot IRF: shock to Y1, response of Y2
irf graph oirf, impulse(Y1) response(Y2)

* FEVD
irf table fevd, impulse(Y1) response(Y2)
```

---

## Identification in SVAR

**Problem**: Reduced-form VAR innovations $\mathbf{u}_t$ are linear combinations of structural shocks $\mathbf{\varepsilon}_t$:
$$
\mathbf{u}_t = \mathbf{A}_0^{-1} \mathbf{\varepsilon}_t,
$$
where $\mathbf{\varepsilon}_t$ are uncorrelated structural shocks with $\mathrm{Cov}(\mathbf{\varepsilon}_t) = I$.

**Identification strategies**:
1. **Cholesky (recursive)**: $\mathbf{A}_0$ is lower triangular (imposes causal ordering)
2. **Short-run restrictions**: zero restrictions on $\mathbf{A}_0$ (e.g., monetary policy does not affect output contemporaneously)
3. **Long-run restrictions**: some shocks have no long-run effect on certain variables (e.g., demand shocks do not affect output in long run)
4. **Sign restrictions**: IRFs must satisfy sign constraints (e.g., monetary tightening reduces output)
5. **External instruments**: use external shock series (narrative approach, high-frequency identification)

SVAR is crucial for causal interpretation; without identification, IRFs have limited structural meaning.

---

## Forecasting

**h-step ahead forecast**:
$$
\hat{\mathbf{Y}}_{T+h|T} = \mathbb{E}[\mathbf{Y}_{T+h} \mid \mathbf{Y}_T, \mathbf{Y}_{T-1}, \ldots],
$$
computed via recursive substitution.

**Forecast intervals**: bootstrap or analytic (using estimated $\Sigma_u$ and parameter uncertainty).

**Alternative: [[Local projections (Jordà)]]**: estimates IRFs directly via horizon-specific regressions; more robust to misspecification but less efficient.

---

## Practical guidance

> [!tip] When to use VAR
> - Modeling interdependencies among multiple stationary time series
> - Forecasting several related variables jointly
> - Estimating dynamic effects (IRFs, FEVD)
> - Granger causality testing

> [!warning] Limitations
> - Requires stationarity (or use [[VECM]] for cointegrated I(1) series)
> - Large parameter space: $K^2 p$ coefficients per equation; overfitting risk if $T$ is small
> - IRFs sensitive to identification (ordering in Cholesky; SVAR restrictions)
> - Difficult to incorporate exogenous variables (VARX exists but less common)
> - Not suitable for long-run forecasts (uncertainty grows rapidly)

> [!check] Best practices
> - Test stationarity for each series ([[ADF test]]); difference if needed (or use [[VECM]])
> - Use AIC/BIC for lag selection; verify residuals are white noise
> - For IRFs, report identification scheme (Cholesky ordering or SVAR restrictions)
> - Check robustness: alternative orderings, bootstrap confidence bands
> - Compare forecasts with univariate models (ARIMA) to assess gains from multivariate modeling

---

## Related notes

- [[VECM]]
- [[Granger causality]]
- [[Time Series (MOC)]]
- [[Local projections (Jordà)]]
- [[ARIMA]]
- [[ADF test]]
- [[Newey–West]]
- [[Ordinary Least Squares (OLS)|OLS]]

---

## References

- Lütkepohl, *New Introduction to Multiple Time Series Analysis*
- Hamilton, *Time Series Analysis* (Ch. 11: VAR models)
- Stock & Watson, "Vector Autoregressions," *Journal of Economic Perspectives* (2001)
- Kilian & Lütkepohl, *Structural Vector Autoregressive Analysis*
