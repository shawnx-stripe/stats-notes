---
title: Never-Takers
aliases: [never-takers, never takers]
tags: [causal-inference, iv, noncompliance, principal-strata]
updated: 2026-03-05
---

# Never-Takers

> [!summary]
> Units who never take up treatment regardless of instrument assignment: $D_i(1)=0$ and $D_i(0)=0$. One of the four principal strata in the [[Local Average Treatment Effect (LATE)|LATE]] framework.

## Formal Definition

Let $D_i(z)$ denote the **potential treatment** unit $i$ would receive if assigned instrument value $z$. A unit is a **never-taker** if:

$$
D_i(1) = 0 \quad \text{and} \quad D_i(0) = 0
$$

**Interpretation**: Never-takers refuse treatment regardless of whether the instrument encourages treatment ($z=1$) or not ($z=0$). Their treatment status is unaffected by the instrument.

## Role in the LATE Framework

In the presence of [[noncompliance]], the population is partitioned into four **principal strata** based on potential treatments $(D_i(0), D_i(1))$:

| Stratum | $D_i(0)$ | $D_i(1)$ | Observed $D$ when $Z=0$ | Observed $D$ when $Z=1$ |
|---------|----------|----------|-------------------------|-------------------------|
| [[compliers|Compliers]] | 0 | 1 | 0 | 1 |
| **Never-takers** | 0 | 0 | 0 | 0 |
| [[always-takers|Always-takers]] | 1 | 1 | 1 | 1 |
| [[defiers|Defiers]] | 1 | 0 | 1 | 0 |

Never-takers are observed to have $D_i=0$ regardless of $Z_i$. Because their treatment does not vary with the instrument, they **do not contribute** to identification of the treatment effect.

> [!note]
> We cannot directly observe who is a never-taker. Principal strata are defined by counterfactuals $(D_i(0), D_i(1))$, but we only observe one potential treatment per unit.

## Why Never-Takers Don't Identify Effects

The [[Local Average Treatment Effect (LATE)|LATE]] is identified from variation in $D$ induced by $Z$:

$$
\text{LATE} = \frac{E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]}{E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]}
$$

For never-takers:
- When $Z=0$: $D=0$, so $Y = Y_i(0)$
- When $Z=1$: $D=0$, so $Y = Y_i(0)$

There is **no variation** in treatment status for never-takers across $Z$. Hence, we cannot learn about their treatment effect $Y_i(1) - Y_i(0)$ from the IV design.

> [!warning]
> The IV estimand identifies the effect **only among [[compliers]]**—those whose treatment status changes with $Z$. We cannot identify the ATE for never-takers from the instrument alone.

## Estimating the Proportion of Never-Takers

Under [[monotonicity]] (no [[defiers]]), the share of never-takers is:

$$
\pi_n = P(D_i(1)=0, D_i(0)=0) = 1 - E[D_i \mid Z_i=1]
$$

**Intuition**: Among units with $Z=1$, only compliers and always-takers have $D=1$. So the share with $D=0$ when $Z=1$ are never-takers.

Alternatively:

$$
\pi_n = 1 - \pi_c - \pi_a
$$

where:
- $\pi_c = E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]$ (share of compliers)
- $\pi_a = E[D_i \mid Z_i=0]$ (share of always-takers)

> [!example]
> In a job training encouragement RCT:
> - 40% of the control group enrolls ($\pi_a = 0.40$)
> - 70% of the treatment group enrolls
> - First stage: $\pi_c = 0.70 - 0.40 = 0.30$
> - Never-takers: $\pi_n = 1 - 0.70 = 0.30$

## Relation to Intent-to-Treat (ITT)

The ITT effect averages over all principal strata:

$$
\text{ITT} = E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]
$$

Under the [[exclusion restriction]], $Z$ affects $Y$ only through $D$. For never-takers, $D$ is constant at 0, so:

