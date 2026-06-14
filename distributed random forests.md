---
title: Distributed Random Forests
aliases: [distributed random forests, distributed RF]
tags: [machine-learning]
updated: 2026-03-05
---

# Distributed Random Forests

> [!summary]
> Variants of [[random forests]] designed for distributed computing environments, partitioning data or trees across nodes for scalability to large datasets.

## Key approaches

| Method | Strategy | Trade-off |
|--------|----------|-----------|
| **Data-parallel** | Each node trains on a data partition; aggregate predictions | Communication overhead for splits |
| **Tree-parallel** | Each node grows a subset of trees independently | Requires data replication or streaming |
| **Vertical partitioning** | Features split across nodes (feature-parallel) | High communication for large feature sets |

Popular implementations: Spark MLlib (data-parallel), H2O (distributed in-memory), XGBoost distributed mode.

> [!tip]
> For large-scale causal inference (e.g., [[causal forests]] on billions of observations), tree-parallel strategies work well because trees are independent once bootstrap samples are drawn.

## Minimal code snippets

```python
# Python: distributed RF with PySpark
from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(numTrees=100, maxDepth=10)
model = rf.fit(train_df)
predictions = model.transform(test_df)
```

```r
# R: parallel RF with ranger (shared memory)
library(ranger)
rf <- ranger(y ~ ., data = df, num.trees = 500, num.threads = 8)
print(rf)
```

## Related notes

- [[random forests]]
- [[ML for Econometrics (MOC)]]
