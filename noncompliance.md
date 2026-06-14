---
title: Noncompliance
aliases:
- partial compliance
- imperfect take-up
- non-adherence
- non-compliance
- Noncompliance
tags:
- causal-inference
- rct
- iv
- did
- policy-evaluation
- principal-strata
updated: 2025-09-17
---

# Noncompliance

> [!summary] Quick definition
> Noncompliance occurs when units do not follow their assigned treatment: some assigned to treatment do not take it, and/or some assigned to control obtain it. This breaks “treatment = assignment” and motivates analyzing the [[Intent-to-Treat (ITT)]] and using [[Instrumental Variables (IV)]] to identify effects like [[Local Average Treatment Effect (LATE)|LATE]].

- Settings: RCTs with take-up issues, encouragement designs, policy eligibility vs. actual receipt, phased rollouts with partial adoption.
- Key message: keep randomization/assignment intact in estimation; avoid “as-treated” analyses that condition on realized treatment.

## Basic setup and notation

- Assignment/offer Z ∈ {0,1}; receipt D ∈ {0,1} (or continuous); outcome Y.
- ITT effect of assignment:
$$
ITT = \mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]
$$
- First stage (effect of Z on D):
$$
\Delta_D = \mathbb{E}[D \mid Z=1] - \mathbb{E}[D \mid Z=0]
$$
- Wald (ratio) estimator for [[Local Average Treatment Effect (LATE)|LATE]] (under IV assumptions):
$$
LATE = \frac{ITT}{\Delta_D}
$$

## Principal strata (compliance types)

- Compliers: D(1)=1, D(0)=0
- Always-takers: D(1)=1, D(0)=1
- Never-takers: D(1)=0, D(0)=0
- Defiers: D(1)=0, D(0)=1

> [!tip] [[monotonicity]]
> The standard LATE framework assumes no defiers. With [[exclusion restriction]] and independence of Z, the Wald ratio identifies the average effect for compliers.

## What to estimate (and what to avoid)

- Estimate:
  - [[Intent-to-Treat (ITT)]]: unbiased under random assignment even with noncompliance.
  - [[Local Average Treatment Effect (LATE)|LATE]] via IV/Wald when [[exclusion restriction]] and [[monotonicity]] are credible.
- Avoid:
  - “As-treated” or “per-protocol” comparisons that condition on D; these are typically biased because D is endogenous.
  - Dropping noncompliers; this breaks randomization.

## Interpreting ITT, LATE, and TOT

- ITT: policy-relevant “offer effect,” often attenuated when take-up is incomplete.
- LATE: effect for compliers (those whose D is moved by Z); may differ from the overall ATE/ATT.
- [[Treatment-on-the-Treated (TOT)]]: effect for those who actually received treatment. Not point-identified without additional assumptions; equals LATE only in special cases (e.g., one-sided compliance with no always-takers and monotonicity).

## Diagnostics and reporting

> [!check] Good practice
> - [ ] Report compliance rates: E[D|Z=1], E[D|Z=0], and first-stage Δ_D; provide F-stat for the first stage (rule of thumb > 10).
> - [ ] Present ITT with CIs; if reporting LATE, justify [[exclusion restriction]] and [[monotonicity]].
> - [ ] Discuss potential [[interference]]/[[No spillovers]] from the offer to controls.
> - [ ] Address attrition/[[composition]] differences by assignment (weights or bounds like [[Lee bounds]] if applicable).
> - [ ] Cluster SEs at the assignment level; see [[clustered standard errors]] and [[few-cluster corrections]] when clusters are few.

## Noncompliance beyond simple RCTs

### 1) Noncompliance in DiD (“fuzzy DiD”)
- Use assignment Z (e.g., eligibility or policy mandate) as an instrument for realized treatment D in a panel DiD:
$$
Y_{it} = \alpha_i + \gamma_t + \tau \,(D_{it}\cdot Post_t) + X_{it}'\theta + \varepsilon_{it}, \quad \text{IV: } D_{it}\cdot Post_t \text{ with } Z_{it}\cdot Post_t
$$
- Then τ is a LATE-type DiD effect for compliers with respect to the rollout. Maintain [[parallel trends assumption]] relative to assignment groups and ensure a strong first stage.

