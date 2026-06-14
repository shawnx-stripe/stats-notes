---
title: LTMLE
aliases: [LTMLE, Longitudinal TMLE, longitudinal targeted learning]
tags: [causal-inference, longitudinal, tmle]
updated: 2026-03-05
---

# LTMLE

> [!summary]
> Longitudinal Targeted Minimum Loss-Based Estimation: extends [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] to time-varying treatments and confounders. Sequentially targets the estimand across time points using clever covariates; doubly robust and efficient.

## Sequential Targeting

For time-varying treatment $A_t$ and confounders $L_t$ ($t = 1, \ldots, T$):

1. **Initial estimation**: Fit outcome regression $\bar{Q}_T(L_T, A_T)$ and propensity scores $g_t(A_t | \bar{L}_t, \bar{A}_{t-1})$
2. **Sequential updating**: For $t = T, T-1, \ldots, 1$, update $\bar{Q}_t$ using clever covariate:
   $$
   H_t = \frac{\mathbb{1}(A_t = a_t)}{g_t(A_t | \bar{L}_t, \bar{A}_{t-1})}
   $$
3. **Marginal effect**: Integrate over treatment and confounder distributions forward in time

> [!check] Properties
> - **Doubly robust**: Consistent if either outcome model or propensity model is correct (at each time)
> - **Efficiency**: Achieves semiparametric efficiency bound under correct specification
> - **Time-varying confounding**: Naturally handles feedback between treatment and confounders

## Code

```r
# R: LTMLE package
library(ltmle)
result <- ltmle(data, Anodes = c("A1", "A2", "A3"),
                Lnodes = c("L1", "L2", "L3"),
                Ynodes = "Y", abar = c(1, 1, 1))
summary(result)
```

## Related notes

- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[Marginal Structural Models (MSM)]]
- [[Unconfoundedness]]
