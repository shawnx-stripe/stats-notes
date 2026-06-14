---
title: Arellano–Bond
aliases: [Arellano-Bond, Arellano–Bond estimator, AB estimator, difference GMM]
tags: [econometrics, panel-data, dynamic-panels, gmm]
updated: 2026-03-05
---

# Arellano–Bond

> [!summary]
> GMM estimator for dynamic panel data models. First-differences the equation to remove fixed effects, then uses lagged levels as instruments. Assumes no serial correlation in idiosyncratic errors beyond order 1.

## Model and instruments

For the dynamic panel model $y_{it} = \alpha y_{i,t-1} + x_{it}'\beta + \eta_i + \varepsilon_{it}$, Arellano–Bond first-differences:

$$\Delta y_{it} = \alpha \Delta y_{i,t-1} + \Delta x_{it}'\beta + \Delta \varepsilon_{it}$$

Instruments: $y_{i,t-2}, y_{i,t-3}, \ldots, y_{i1}$ (and similarly for $x$ if predetermined). Requires $\mathbb{E}[\varepsilon_{it}\varepsilon_{is}] = 0$ for $t \neq s$.

## Stata

```stata
xtabond y x1 x2, lags(1) vce(robust)
estat abond  // test for AR(2) in first-differenced residuals
```

> [!warning]
> Difference GMM performs poorly with persistent series (weak instruments). Use [[System GMM]] (Blundell–Bond) instead, which adds level equations with differenced instruments.

## Related notes

- [[Generalized Method of Moments (GMM)|GMM]]
- [[System GMM]]
- [[Panel Data Methods (MOC)]]
- [[Nickell bias]]
- [[two-way fixed effects]]