### 2) Fuzzy [[Regression Discontinuity Design (RDD)]]
- If treatment jumps in probability at a cutoff (not perfectly assigned), use fuzzy RD (local Wald ratio around the threshold) to identify a local LATE.

### 3) Principal stratification
- When exclusion is doubtful but strata are of interest, model outcomes within principal strata (compliers, etc.). Requires strong assumptions or additional design features.

## Common pitfalls

> [!warning] Avoid these
> - Using post-assignment covariates or compliance status to “fix” imbalance (creates [[bad controls]]).
> - Weak instruments (small Δ_D): leads to biased IV and inflated variance; report first-stage F.
> - Assuming LATE generalizes to all units without discussion.
> - Ignoring anticipatory take-up or information effects (violates exclusion).

## Minimal code snippets

> [!example] ITT and LATE (difference-in-means and 2SLS)

```r
# R
ITT_y <- with(df, mean(Y[Z==1]) - mean(Y[Z==0]))
ITT_d <- with(df, mean(D[Z==1]) - mean(D[Z==0]))
LATE  <- ITT_y / ITT_d

# 2SLS with AER
library(AER)
summary(ivreg(Y ~ D | Z, data = df))  # reports first-stage and 2SLS
```

```stata
* Stata
ttest Y, by(Z)                      // ITT
ttest D, by(Z)                      // first stage
ivregress 2sls Y (D = Z), robust    // LATE via 2SLS
estat firststage
```

```python
# Python
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula('Y ~ 1 + [D ~ Z]', data=df).fit(cov_type='robust')
print(res.summary)
```

> [!example] Fuzzy DiD (panel IV with FE)

```r
# R (fixest)
library(fixest)
# Instrument D:Post using Z:Post, include unit and time FE, cluster appropriately
est_iv <- feols(Y ~ 1 | id + time, data = df,
                iv = ~ D:Post ~ Z:Post, cluster = ~id)
etable(est_iv)
```

```stata
* Stata (FE 2SLS)
ivreghdfe Y (c.Post#i.D = c.Post#i.Z), absorb(id time) vce(cluster id)
* or:
xtivreg Y (c.Post#i.D = c.Post#i.Z), fe cluster(id)
```

```python
# Python (linearmodels 2SLS with FE via demeaning not shown; sketch with formulas)
from linearmodels.iv import IV2SLS
# Create interaction terms:
df["DPost"] = df["D"] * df["Post"]
df["ZPost"] = df["Z"] * df["Post"]
# Absorb FE by including entity/time dummies or use within transforms if feasible
res = IV2SLS.from_formula('Y ~ C(id) + C(time) + [DPost ~ ZPost]', data=df).fit(cov_type='clustered', clusters=df['id'])
print(res.summary)
```

> [!example] Fuzzy RDD (local Wald around cutoff)

```r
# R (rdrobust; sketch)
library(rdrobust)
# First stage: D on running variable near cutoff
# Outcome: Y; LATE ~ ratio of reduced-form to first-stage at cutoff
```

## Copy-ready assumptions for LATE

- Independence (random assignment):
$$
Z \perp \{Y(0), Y(1), D(0), D(1)\}
$$
- [[exclusion restriction]]:
$$
Y(z,d) = Y(d) \quad \text{(assignment affects Y only through D)}
$$
- [[monotonicity]]:
$$
D(1) \ge D(0) \quad \text{(no defiers)}
$$

## When is ITT preferred?

- Policy makers care about the effect of offering/assigning a program.
- Exclusion or monotonicity are questionable.
- Spillovers from the offer likely exist (then report ITT and discuss violations for LATE).

---

Related notes to create:
- [[Intent-to-Treat (ITT)]]
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Treatment-on-the-Treated (TOT)]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[fuzzy RDD]]
- [[Regression Discontinuity Design (RDD)]]
- [[principal stratification]]
- [[compliers]]
- [[always-takers]]
- [[never-takers]]
- [[defiers]]
- [[first stage]]
- [[bad controls]]
- [[composition]]
- [[clustered standard errors]]
- [[few-cluster corrections]]