---
title: Selection on Gains
aliases: [selection on gains, Roy model selection]
tags: [causal-inference, treatment-effects, heterogeneity]
updated: 2026-03-05
---

# Selection on Gains

> [!summary]
> Pattern where units select into treatment based on their expected benefit (heterogeneous treatment effect). Creates sorting that differs from selection on levels. Central to the [[marginal treatment effect (MTE)]] framework and Roy model.

## Formal characterization

Selection on gains occurs when:

$$
\mathbb{E}[Y(1) - Y(0) \mid D = 1] > \mathbb{E}[Y(1) - Y(0) \mid D = 0]
$$

Those who take treatment benefit more than those who do not. Equivalently, $\text{Cov}(D, Y(1) - Y(0)) > 0$.

## Implications

- [[Average Treatment Effect on the Treated (ATT)|ATT]] $>$ [[Average Treatment Effect on the Untreated (ATU)|ATU]]
- [[Average Treatment Effect on the Treated (ATT)|ATT]] $>$ [[Average Treatment Effect (ATE)|ATE]] if selection is positive
- OLS estimates of treatment effects are biased upward under positive selection on gains
- Identifying ATE requires instruments or assumptions beyond [[unconfoundedness]]

> [!example] Roy model
> In occupational choice, high-skill workers select into skill-intensive jobs where their comparative advantage is greatest. Simple comparisons of wages across occupations overstate returns because they ignore selection on individual-specific gains.

## Related notes

- [[essential heterogeneity]]
- [[marginal treatment effect (MTE)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Treatment Effect Heterogeneity (MOC)]]
