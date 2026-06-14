---
title: MIV
aliases: [MIV, monotone instrumental variable, monotone instrument]
tags: [causal-inference, partial-identification, iv]
updated: 2026-03-05
---

# MIV

> [!summary]
> Monotone Instrumental Variable assumption: imposes a monotone relationship between the instrument and the outcome's potential values. Used in [[Manski bounds]] to tighten partial-identification bounds.

## Assumption

Let $Y(d, z)$ denote the potential outcome under treatment $d$ and instrument value $z$. MIV assumes:

$$
Y(d, z) \leq Y(d, z') \quad \text{for all } z < z'
$$

(or the reverse inequality). This means higher instrument values weakly increase potential outcomes.

## Application

Combined with [[monotonicity]] (instrument affects treatment monotonically), MIV allows sharper bounds on treatment effects without exclusion restrictions. Particularly useful when the [[exclusion restriction]] is doubtful but monotone relationships are plausible.

> [!example]
> Distance to college as IV for college attendance: MIV posits that potential earnings are (weakly) higher for those living closer to college, even if they don't attend.

## Related notes

- [[Manski bounds]]
- [[monotonicity]]
- [[Instrumental Variables (IV)]]
- [[Identification Strategies (MOC)]]
