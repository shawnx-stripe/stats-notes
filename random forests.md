---
title: Random forest
aliases:
  - Random forests
  - RF
  - Random forest classifier
  - Random forest regressor
  - Breiman random forest
tags:
  - machine-learning
  - statistics
  - ensemble-methods
  - prediction
  - nonparametric
updated: 2025-09-26
---

# Random forest

> [!summary] Quick definition
> An ensemble learning method that constructs many [[decision trees]] during training, each fitted on a [[bootstrap]] sample of the data with random feature selection at each split. Predictions are made by averaging (regression) or majority voting (classification) across all trees.

## Core algorithm

### Training procedure
1. Draw B bootstrap samples from training data (n observations with replacement)
2. For each bootstrap sample b = 1,...,B:
   - Grow a tree Tb by recursively splitting nodes
   - At each node, randomly select m features from p total features
   - Choose best split among these m features (not all p)
   - Grow tree deep (low bias, high variance)
   - No pruning
3. Output ensemble of trees {T₁, T₂, ..., TB}

### Prediction
- **Regression**: 
$$
\hat{f}(x) = \frac{1}{B} \sum_{b=1}^B T_b(x)
$$
- **Classification** (majority vote):
$$
\hat{C}(x) = \text{mode}\{T_1(x), T_2(x), \ldots, T_B(x)\}
$$
- **Class probabilities**:
$$
\hat{p}_k(x) = \frac{1}{B} \sum_{b=1}^B \mathbf{1}\{T_b(x) = k\}
$$

## Key hyperparameters

| Parameter | Symbol | Typical values | Effect |
|-----------|--------|---------------|--------|
| Number of trees | B | 100-1000 | More trees → better performance, more computation |
| Features per split | m | √p (classification), p/3 (regression) | Lower m → more diversity, less correlation |
| Min samples split | - | 2-10 | Higher → simpler trees, less overfitting |
| Max depth | - | None or 10-50 | Lower → simpler trees, potential underfitting |
| Min samples leaf | - | 1-5 | Higher → smoother predictions |
| Bootstrap | - | True/False | False → each tree sees all data |

### Feature sampling rules of thumb
- **Classification**: m ≈ √p
- **Regression**: m ≈ p/3
- **High correlation**: use smaller m
- **Few features**: m closer to p

## Why it works

### Variance reduction through averaging
For B independent trees with variance σ²:
$$
\text{Var}\left(\frac{1}{B}\sum_{b=1}^B T_b\right) = \frac{\sigma^2}{B}
$$

With correlation ρ between trees:
$$
\text{Var}\left(\frac{1}{B}\sum_{b=1}^B T_b\right) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2
$$

As B → ∞, variance → ρσ². Random feature selection reduces ρ.

### Bias-variance tradeoff
- Individual trees: low bias (deep), high variance
- Ensemble: maintains low bias, reduces variance
- [[bagging|Bagging]] alone: reduces variance
- Random feature selection: further decorrelates trees

## Out-of-bag (OOB) error

Each tree is trained on ~63.2% of data (bootstrap property). Use remaining ~36.8% for validation:

$$
\widehat{\text{OOB}} = \frac{1}{n} \sum_{i=1}^n L\left(y_i, \hat{f}^{(-i)}(x_i)\right)
$$

where $\hat{f}^{(-i)}$ averages only trees not trained on observation i.

> [!tip] OOB advantages
> - Free cross-validation (no separate validation set needed)
> - Unbiased estimate of test error
> - Can track during training for early stopping
> - Provides confidence intervals for predictions

## Variable importance measures

### 1. Permutation importance (preferred)
For variable j:
1. Randomly permute values of variable j in OOB samples
2. Compute increase in OOB error
3. Average across all trees

$$
\text{VI}_j = \frac{1}{B} \sum_{b=1}^B \left(\text{err}_{b,\text{perm}(j)} - \text{err}_{b,\text{OOB}}\right)
$$

### 2. Gini importance (classification)
Sum of Gini decreases from splits on variable j:
$$
\text{VI}_j^{\text{Gini}} = \sum_{\text{nodes splitting on } j} n_{\text{node}} \cdot \Delta\text{Gini}
$$

### 3. Mean decrease in MSE (regression)
Similar to Gini but using MSE reduction.

> [!warning] Importance caveats
> - Biased toward high-cardinality features
> - Correlated features share importance
> - Scale-dependent for Gini/MSE methods
> - Use permutation importance for inference

## Advantages and disadvantages

### Advantages
- Excellent out-of-the-box performance
- Handles mixed data types naturally
- Robust to outliers and noise
- No scaling/normalization needed
- Captures non-linear relationships and interactions
- Parallel training possible
- Built-in feature importance
- OOB error estimation

### Disadvantages
- Black box model (limited interpretability)
- Large memory footprint (stores all trees)
- Slower prediction than single tree
- Can overfit with small n, large p
- Biased toward categorical variables with many levels
- Extrapolation issues (predicts within training range)

