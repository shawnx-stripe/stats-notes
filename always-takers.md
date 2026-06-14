---
title: always-takers
aliases:
  - Always-takers
  - always takers
tags:
  - causal-inference
  - iv
  - compliance
  - noncompliance
updated: 2026-03-05
---

# always-takers

> [!summary]
> Always-takers are units that receive treatment regardless of their instrument/assignment value ($D_i(1) = D_i(0) = 1$). Under the [[monotonicity]] assumption in the [[Instrumental Variables (IV)|IV]]/[[Local Average Treatment Effect (LATE)|LATE]] framework, the population is partitioned into always-takers, [[never-takers]], and [[compliers]]. Always-takers contribute no identifying variation; [[Local Average Treatment Effect (LATE)|LATE]] is identified from [[compliers]] alone.

## Formal Definition

Let $D_i(z)$ denote the **potential treatment** unit $i$ would receive if assigned instrument value $z$. A unit is an **always-taker** if:

$$
D_i(1) = 1 \quad \text{and} \quad D_i(0) = 1
$$

**Interpretation**: Always-takers receive treatment regardless of whether the instrument encourages treatment ($z=1$) or not ($z=0$). Their treatment status is unaffected by the instrument.

## Role in the LATE Framework

In the presence of [[noncompliance]], the population is partitioned into four **principal strata**:

| Stratum | $D_i(0)$ | $D_i(1)$ | Observed $D$ when $Z=0$ | Observed $D$ when $Z=1$ |
|---------|----------|----------|-------------------------|-------------------------|
| [[compliers|Compliers]] | 0 | 1 | 0 | 1 |
| [[never-takers|Never-takers]] | 0 | 0 | 0 | 0 |
| **Always-takers** | 1 | 1 | 1 | 1 |
| [[defiers|Defiers]] | 1 | 0 | 1 | 0 |

Always-takers are observed to have $D_i=1$ regardless of $Z_i$. Because their treatment does not vary with the instrument, they **do not contribute** to identification of the treatment effect.

> [!note]
> We cannot directly observe who is an always-taker. Principal strata are defined by counterfactuals $(D_i(0), D_i(1))$, but we only observe one potential treatment per unit.

## Why Always-Takers Don't Identify Effects

The [[Local Average Treatment Effect (LATE)|LATE]] is identified from variation in $D$ induced by $Z$:

$$
\text{LATE} = \frac{E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]}{E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]}
$$

For always-takers:
- When $Z=0$: $D=1$, so $Y = Y_i(1)$
- When $Z=1$: $D=1$, so $Y = Y_i(1)$

There is **no variation** in treatment status for always-takers across $Z$. Hence, we cannot learn about their treatment effect $Y_i(1) - Y_i(0)$ from the IV design.

> [!warning]
> The IV estimand identifies the effect **only among [[compliers]]**—those whose treatment status changes with $Z$. We cannot identify the ATE for always-takers from the instrument alone.

## Estimating the Proportion of Always-Takers

Under [[monotonicity]] (no [[defiers]]), the share of always-takers is:

$$
\pi_a = P(D_i(1)=1, D_i(0)=1) = E[D_i \mid Z_i=0]
$$

**Intuition**: Among units with $Z=0$, only always-takers have $D=1$ (compliers and never-takers have $D=0$).

In an [[randomized controlled trial (RCT)|RCT]] with encouragement design:
- $\pi_a$ = treatment take-up rate in the control group
- $\pi_c$ = difference in take-up rates between treatment and control groups

> [!example]
> If 40% of the control group enrolls in a job training program ($Z=0$, $D=1$), then $\pi_a = 0.40$. These are always-takers who enroll regardless of encouragement.

## Implications for External Validity

Because always-takers self-select into treatment, they likely differ from [[compliers]] and [[never-takers]]:
- **Selection**: Always-takers may have higher baseline motivation, ability, or need
- **Treatment effects**: $E[Y_i(1) - Y_i(0) \mid \text{always-taker}]$ may differ from $E[Y_i(1) - Y_i(0) \mid \text{complier}]$

> [!warning]
> LATE does not generalize to always-takers. If a policy change converts always-takers to never-takers (e.g., by removing treatment), the effect on them is unknown.

## Relation to Intent-to-Treat (ITT)

The ITT effect averages over all principal strata:

$$
\text{ITT} = E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]
$$

Decomposing by strata:

$$
\text{ITT} = \pi_c \cdot E[Y_i(1) - Y_i(0) \mid \text{complier}] + \pi_a \cdot 0 + \pi_n \cdot 0
$$

