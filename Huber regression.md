---
title: Huber Regression
aliases: [Huber regression, Huber M-estimator, Huber loss]
tags: [econometrics, robust-methods, estimation]
updated: 2026-03-05
---

# Huber Regression

> [!summary]
> M-estimator using the Huber loss function: quadratic for small residuals, linear for large ones. Provides a smooth transition between least-squares and least-absolute-deviations, downweighting outliers while maintaining efficiency near the normal model.

## Huber Loss

$$
\rho_c(r) = \begin{cases}
\frac{1}{2} r^2 & \text{if } |r| \leq c \\
c |r| - \frac{1}{2} c^2 & \text{if } |r| > c
\end{cases}
$$

Estimate $\hat{\beta}$ by minimizing $\sum_{i=1}^n \rho_c(y_i - x_i^\top \beta)$.

Tuning parameter $c$ (often $c = 1.345\hat{\sigma}$) controls the transition; smaller $c$ → more robust, less efficient.

> [!tip]
> - **Efficiency vs. robustness**: Huber achieves 95% efficiency at the normal model while being highly robust to outliers
> - **Compared to quantile regression**: Quantile regression (LAD) is fully robust but less efficient under light-tailed errors
> - **Compared to OLS**: OLS is most efficient under normality but highly sensitive to outliers

## Code

```python
from sklearn.linear_model import HuberRegressor

model = HuberRegressor(epsilon=1.35, max_iter=100)
model.fit(X, y)
```

## Related notes

- [[quantile regression]]
- [[M-estimation]]
- [[Robust Methods (MOC)]]
