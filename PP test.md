---
title: PP Test
aliases: [PP test, Phillips-Perron test, Phillips–Perron test]
tags: [econometrics, time-series, diagnostics, stationarity]
updated: 2026-03-05
---

# PP Test

> [!summary]
> Phillips–Perron unit root test: nonparametric correction to the Dickey–Fuller t-statistic that is robust to serial correlation and heteroskedasticity. Same null hypothesis (unit root) as [[ADF test]] but with different serial correlation treatment.

## Test statistic

$$
Z_t = t_{\hat{\rho}} \sqrt{\frac{\hat{\gamma}_0}{\hat{\lambda}^2}} - \frac{T(\hat{\lambda}^2 - \hat{\gamma}_0)}{2\hat{\lambda}^2} \cdot \frac{\operatorname{se}(\hat{\rho})}{\hat{\sigma}}
$$

where $t_{\hat{\rho}}$ is the DF t-statistic from $\Delta y_t = \alpha + \rho y_{t-1} + \epsilon_t$, and $\hat{\lambda}^2$ is the Newey–West long-run variance estimator. Under $H_0: \rho = 0$ (unit root), $Z_t$ has the same asymptotic distribution as the ADF statistic.

## PP vs. ADF

| Aspect | ADF | PP |
|--------|-----|-----|
| Serial correlation | Parametric (add lags) | Nonparametric (HAC correction) |
| Lag selection | Required (AIC/BIC) | Bandwidth selection for HAC |
| Power | Higher if lag structure is correct | More robust to lag misspecification |

## Python snippet

```python
from statsmodels.tsa.stattools import adfuller
# adfuller with regression='ct' and autolag='AIC' is standard ADF
# For PP test:
from arch.unitroot import PhillipsPerron
pp_test = PhillipsPerron(y)
print(pp_test.summary())
```

## Related notes

- [[ADF test]]
- [[KPSS test]]
- [[Time Series (MOC)]]
