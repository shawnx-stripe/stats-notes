---
title: Durbin–Wu–Hausman Test
aliases: [Durbin-Wu-Hausman test, Durbin–Wu–Hausman, endogeneity test, DWH test]
tags: [econometrics, iv, diagnostics]
updated: 2026-03-05
---

# Durbin–Wu–Hausman Test

> [!summary]
> Test comparing OLS and IV estimates to diagnose endogeneity. Under the null of exogeneity, both are consistent but OLS is more efficient. Rejection favors IV. Equivalent to testing significance of first-stage residuals in the structural equation.

## Implementation

1. Regress endogenous variable $X$ on instruments $Z$ (first stage); save residuals $\hat{v}$
2. Regress $y$ on $X$, exogenous controls, *and* $\hat{v}$
3. Test $H_0: \gamma = 0$ in $y = \alpha + \beta X + \gamma \hat{v} + \varepsilon$

If $\gamma \neq 0$, then $X$ is correlated with the structural error, confirming endogeneity.

## Stata

```stata
ivregress 2sls y x1 x2 (x_endog = z1 z2), first
estat endogenous  // Durbin-Wu-Hausman test
```

> [!tip]
> This test has low power with weak instruments. Rejection supports IV, but failure to reject doesn't prove exogeneity. Always report first-stage $F$-statistic alongside.

## Related notes

- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[Hausman test]]
- [[exogeneity]]
