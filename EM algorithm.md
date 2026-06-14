---
title: EM Algorithm
aliases: [EM algorithm, EM, expectation-maximization, expectation maximization algorithm]
tags: [econometrics, estimation, missing-data]
updated: 2026-03-05
---

# EM Algorithm

> [!summary]
> Expectation-Maximization: iterative algorithm for MLE with latent variables or missing data. E-step computes expected log-likelihood given current parameters; M-step maximizes it. Converges to a local maximum; widely used in mixture models.

## Algorithm

Given observed data $y$ and latent variables $z$, maximize $\ell(\theta; y) = \log p(y \mid \theta)$:

1. **E-step**: Compute $Q(\theta \mid \theta^{(t)}) = \mathbb{E}_{z \mid y, \theta^{(t)}}[\log p(y,z \mid \theta)]$
2. **M-step**: Set $\theta^{(t+1)} = \arg\max_\theta Q(\theta \mid \theta^{(t)})$
3. Repeat until convergence

Each iteration is guaranteed to increase the likelihood. Convergence is slow near optimum (linear rate) but robust to initialization.

## Python

```python
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3, max_iter=100, tol=1e-3)
gmm.fit(X)  # EM for Gaussian mixture model
labels = gmm.predict(X)
```

> [!tip]
> Try multiple random initializations to avoid poor local maxima. For large data, use stochastic EM or variational inference for speed.

## Related notes

- [[Maximum Likelihood Estimation (MLE)|MLE]]
- [[Model Estimation (MOC)]]
- [[Missing Data and Selection (MOC)]]
