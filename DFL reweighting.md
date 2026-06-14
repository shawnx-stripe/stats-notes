---
title: DFL Reweighting
aliases: [DFL reweighting, DiNardo-Fortin-Lemieux, DFL decomposition]
tags: [econometrics, decomposition, weighting]
updated: 2026-03-05
---

# DFL Reweighting

> [!summary]
> DiNardo, Fortin & Lemieux (1996) reweighting method for decomposing distributional changes. Reweights one period's distribution to have the other period's covariate distribution, isolating composition vs. structure effects.

## Decomposition formula

To decompose changes in outcome distribution $F_t(y)$ between periods $t=0,1$:

$$F_1(y) - F_0(y) = \underbrace{[F_1(y \mid X) - F_0(y \mid X)]}_{\text{structure}} + \underbrace{[F_0(y \mid X=x_1) - F_0(y \mid X=x_0)]}_{\text{composition}}$$

Estimate composition effect using weights $\psi(X) = \frac{\Pr(t=1 \mid X)}{\Pr(t=0 \mid X)} \cdot \frac{\Pr(t=0)}{\Pr(t=1)}$ applied to period-0 observations.

## Stata

```stata
logit period x1 x2 x3
predict pscore
gen weight = pscore / (1 - pscore) * (1 - p) / p if period == 0
kdensity y [aw=weight] if period == 0, addplot(kdensity y if period == 1)
```

## Related notes

- [[composition]]
- [[Oaxaca–Blinder decomposition]]
- [[Inverse Probability Weighting (IPW)|IPW]]
