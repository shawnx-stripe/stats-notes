---
title: GARCH
aliases: [GARCH, ARCH, generalized autoregressive conditional heteroskedasticity]
tags: [econometrics, time-series, volatility]
updated: 2026-03-05
---

# GARCH

> [!summary]
> Generalized Autoregressive Conditional Heteroskedasticity model. Models time-varying variance as a function of past squared residuals (ARCH terms) and past conditional variances (GARCH terms). Foundation for volatility modeling in finance.

## GARCH(p,q) Specification

$$
\begin{aligned}
y_t &= \mu_t + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim N(0,1) \\
\sigma_t^2 &= \omega + \sum_{i=1}^q \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^p \beta_j \sigma_{t-j}^2
\end{aligned}
$$

GARCH(1,1) is most common: $\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2$.

**Stationarity** requires $\sum \alpha_i + \sum \beta_j < 1$.

## Code

```python
from arch import arch_model
import pandas as pd

# Fit GARCH(1,1) to returns
model = arch_model(returns, vol='Garch', p=1, q=1)
results = model.fit(disp='off')
print(results.summary())

# Forecast volatility
forecasts = results.forecast(horizon=5)
```

## Related notes

- [[ARIMA]]
- [[Time Series (MOC)]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