## Extensions and variants

### Extremely randomized trees (Extra-Trees)
- Random splits instead of optimal splits
- No bootstrap (use full dataset)
- Even more randomness → lower variance

### Quantile regression forests
For prediction intervals and conditional quantiles:
$$
\hat{F}(y \mid x) = \frac{1}{B} \sum_{b=1}^B \sum_{i: x_i \in \text{leaf}(x,T_b)} \frac{w_i(x)}{n_{\text{leaf}}}
$$

### [[causal forests|Causal forests]]
For heterogeneous treatment effects:
- Modified splitting criterion (maximize treatment effect heterogeneity)
- Honest trees (separate samples for splitting and estimation)
- Local centering for bias reduction

### Survival forests
For time-to-event data with censoring:
- Split using log-rank test or C-index
- Predict survival function or cumulative hazard

## Practical implementation tips

> [!check] Best practices checklist
> - [ ] Set random seed for reproducibility
> - [ ] Start with default hyperparameters
> - [ ] Use OOB score for model selection
> - [ ] Check variable importance stability
> - [ ] Increase B until OOB stabilizes
> - [ ] For small n: reduce tree complexity
> - [ ] For large p: consider feature selection first
> - [ ] Monitor training time vs performance tradeoff

### Hyperparameter tuning strategy
1. Fix B = 500 (reasonable default)
2. Tune m (most important)
3. Tune tree complexity (max_depth, min_samples)
4. Increase B if needed for stability
5. Use [[cross-validation]] or OOB for selection

### Computational considerations
- Time complexity: O(B × n × m × log n)
- Space complexity: O(B × n)
- Parallelizable across trees (embarrassingly parallel)
- For big data: use subsampling or [[distributed random forests]]

## Common pitfalls

> [!warning] What to avoid
> - Using too few trees (B < 100)
> - Ignoring class imbalance (use class_weight or balanced sampling)
> - Over-interpreting variable importance rankings
> - Using for extrapolation beyond training range
> - Not checking OOB error convergence
> - Default m with very high/low p

## Comparison with other methods

| Method | Random Forest | [[gradient boosting|Gradient boosting]] | Single [[decision trees|decision tree]] | Neural network |
|--------|--------------|---------------------|------------------------|-------------------|
| Bias | Low | Very low | Low-Medium | Very low |
| Variance | Low | Low | High | Low |
| Interpretability | Low | Low | High | Very low |
| Training speed | Fast | Slow | Very fast | Slow |
| Tuning needed | Little | Much | Some | Much |
| Handles interactions | Yes | Yes | Yes | Yes |
| Parallel training | Yes | No | No | Partially |

## Copy-ready formulas

- Ensemble prediction (regression):
$$
\hat{f}(x) = \frac{1}{B} \sum_{b=1}^B T_b(x)
$$

- Variance with correlation:
$$
\text{Var}(\hat{f}) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2
$$

- OOB error:
$$
\widehat{\text{OOB}} = \frac{1}{n} \sum_{i=1}^n L\left(y_i, \hat{f}^{(-i)}(x_i)\right)
$$

- Variable importance (permutation):
$$
\text{VI}_j = \mathbb{E}[\text{err}_{\text{perm}(j)} - \text{err}_{\text{original}}]
$$

## Minimal code snippets

```python
# Python: scikit-learn implementation
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Regression
rf_reg = RandomForestRegressor(
    n_estimators=500,
    max_features='sqrt',  # or 'auto', int, float
    oob_score=True,
    random_state=42,
    n_jobs=-1  # parallel
)
rf_reg.fit(X_train, y_train)
print(f"OOB R²: {rf_reg.oob_score_:.3f}")

# Feature importance (permutation preferred; see variable importance section)
importances = rf_reg.feature_importances_
for i in np.argsort(importances)[::-1][:5]:
    print(f"{feature_names[i]}: {importances[i]:.3f}")
```

```r
# R: randomForest and ranger implementations
library(randomForest)
library(ranger)

# randomForest (original Breiman/Cutler)
rf_model <- randomForest(
  y ~ ., 
  data = train_data,
  ntree = 500,
  mtry = sqrt(ncol(train_data) - 1),
  importance = TRUE,
  proximity = FALSE  # save memory
)
print(rf_model)
varImpPlot(rf_model)

# ranger (faster, modern implementation)
rf_ranger <- ranger(
  y ~ ., 
  data = train_data,
  num.trees = 500,
  importance = 'permutation',
  oob.error = TRUE,
  num.threads = parallel::detectCores() - 1
)

```

---

## Related notes
- [[decision trees]]
- [[bootstrap]]
- [[bagging]]
- [[ensemble methods]]
- [[gradient boosting]]
- extremely randomized trees
- quantile regression forests
- [[causal forests]]
- survival forests
- [[distributed random forests]]
- [[cross-validation]]
- [[variable importance]]
- [[bias-variance tradeoff]]