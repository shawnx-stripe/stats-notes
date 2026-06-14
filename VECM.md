---
title: VECM
aliases: [VECM, vector error correction model, VEC model]
tags: [econometrics, time-series, cointegration]
updated: 2026-03-05
---

# VECM

> [!summary]
> Vector Error Correction Model: VAR in first differences augmented with error-correction terms from cointegrating relationships. Captures both short-run dynamics and long-run equilibrium among non-stationary but cointegrated series.

## Model specification

$$
\Delta Y_t = \alpha \beta' Y_{t-1} + \Gamma_1 \Delta Y_{t-1} + \cdots + \Gamma_{p-1}\Delta Y_{t-p+1} + \epsilon_t
$$

where:
- $Y_t$ is a vector of I(1) non-stationary variables
- $\beta' Y_{t-1}$ is the error-correction term (cointegrating relationship)
- $\alpha$ measures the speed of adjustment to equilibrium
- $\Gamma_i$ capture short-run dynamics

The rank of $\alpha\beta'$ equals the number of cointegrating relationships.

## When to use

- Multiple non-stationary (I(1)) time series that are cointegrated
- Want to model both short-run fluctuations and long-run equilibrium
- [[Johansen]] test confirms cointegration

> [!tip]
> Estimate the number of cointegrating relationships using the [[Johansen]] trace or max-eigenvalue test before fitting the VECM.

## Python snippet

```python
from statsmodels.tsa.vector_ar.vecm import VECM

# Fit VECM with 2 lags and 1 cointegrating relationship
model = VECM(data, k_ar_diff=2, coint_rank=1, deterministic='ci')
vecm_fit = model.fit()
print(vecm_fit.summary())
```

## R snippet

```r
library(urca)
# Johansen test for cointegration rank
johansen <- ca.jo(data, type = "trace", K = 2)
# Estimate VECM
vecm_fit <- cajorls(johansen, r = 1)  # r = number of cointegrating vectors
```

## Related notes

- [[VAR]]
- [[cointegration]]
- [[Engle–Granger]]
- [[Johansen]]
- [[Time Series (MOC)]]
