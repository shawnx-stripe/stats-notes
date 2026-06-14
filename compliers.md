---
title: Compliers
aliases: [compliers, complier subpopulation]
tags: [causal-inference, iv, noncompliance, principal-strata]
updated: 2026-03-05
---

# Compliers

> [!summary]
> Units whose treatment take-up responds to the instrument as intended: $D_i(1)=1$ and $D_i(0)=0$. The [[Local Average Treatment Effect (LATE)|LATE]] is identified on this subpopulation under [[monotonicity]].

## Formal Definition

Let $D_i(z)$ denote the **potential treatment** unit $i$ would receive if assigned instrument value $z$. A unit is a **complier** if:

$$
D_i(1) = 1 \quad \text{and} \quad D_i(0) = 0
$$

**Interpretation**: Compliers take treatment when encouraged ($z=1$) and do not take treatment when not encouraged ($z=0$). Their treatment status is entirely determined by the instrument.

## Principal Strata Framework

In the presence of [[noncompliance]], the population is partitioned into four **principal strata** based on $(D_i(0), D_i(1))$:

| Stratum | $D_i(0)$ | $D_i(1)$ | Description |
|---------|----------|----------|-------------|
| **Compliers** | 0 | 1 | Respond as intended |
| [[never-takers|Never-takers]] | 0 | 0 | Never take treatment |
| [[always-takers|Always-takers]] | 1 | 1 | Always take treatment |
| [[defiers|Defiers]] | 1 | 0 | Do the opposite |

> [!note]
> Principal strata are defined by potential treatments $D_i(z)$, not observed treatment. We never observe both $D_i(0)$ and $D_i(1)$ for the same unit.

## Relation to LATE

The [[Local Average Treatment Effect (LATE)|LATE]] is the average treatment effect **among compliers**:

$$
\text{LATE} = E[Y_i(1) - Y_i(0) \mid D_i(1)=1, D_i(0)=0]
$$

Under the standard IV assumptions (relevance, [[exclusion restriction]], [[monotonicity]]), the Wald estimand identifies LATE:

$$
\text{LATE} = \frac{E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]}{E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]}
$$

**Key insight**: IV methods recover a causal effect only for the subpopulation whose treatment is affected by the instrument. This is *not* the ATE unless everyone is a complier.

## Why Only Compliers?

- **[[never-takers|Never-takers]]**: Always have $D_i=0$, so no variation in treatment induced by $Z$
- **[[always-takers|Always-takers]]**: Always have $D_i=1$, so no variation in treatment induced by $Z$
- **[[defiers|Defiers]]**: Ruled out by [[monotonicity]] assumption
- **Compliers**: Only group whose treatment varies with $Z$, enabling identification

> [!warning]
> LATE may not equal the ATE if treatment effects are heterogeneous. Compliers may be systematically different from the full population.

## Estimating the Proportion of Compliers

The share of compliers in the population is identified by:

$$
\pi_c = P(D_i(1)=1, D_i(0)=0) = E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]
$$

This is the **first-stage** coefficient in IV estimation.

> [!check] Interpretation
> If the first stage is 0.2, then 20% of the sample are compliers. This bounds external validity: LATE generalizes only to settings where compliers are similar.

## Characterizing Compliers

We cannot observe which units are compliers, but we can learn about their characteristics:

### Abadie (2003) Complier Means

For any covariate $X$:

$$
E[X_i \mid \text{complier}] = E[X_i] + \frac{\text{Cov}(X_i, Z_i) - E[X_i] \cdot \text{Cov}(D_i, Z_i)}{\text{Cov}(D_i, Z_i)}
$$

Alternatively:

$$
E[X_i \mid \text{complier}] = \frac{E[X_i D_i \mid Z_i=1] - E[X_i D_i \mid Z_i=0]}{\pi_c}
$$

### Conditional LATE

If the instrument is valid conditional on covariates $X$, we can estimate LATE within subgroups:

$$
\text{LATE}(x) = E[Y_i(1) - Y_i(0) \mid X_i=x, \text{complier}]
$$

This reveals treatment effect heterogeneity among compliers.

> [!tip]
> Use 2SLS with interactions $(Z \times X)$ in the first stage to estimate heterogeneous LATE by $X$.

## Complier Average Causal Effect (CACE)

CACE is synonymous with LATE:

$$
\text{CACE} = E[Y_i(1) - Y_i(0) \mid D_i(1) > D_i(0)]
$$

