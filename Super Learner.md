---
title: Super Learner
aliases: [Super Learner, super learner, SuperLearner, stacked generalization]
tags: [machine-learning, causal-inference, estimation, ensemble]
updated: 2026-03-05
---

# Super Learner

> [!summary]
> Ensemble method that uses cross-validation to optimally combine predictions from a library of candidate learners. Achieves oracle-optimal risk. Commonly used as the nuisance estimator in [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] and [[Augmented Inverse Probability Weighting (AIPW)|AIPW]].

## Algorithm

1. Split data into $K$ folds
2. For each learner $\ell$ in the library (e.g., logistic regression, random forest, XGBoost):
   - Train on $K-1$ folds, predict on the held-out fold
   - Repeat for all folds to obtain cross-validated predictions $\hat{f}_\ell^{\text{CV}}$
3. Find optimal weights $\alpha_\ell \geq 0$, $\sum_\ell \alpha_\ell = 1$, by minimizing cross-validated risk:
   $$\hat{\alpha} = \arg\min_{\alpha} \sum_i L\left(Y_i, \sum_\ell \alpha_\ell \hat{f}_\ell^{\text{CV}}(X_i)\right)$$
4. Final predictor: $\hat{f}(X) = \sum_\ell \hat{\alpha}_\ell \hat{f}_\ell(X)$

## When to use

- Nuisance function estimation in [[double machine learning]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- Unknown functional form; want to hedge across multiple models
- Goal is prediction, not interpretation

> [!tip]
> Include a diverse library: parametric (GLM), tree-based (RF, XGBoost), and regularized (lasso, ridge). Super Learner will downweight poor performers.

## Python snippet

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict
import numpy as np

# Cross-validated predictions from library
library = [RandomForestRegressor(), GradientBoostingRegressor(), Ridge()]
cv_preds = np.column_stack([cross_val_predict(learner, X, y, cv=5) for learner in library])

# Optimize weights (non-negative least squares)
from scipy.optimize import nnls
alpha, _ = nnls(cv_preds, y)
alpha /= alpha.sum()
```

## Related notes

- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[cross-fitting]]
- [[double machine learning]]
- [[ML for Econometrics (MOC)]]
