---
title: Hausman Test
aliases: [Hausman test, Hausman specification test, Hausman–Wu test]
tags: [econometrics, diagnostics, panel-data]
updated: 2026-03-05
---

# Hausman Test

> [!summary]
> Specification test comparing a consistent estimator with an efficient-under-$H_0$ estimator. Classic application: FE vs. RE in panels — rejection favors FE (individual effects correlated with regressors). Also used for endogeneity testing.

## Test Statistic

$$
H = (\hat{\beta}_{\text{FE}} - \hat{\beta}_{\text{RE}})^\top \left[\widehat{\text{Var}}(\hat{\beta}_{\text{FE}}) - \widehat{\text{Var}}(\hat{\beta}_{\text{RE}})\right]^{-1} (\hat{\beta}_{\text{FE}} - \hat{\beta}_{\text{RE}}) \sim \chi^2(k)
$$

Under $H_0$ (no correlation), both estimators are consistent but RE is efficient. Under $H_a$, RE is inconsistent.

> [!warning]
> - Requires the variance difference matrix to be positive definite (can fail in practice)
> - Sensitive to violations of other RE assumptions (homoskedasticity, serial independence)
> - Rejection indicates misspecification but doesn't specify the source

## Code

```r
# R: Hausman test for panel data
library(plm)
fe <- plm(y ~ x, data = pdata, model = "within")
re <- plm(y ~ x, data = pdata, model = "random")
phtest(fe, re)
```

## Related notes

- [[random effects]]
- [[two-way fixed effects]]
- [[Panel Data Methods (MOC)]]
- [[Durbin–Wu–Hausman test]]