This terminology is common in RCTs with [[noncompliance]]. The "intention-to-treat" (ITT) effect is:

$$
\text{ITT} = E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0] = \pi_c \cdot \text{CACE}
$$

So $\text{CACE} = \text{ITT} / \pi_c$.

## External Validity Concerns

Because LATE applies only to compliers, generalization requires asking:
1. Who are the compliers in *this* setting?
2. Would compliers in *another* setting (different instrument, population) have similar treatment effects?

> [!warning]
> A LATE estimate from a [[randomized controlled trial (RCT)|randomized encouragement]] trial may not generalize to a policy mandate (different compliers) or a different population.

## Minimal Code Snippets

### R: Characterizing compliers (Abadie 2003)

```r
library(AER)

# 2SLS IV regression
iv_model <- ivreg(Y ~ D + X | Z + X, data = df)
summary(iv_model)

# First-stage F-statistic (test for weak instruments)
summary(iv_model, diagnostics = TRUE)$diagnostics["Weak instruments", "p-value"]

# Estimate proportion of compliers
first_stage <- lm(D ~ Z, data = df)
pi_c <- coef(first_stage)["Z"]

# Complier mean for covariate X (Abadie formula)
mean_X <- mean(df$X)
cov_XZ <- cov(df$X, df$Z)
cov_DZ <- cov(df$D, df$Z)
complier_mean_X <- mean_X + (cov_XZ - mean_X * cov_DZ) / cov_DZ
```

### Python: IV estimation and complier profiling

```python
from linearmodels.iv import IV2SLS
import numpy as np

# 2SLS estimation
iv_model = IV2SLS(
    dependent=df['Y'],
    exog=df[['const', 'X']],
    endog=df['D'],
    instruments=df['Z']
).fit(cov_type='robust')
print(iv_model)

# First stage
from statsmodels.api import OLS
first_stage = OLS(df['D'], df[['const', 'Z']]).fit()
pi_c = first_stage.params['Z']

# Complier mean for X
mean_X = df['X'].mean()
cov_XZ = np.cov(df['X'], df['Z'])[0, 1]
cov_DZ = np.cov(df['D'], df['Z'])[0, 1]
complier_mean_X = mean_X + (cov_XZ - mean_X * cov_DZ) / cov_DZ
```

### Stata: IV and first-stage diagnostics

```stata
* 2SLS estimation
ivregress 2sls Y X (D = Z), robust first

* Store first-stage F-statistic
estat firststage

* Manually compute proportion of compliers
reg D Z
scalar pi_c = _b[Z]
display "Proportion of compliers: " pi_c

* Test for weak instruments
estat firststage
```

### R: Heterogeneous LATE by subgroup

```r
library(AER)

# LATE for each level of categorical covariate X
levels <- unique(df$X_cat)
late_by_group <- sapply(levels, function(g) {
  sub <- df[df$X_cat == g, ]
  iv_fit <- ivreg(Y ~ D | Z, data = sub)
  coef(iv_fit)["D"]
})

names(late_by_group) <- levels
print(late_by_group)
```

## Testing for Complier Heterogeneity

If LATE varies by complier characteristics, the IV estimate is a **variance-weighted average** across subgroups. To test:

1. Estimate LATE in subgroups defined by pre-treatment $X$
2. Test equality: $\text{LATE}(x) = \text{LATE}(x')$ using Chow test or interaction terms
3. If rejected, report conditional LATE estimates separately

## Relation to Monotonicity

[[Monotonicity]] states $D_i(1) \geq D_i(0)$ for all $i$, which rules out [[defiers]]. Without monotonicity:
- The Wald estimand is $(π_c - π_d) \cdot \text{LATE}$, where $π_d$ is the share of defiers
- If $π_c = π_d$, IV has no power (first stage = 0)
- If $π_d > 0$, IV estimates a weighted effect of compliers and defiers (with opposite signs)

> [!check]
> Monotonicity is untestable but plausible in many settings (e.g., randomized encouragement, eligibility instruments).

## Related notes

- [[Local Average Treatment Effect (LATE)|LATE]]
- [[noncompliance]]
- [[Instrumental Variables (IV)]]
- [[never-takers]]
- [[defiers]]
- [[always-takers]]
- [[monotonicity]]
- [[exclusion restriction]]
- [[randomized controlled trial (RCT)]]
- [[weak instruments]]
