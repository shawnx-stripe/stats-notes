---
title: Rademacher Weights
aliases: [Rademacher weights, Rademacher distribution]
tags: [econometrics, inference, bootstrap]
updated: 2026-03-05
---

# Rademacher Weights

> [!summary]
> Random weights taking values $\{-1, +1\}$ with equal probability. Used in the [[wild cluster bootstrap]] as the default weight distribution. Webb (six-point) weights are an alternative for very few clusters.

## Bootstrap procedure

For each bootstrap iteration $b$:
1. Draw $\omega_{gb} \sim \{-1, +1\}$ i.i.d. for each cluster $g = 1, \ldots, G$
2. Construct bootstrap residuals: $\epsilon_{igb}^* = \omega_{gb} \hat{\epsilon}_{ig}$
3. Generate bootstrap outcomes: $y_{igb}^* = X_{ig}\hat{\beta} + \epsilon_{igb}^*$
4. Re-estimate the model on $(y_{igb}^*, X_{ig})$ to obtain $\hat{\beta}_b^*$

The distribution of $\hat{\beta}_b^* - \hat{\beta}$ approximates the sampling distribution of $\hat{\beta}$.

> [!tip]
> Rademacher weights preserve the cluster-level correlation structure and impose symmetry. For $G \leq 12$, [[Webb weights]] (six-point distribution) provide better size control.

## Python snippet

```python
import numpy as np
# Wild cluster bootstrap with Rademacher weights
n_boot = 999
cluster_ids = data['cluster_id'].values
unique_clusters = np.unique(cluster_ids)
G = len(unique_clusters)

for b in range(n_boot):
    # Draw cluster-level Rademacher weights
    omega = np.random.choice([-1, 1], size=G)
    cluster_weights = dict(zip(unique_clusters, omega))

    # Apply weights to residuals
    weights_i = np.array([cluster_weights[c] for c in cluster_ids])
    y_boot = X @ beta_hat + weights_i * residuals
    # Re-estimate model...
```

## Related notes

- [[wild cluster bootstrap]]
- [[Webb weights]]
- [[few-cluster corrections]]
