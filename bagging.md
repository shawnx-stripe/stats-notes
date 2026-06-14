---
title: Bagging
aliases: [bagging, Bagging, bootstrap aggregating]
tags: [ml]
updated: 2026-03-05
---

# Bagging

> [!summary]
> Bootstrap aggregating (bagging) reduces variance of high-variance estimators by averaging predictions over many bootstrap resamples. Foundation of [[random forests]].

## Algorithm

1. Draw $B$ bootstrap samples from the training data (sampling with replacement)
2. Train a base learner (e.g., decision tree) on each bootstrap sample to get $\hat{f}_b(x)$
3. Aggregate predictions:
   - Regression: $\hat{f}_{\text{bag}}(x) = \frac{1}{B}\sum_{b=1}^B \hat{f}_b(x)$
   - Classification: majority vote across $\hat{f}_b(x)$

Bagging reduces variance without increasing bias. Works best for unstable learners (high variance, low bias) like deep [[decision trees]].

## Why it works

Bootstrap samples are correlated but not identical. Averaging reduces variance by:

$$
\operatorname{Var}\left(\frac{1}{B}\sum_{b=1}^B \hat{f}_b\right) = \frac{\sigma^2}{B} + \left(1 - \frac{1}{B}\right)\rho\sigma^2
$$

where $\rho$ is the average correlation among the $\hat{f}_b$. Lower $\rho$ (more diversity) gives more variance reduction.

## Python snippet

```python
from sklearn.ensemble import BaggingRegressor
from sklearn.tree import DecisionTreeRegressor

# Bagging with 100 decision trees
bagging = BaggingRegressor(
    estimator=DecisionTreeRegressor(max_depth=None),
    n_estimators=100,
    max_samples=1.0,
    bootstrap=True
)
bagging.fit(X_train, y_train)
```

## Related notes

- [[random forests]]
- [[bootstrap]]
- [[decision trees]]
