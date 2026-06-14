---
title: Cross-Validation
aliases: [cross-validation, Cross-validation, CV, k-fold cross-validation, leave-one-out CV]
tags: [machine-learning, estimation, model-selection, diagnostics]
updated: 2026-03-05
---

# Cross-Validation

> [!summary]
> Resampling method for estimating out-of-sample prediction error. Partitions data into K folds; iteratively trains on K−1 folds and evaluates on the held-out fold. Also used within [[cross-fitting]] for causal ML.

## K-fold cross-validation procedure

1. Partition data into $K$ folds of approximately equal size
2. For $k = 1, \ldots, K$:
   - Train model on folds $\{1, \ldots, K\} \setminus \{k\}$
   - Predict on fold $k$, compute loss $L_k$
3. Average: $\text{CV} = \frac{1}{K} \sum_{k=1}^K L_k$

Common choices: $K=5$ (faster), $K=10$ (standard), $K=n$ (leave-one-out, expensive).

> [!tip]
> In causal ML, use cross-validation for hyperparameter tuning but never for causal parameter selection. Cross-fitting (sample splitting) is required for valid inference on causal effects when using flexible ML models.

## Minimal code snippets

```python
# Python: k-fold CV with sklearn
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100)
scores = cross_val_score(rf, X, y, cv=5, scoring='neg_mean_squared_error')
print(f"CV MSE: {-scores.mean():.3f} ± {scores.std():.3f}")
```

```r
# R: k-fold CV with caret
library(caret)
train_control <- trainControl(method = "cv", number = 10)
model <- train(y ~ ., data = df, method = "rf", trControl = train_control)
print(model$results)
```

## Related notes

- [[cross-fitting]]
- [[bootstrap]]
- [[Model Estimation (MOC)]]
- [[regularization]]
