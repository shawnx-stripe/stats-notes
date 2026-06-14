---
title: Quantile Regression
aliases: [quantile regression, Quantile regression, conditional quantile, LAD regression]
tags: [econometrics, estimation, robust-methods]
updated: 2026-03-05
---

# Quantile Regression

> [!summary]
> Estimates conditional quantiles of the outcome distribution rather than the conditional mean. Robust to outliers and reveals heterogeneous effects across the distribution. Minimizes an asymmetric absolute-loss function.

## Loss function

For quantile $\tau \in (0,1)$, minimize:

$$
\hat{\beta}(\tau) = \operatorname{argmin}_\beta \sum_{i=1}^n \rho_\tau(Y_i - X_i'\beta)
$$

where $\rho_\tau(u) = u(\tau - \mathbb{1}\{u < 0\})$ is the check function (asymmetric absolute loss).

## Minimal code

```python
import statsmodels.api as sm

# Estimate median (50th percentile) regression
model = sm.QuantReg(Y, X).fit(q=0.5)

# Multiple quantiles
quantiles = [0.25, 0.5, 0.75]
results = [sm.QuantReg(Y, X).fit(q=q) for q in quantiles]
```

> [!tip] When to use
> - Heterogeneous treatment effects across the outcome distribution
> - Robust estimation when outcome has heavy tails or outliers
> - Interest in effects on inequality (e.g., wage gaps at different quantiles)
> - Standard errors via bootstrap or asymptotic approximation

## Related notes

- [[Ordinary Least Squares (OLS)|OLS]]
- [[Model Estimation (MOC)]]
- [[Robust Methods (MOC)]]
- [[quantile treatment effects]]
