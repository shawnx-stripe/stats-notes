---
title: Multiple Imputation
aliases: [multiple imputation, MI, multiple imputation by chained equations, MICE]
tags: [missing-data, estimation]
updated: 2026-03-05
---

# Multiple Imputation

> [!summary]
> Missing data method that generates $M$ complete datasets by drawing from the predictive distribution of missing values, analyzes each, and combines results using [[Rubin's rules]]. Valid under MAR; accounts for imputation uncertainty.

## Combining rules

For parameter estimate $\hat{\theta}$ and variance $\hat{V}$:

$$
\bar{\theta} = \frac{1}{M}\sum_{m=1}^M \hat{\theta}_m
$$

$$
T = \bar{V} + \left(1 + \frac{1}{M}\right) B
$$

where $\bar{V} = \frac{1}{M}\sum_{m=1}^M \hat{V}_m$ is within-imputation variance and $B = \frac{1}{M-1}\sum_{m=1}^M (\hat{\theta}_m - \bar{\theta})^2$ is between-imputation variance.

## When to use

- Data are missing at random (MAR) conditional on observed covariates
- Single imputation underestimates uncertainty
- Preferred over complete case analysis when missingness is related to observables
- Typical choices: $M = 5-20$ for most applications, $M = 100+$ for high missing fractions

> [!tip] Implementation
> Use `mice` package in R or `IterativeImputer` in Python. Always check convergence diagnostics and verify that the imputation model is richer than the analysis model.

## Related notes

- [[Missing Data and Selection (MOC)]]
- [[EM algorithm]]
- [[ignorability]]
