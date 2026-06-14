---
title: RESET Test
aliases: [RESET test, Ramsey RESET test, regression specification error test]
tags: [econometrics, diagnostics]
updated: 2026-03-05
---

# RESET Test

> [!summary]
> Ramsey's Regression Equation Specification Error Test: tests for omitted nonlinearities by adding powers of fitted values to the regression and testing their joint significance. Rejection suggests functional form misspecification.

## Procedure

1. Run the baseline regression: $y_i = X_i\beta + \epsilon_i$, obtain fitted values $\hat{y}_i$
2. Augment the model: $y_i = X_i\beta + \gamma_2\hat{y}_i^2 + \gamma_3\hat{y}_i^3 + \cdots + \gamma_p\hat{y}_i^p + u_i$
3. Test $H_0: \gamma_2 = \gamma_3 = \cdots = \gamma_p = 0$ using an F-test

Rejection indicates the linear specification is inadequate; the nonlinear terms capture omitted nonlinearities or interactions.

> [!warning]
> RESET is a general test; it does not tell you which nonlinearities to add. Use domain knowledge or exploratory methods to guide functional form.

## Stata snippet

```stata
reg y x1 x2 x3
estat ovtest  // Ramsey RESET test with default powers 2, 3, 4
```

## Python snippet

```python
from statsmodels.stats.diagnostic import linear_reset
from statsmodels.regression.linear_model import OLS

model = OLS(y, X).fit()
reset_stat, reset_pval, _ = linear_reset(model, power=3, use_f=True)
print(f"RESET F-statistic: {reset_stat:.3f}, p-value: {reset_pval:.3f}")
```

## Related notes

- [[Ordinary Least Squares (OLS)|OLS]]
- [[Econometrics (MOC)]]
