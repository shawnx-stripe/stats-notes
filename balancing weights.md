---
title: Balancing Weights
aliases: [balancing weights, covariate balancing weights]
tags: [causal-inference, weighting, identification]
updated: 2026-03-05
---

# Balancing Weights

> [!summary]
> Weights that directly target covariate balance between treatment groups rather than modeling the propensity score. Includes [[entropy balancing]], [[CBPS]], and overlap/matching weights. Often more stable than IPW.

## Approaches

| Method | Key idea |
|--------|----------|
| [[Entropy balancing]] | Choose weights to exactly balance moments while minimizing entropy loss |
| [[CBPS]] | Estimate propensity score and balance constraints jointly via GMM |
| Overlap weights | Weight by $w_i = (1-e(X_i))$ for treated, $e(X_i)$ for controls; emphasizes common support |
| Matching weights | Binary weights from matching; balance is achieved by design |

## Why use balancing weights

- More robust to propensity score misspecification than [[Inverse Probability Weighting (IPW)|IPW]]
- Directly target balance diagnostics (e.g., standardized mean differences)
- Can enforce exact balance on selected covariates
- Often produce lower variance estimates than IPW

> [!tip]
> Check balance after weighting using standardized mean differences (SMD). Target: SMD < 0.1 for all covariates.

## Python snippet

```python
# Entropy balancing example
from causalinference import CausalModel
cm = CausalModel(Y, D, X)
cm.est_via_weighting()  # Uses entropy balancing by default
print(cm.estimates)
```

## R snippet

```r
library(WeightIt)
# Entropy balancing
w_eb <- weightit(D ~ X1 + X2 + X3, data = data, method = "ebal")
# Overlap weights
w_ow <- weightit(D ~ X1 + X2 + X3, data = data, method = "ps", estimand = "ATO")
```

## Related notes

- [[Inverse Probability Weighting (IPW)|IPW]]
- [[entropy balancing]]
- [[propensity score]]
- [[Identification Strategies (MOC)]]
