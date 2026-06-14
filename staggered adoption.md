---
title: Staggered Adoption
aliases:
- staggered treatment timing
- staggered rollout
- staggered DiD
- Staggered Adoption
- Staggered adoption
tags:
- econometrics
- causal-inference
- did
- panels
- twfe
- heterogeneous-effects
updated: 2025-09-17
---

# Staggered Adoption

> [!summary] Quick definition
> Staggered adoption means different units begin treatment at different times. This is common in policy rollouts and creates complications for standard [[two-way fixed effects]] DiD when there is [[treatment effect heterogeneity]] across cohorts or over event time.

- Typical setup: each unit i has a first-treatment time $G_i \in \{t_0,\dots,t_T\}$ or is never-treated ($G_i=\infty$). Event time is $k = t - G_i$.

## Why it matters

- Classic TWFE with a single coefficient can be biased when:
  - Effects vary by cohort or over time since treatment.
  - Already-treated units act as “controls” for later-treated units.
- Insight: the TWFE coefficient is a weighted average of many 2×2 DiD contrasts, with possibly negative weights. See [[Goodman–Bacon decomposition]].

> [!warning] Consequence
> With heterogeneity, the sign and magnitude of TWFE estimates can be misleading even if each underlying 2×2 contrast is positive.

## Notation and target estimands

- Group (cohort) $G$: first treatment time.
- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1) - Y_t(0) \mid G=g\right], \quad t \ge g
$$
- Dynamic (event-time) effect for cohort g at relative time k:
$$
\theta_g(k) = \mathbb{E}\!\left[Y_{g+k}(1) - Y_{g+k}(0) \mid G=g\right]
$$

> [!tip] Aggregation
> Report transparent aggregations: by cohort, by calendar time, or by relative time (dynamic/event-study). See [[group-time average treatment effect]].

## Identification assumptions (staggered context)

- [[parallel trends assumption]] for untreated potential outcomes, using valid comparison sets (never-treated and/or not-yet-treated units).
- [[No spillovers]]/[[interference]] across units (or model exposure).
- [[Anticipatory effects]] absent or modeled via pre-treatment leads.
- Stable [[composition]] or adjustments for entry/exit/attrition.

## What goes wrong with naive TWFE

- Contaminated controls: once treated, units should not serve as controls, but TWFE implicitly uses them unless you restrict comparisons.
- Negative weights: some cohort contrasts receive negative weights, distorting averages.
- Dynamic heterogeneity: effects evolving over k can bias a single static β.

## Modern estimators for staggered adoption

### 1) [[Callaway–Sant’Anna estimator]]
- Estimates cohort-time $ATT(g,t)$ using never-treated or not-yet-treated controls; then aggregates by choice (simple, calendar, cohort, dynamic).
- Robust to heterogeneity by design.

### 2) [[Sun–Abraham estimator]]
- Interaction-weighted event study: estimates cohort-specific relative-time effects and combines them to avoid contamination by already-treated units.

### 3) Imputation/“untreated outcome” methods
- [[Borusyak–Jaravel–Spiess (imputation)]]: predict $Y_{it}(0)$ using untreated observations (unit and time effects, possibly controls), then average $Y_{it}-\hat Y_{it}(0)$ over treated observations.
- [[Gardner DID2S]]: two-stage regression that mimics valid comparisons while retaining TWFE convenience.

### 4) Other robust approaches
- [[de Chaisemartin–D’Haultfœuille]] (DID_M and two-by-two aggregations).
- Weighted or design-based event studies using valid comparison sets only.

## Event study under staggered timing

- Use cohort-valid construction:
  - Compare each treated cohort to never-treated or not-yet-treated at each k.
  - Aggregate cohort-specific $\beta_{g,k}$ into overall dynamic effects.
- Avoid naive TWFE event studies that use already-treated as controls. Prefer Sun–Abraham or group-time ATT aggregation. See [[event study]].

## Practical workflow

> [!check] Recommended steps
> - [ ] Define cohorts $G_i$ and event time k; document announcements vs. implementation.
> - [ ] Plot [[pre-trends]] using a robust event-study estimator.
> - [ ] Estimate $ATT(g,t)$ or cohort-specific event studies.
> - [ ] Aggregate transparently (report weights and chosen scheme).
> - [ ] Use appropriate [[clustered standard errors]]; apply [[few-cluster corrections]] if needed.
> - [ ] Conduct robustness: alternative control sets (never vs. not-yet), time windows, and exclusion of early/late adopters.

## When is TWFE acceptable?

- Two groups, two periods (classic DiD).
- Homogeneous treatment effects across cohorts and event time.
- Or when you restructure the sample so that comparisons are only between treated and not-yet-treated, and verify assumptions.

