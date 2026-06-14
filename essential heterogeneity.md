---
title: Essential Heterogeneity
aliases: [essential heterogeneity, selection on gains]
tags: [causal-inference, treatment-effects, heterogeneity]
updated: 2026-03-05
---

# Essential Heterogeneity

> [!summary]
> Setting where individuals select into treatment based on their idiosyncratic treatment effect (gains from treatment). The [[marginal treatment effect (MTE)]] framework identifies the full distribution of effects under this pattern.

## Selection on gains

**Standard selection**: $D_i = 1$ if $\pi(X_i) + U_i > 0$, where $U_i \perp (Y_i(0), Y_i(1))$.

**Essential heterogeneity**: $D_i = 1$ depends on $(Y_i(1) - Y_i(0))$. Example:
$$
D_i = \mathbb{1}\{Y_i(1) - Y_i(0) - C_i > 0\}
$$
where $C_i$ is the cost of treatment.

In this case, [[Average Treatment Effect (ATE)|ATE]] $\neq$ [[Average Treatment Effect on the Treated (ATT)|ATT]], and neither equals the effect for marginal individuals (those induced by the instrument).

> [!note]
> The [[marginal treatment effect (MTE)]] framework uses instrumental variables to trace out $\operatorname{MTE}(x, u) = \mathbb{E}[Y_i(1) - Y_i(0) \mid X_i = x, U_i = u]$, recovering the full distribution of treatment effects and testing for essential heterogeneity.

## Key insight

Under essential heterogeneity, policy conclusions depend critically on which margin is moved. An IV estimate ([[Local Average Treatment Effect (LATE)|LATE]]) identifies the effect for compliers, not the population average or the effect on those most likely to benefit.

## Related notes

- [[marginal treatment effect (MTE)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[treatment effect heterogeneity]]
- [[Treatment Effect Heterogeneity (MOC)]]
