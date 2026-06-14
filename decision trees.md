---
title: Decision Trees
aliases: [decision trees, decision tree, classification tree, regression tree, CART]
tags: [machine-learning]
updated: 2026-03-05
---

# Decision Trees

> [!summary]
> Nonparametric method that recursively partitions feature space into regions and fits constant predictions within each. Foundation for ensemble methods like [[random forests]] and gradient boosting. Prone to overfitting when unpruned.

## Recursive partitioning algorithm

At each node, choose the split $(j, s)$ that minimizes:
$$
\sum_{i: x_i \in R_L} (y_i - \bar{y}_L)^2 + \sum_{i: x_i \in R_R} (y_i - \bar{y}_R)^2
$$
where $R_L = \{x \mid x_j \leq s\}$ and $R_R = \{x \mid x_j > s\}$.

Stop when:
- Node reaches minimum size
- Split does not improve fit beyond threshold
- Maximum depth is reached

**Prediction**: $\hat{y}(x) = \bar{y}_\ell$ where $\ell$ is the leaf containing $x$.

> [!warning]
> Single trees have high variance and overfit easily. Use ensemble methods (bagging, random forests, boosting) or regularization (minimum leaf size, pruning) for production use.

## Minimal code snippets

```python
# Python: fit and visualize a decision tree
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt

tree = DecisionTreeRegressor(max_depth=5, min_samples_leaf=10)
tree.fit(X_train, y_train)
plot_tree(tree, feature_names=X.columns, filled=True)
plt.show()
```

```r
# R: decision tree with rpart
library(rpart)
library(rpart.plot)
tree <- rpart(y ~ ., data = df, control = rpart.control(maxdepth = 5, minsplit = 20))
rpart.plot(tree)
```

## Related notes

- [[random forests]]
- [[causal forests]]
- [[ML for Econometrics (MOC)]]
