---
title: Variance Estimation
aliases: [variance estimation, Variance estimation, covariance estimation, standard error estimation]
tags: [inference, estimation, statistics]
updated: 2026-04-02
---

# Variance Estimation

> [!summary] Quick definition
> Variance estimation computes the uncertainty of an estimator, typically to produce [[clustered standard errors|standard errors]], confidence intervals, and hypothesis tests.

## Common approaches

- Plug-in formulas under a parametric model.
- Sandwich / robust estimators when the mean model is correct but the variance model may be misspecified.
- Resampling methods such as [[bootstrap]] or jackknife.
- Influence-function-based estimators in semiparametric and causal-ML settings.

## Canonical form

For many M-estimators,

$$
\widehat{\mathrm{Var}}(\hat\theta) = \frac{1}{n} A^{-1} B A^{-1},
$$

where $A$ is a curvature or Jacobian term and $B$ is the variance of the score or influence function.

## Why it matters

- Standard errors can be badly wrong if dependence, heteroskedasticity, or clustering is ignored.
- The estimator and its variance formula need to match the sampling design.
- Small-sample corrections often matter when clusters or effective sample sizes are limited.

## Related notes

- [[Standard Errors and Inference (MOC)]]
- [[clustered standard errors]]
- [[bootstrap]]
- [[influence function]]

