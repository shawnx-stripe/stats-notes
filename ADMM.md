---
title: ADMM
aliases: [ADMM, alternating direction method of multipliers]
tags: [optimization, estimation]
updated: 2026-03-05
---

# ADMM

> [!summary]
> Alternating Direction Method of Multipliers: splits convex optimization problems into smaller subproblems via augmented Lagrangian decomposition. Useful for distributed optimization and problems with mixed $\ell_1/\ell_2$ penalties.

## Algorithm

For minimizing $f(x) + g(z)$ subject to $Ax + Bz = c$:

$$
\begin{align}
x^{k+1} &= \arg\min_x \left[ f(x) + \frac{\rho}{2}\|Ax + Bz^k - c + u^k\|^2 \right] \\
z^{k+1} &= \arg\min_z \left[ g(z) + \frac{\rho}{2}\|Ax^{k+1} + Bz - c + u^k\|^2 \right] \\
u^{k+1} &= u^k + (Ax^{k+1} + Bz^{k+1} - c)
\end{align}
$$

where $\rho > 0$ is a penalty parameter and $u$ is the scaled dual variable.

> [!tip]
> ADMM is the workhorse for Lasso, elastic net, and group Lasso. Converges slowly to high accuracy but reaches moderate accuracy quickly, making it practical for large-scale problems.

## Related notes

- [[regularization]]
- [[Model Estimation (MOC)]]
