---
title: BFGS
aliases: [BFGS, Broyden-Fletcher-Goldfarb-Shanno, quasi-Newton method, L-BFGS]
tags: [optimization, estimation]
updated: 2026-03-05
---

# BFGS

> [!summary]
> Quasi-Newton optimization method that approximates the Hessian using gradient information, avoiding expensive second-derivative computation. L-BFGS (limited memory) variant scales to high dimensions. Standard workhorse for smooth unconstrained optimization.

## Key insight

BFGS builds a positive-definite approximation $B_k \approx \nabla^2 f(x_k)$ via rank-2 updates using gradient differences. Converges superlinearly (faster than gradient descent, slower than Newton). L-BFGS stores only $m \approx 5$–$20$ vector pairs instead of the full Hessian, reducing memory from $O(n^2)$ to $O(mn)$.

## Python

```python
from scipy.optimize import minimize

result = minimize(fun, x0, method='L-BFGS-B', jac=grad_fun,
                  bounds=bounds, options={'maxiter': 1000})
print(f"Converged: {result.success}, f(x*): {result.fun:.4f}")
```

> [!tip]
> Use BFGS for moderate-dimensional problems ($n < 1000$), L-BFGS for high dimensions. Both require smooth, differentiable objectives. For non-smooth problems, use Nelder–Mead or subgradient methods.

## Related notes

- [[Maximum Likelihood Estimation (MLE)|MLE]]
- [[Model Estimation (MOC)]]
- [[trust region]]
