---
title: sequential unconfoundedness
aliases: [sequential ignorability, sequential exchangeability]
tags: [causal-inference, longitudinal, assumptions]
updated: 2026-06-16
---

# sequential unconfoundedness

> [!summary] Quick definition
> Sequential unconfoundedness requires each time-varying treatment to be as-if randomized conditional on observed treatment and covariate history.

## When it matters

It identifies longitudinal causal effects with time-varying confounders affected by prior treatment. Use g-methods, IPW, or marginal structural models rather than conditioning naively on post-treatment covariates.

## Related notes

- [[Unconfoundedness]]
- [[Marginal Structural Models (MSM)]]
- [[g-formula]]
