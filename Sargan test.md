---
title: Sargan Test
aliases: [Sargan test, Sargan–Hansen test, Sargan overidentification test]
tags: [econometrics, iv, diagnostics]
updated: 2026-03-05
---

# Sargan Test

> [!summary]
> Test of overidentifying restrictions for IV/2SLS under homoskedasticity. Equivalent to [[Hansen J test]] when errors are i.i.d. Rejection suggests instrument invalidity.

## Test statistic

$$
S = N \cdot R^2 \xrightarrow{d} \chi^2_{k - m}
$$

where $R^2$ comes from regressing the 2SLS residuals $\hat{\epsilon}_i$ on all instruments $Z_i$, and $k - m$ is the number of overidentifying restrictions (instruments minus endogenous regressors). Under $H_0$ (all instruments valid), $S \sim \chi^2_{k-m}$.

## When to use

- You have more instruments than endogenous variables ($k > m$, overidentified model)
- Errors are homoskedastic or you are willing to assume i.i.d. for initial diagnostics
- For robust version under heteroskedasticity, use [[Hansen J test]]

> [!warning]
> The Sargan test has low power when all instruments are invalid or when invalidity is weak. Failing to reject does not prove instrument validity.

## Stata snippet

```stata
ivregress 2sls y x1 (x_endog = z1 z2 z3), first
estat overid  // Sargan test (assumes homoskedasticity)
```

## Related notes

- [[Hansen J test]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Generalized Method of Moments (GMM)|GMM]]
