---
title: Influence Function
aliases: [influence function, efficient influence function, IF, influence curve]
tags: [econometrics, inference, semiparametric]
updated: 2026-03-05
---

# Influence Function

> [!summary]
> Function characterizing the first-order effect of a single observation on an estimator. The efficient influence function achieves the semiparametric efficiency bound. Central to [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], and variance estimation in causal ML.

## Definition

The **influence function** of an estimator $\hat{\theta}$ at observation $i$ is:
$$
\operatorname{IF}_i(\theta) = \lim_{\epsilon \to 0} \frac{\hat{\theta}((1-\epsilon)F + \epsilon \delta_{Z_i}) - \hat{\theta}(F)}{\epsilon}
$$
where $\delta_{Z_i}$ is a point mass at observation $Z_i$.

**Asymptotic variance**: $\operatorname{Var}(\sqrt{n}\hat{\theta}) = \mathbb{E}[\operatorname{IF}^2]$.

**Efficient influence function (EIF)**: The unique IF that achieves the semiparametric efficiency bound for estimating $\theta$.

> [!example]
> For the ATE under unconfoundedness, the EIF is:
> $$
> \operatorname{IF}_i = \frac{D_i(Y_i - \hat{\mu}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-D_i)(Y_i - \hat{\mu}_0(X_i))}{1 - \hat{e}(X_i)} + \hat{\mu}_1(X_i) - \hat{\mu}_0(X_i) - \tau
> $$
> This is the AIPW estimator's score function.

## Minimal code snippets

```python
# Python: AIPW with explicit influence function
def aipw_if(y, d, x, e_hat, mu1_hat, mu0_hat):
    """Compute AIPW influence function."""
    tau = (mu1_hat - mu0_hat).mean()
    if_vals = (d * (y - mu1_hat) / e_hat -
               (1 - d) * (y - mu0_hat) / (1 - e_hat) +
               (mu1_hat - mu0_hat) - tau)
    return if_vals, tau, if_vals.std() / np.sqrt(len(y))

# Inference via influence function
if_vals, ate_hat, se = aipw_if(df['Y'], df['D'], df['X'], e_hat, mu1_hat, mu0_hat)
print(f"ATE: {ate_hat:.3f} (SE: {se:.3f})")
```

## Related notes

- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[M-estimation]]
- [[Robust Methods (MOC)]]
- [[Model Estimation (MOC)]]
