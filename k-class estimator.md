---
title: K-Class Estimator
aliases: [k-class estimator, k-class, kappa-class estimator]
tags: [econometrics, iv, estimation]
updated: 2026-03-05
---

# K-Class Estimator

> [!summary]
> Family of IV estimators parameterized by $\kappa$. Includes [[Two-Stage Least Squares (2SLS)|2SLS]] ($\kappa=1$), [[Limited Information Maximum Likelihood (LIML)|LIML]] ($\kappa=$ smallest eigenvalue), and [[Fuller estimator]] ($\kappa=$ LIML − $c/n$). Higher $\kappa$ reduces bias but increases variance.

## Definition

The k-class estimator for $\beta$ in $Y = D\beta + X\gamma + u$ is:
$$
\hat{\beta}_\kappa = (D'(I - \kappa M_Z)D)^{-1} D'(I - \kappa M_Z)Y
$$
where $M_Z = I - P_Z$ and $P_Z = Z(Z'Z)^{-1}Z'$ projects onto the instrument space.

| $\kappa$ | Estimator | Properties |
|----------|-----------|------------|
| 0 | OLS | Inconsistent under endogeneity |
| 1 | 2SLS | Consistent, median-unbiased, large finite-sample bias with weak IV |
| $\hat{\kappa}_{\text{LIML}}$ | LIML | Consistent, approximately median-unbiased, more robust to weak IV |
| $\hat{\kappa}_{\text{Fuller}}$ | Fuller | Nearly unbiased, lower variance than LIML |

> [!tip]
> With weak instruments ($F < 10$), prefer LIML or Fuller over 2SLS. LIML has smaller median bias, and Fuller ($\kappa = \kappa_{\text{LIML}} - c/n$ with $c=1$) has approximately unbiased finite-sample distribution.

## When to use

Use 2SLS by default. Switch to LIML/Fuller if:
- First-stage F-statistic is weak (< 10)
- Many instruments relative to sample size
- Concerned about finite-sample bias

## Related notes

- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Fuller estimator]]
- [[Instrumental Variables (IV)]]