$$
E[Y_i \mid Z_i=1, \text{never-taker}] = E[Y_i \mid Z_i=0, \text{never-taker}] = E[Y_i(0) \mid \text{never-taker}]
$$

Never-takers contribute **zero** to the ITT:

$$
\text{ITT} = \pi_c \cdot E[Y_i(1) - Y_i(0) \mid \text{complier}] + \pi_a \cdot 0 + \pi_n \cdot 0
$$

Thus:

$$
\text{LATE} = \frac{\text{ITT}}{\pi_c}
$$

Never-takers "dilute" the ITT but do not bias the LATE estimate.

## Implications of Exclusion Restriction

The [[exclusion restriction]] states that $Z$ affects $Y$ **only** through $D$:

$$
Y_i(z, D_i(z)) = Y_i(z', D_i(z)) \quad \text{for all } z, z'
$$

For never-takers, this simplifies to:

$$
Y_i(1, 0) = Y_i(0, 0) = Y_i(0)
$$

**Testable implication**: Among units with $D=0$, outcomes should not differ by $Z$:

$$
E[Y_i \mid Z_i=1, D_i=0] = E[Y_i \mid Z_i=0, D_i=0]
$$

> [!check] Exclusion restriction test
> Compare outcomes for $D=0$ units across $Z=0$ and $Z=1$. If they differ significantly, the exclusion restriction may fail (or there are defiers).

## External Validity Concerns

Because never-takers self-select out of treatment, they likely differ from [[compliers]] and [[always-takers]]:
- **Selection**: Never-takers may have lower motivation, face higher barriers, or expect lower returns
- **Treatment effects**: $E[Y_i(1) - Y_i(0) \mid \text{never-taker}]$ may differ from LATE

> [!warning]
> LATE does not generalize to never-takers. If a policy change compels never-takers to take treatment (e.g., by mandate), the effect on them is unknown.

## Bounds on Treatment Effects for Never-Takers

Without additional assumptions, the treatment effect for never-takers is **not identified**. We observe $Y_i(0)$ for never-takers but never $Y_i(1)$.

Under further assumptions (e.g., [[MTR]], monotone treatment response, mean dominance), we can derive **bounds**:

$$
E[Y_i(1) \mid \text{never-taker}] \geq E[Y_i(0) \mid \text{never-taker}]
$$

(if treatment weakly increases outcomes for everyone).

> [!note]
> Partial identification methods (e.g., Manski bounds) can narrow the range of plausible effects for never-takers, but these require untestable assumptions.

## Relation to Monotonicity

[[monotonicity]] assumes $D_i(1) \geq D_i(0)$ for all $i$, ruling out [[defiers]]. This allows us to partition the population into compliers, never-takers, and always-takers.

Without monotonicity:
- We cannot separately identify $\pi_n$ and $\pi_d$ (the share of defiers)
- The Wald estimand confounds complier and defier effects

> [!check]
> Monotonicity is untestable but often plausible (e.g., encouragement designs, eligibility cutoffs).

## Testing for Never-Takers

In a randomized encouragement design:
1. Estimate $\pi_n = P(D=0 \mid Z=1)$
2. If $\pi_n = 0$, everyone encouraged takes treatment (perfect compliance in treated group)
3. If $\pi_n > 0$, some units refuse treatment even when encouraged

> [!example]
> In a vaccine encouragement trial, if 20% of the encouraged group does not get vaccinated, then $\pi_n \geq 0.20$ (at least 20% are never-takers).

## Minimal Code Snippets

### R: Estimating proportion of never-takers

```r
library(AER)

# Proportion of never-takers (non-compliance in treated group)
pi_n <- mean(1 - df$D[df$Z == 1])
print(paste("Proportion never-takers:", pi_n))

# Alternative: 1 - proportion compliers - proportion always-takers
first_stage <- lm(D ~ Z, data = df)
pi_c <- coef(first_stage)["Z"]
pi_a <- mean(df$D[df$Z == 0])
pi_n_alt <- 1 - pi_c - pi_a
print(paste("Proportion never-takers (alternative):", pi_n_alt))

# Test exclusion restriction among D=0 units
never_taker_test <- t.test(Y ~ Z, data = df[df$D == 0, ])
print(never_taker_test)
```

### Python: Principal strata proportions and exclusion test

```python
import pandas as pd
from scipy import stats

# Proportion never-takers
pi_n = (1 - df.loc[df['Z'] == 1, 'D']).mean()
print(f"Proportion never-takers: {pi_n:.3f}")

# Alternative calculation
from statsmodels.api import OLS
first_stage = OLS(df['D'], df[['const', 'Z']]).fit()
pi_c = first_stage.params['Z']
pi_a = df.loc[df['Z'] == 0, 'D'].mean()
pi_n_alt = 1 - pi_c - pi_a
print(f"Proportion never-takers (alternative): {pi_n_alt:.3f}")

# Test exclusion restriction for D=0 units
d0 = df[df['D'] == 0]
y0_z0 = d0.loc[d0['Z'] == 0, 'Y']
y0_z1 = d0.loc[d0['Z'] == 1, 'Y']
t_stat, p_val = stats.ttest_ind(y0_z1, y0_z0)
print(f"Exclusion restriction test (D=0): t={t_stat:.3f}, p={p_val:.3f}")
```

### Stata: Principal strata and exclusion test

```stata
* Proportion never-takers
summ D if Z == 1
scalar pi_n = 1 - r(mean)
display "Proportion never-takers: " pi_n

* Alternative: 1 - compliers - always-takers
reg D Z
scalar pi_c = _b[Z]
summ D if Z == 0
scalar pi_a = r(mean)
scalar pi_n_alt = 1 - pi_c - pi_a
display "Proportion never-takers (alternative): " pi_n_alt

* Test exclusion restriction among D=0 units
ttest Y if D == 0, by(Z)
```

## One-Sided Noncompliance

In some designs, noncompliance occurs **only** in the treatment group (e.g., randomized to training but don't attend). Here:
- $\pi_a = 0$ (no always-takers)
- $\pi_n > 0$ (never-takers exist)
- $\pi_c = E[D \mid Z=1]$ (all compliers)

This simplifies identification:

$$
\text{LATE} = \frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{E[D \mid Z=1]}
$$

> [!tip]
> One-sided noncompliance is common in [[randomized controlled trial (RCT)|RCT]]s with encouragement or invitation designs.

## Characterizing Never-Takers

We cannot directly observe who is a never-taker, but we can learn about their characteristics using observed covariates $X$.

For units with $Z=1$ and $D=0$:
- These include never-takers **and possibly defiers** (if monotonicity fails)
- Under monotonicity, all $Z=1, D=0$ units are never-takers

Compare $E[X \mid Z=1, D=0]$ to the overall sample mean to characterize never-takers.

> [!warning]
> This is descriptive only—it does not identify the treatment effect for never-takers.

## Policy Implications

Understanding the share of never-takers is crucial for policy design:
1. **High $\pi_n$**: Many units resist treatment even when encouraged. Policy must address barriers.
2. **Low $\pi_n$**: Most units respond to encouragement. Scaling up the instrument may be effective.
3. **LATE generalization**: LATE applies to compliers, not never-takers. If policy compels never-takers to take treatment, effects are unknown.

> [!example]
> A job training program with $\pi_n = 0.50$ means half the population will not participate even when strongly encouraged. Mandating participation would affect these never-takers, but LATE provides no evidence on whether they would benefit.

## Related notes

- [[compliers]]
- [[defiers]]
- [[always-takers]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[noncompliance]]
- [[monotonicity]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[randomized controlled trial (RCT)]]
- [[Intent-to-Treat (ITT)]]
