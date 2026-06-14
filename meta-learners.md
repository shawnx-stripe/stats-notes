---
title: Meta-Learners
aliases: [meta-learners, T-learner, S-learner, X-learner, R-learner, DR-learner]
tags: [machine-learning, causal-inference, treatment-effects]
updated: 2026-03-05
---

# Meta-Learners

> [!summary]
> Modular strategies for CATE estimation using generic ML base learners. T-learner fits separate models per arm; S-learner includes treatment as feature; X-learner uses imputed treatment effects; R-learner uses Robinson decomposition.

## Comparison of meta-learners

| Method | Approach | Pros | Cons |
|--------|----------|------|------|
| **S-learner** | Fit $\hat{\mu}(x, d)$, predict $\hat{\tau}(x) = \hat{\mu}(x,1) - \hat{\mu}(x,0)$ | Simple, single model | Regularization penalizes treatment effect |
| **T-learner** | Fit $\hat{\mu}_0(x)$ and $\hat{\mu}_1(x)$ separately | Flexible, no regularization bias | Inefficient, ignores commonality |
| **X-learner** | Impute $\tilde{\tau}_1 = Y_1 - \hat{\mu}_0(X_1)$, $\tilde{\tau}_0 = \hat{\mu}_1(X_0) - Y_0$; fit $\tau$ models | Efficient, good with imbalance | More complex |
| **R-learner** | Partial out $D, Y$ w.r.t. $X$, fit residual-on-residual | Orthogonalized, low bias | Requires propensity score estimate |
| **DR-learner** | Doubly robust combination of OR + IPW | Consistent if either model correct | Requires both models |

> [!tip]
> For experimentation with balanced treatment:
> - Use **T-learner** for simplicity
> - Use **X-learner** if sample sizes differ across arms
> - Use **R-learner** or **DR-learner** for observational data

## Minimal code snippets

```python
# Python: T-learner with sklearn
from sklearn.ensemble import GradientBoostingRegressor

# Fit separate models
mu0 = GradientBoostingRegressor().fit(X[D == 0], Y[D == 0])
mu1 = GradientBoostingRegressor().fit(X[D == 1], Y[D == 1])

# Predict CATE
tau_hat = mu1.predict(X) - mu0.predict(X)
```

```r
# R: meta-learners with causalml (via reticulate)
# Or use grf for causal forests as an alternative
library(grf)
cf <- causal_forest(X, Y, W)
tau_hat <- predict(cf)$predictions
```

## Related notes

- [[treatment effect heterogeneity]]
- [[double machine learning]]
- [[causal forests]]
- [[Machine Learning for Causal Inference (MOC)]]
