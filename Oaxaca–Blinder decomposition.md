---
title: Oaxaca–Blinder Decomposition
aliases: [Oaxaca-Blinder decomposition, Oaxaca–Blinder, wage decomposition]
tags: [econometrics, decomposition]
updated: 2026-03-05
---

# Oaxaca–Blinder Decomposition

> [!summary]
> Decomposes the mean outcome gap between two groups into explained (differences in characteristics/endowments) and unexplained (differences in coefficients/returns) components. Standard tool for wage gap and inequality analysis.

## Decomposition formula

$$
\bar{Y}_A - \bar{Y}_B = \underbrace{(\bar{X}_A - \bar{X}_B)'\hat{\beta}_B}_{\text{Explained}} + \underbrace{\bar{X}_A'(\hat{\beta}_A - \hat{\beta}_B)}_{\text{Unexplained}}
$$

where:
- $\bar{Y}_A, \bar{Y}_B$ are mean outcomes for groups A and B
- $\bar{X}_A, \bar{X}_B$ are mean characteristics
- $\hat{\beta}_A, \hat{\beta}_B$ are estimated coefficients from separate regressions

The "explained" part is due to differences in observables; "unexplained" captures coefficient differences (often interpreted as discrimination or unobserved factors).

## Python snippet

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Separate regressions by group
model_A = LinearRegression().fit(X_A, y_A)
model_B = LinearRegression().fit(X_B, y_B)

explained = (X_A.mean(axis=0) - X_B.mean(axis=0)) @ model_B.coef_
unexplained = X_A.mean(axis=0) @ (model_A.coef_ - model_B.coef_)
total_gap = y_A.mean() - y_B.mean()
```

> [!tip]
> The choice of reference group (using $\hat{\beta}_A$ or $\hat{\beta}_B$ as the baseline) affects the magnitude of each component but not the total gap. A pooled regression can also be used as a neutral reference.

## Related notes

- [[composition]]
- [[DFL reweighting]]
- [[Ordinary Least Squares (OLS)|OLS]]
