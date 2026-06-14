---
title: Defiers
aliases: [defiers]
tags: [causal-inference, iv, noncompliance, principal-strata]
updated: 2026-03-05
---

# Defiers

> [!summary]
> Units who do the opposite of what the instrument encourages: $D_i(1)=0$ and $D_i(0)=1$. [[Monotonicity]] rules out defiers, enabling identification of [[Local Average Treatment Effect (LATE)|LATE]].

## Formal Definition

Let $D_i(z)$ denote the **potential treatment** unit $i$ would receive if assigned instrument value $z$. A unit is a **defier** if:

$$
D_i(1) = 0 \quad \text{and} \quad D_i(0) = 1
$$

**Interpretation**: Defiers take treatment when **not** encouraged ($z=0$) and refuse treatment when **encouraged** ($z=1$). Their response to the instrument is opposite the intended direction.

## Role in the LATE Framework

In the presence of [[noncompliance]], the population can theoretically be partitioned into four **principal strata**:

| Stratum | $D_i(0)$ | $D_i(1)$ | Response to instrument |
|---------|----------|----------|------------------------|
| [[compliers|Compliers]] | 0 | 1 | As intended |
| [[never-takers|Never-takers]] | 0 | 0 | No response |
| [[always-takers|Always-takers]] | 1 | 1 | No response |
| **Defiers** | 1 | 0 | Opposite direction |

However, standard IV analysis **assumes defiers do not exist** via the [[monotonicity]] assumption.

> [!note]
> Defiers are defined by counterfactuals $(D_i(0), D_i(1))$. We never observe both potential treatments for the same unit, so we cannot directly identify who is a defier.

## The Monotonicity Assumption

[[Monotonicity]] states:

$$
D_i(1) \geq D_i(0) \quad \text{for all } i
$$

This rules out defiers by assumption. Under monotonicity, the population consists only of [[compliers]], [[never-takers]], and [[always-takers]].

**Why is monotonicity needed?** Without it, the Wald estimand is:

$$
\frac{E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]}{E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]} = \frac{\pi_c \cdot \text{LATE}_c - \pi_d \cdot \text{LATE}_d}{\pi_c - \pi_d}
$$

where:
- $\pi_c$ = share of compliers
- $\pi_d$ = share of defiers
- $\text{LATE}_c$ = treatment effect for compliers
- $\text{LATE}_d$ = treatment effect for defiers

> [!warning]
> If defiers exist, the IV estimand is a **weighted average** of complier and defier effects with **opposite signs**. This can yield misleading or even sign-reversed estimates.

## What Happens When Defiers Exist?

### Case 1: Equal shares of compliers and defiers ($\pi_c = \pi_d$)

The first-stage coefficient is:

$$
E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0] = \pi_c - \pi_d = 0
$$

The instrument has **no power**—it does not predict treatment. IV estimation fails.

### Case 2: Defiers outnumber compliers ($\pi_d > \pi_c$)

The first-stage coefficient is **negative**. The IV estimand has the **opposite sign** of the complier effect:

$$
\text{IV estimate} = \frac{\pi_c \cdot \text{LATE}_c - \pi_d \cdot \text{LATE}_d}{\pi_c - \pi_d}
$$

If $\pi_d > \pi_c$ and $\text{LATE}_c > 0$, the IV estimate can be negative even when treatment benefits both compliers and defiers.

### Case 3: Small share of defiers ($\pi_d < \pi_c$)

The IV estimand is:

$$
\text{IV estimate} \approx \text{LATE}_c - \frac{\pi_d}{\pi_c - \pi_d} \cdot \text{LATE}_d
$$

The estimate is **biased** toward zero (or in the opposite direction) depending on the relative sizes of $\pi_d$ and $\text{LATE}_d$.

> [!warning]
> Even a small fraction of defiers can substantially bias the IV estimate if $\text{LATE}_d$ is large.

## Testing for Defiers

The share of defiers is **not identified** without additional assumptions. However, we can perform **indirect tests**:

### 1. Sign of the first-stage coefficient

