---
title: Sequential Ignorability
aliases: [sequential ignorability, sequential exchangeability]
tags: [causal-inference, longitudinal, assumptions]
updated: 2026-03-05
---

# Sequential Ignorability

> [!summary]
> Assumption that treatment assignment at each time point is independent of future potential outcomes conditional on observed history. Required for identifying causal effects of time-varying treatments. Extends static [[ignorability]] to longitudinal settings.

## Formal statement

For time-varying treatment $D_t$ and history $\bar{D}_{t-1}, \bar{X}_t$:

$$
Y(\bar{d}_T) \perp D_t \mid \bar{D}_{t-1} = \bar{d}_{t-1}, \bar{X}_t = \bar{x}_t
$$

for all $t$ and treatment sequences $\bar{d}_t$. No unmeasured time-varying confounding at any stage.

## Why it's strong

Sequential ignorability requires:
- Measuring all confounders at every time point
- No unmeasured mediator-outcome confounding
- Correct model of time-varying confounding

Violations are common when unobserved health states affect both treatment initiation and outcomes.

> [!tip] Estimation methods under sequential ignorability
> - [[Marginal Structural Models (MSM)]] with inverse probability of treatment weighting
> - [[LTMLE]] (longitudinal targeted maximum likelihood)
> - G-computation (parametric g-formula)
> - Sequential g-estimation

## Related notes

- [[ignorability]]
- [[LTMLE]]
- [[Marginal Structural Models (MSM)]]
- [[Unconfoundedness]]
