---
title: Newey–West
aliases: [Newey-West, Newey–West standard errors, Newey-West standard errors, HAC standard errors, NW standard errors]
tags: [econometrics, inference, time-series, standard-errors]
updated: 2026-03-05
---

# Newey–West

> [!summary]
> Heteroskedasticity- and autocorrelation-consistent (HAC) covariance estimator. Uses a kernel-weighted sum of autocovariance matrices (typically Bartlett) with a bandwidth parameter to produce SEs robust to both heteroskedasticity and serial correlation.

---

## Model and motivation

In time-series regression:
$$
Y_t = X_t' \beta + u_t,\quad t = 1,\ldots,T,
$$
OLS $\hat\beta = (X'X)^{-1}X'Y$ is consistent under $\mathbb{E}[u_t \mid X]=0$, but standard errors are invalid when:
- Heteroskedasticity: $\mathrm{Var}(u_t \mid X) = \sigma_t^2$ varies over time
- Serial correlation (autocorrelation): $\mathrm{Cov}(u_t, u_s \mid X) \neq 0$ for $t \neq s$

Newey–West (1987) provides consistent covariance estimation under both violations, allowing valid inference without modeling the correlation structure.

---

## HAC covariance estimator

The asymptotic covariance of $\hat\beta$ is:
$$
\mathrm{Var}(\hat\beta) = (X'X)^{-1} \Omega (X'X)^{-1},
$$
where $\Omega$ is the long-run variance matrix of the score:
$$
\Omega = \sum_{j=-\infty}^{\infty} \mathbb{E}[X_t u_t u_{t-j} X_{t-j}'].
$$

Newey–West estimator uses kernel weighting with bandwidth $L$:
$$
\hat\Omega_{NW} = \hat\Gamma_0 + \sum_{j=1}^{L} w_j \left( \hat\Gamma_j + \hat\Gamma_j' \right),
$$
where:
- $\hat\Gamma_j = \frac{1}{T} \sum_{t=j+1}^{T} X_t e_t e_{t-j} X_{t-j}'$ (sample autocovariances)
- $e_t = Y_t - X_t'\hat\beta$ (OLS residuals)
- $w_j = 1 - \frac{j}{L+1}$ (Bartlett kernel weights; default)

The Bartlett kernel ensures $\hat\Omega_{NW}$ is positive semi-definite. Alternative kernels (Parzen, quadratic spectral) are also used.

Standard errors:
$$
\mathrm{se}(\hat\beta_k) = \sqrt{\left[ (X'X)^{-1} \hat\Omega_{NW} (X'X)^{-1} \right]_{kk}}.
$$

---

## Bandwidth selection

The bandwidth $L$ (lag truncation) governs bias-variance tradeoff:
- Too small $L$: underestimates serial correlation → SEs too small
- Too large $L$: noisy autocovariance estimates → SEs too large

Common choices:

1. **Newey–West plug-in rule** (default in most software):
$$
L = \lfloor 4(T/100)^{2/9} \rfloor.
$$
Motivated by rate-optimal MSE for AR(1) errors.

2. **Andrews (1991) data-dependent bandwidth**:
- Estimate AR(1) coefficient $\hat\rho$
- $L = \lfloor 1.3 (\hat\alpha}(2) T)^{1/3} \rfloor$, where $\hat\alpha}(2)$ depends on $\hat\rho$
- More adaptive but sensitive to misspecification

3. **Fixed rule-of-thumb**: $L = \lfloor T^{1/4} \rfloor$

> [!tip] Practical advice
> - Start with default Newey–West bandwidth
> - Report results for $L-2, L, L+2$ to check sensitivity
> - Larger $L$ is conservative (wider CIs) when uncertain

---

## When to use Newey–West vs other robust SEs

| Data structure | Recommended SE |
|----------------|----------------|
| i.i.d. with heteroskedasticity | HC/White robust (HC1, HC2, HC3) |
| Time series with serial correlation | Newey–West HAC |
| Panel with clustering by entity | [[clustered standard errors]] |
| Panel with cross-section + time dependence | [[Driscoll–Kraay]] (HAC + clustering) |
| Spatial correlation | [[Conley standard errors]] |

> [!warning] When NOT to use Newey–West
> - Cross-sectional data with clustering (use [[clustered standard errors]] instead)
> - Panel data with clustering by entity/group (NW treats observations as ordered time series)
> - Short time series (T < 30): HAC estimators have poor small-sample properties; consider parametric modeling (GLS with AR errors)

---

## Prewhitening and small-sample corrections

**Prewhitening**: Fit AR(1) to residuals, apply NW to prewhitened errors, adjust covariance. Can improve finite-sample performance but adds model assumptions.

**Small-sample adjustment**: Multiply $\hat\Omega_{NW}$ by $\frac{T}{T-k}$ (analogous to HC1). Not always applied; check software defaults.

---

## Code snippets

> [!example] R: Newey–West with sandwich

```r
library(lmtest)
library(sandwich)

# OLS fit
fit <- lm(Y ~ X1 + X2, data = ts_data)

# Newey–West HAC SEs (default bandwidth)
coeftest(fit, vcov = NeweyWest(fit))

# Custom bandwidth L=4
coeftest(fit, vcov = NeweyWest(fit, lag = 4))

# With prewhitening and adjustment
coeftest(fit, vcov = NeweyWest(fit, lag = 4, prewhite = TRUE, adjust = TRUE))

# Extract covariance matrix
vcov_nw <- NeweyWest(fit, lag = 4)
```

> [!example] Python: statsmodels HAC

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# OLS fit
res = smf.ols('Y ~ X1 + X2', data=ts_data).fit()

# Newey–West HAC (maxlags = bandwidth L)
res_hac = smf.ols('Y ~ X1 + X2', data=ts_data).fit(
    cov_type='HAC',
    cov_kwds={'maxlags': 4}
)
print(res_hac.summary())

# Use default bandwidth (automatic)
res_hac_auto = smf.ols('Y ~ X1 + X2', data=ts_data).fit(cov_type='HAC')

# Access covariance matrix
cov_nw = res_hac.cov_params()
```

> [!example] Stata: newey command

```stata
* Newey–West with lag(L)
newey Y X1 X2, lag(4)

* Automatic bandwidth selection
newey Y X1 X2, lag(auto)

* Store results
estimates store nw_model

* Test joint hypothesis
test X1 = X2
```

> [!example] R: Sensitivity to bandwidth choice

```r
library(lmtest)
library(sandwich)

fit <- lm(Y ~ X1 + X2, data = ts_data)

# Compare bandwidths
for (L in c(2, 4, 6, 8)) {
  cat(sprintf("Bandwidth L = %d:\n", L))
  print(coeftest(fit, vcov = NeweyWest(fit, lag = L)))
}
```

---

## Diagnostics and checks

> [!check] Pre-estimation
> - [ ] Check for serial correlation: ACF/PACF of residuals, Ljung-Box test
> - [ ] If no serial correlation detected, HC robust SEs may suffice

> [!check] Post-estimation
> - [ ] Report bandwidth $L$ used
> - [ ] Sensitivity: rerun with $L \pm 2$ to verify inference robustness
> - [ ] Compare with model-based SEs to gauge adjustment magnitude

---

## Relation to other methods

- **White/HC robust SEs**: Special case with $L=0$ (no serial correlation)
- [[Driscoll–Kraay]]: Extends NW to panel data (HAC + clustering by time)
- [[Conley standard errors]]: Spatial HAC (distance-based kernel instead of time lag)
- **Clustered SEs**: For grouped/hierarchical data; NW is for ordered time series
- **Parametric GLS**: Model AR(1) or AR(p) errors explicitly; more efficient if correct but misspecification risk

---

## Practical guidance

> [!tip] When to use
> - Time-series regression with potential serial correlation (macro data, daily/weekly returns)
> - You want robust inference without specifying correlation structure
> - T is reasonably large (T > 30)

> [!warning] Limitations
> - Poor small-sample performance (T < 30): CIs may undercover
> - Assumes stationarity and weak dependence
- Does not account for structural breaks or regime changes
> - Panel data: use [[clustered standard errors]] or [[Driscoll–Kraay]], not NW

> [!check] Reporting
> - Specify kernel (Bartlett is standard) and bandwidth $L$
> - Report rule used (plug-in, Andrews, fixed)
> - Show sensitivity to bandwidth choice if borderline inference

---

## Related notes

- [[Ordinary Least Squares (OLS)|OLS]]
- [[Generalized Linear Model (GLM)|GLM]]
- [[clustered standard errors]]
- [[Conley standard errors]]
- [[Driscoll–Kraay]]
- [[Hypothesis testing]]
- [[Wald, LM, and LR tests]]

---

## References

- Newey & West (1987), "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix," *Econometrica*
- Andrews (1991), "Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation," *Econometrica*
- Wooldridge, *Econometric Analysis of Cross Section and Panel Data* (Ch. 12: HAC inference)
