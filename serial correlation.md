---
title: Serial correlation
aliases: [serial correlation, Serial correlation, autocorrelation of errors]
tags: [econometrics, time-series]
updated: 2026-03-05
---

# Serial correlation

> [!summary]
> Correlation of error terms across time periods. Invalidates standard OLS inference; requires HAC standard errors ([[Newey–West]]), GLS/FGLS, or design-based corrections. Diagnosed via [[Durbin–Watson]] and [[Breusch–Godfrey]] tests.

## Structure

Error $\varepsilon_t$ satisfies:

$$
\mathbb{E}[\varepsilon_t \varepsilon_s] \neq 0 \quad \text{for } t \neq s
$$

Common forms: AR(1) with $\varepsilon_t = \rho \varepsilon_{t-1} + u_t$, MA(q), or general HAC covariance.

## Consequences

- OLS remains unbiased and consistent (under exogeneity)
- Standard errors are wrong: $\text{Var}(\hat{\beta}) \neq \sigma^2 (X'X)^{-1}$
- t-statistics and confidence intervals invalid
- Can lead to spurious significance in time series regressions

## Minimal code

```python
from statsmodels.regression.linear_model import OLS
from statsmodels.stats.diagnostic import acorr_breusch_godfrey

model = OLS(y, X).fit()

# Test for serial correlation (up to 4 lags)
bg_test = acorr_breusch_godfrey(model, nlags=4)
print(f"Breusch-Godfrey test: LM stat={bg_test[0]:.3f}, p-value={bg_test[1]:.3f}")

# Correct with Newey-West HAC standard errors
model_hac = OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
```

## Related notes

- [[Newey–West]]
- [[Durbin–Watson]]
- [[Breusch–Godfrey]]
- [[clustered standard errors]]
- [[Moulton problem]]