If the first stage is **negative**, either:
- Defiers outnumber compliers ($\pi_d > \pi_c$), or
- The instrument is coded incorrectly

A negative first stage is strong evidence against monotonicity.

### 2. Exclusion restriction violations

Among units with $D=0$, test whether $Y$ differs by $Z$:

$$
E[Y_i \mid Z_i=1, D_i=0] \stackrel{?}{=} E[Y_i \mid Z_i=0, D_i=0]
$$

Under monotonicity and [[exclusion restriction]], this should hold. A significant difference suggests either:
- Defiers exist, or
- The exclusion restriction fails

Similarly, test among units with $D=1$:

$$
E[Y_i \mid Z_i=1, D_i=1] \stackrel{?}{=} E[Y_i \mid Z_i=0, D_i=1]
$$

### 3. Sensitivity analysis

Assume a range of plausible values for $\pi_d$ and compute implied bounds on $\text{LATE}_c$:

$$
\text{LATE}_c = \frac{\text{IV estimate} \cdot (\pi_c - \pi_d) + \pi_d \cdot \text{LATE}_d}{\pi_c}
$$

If $\text{LATE}_c$ is sensitive to small $\pi_d$, the monotonicity assumption is critical.

> [!check]
> Report sensitivity to violations of monotonicity, especially if the first stage is weak or the instrument is controversial.

## Partial Identification Without Monotonicity

If monotonicity is implausible, we can **bound** the treatment effect without it (Balke & Pearl, 1997; Manski & Pepper, 2000):

### Balke-Pearl bounds

Without monotonicity, the treatment effect for compliers is bounded by:

$$
\text{LATE}_c \in \left[ \frac{E[Y \mid Z=1] - E[Y \mid Z=0] - \pi_d \cdot \text{LATE}_d}{\pi_c - \pi_d}, \frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{\pi_c - \pi_d} \right]
$$

Additional assumptions (e.g., $\text{LATE}_d \leq 0$ or $\text{LATE}_d = -\text{LATE}_c$) can tighten these bounds.

### Worst-case bounds (Manski)

Without monotonicity or exclusion restriction, the treatment effect is bounded by the **worst-case** scenarios:

$$
E[Y_i(1) - Y_i(0)] \in \left[ \min(Y) - \max(Y), \max(Y) - \min(Y) \right]
$$

These bounds are often wide but may be tightened with monotone treatment response or mean dominance assumptions.

> [!note]
> Partial identification is useful when monotonicity is questionable but complete identification is infeasible.

## When Does Monotonicity Fail?

Defiers are rare in most IV applications but can arise in:

1. **Psychological reactance**: Units who dislike being told what to do (e.g., anti-vaccine sentiment when encouraged)
2. **Substitution effects**: Units who seek treatment elsewhere when denied (e.g., private insurance when excluded from public program)
3. **Misclassification**: Measurement error in $D$ or $Z$ can create apparent defiers
4. **Strategic behavior**: Units who game the instrument (e.g., applying for a program to signal non-neediness)

> [!example]
> In a randomized encouragement design for vaccination, some individuals may **refuse** vaccination precisely because they were encouraged (reactance). These are defiers.

## Minimal Code Snippets

### R: Testing for defiers (first-stage sign, exclusion tests)

```r
library(AER)

# Estimate first stage
first_stage <- lm(D ~ Z, data = df)
summary(first_stage)

# Check sign of first-stage coefficient
pi_c_minus_pi_d <- coef(first_stage)["Z"]
if (pi_c_minus_pi_d < 0) {
  warning("Negative first stage: defiers may outnumber compliers")
}

# Test exclusion restriction among D=0 units (should be 0 under monotonicity)
test_d0 <- t.test(Y ~ Z, data = df[df$D == 0, ])
print(test_d0)

# Test exclusion restriction among D=1 units
test_d1 <- t.test(Y ~ Z, data = df[df$D == 1, ])
print(test_d1)

# IV estimate (potentially biased if defiers exist)
iv_model <- ivreg(Y ~ D | Z, data = df)
summary(iv_model)
```

### Python: First-stage diagnostics and exclusion tests

