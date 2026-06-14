---
title: Quantile Treatment Effects
aliases: [quantile treatment effects, QTE, distributional treatment effects]
tags: [causal-inference, treatment-effects, heterogeneity]
updated: 2026-03-05
---

# Quantile Treatment Effects

> [!summary]
> Treatment effects defined at specific quantiles of the outcome distribution rather than the mean. Reveals how treatment shifts different parts of the distribution. Identified under rank invariance or via unconditional quantile methods.

## Two main types

**Conditional QTE**: Effect on the $\tau$-quantile of $Y \mid X$

$$
\text{QTE}(\tau \mid X) = Q_{Y(1) \mid X}(\tau) - Q_{Y(0) \mid X}(\tau)
$$

Estimated via [[quantile regression]].

**Unconditional QTE**: Effect on the marginal $\tau$-quantile of $Y$

$$
\text{QTE}(\tau) = Q_{Y(1)}(\tau) - Q_{Y(0)}(\tau)
$$

Requires rank-invariance or distributional assumptions.

> [!check] Key distinction
> Conditional QTE describes how treatment affects quantiles *within covariate strata*. Unconditional QTE describes the effect on the *population quantile*. They differ when treatment effects are heterogeneous across $X$.

## Minimal code

```python
from causalml.inference.meta import BaseRRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Unconditional QTE via RLearner with quantile loss
qte_learner = BaseRRegressor(GradientBoostingRegressor(loss='quantile', alpha=0.5))
qte = qte_learner.estimate_ate(X, treatment, Y)
```

## Related notes

- [[treatment effect heterogeneity]]
- [[quantile regression]]
- [[Average Treatment Effect (ATE)]]
- [[Treatment Effect Heterogeneity (MOC)]]
