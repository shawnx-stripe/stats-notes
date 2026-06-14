---
title: Regression Kink Design (RKD)
aliases: [Regression Kink Design, RKD, regression kink design, kink design, fuzzy kink design]
tags: [econometrics, rdd, identification]
updated: 2026-03-05
---

# Regression Kink Design (RKD)

> [!summary]
> Variant of RDD where the treatment intensity (not level) changes at a kink point. Identifies the treatment effect from the ratio of kinks in the outcome and treatment regressions at the threshold.

## Identification

At the kink point $c$, the treatment dose $D(x)$ is continuous but its slope changes:

$$
\lim_{x \downarrow c} \frac{dD}{dx} \neq \lim_{x \uparrow c} \frac{dD}{dx}
$$

The causal effect is:

$$
\tau = \frac{\lim_{x \downarrow c} \frac{dY}{dx} - \lim_{x \uparrow c} \frac{dY}{dx}}{\lim_{x \downarrow c} \frac{dD}{dx} - \lim_{x \uparrow c} \frac{dD}{dx}}
$$

Identifies the marginal treatment effect for units at the kink.

## When to use

- Tax schedules with changing marginal rates
- Unemployment benefits with kinks in replacement rates
- Any policy where the rate of change (not level) of treatment shifts discontinuously

> [!warning]
> RKD requires smooth density of the running variable at $c$ and no kinks in other determinants of $Y$. Weaker design than sharp RDD (level jump); requires larger samples.

## R snippet

```r
library(rdrobust)
# Estimate kink using derivative-based local polynomial
rdrobust(y, x, c = kink_point, deriv = 1)  # deriv=1 for slope
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy RDD]]
- [[running variable]]