```python
import pandas as pd
from scipy import stats
from statsmodels.api import OLS

# First stage
first_stage = OLS(df['D'], df[['const', 'Z']]).fit()
pi_c_minus_pi_d = first_stage.params['Z']
print(f"First stage coefficient: {pi_c_minus_pi_d:.3f}")

if pi_c_minus_pi_d < 0:
    print("WARNING: Negative first stage suggests defiers > compliers")

# Exclusion test for D=0 units
d0 = df[df['D'] == 0]
y0_z0 = d0.loc[d0['Z'] == 0, 'Y']
y0_z1 = d0.loc[d0['Z'] == 1, 'Y']
t_stat_d0, p_val_d0 = stats.ttest_ind(y0_z1, y0_z0)
print(f"Exclusion test (D=0): t={t_stat_d0:.3f}, p={p_val_d0:.3f}")

# Exclusion test for D=1 units
d1 = df[df['D'] == 1]
y1_z0 = d1.loc[d1['Z'] == 0, 'Y']
y1_z1 = d1.loc[d1['Z'] == 1, 'Y']
t_stat_d1, p_val_d1 = stats.ttest_ind(y1_z1, y1_z0)
print(f"Exclusion test (D=1): t={t_stat_d1:.3f}, p={p_val_d1:.3f}")
```

### Stata: First-stage and exclusion tests

```stata
* First stage
reg D Z, robust
scalar fs_coef = _b[Z]
display "First stage coefficient: " fs_coef

* Warn if negative
if fs_coef < 0 {
    display "WARNING: Negative first stage - possible defiers"
}

* Test exclusion among D=0 units
ttest Y if D == 0, by(Z)

* Test exclusion among D=1 units
ttest Y if D == 1, by(Z)

* IV estimate
ivregress 2sls Y (D = Z), robust
```

### Python: Sensitivity analysis for defiers

```python
import numpy as np

# Suppose we have IV estimate and first stage
iv_estimate = 5.0  # example
fs_coef = 0.20     # pi_c - pi_d

# Assume a range of defier shares
pi_d_range = np.linspace(0, 0.10, 11)
late_d_range = [-10, 0, 10]  # assume different LATE_d values

for late_d in late_d_range:
    print(f"\nAssuming LATE_d = {late_d}")
    for pi_d in pi_d_range:
        pi_c = fs_coef + pi_d
        if pi_c > 0:
            late_c = (iv_estimate * (pi_c - pi_d) + pi_d * late_d) / pi_c
            print(f"  pi_d={pi_d:.2f} → pi_c={pi_c:.2f} → LATE_c={late_c:.2f}")
```

## Plausibility of Monotonicity

Monotonicity is **untestable** but often **plausible**:

### Plausible settings
- **Randomized encouragement**: Being encouraged to enroll should not make someone *less* likely to enroll
- **Eligibility thresholds**: Being eligible should not make someone *less* likely to participate
- **Distance instruments**: Living closer to a facility should not make someone *less* likely to use it

### Questionable settings
- **Nudges with reactance**: Encouragement may backfire for some individuals
- **Substitution effects**: Being denied treatment may prompt alternative acquisition
- **Strategic responses**: Individuals may game the instrument in unexpected ways

> [!tip]
> Justify monotonicity with institutional knowledge. If it's questionable, report sensitivity analyses or use partial identification.

## Policy Implications

Understanding whether defiers exist is critical for policy:
1. **If defiers exist**: IV estimates may be biased or sign-reversed. Use bounds or assume monotonicity with sensitivity checks.
2. **If monotonicity holds**: IV identifies the complier effect, which may inform policy if compliers are the target population.
3. **External validity**: Even if monotonicity holds in one context, it may fail in another (e.g., voluntary program vs. mandate).

> [!example]
> A health insurance encouragement trial may satisfy monotonicity (encouragement increases take-up). But a mandate that penalizes non-enrollment may induce defiance, violating monotonicity.

## Related notes

- [[compliers]]
- [[never-takers]]
- [[always-takers]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[monotonicity]]
- [[noncompliance]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[weak instruments]]
- [[randomized controlled trial (RCT)]]
