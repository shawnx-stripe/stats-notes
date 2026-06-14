---
title: Partialling Out
aliases: [partialling out, Frisch-Waugh-Lovell, FWL theorem]
tags: [econometrics, estimation]
updated: 2026-03-05
---

# Partialling Out

> [!summary]
> Frisch–Waugh–Lovell theorem: the coefficient on $X_1$ in a multiple regression equals the coefficient from regressing the residualized $Y$ on residualized $X_1$ (both orthogonalized to other covariates). Foundation of [[double machine learning]].

## Theorem

For the regression $Y = X_1 \beta_1 + X_2 \beta_2 + \varepsilon$:

$$
\hat{\beta}_1 = \operatorname{argmin}_b \| \tilde{Y} - b \tilde{X}_1 \|^2
$$

where $\tilde{Y} = M_{X_2} Y$ and $\tilde{X}_1 = M_{X_2} X_1$ are residuals from projecting onto $X_2$, and $M_{X_2} = I - X_2(X_2'X_2)^{-1}X_2'$.

## Minimal code

```python
from sklearn.linear_model import LinearRegression

# Partial out X2 from both Y and X1
resid_y = Y - LinearRegression().fit(X2, Y).predict(X2)
resid_x1 = X1 - LinearRegression().fit(X2, X1).predict(X2)

# Coefficient from residualized regression equals full regression
beta1_partial = LinearRegression().fit(resid_x1, resid_y).coef_
```

> [!tip] Application to causal inference
> In [[double machine learning]], partialling out allows flexible (ML) estimation of nuisance functions while preserving $\sqrt{n}$-consistency for the causal parameter. The key is that prediction errors in $\tilde{Y}$ and $\tilde{X}_1$ are orthogonal to first order.

## Related notes

- [[Ordinary Least Squares (OLS)|OLS]]
- [[double machine learning]]
- [[Local IV]]
