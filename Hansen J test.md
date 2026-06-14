---
title: Hansen J Test
aliases: [Hansen J test, J test, Hansen's J statistic]
tags: [econometrics, iv, diagnostics]
updated: 2026-03-05
---

# Hansen J Test

> [!summary]
> Test of overidentifying restrictions in GMM/IV. Under the null that all instruments are valid, $J = n \cdot \hat{Q} \sim \chi^2(m-k)$. Rejection suggests at least one instrument violates the [[exclusion restriction]].

## Test Statistic

$$
J = n \cdot \hat{Q} = n \cdot \left(\frac{1}{n} Z^\top \hat{u}\right)^\top \hat{W} \left(\frac{1}{n} Z^\top \hat{u}\right) \sim \chi^2(m - k)
$$

where $m$ = number of instruments, $k$ = number of endogenous regressors, $\hat{u}$ are 2SLS residuals, and $\hat{W}$ is a consistent weight matrix.

> [!tip]
> - Requires $m > k$ (overidentification); exactly identified models have $J=0$ by construction
> - Failure to reject does not prove instruments are valid (low power)
> - Consider Hansen J alongside first-stage diagnostics and economic reasoning

## Code

```r
# R: test overidentifying restrictions
library(ivreg)
mod <- ivreg(y ~ x | z1 + z2 + z3)
summary(mod, diagnostics = TRUE)  # includes Hansen J test
```

## Related notes

- [[Generalized Method of Moments (GMM)|GMM]]
- [[Sargan test]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
