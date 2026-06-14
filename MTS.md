---
title: MTS
aliases: [MTS, monotone treatment selection]
tags: [causal-inference, partial-identification]
updated: 2026-03-05
---

# MTS

> [!summary]
> Assumption that units selecting into treatment have weakly higher (or lower) potential outcomes. Combined with other assumptions (MTR, MIV) to tighten [[Manski bounds]].

## Assumption

For treatment indicator $D \in \{0, 1\}$:

$$
\mathbb{E}[Y(1) | D=1] \geq \mathbb{E}[Y(1) | D=0] \quad \text{and} \quad \mathbb{E}[Y(0) | D=1] \geq \mathbb{E}[Y(0) | D=0]
$$

**Interpretation**: Units who choose treatment have (weakly) higher potential outcomes under both treatment and control.

## Application

MTS captures positive selection: units select into treatment based on (unobserved) factors that increase outcomes. Combined with [[MTR]], provides informative bounds on [[Average Treatment Effect (ATE)]].

> [!example]
> College attendance: MTS posits that those who attend college have higher earnings potential even if they hadn't attended (e.g., due to ability, motivation, family support).

> [!tip]
> Reverse MTS (negative selection) applies when low-outcome units select into treatment (e.g., remedial education programs).

## Related notes

- [[Manski bounds]]
- [[MTR]]
- [[MIV]]
- [[selection bias]]
