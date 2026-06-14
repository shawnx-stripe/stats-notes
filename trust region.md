---
title: Trust Region
aliases: [trust region, trust region method]
tags: [optimization, estimation]
updated: 2026-03-05
---

# Trust Region

> [!summary]
> Optimization method that restricts steps to a region where the local model (e.g., quadratic) is trusted. Adaptively adjusts the region size based on agreement between model and actual function. More robust than line search for ill-conditioned problems.

## Algorithm

At iteration $k$:

1. Solve subproblem: $\min_s m_k(s) = f(x_k) + g_k's + \frac{1}{2}s'B_k s$ subject to $\|s\| \leq \Delta_k$
2. Compute reduction ratio: $\rho_k = \frac{f(x_k) - f(x_k + s_k)}{m_k(0) - m_k(s_k)}$
3. Update:
   - If $\rho_k > \eta_1$: accept step, possibly increase $\Delta_k$
   - If $\rho_k < \eta_2$: reject step, decrease $\Delta_k$

The trust region radius $\Delta_k$ shrinks when the model is poor, expands when it's good.

## Comparison

| Method | Step size | Robustness | Use case |
|--------|-----------|------------|----------|
| Line search | Unconstrained direction, then search | Moderate | Well-conditioned |
| Trust region | Constrained step, adapt region | High | Ill-conditioned, nonconvex |

> [!tip] When to use
> Trust region methods are preferred for maximum likelihood estimation with difficult likelihood surfaces, nonlinear least squares with outliers, and when Hessian approximations are poor.

## Related notes

- [[Model Estimation (MOC)]]
- [[BFGS]]
