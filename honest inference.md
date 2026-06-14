---
title: Honest Inference
aliases: [honest inference, honest confidence intervals]
tags: [machine-learning, causal-inference, inference]
updated: 2026-03-05
---

# Honest Inference

> [!summary]
> Inferential framework guaranteeing valid coverage uniformly over a class of data-generating processes, even when the same data are used for model selection and inference. Key principle in [[causal forests]] and adaptive estimation.

## Sample splitting for honesty

**Naive approach**: Use the same data to grow trees and estimate leaf means. Results in over-optimistic confidence intervals.

**Honest approach**: Split each tree's sample into:
1. **Training sample** ($S_{\text{train}}$): Choose splits
2. **Estimation sample** ($S_{\text{est}}$): Estimate leaf means

Confidence intervals based on $S_{\text{est}}$ alone have correct coverage uniformly over the parameter space.

> [!check]
> In [[causal forests]], honesty is implemented by default: each tree uses half the subsample to build the tree structure and the other half to estimate treatment effects within leaves.

## Key insight

Honest inference trades off bias and variance differently than standard ML. By separating model selection from estimation, it ensures valid inference at the cost of reduced sample size for estimation. This is critical when the goal is not just prediction but inference (e.g., confidence intervals, hypothesis tests).

## Minimal code snippets

```r
# R: honest causal forest with grf
library(grf)
cf <- causal_forest(X, Y, W, honesty = TRUE, honesty.fraction = 0.5)
tau_hat <- predict(cf, estimate.variance = TRUE)
ci <- data.frame(tau = tau_hat$predictions,
                 se = sqrt(tau_hat$variance.estimates))
ci$lower <- ci$tau - 1.96 * ci$se
ci$upper <- ci$tau + 1.96 * ci$se
```

## Related notes

- [[causal forests]]
- [[treatment effect heterogeneity]]
- [[Machine Learning for Causal Inference (MOC)]]
