---
title: Propensity Score Matching (PSM)
aliases: [Propensity Score Matching (PSM), PSM, propensity score matching]
tags: [causal-inference, matching, weighting]
updated: 2026-03-05
---

# Propensity Score Matching (PSM)

> [!summary]
> Matching method that pairs treated and control units with similar estimated propensity scores. Reduces dimensionality of the matching problem from $X$ to a scalar. Requires [[Unconfoundedness]] and [[Overlap]].

## Procedure

1. Estimate propensity score $\hat{e}(X_i) = \hat{P}(D_i = 1 \mid X_i)$ via logistic regression
2. Match each treated unit to one or more control units with similar $\hat{e}(X_i)$
3. Compute treatment effect as the average difference in outcomes among matched pairs

Common matching algorithms: nearest neighbor, caliper matching, kernel matching.

## Estimand

$$
\hat{\tau}_{\text{ATT}} = \frac{1}{N_1}\sum_{i:D_i=1}\left(Y_i - \sum_{j:D_j=0}w_{ij}Y_j\right)
$$

where $w_{ij}$ are matching weights (e.g., $w_{ij} = 1$ for nearest neighbor, $w_{ij} \propto K(\hat{e}(X_i) - \hat{e}(X_j))$ for kernel).

## Python snippet

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

# Estimate propensity scores
ps_model = LogisticRegression().fit(X, D)
ps = ps_model.predict_proba(X)[:, 1]

# Nearest neighbor matching (1:1)
nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
nn.fit(ps[D == 0].reshape(-1, 1))
distances, indices = nn.kneighbors(ps[D == 1].reshape(-1, 1))

# ATT = mean(Y_treated - Y_matched_control)
```

> [!tip]
> Always check covariate balance after matching. If balance is poor, IPW or more flexible matching methods may be better.

## Related notes

- [[propensity score]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Unconfoundedness]]
- [[Overlap]]