(Under [[exclusion restriction]], $Z$ affects $Y$ only through $D$, so the instrument has no effect on always-takers' or never-takers' outcomes.)

Thus:

$$
\text{LATE} = \frac{\text{ITT}}{\pi_c}
$$

Always-takers "dilute" the ITT but do not bias the LATE estimate.

## Testing for Always-Takers

In a randomized encouragement design:
1. Estimate $\pi_a = P(D=1 \mid Z=0)$
2. If $\pi_a = 0$, there are no always-takers (one-sided noncompliance)
3. If $\pi_a > 0$, both always-takers and compliers are present (two-sided noncompliance)

> [!check] One-sided vs. two-sided noncompliance
> - **One-sided**: Only control group non-compliers (always-takers). Treated group fully complies.
> - **Two-sided**: Noncompliance in both groups (always-takers and never-takers).

## Bounds on Treatment Effects for Always-Takers

Without additional assumptions, the treatment effect for always-takers is **not identified**. However, under further assumptions (e.g., [[monotone treatment response]]), we can derive bounds:

$$
E[Y_i(0) \mid \text{always-taker}] \leq E[Y_i \mid Z=0, D=1]
$$

This provides a **lower bound** on $Y_i(0)$ for always-takers under the assumption that treatment weakly increases outcomes for everyone.

> [!note]
> Bounding approaches (e.g., Manski bounds, monotone treatment response) can partially identify effects for always-takers, but these require strong untestable assumptions.

## Relation to Monotonicity

[[Monotonicity]] assumes $D_i(1) \geq D_i(0)$ for all $i$, ruling out [[defiers]]. This allows us to partition the population into compliers, never-takers, and always-takers.

Without monotonicity:
- We cannot separately identify $\pi_a$ and $\pi_d$ (the share of defiers)
- The Wald estimand confounds complier and defier effects

> [!check]
> Monotonicity is untestable but often plausible (e.g., encouragement designs, eligibility thresholds).

## Minimal Code Snippets

### R: Estimating proportion of always-takers

```r
library(AER)

# Randomized encouragement: Z is the instrument
# Estimate proportion of always-takers (treatment take-up in control group)
pi_a <- mean(df$D[df$Z == 0])
print(paste("Proportion always-takers:", pi_a))

# Proportion of compliers (first-stage coefficient)
first_stage <- lm(D ~ Z, data = df)
pi_c <- coef(first_stage)["Z"]
print(paste("Proportion compliers:", pi_c))

# Proportion of never-takers (1 - pi_a - pi_c under monotonicity)
pi_n <- 1 - pi_a - pi_c
print(paste("Proportion never-takers:", pi_n))
```

### Python: Estimating principal strata proportions

```python
import pandas as pd
import numpy as np

# Proportion always-takers
pi_a = df.loc[df['Z'] == 0, 'D'].mean()
print(f"Proportion always-takers: {pi_a:.3f}")

# Proportion compliers (first stage)
from statsmodels.api import OLS
first_stage = OLS(df['D'], df[['const', 'Z']]).fit()
pi_c = first_stage.params['Z']
print(f"Proportion compliers: {pi_c:.3f}")

# Proportion never-takers
pi_n = 1 - pi_a - pi_c
print(f"Proportion never-takers: {pi_n:.3f}")
```

### Stata: Principal strata proportions

```stata
* Proportion of always-takers
summ D if Z == 0
scalar pi_a = r(mean)
display "Proportion always-takers: " pi_a

* First stage (proportion compliers)
reg D Z
scalar pi_c = _b[Z]
display "Proportion compliers: " pi_c

* Proportion never-takers
scalar pi_n = 1 - pi_a - pi_c
display "Proportion never-takers: " pi_n
```

## Sensitivity to Always-Taker Assumptions

When interpreting LATE, consider:
1. **How large is $\pi_a$?** A large share of always-takers limits the external validity of LATE.
2. **Are always-takers systematically different?** Compare pre-treatment covariates of $D=1, Z=0$ units (always-takers) to the full sample.
3. **Would policy affect always-takers?** If a policy mandates treatment, always-takers are unaffected; LATE applies only to compliers.

> [!tip]
> Report $\pi_a$, $\pi_c$, and $\pi_n$ in your results. This helps readers assess the generalizability of your LATE estimate.

## Related notes

- [[Local Average Treatment Effect (LATE)|LATE]]
- [[compliers]]
- [[never-takers]]
- [[Instrumental Variables (IV)]]
- [[noncompliance]]
- [[Policy-Relevant Treatment Effect (PRTE)|PRTE]]
- [[monotonicity]]
- [[exclusion restriction]]
- [[randomized controlled trial (RCT)]]
- [[selection bias]]
