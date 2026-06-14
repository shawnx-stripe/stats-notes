---
title: Profile Likelihood
aliases: [profile likelihood, profile-likelihood, profile likelihood CI]
tags: [estimation, inference, likelihood]
updated: 2026-04-02
---

# Profile Likelihood

> [!summary] Quick definition
> Profile likelihood fixes the parameter of interest at candidate values, re-optimizes nuisance parameters, and uses the resulting likelihood curve for tests or confidence intervals.

## Why use it

- Handles asymmetric likelihoods better than Wald approximations.
- Useful near boundaries or when curvature is far from quadratic.
- Common in GLMs, mixed models, and nonlinear likelihoods.

## Minimal code snippets

```r
fit <- glm(y ~ x1 + x2, family = binomial(), data = df)
confint(fit)  # profile-likelihood intervals for glm objects
```

## Related notes

- [[Maximum Likelihood Estimation (MLE)]] · [[Wald, LM, and LR tests]] · [[Bayesian econometrics]]
