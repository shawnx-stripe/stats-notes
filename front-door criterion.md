---
title: Front-Door Criterion
aliases: [front-door criterion, front door criterion, front-door adjustment]
tags: [causal-inference, identification, graphical-models]
updated: 2026-03-05
---

# Front-Door Criterion

> [!summary]
> Identification strategy (Pearl) using a mediator $M$ that fully mediates the effect of $X$ on $Y$ and is unconfounded given $X$. Allows identification even when $X \to Y$ has unmeasured confounders, by combining two unconfounded relationships.

## Identification formula

Let $X \to M \to Y$ with unmeasured $U$ confounding $X \gets U \to Y$ but not affecting $M$.

**Front-door criterion** requires:
1. $M$ blocks all directed paths from $X$ to $Y$
2. No unblocked back-door path from $X$ to $M$
3. $X$ blocks all back-door paths from $M$ to $Y$

**Causal effect**:
$$
P(Y = y \mid \operatorname{do}(X = x)) = \sum_m P(M = m \mid X = x) \sum_{x'} P(Y = y \mid M = m, X = x') P(X = x')
$$

> [!example]
> Classic example: effect of smoking ($X$) on lung cancer ($Y$) with unmeasured genetic factor $U$. If tar in lungs ($M$) fully mediates and is only caused by smoking, front-door applies.

> [!warning]
> Front-door is rarely applicable in practice because:
> - Hard to find a mediator that captures 100% of the effect
> - Mediator may have its own unmeasured confounders
> - More restrictive than the [[back-door criterion]] when it holds

## Related notes

- [[causal DAGs]]
- [[back-door criterion]]
- [[Identification Strategies (MOC)]]
- [[collider bias]]
