---
title: Reflection Problem
aliases: [reflection problem, Manski reflection problem]
tags: [econometrics, interference, identification]
updated: 2026-03-05
---

# Reflection Problem

> [!summary]
> Identification problem (Manski 1993) in linear-in-means models of social interactions: group average outcomes reflect both endogenous social effects, exogenous contextual effects, and correlated effects. Without exclusion restrictions, these are not separately identified.

## The three effects

Linear-in-means model for unit $i$ in group $g$:

$$
Y_{ig} = \alpha + \beta \mathbb{E}[Y_{jg} \mid j \neq i] + \gamma \mathbb{E}[X_{jg} \mid j \neq i] + \delta X_{ig} + \varepsilon_{ig}
$$

- **Endogenous effect** ($\beta$): peer outcomes affect own outcome
- **Contextual (exogenous) effect** ($\gamma$): peer characteristics affect own outcome
- **Correlated effect**: common shocks or sorting (captured by group fixed effects)

## Why identification fails

Taking group means: $\bar{Y}_g = \alpha + \beta \bar{Y}_g + \gamma \bar{X}_g + \delta \bar{X}_g + \bar{\varepsilon}_g$, which implies $\bar{Y}_g = \frac{\alpha + (\gamma + \delta)\bar{X}_g + \bar{\varepsilon}_g}{1 - \beta}$. Observationally equivalent to any combination of $\beta, \gamma, \delta$ satisfying this reduced form. The "reflection": does peer behavior affect me, or do we simply share the same environment?

> [!tip] Solutions
> - Exclude some peer characteristics from own equation (use $Z_j$ that affect $Y_i$ only through $Y_j$)
> - Exploit network structure (friends-of-friends)
> - Randomize peer groups or group composition

## Related notes

- [[interference]]
- [[spillovers]]
- [[Spillovers and Interference (MOC)]]
