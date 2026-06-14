---
title: CBPS
aliases: [CBPS, covariate balancing propensity score]
tags: [causal-inference, weighting]
updated: 2026-03-05
---

# CBPS

> [!summary]
> Covariate Balancing Propensity Score (Imai & Ratkovic 2014): estimates propensity scores by directly optimizing covariate balance rather than prediction accuracy. Combines propensity score estimation and balance checking into a single step.

## Key insight

Standard propensity scores (logit/probit) maximize likelihood, which may yield poor balance even with correct specification. CBPS adds moment conditions requiring that weighted covariate means match across treatment groups. This produces weights that *both* satisfy the score equations *and* achieve exact balance on included covariates, often improving finite-sample efficiency over IPW with estimated propensity scores.

## R

```r
library(CBPS)
fit <- CBPS(treat ~ x1 + x2 + x3, data = df, ATT = 0)  # ATE
balance <- balance(fit)  # check standardized mean differences
ate <- lm(y ~ treat, weights = fit$weights)$coef[2]
```

> [!tip]
> CBPS is particularly useful when you have many covariates or suspect propensity score misspecification. For doubly robust estimation, combine CBPS weights with outcome regression.

## Related notes

- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[entropy balancing]]
- [[balancing weights]]
