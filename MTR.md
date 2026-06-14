---
title: MTR
aliases: [MTR, monotone treatment response]
tags: [causal-inference, partial-identification]
updated: 2026-03-05
---

# MTR

> [!summary]
> Assumption that potential outcomes are monotone in treatment level (e.g., more treatment never hurts). Combined with other shape restrictions to tighten [[Manski bounds]].

## Assumption

For treatment levels $d < d'$:

$$
Y(d) \leq Y(d') \quad \text{for all units}
$$

(or the reverse inequality). **Interpretation**: More intensive treatment weakly improves outcomes.

## Application

MTR tightens [[Manski bounds]] on average treatment effects. Combined with [[MTS]] (monotone treatment selection) or [[MIV]] (monotone instrumental variable), can produce informative bounds without point identification.

> [!example]
> Job training hours: MTR assumes more training hours never reduce earnings. Even without identifying individual treatment effects, this yields bounds on the average effect of training.

> [!warning]
> - Strong assumption: rules out any harmful effects at the unit level
> - Plausibility depends on context; often reasonable for "dose" of beneficial treatment

## Related notes

- [[Manski bounds]]
- [[MIV]]
- [[MTS]]
- [[Identification Strategies (MOC)]]
