---
title: Mediation Analysis
aliases: [mediation analysis, mediation, causal mediation, natural direct and indirect effects]
tags: [causal-inference, identification]
updated: 2026-03-05
---

# Mediation Analysis

> [!summary]
> Decomposition of a total causal effect into direct and indirect (mediated) pathways. Requires strong identification assumptions (sequential ignorability). Defines natural direct/indirect effects (NDE/NIE) via nested counterfactuals.

## Decomposition formula

Total effect:
$$
\text{TE} = \mathbb{E}[Y(1) - Y(0)]
$$

**Natural indirect effect (NIE)**: Effect transmitted through mediator $M$:
$$
\text{NIE} = \mathbb{E}[Y(1, M(1)) - Y(1, M(0))]
$$

**Natural direct effect (NDE)**: Effect not through $M$:
$$
\text{NDE} = \mathbb{E}[Y(1, M(0)) - Y(0, M(0))]
$$

Then: $\text{TE} = \text{NDE} + \text{NIE}$ (under no interaction).

> [!warning]
> Identification requires **sequential ignorability**:
> 1. $(Y(d, m), M(d')) \perp\!\!\perp D \mid X$ (no confounding of $D \to M$ or $D \to Y$)
> 2. $Y(d, m) \perp\!\!\perp M \mid D, X$ (no confounding of $M \to Y$ given $D, X$)
>
> The second condition is strong: no unmeasured mediator-outcome confounders even after conditioning on treatment.

## Minimal code snippets

```r
# R: mediation analysis with mediation package
library(mediation)

# Fit mediator and outcome models
med_model <- lm(M ~ D + X, data = df)
out_model <- lm(Y ~ D + M + X, data = df)

# Estimate NIE and NDE
med_out <- mediate(med_model, out_model, treat = "D", mediator = "M", boot = TRUE, sims = 500)
summary(med_out)
```

```python
# Python: mediation with statsmodels (simplified)
from statsmodels.api import OLS, add_constant

# Total effect
te_model = OLS(df['Y'], add_constant(df[['D', 'X']])).fit()
te = te_model.params['D']

# Controlled direct effect (mediator held constant)
cde_model = OLS(df['Y'], add_constant(df[['D', 'M', 'X']])).fit()
cde = cde_model.params['D']

# Indirect effect (approximate)
nie_approx = te - cde
print(f"TE: {te:.3f}, CDE: {cde:.3f}, NIE (approx): {nie_approx:.3f}")
```

## Related notes

- [[causal DAGs]]
- [[bad controls]]
- [[potential outcomes]]
- [[Identification Strategies (MOC)]]
