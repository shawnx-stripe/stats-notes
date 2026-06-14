---
title: Measurement Error
aliases: [Measurement error, measurement error, errors-in-variables, mismeasurement, misclassification]
tags: [estimation, identification, regression]
updated: 2026-04-02
---

# Measurement Error

> [!summary] Quick definition
> Measurement error occurs when the recorded variable differs from the true latent quantity, creating bias, attenuation, or misclassification problems in estimation.

## Common cases

- Classical error in regressors, which attenuates OLS coefficients toward zero in simple linear models.
- Nonclassical error, where the error is correlated with the true value or other covariates.
- Misclassification in binary treatment, instrument, or outcome variables.

## Why it matters

- Coefficients can be biased even when treatment assignment is otherwise exogenous.
- DiD, IV, and compliance classifications can all be distorted by miscoding.
- Fixes usually require validation data, repeated measurements, instruments, or structural assumptions.

## Related notes

- [[exogeneity]]
- [[Instrumental Variables (IV)]]
- [[quasi-experimental design]]
- [[defiers]]

