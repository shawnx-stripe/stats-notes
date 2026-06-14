---
title: Rosenbaum Sensitivity
aliases:
  - Rosenbaum bounds
  - Rosenbaum sensitivity analysis
  - sensitivity to hidden bias
tags:
  - causal-inference
  - sensitivity
  - matching
  - observational-studies
  - diagnostics
updated: 2026-03-05
---

# Rosenbaum Sensitivity

> [!summary] Quick definition
> Rosenbaum sensitivity analysis asks how large an unmeasured confounder (hidden bias) would need to be to alter the conclusions of an observational study. The parameter $\Gamma$ bounds the odds ratio by which two units with the same observed covariates can differ in treatment probability. As $\Gamma$ increases from 1, the p-value bounds widen; the value of $\Gamma$ at which significance is lost indicates the fragility of the finding.

## Model

For matched pairs $(i, j)$ with the same $X$, the odds ratio of treatment assignment is bounded:

$$
\frac{1}{\Gamma} \leq \frac{P(D_i = 1 \mid X_i) / P(D_i = 0 \mid X_i)}{P(D_j = 1 \mid X_j) / P(D_j = 0 \mid X_j)} \leq \Gamma
$$

When $\Gamma = 1$, no hidden bias (randomization conditional on $X$). As $\Gamma > 1$, unmeasured confounding is allowed; the p-value bounds become wider.

## Interpretation

Report the critical $\Gamma^*$ at which the upper $p$-value bound exceeds 0.05. Example: "$\Gamma^* = 2.5$" means the result is robust to a confounder that doubles the odds of treatment. Larger $\Gamma^*$ indicates more robust findings.

## R snippet

```r
library(rbounds)
# Rosenbaum bounds for matched pairs (treatment effects)
psens(x = treated_outcomes, y = control_outcomes)
# Reports p-value bounds for a range of Gamma values
```

> [!tip]
> Use Rosenbaum sensitivity alongside covariate balance checks. If $\Gamma^* < 1.5$, the result is fragile to small unmeasured confounders.

## Related notes

- [[Unconfoundedness]]
- [[propensity score]]
- [[selection bias]]
- [[matching|Matching]]
