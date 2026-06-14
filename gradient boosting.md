---
title: Gradient boosting
aliases: [gradient boosting, Gradient boosting, GBM, GBRT]
tags: [ml]
updated: 2026-03-05
---

# Gradient boosting

> [!summary]
> Ensemble method that sequentially fits weak learners (usually shallow trees) to the negative gradient of a loss function. Implementations include XGBoost, LightGBM, and CatBoost.

## Algorithm

Initialize $\hat{f}_0(x) = \arg\min_c \sum_{i=1}^n L(y_i, c)$.

For $m = 1, \ldots, M$:
1. Compute pseudo-residuals: $r_{im} = -\left[\frac{\partial L(y_i, f(x_i))}{\partial f(x_i)}\right]_{f = \hat{f}_{m-1}}$
2. Fit a weak learner $h_m(x)$ to $(x_i, r_{im})$
3. Update: $\hat{f}_m(x) = \hat{f}_{m-1}(x) + \nu \cdot h_m(x)$

where $\nu$ is the learning rate (shrinkage parameter).

> [!tip]
> For causal inference, gradient boosting can be used within [[meta-learners]] (T-learner, X-learner) or [[double machine learning]] for flexible outcome modeling. Tune hyperparameters via [[cross-validation]], but use [[cross-fitting]] for valid causal inference.

## Minimal code snippets

```python
# Python: gradient boosting with XGBoost
import xgboost as xgb

dtrain = xgb.DMatrix(X_train, label=y_train)
params = {'max_depth': 5, 'eta': 0.1, 'objective': 'reg:squarederror'}
bst = xgb.train(params, dtrain, num_boost_round=100)
y_pred = bst.predict(xgb.DMatrix(X_test))
```

```r
# R: gradient boosting with xgboost
library(xgboost)
bst <- xgboost(data = as.matrix(X_train), label = y_train,
               max_depth = 5, eta = 0.1, nrounds = 100, objective = "reg:squarederror")
pred <- predict(bst, as.matrix(X_test))
```

## Related notes

- [[random forests]]
- [[decision trees]]
- [[regularization]]
