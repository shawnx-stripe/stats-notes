---
title: Durbin–Watson
aliases: [Durbin-Watson, Durbin–Watson test, DW test, DW statistic]
tags: [econometrics, diagnostics, time-series]
updated: 2026-03-05
---

# Durbin–Watson

> [!summary]
> Test for first-order autocorrelation in OLS residuals. DW ≈ 2 indicates no autocorrelation; DW < 2 suggests positive, DW > 2 negative. Limited: only tests AR(1), not valid with lagged dependent variable (use [[Breusch–Godfrey]] instead).

## Test statistic

$$\text{DW} = \frac{\sum_{t=2}^{n}(\hat{\varepsilon}_t - \hat{\varepsilon}_{t-1})^2}{\sum_{t=1}^{n}\hat{\varepsilon}_t^2} \approx 2(1 - \hat{\rho})$$

where $\hat{\rho}$ is the sample autocorrelation. Critical values depend on $n$ and $k$ (number of regressors); inconclusive region exists between $d_L$ and $d_U$.

## Python

```python
from statsmodels.stats.stattools import durbin_watson
from statsmodels.api import OLS
model = OLS(y, X).fit()
dw = durbin_watson(model.resid)
print(f"DW statistic: {dw:.2f}  (≈2 means no autocorrelation)")
```

> [!warning]
> DW only tests AR(1) and assumes regressors are strictly exogenous. For models with lagged $y$ or more general serial correlation, use [[Breusch–Godfrey]].

## Related notes

- [[Breusch–Godfrey]]
- [[Newey–West]]
- [[Ordinary Least Squares (OLS)|OLS]]
- [[Econometrics (MOC)]]
