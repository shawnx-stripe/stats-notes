---
title: MPEC
aliases: [MPEC, mathematical programming with equilibrium constraints]
tags: [econometrics, structural-models, estimation]
updated: 2026-03-05
---

# MPEC

> [!summary]
> Estimation approach for structural models that reformulates the nested fixed-point problem as a single constrained optimization. Often faster than NFXP for large-state-space dynamic discrete choice models.

## Approach

Standard NFXP (nested fixed-point): inner loop solves dynamic program, outer loop maximizes likelihood.

MPEC reformulation:

$$
\begin{aligned}
\max_{\theta, V} \quad & \mathcal{L}(\theta) \\
\text{s.t.} \quad & V(x) = \max_d \left\{u_d(x, \theta) + \beta \sum_{x'} f(x' | x, d) V(x')\right\} \quad \forall x
\end{aligned}
$$

Solve as a single constrained optimization using NLP solvers (e.g., KNITRO, IPOPT).

> [!check] Advantages
> - **Computational speed**: No repeated inner-loop solutions; modern NLP solvers are fast
> - **Numerical stability**: Avoids iterative convergence issues in nested loops
> - **Large state spaces**: Particularly beneficial when the state space is large

> [!warning]
> - Still requires derivatives of the Bellman constraint (provided automatically in some implementations)
> - Compare with [[Hotz–Miller CCP]] for an alternative two-step approach

## Related notes

- [[Structural models]]
- [[Hotz–Miller CCP]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