## Common pitfalls

> [!warning] Avoid these
> - Reporting a single TWFE β in the presence of obvious heterogeneity.
> - Using all treated units as controls after they are treated.
> - Ignoring [[Anticipatory effects]] and defining $Post$ only at implementation.
> - Failing to report how you aggregated $ATT(g,t)$.
> - Not addressing few treated clusters with [[few-cluster corrections]].

## Minimal code snippets

> [!example] R: Callaway–Sant’Anna (group-time ATTs and aggregation)

```r
library(did)
# df: columns Y (outcome), id (unit), time (period), G (first treatment time, Inf if never-treated)
att <- att_gt(yname="Y", tname="time", idname="id", gname="G", data=df, panel=TRUE)
# Overall ATT (simple average across cohorts/times)
overall <- aggte(att, type="simple")
# Dynamic effects by event time (event-study style)
dyn <- aggte(att, type="dynamic")
summary(overall); summary(dyn)
```

> [!example] R: Sun–Abraham via fixest

```r
library(fixest)
es <- feols(Y ~ sunab(G, time) | id + time, cluster = ~id, data = df)
iplot(es)  # robust event-study plot: leads (pre) and lags (post)
```

> [!example] R: Gardner DID2S (sketch)

```r
# install.packages("did2s")
library(did2s)
res <- did2s(data = df,
             yname = "Y",
             first_stage = ~ id + time,   # fixed effects
             second_stage = ~ D,          # treatment indicator
             treatment = "D",
             cluster_var = "id")
summary(res)
```

> [!example] Stata: Callaway–Sant’Anna and Sun–Abraham style

```stata
* Stata: csdid (Callaway–Sant’Anna)
csdid Y, ivar(id) time(time) gvar(G) method(dripw) vce(cluster id)
estat simple
estat event

* Sun–Abraham style event study (eventstudyinteract)
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
```

> [!example] Python: cohort-valid event study (sketch with linearmodels)

```python
# Sketch: restrict controls to never-/not-yet-treated each period
from linearmodels.panel import PanelOLS
import pandas as pd

df = df.set_index(['id','time'])
# Build relative-time dummies by cohort G and event time k
rel = df.index.get_level_values('time') - df['G']
K = 5
for k in range(-K, K+1):
    if k != -1:
        df[f'rt_{k}'] = (rel == k).astype(int)

# Mask out already-treated controls by interacting with not-yet-treated indicator
df['notyet'] = ((df.index.get_level_values('time') < df['G']) | (df['G'] == float('inf'))).astype(int)
rhs = [f'rt_{k}' for k in range(-K, K+1) if k != -1]
for v in rhs:
    df[v] = df[v] * df['notyet']  # crude restriction; proper CS/SA estimators preferred

formula = 'Y ~ 1 + ' + ' + '.join(rhs) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(formula, data=df).fit(cov_type='clustered', cluster_entity=True)
print(res)
# Prefer dedicated packages in R/Stata for correctness.
```

## Copy-ready formulas

- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1) - Y_t(0) \mid G=g\right], \quad t \ge g
$$

- Dynamic (event-time) effect and aggregation:
$$
\theta_g(k) = \mathbb{E}\!\left[Y_{g+k}(1) - Y_{g+k}(0) \mid G=g\right], \quad
\Theta(k) = \sum_g w_g(k)\, \theta_g(k)
$$
with explicit weights $w_g(k)$ reported (e.g., cohort sizes).

- Valid comparison sets:
  - For $ATT(g,t)$, controls are units with $G > t$ (not-yet-treated at t) and/or $G=\infty$ (never-treated).

## Reporting essentials

- Define cohorts, adoption timing, and whether “never-treated” units exist.
- Describe comparison sets (never vs. not-yet-treated) and justify.
- Present robust event-study plots (with confidence bands) and [[pre-trends]] diagnostics.
- Report aggregation choices and weights for $ATT(g,t)$.
- State clustering level(s), number of clusters, and any [[few-cluster corrections]].

## When to use alternative designs

- Single treated aggregate: consider [[Synthetic Control]].
- Anticipated rollouts: align event time with announcement; see [[Anticipatory effects]].
- Interference across units: model exposure; see [[interference]]/[[No spillovers]].
- Severe composition changes: use reweighting or conditional trends; see [[composition]] and [[covariates]].

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[Goodman–Bacon decomposition]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[Borusyak–Jaravel–Spiess (imputation)]]
- [[Gardner DID2S]]
- [[group-time average treatment effect]]
- [[event study]]
- [[parallel trends assumption]]
- [[treatment effect heterogeneity]]
- [[No spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[pre-trends]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[composition]]
- [[covariates]]
- [[Synthetic Control]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]