---
title: Gaussian Process
aliases: [Gaussian process, GP, Gaussian process regression, kriging]
tags: [machine-learning, nonparametric, estimation]
updated: 2026-03-05
---

# Gaussian Process

> [!summary]
> Nonparametric Bayesian regression method defining a prior distribution over functions via a mean function and kernel (covariance function). Provides natural uncertainty quantification. Computationally $O(n^3)$ without approximations.

## Model

$$
\begin{aligned}
f(x) &\sim \mathcal{GP}(m(x), k(x, x')) \\
y_i &= f(x_i) + \varepsilon_i, \quad \varepsilon_i \sim N(0, \sigma^2)
\end{aligned}
$$

Common kernel: squared exponential $k(x, x') = \sigma_f^2 \exp\left(-\frac{\|x - x'\|^2}{2\ell^2}\right)$.

Posterior prediction at $x_*$:
$$
p(f_* | X, y, x_*) = N(\mu_*, \Sigma_*)
$$
where $\mu_* = k_*^\top (K + \sigma^2 I)^{-1} y$ and $\Sigma_* = k_{**} - k_*^\top (K + \sigma^2 I)^{-1} k_*$.

## Code

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel

kernel = RBF(length_scale=1.0) + WhiteKernel(noise_level=1.0)
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
gp.fit(X_train, y_train)

# Predict with uncertainty
y_pred, sigma = gp.predict(X_test, return_std=True)
```

## Related notes

- [[kernel regression]]
- [[ML for Econometrics (MOC)]]
