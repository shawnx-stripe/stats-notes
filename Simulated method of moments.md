---
title: Simulated Method of Moments
aliases: [Simulated method of moments, SMM, method of simulated moments, MSM estimation]
tags: [econometrics, estimation, structural-models]
updated: 2026-03-05
---

# Simulated Method of Moments

> [!summary]
> Estimation method that matches simulated moments from a structural model to their sample counterparts when the likelihood or exact moments are intractable. Extends [[Generalized Method of Moments (GMM)|GMM]] using simulation.

## Objective function

$$
\hat{\theta}_{\text{SMM}} = \arg\min_\theta \left(\bar{m}_N - \frac{1}{S}\sum_{s=1}^S m(Y_s(\theta))\right)' W \left(\bar{m}_N - \frac{1}{S}\sum_{s=1}^S m(Y_s(\theta))\right)
$$

where:
- $\bar{m}_N$ are sample moments from the data
- $Y_s(\theta)$ are $S$ simulated datasets from the model at parameter $\theta$
- $W$ is a weighting matrix (e.g., inverse of moment variance)

As $S \to \infty$, SMM converges to GMM.

## When to use

- Structural models with intractable likelihoods (e.g., agent-based models, dynamic discrete choice)
- Moments can be computed from simulations but not in closed form
- Need flexibility in choosing identifying moments

> [!tip]
> Use a large number of simulations $S$ (e.g., $S \geq 100N$) to reduce simulation error. Too small $S$ introduces noise in the objective function.

## Python snippet

```python
import numpy as np
from scipy.optimize import minimize

def smm_objective(theta, data_moments, W, S=1000):
    # Simulate S datasets under theta
    sim_moments = np.array([simulate_and_compute_moments(theta) for _ in range(S)])
    avg_sim_moments = sim_moments.mean(axis=0)
    diff = data_moments - avg_sim_moments
    return diff @ W @ diff

result = minimize(smm_objective, x0=theta_init, args=(data_moments, W_matrix))
```

## Related notes

- [[Generalized Method of Moments (GMM)|GMM]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
- [[Structural models]]
- [[Model Estimation (MOC)]]
- [[indirect inference]]
