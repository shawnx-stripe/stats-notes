---
title: geo experiment
aliases: [geographical experiment, market-level experiment, geo lift test, market test]
tags: [experimentation, ab-testing, geo, cluster-randomized, staggered, scm, did, power, spillovers]
updated: 2025-09-17
---

# geo experiment

> [!summary] Quick definition
> A geo experiment randomizes treatment at the geographic/market/cluster level (e.g., cities, regions, DMAs) rather than at the user level. It is used when user-level randomization is infeasible or when interference is strong. Analysis relies on cluster-aware methods (e.g., [[Difference-in-Differences (DiD)]], [[Synthetic Control]]) with [[clustered standard errors]] and careful handling of [[spillovers]] and [[seasonality]].

- Typical applications: ads/marketing lift (geo-lift), pricing/promo pilots, policy rollouts, supply/logistics changes, marketplace/network interventions.

---

## When to use

- Interference at user/session level (network, marketplace, shared inventory) breaks SUTVA.
- Treatment deployable only at region/branch/site level (operational constraints).
- Need for operational realism (store/market pilots) before broader rollouts.
- Measurement and compliance are easier to enforce per geo.

---

## Design

- Unit of randomization: geo/market/cluster (e.g., DMA, city, state, store group).
- Sample size:
  - Power driven primarily by number of clusters (geos), not individuals; prioritize many similar geos over large geo size.
- Assignment:
  - Simple randomization of geos, or matched-pair randomization (pair similar geos and flip a coin within pairs).
  - [[bucketing]] at geo level; maintain a geo namespace and sticky assignment.
- Staggered rollout (stepped-wedge):
  - Treat subsets of geos over time; analyze with staggered DiD (e.g., [[Callaway–Sant’Anna estimator]] / [[Sun–Abraham estimator]]).

> [!tip] Matching and blocking
> Improve balance by pre-matching geos on pre-period outcomes and covariates, then randomize within pairs/blocks. Include pair/block effects in analysis.

---

## Threats and assumptions

- [[spillovers]] across geos (commuting/travel, media bleed, supply chain) → use buffers, exclude near-border areas, or model exposure.
- [[seasonality]] and calendar differences (events, holidays) → align windows and include seasonal controls.
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] violations within and across geos → consider saturation/exposure modeling if needed.
- Few clusters → inference challenges; apply [[few-cluster corrections]].

---

## Analysis options

### 1) Matched-pair difference-in-means or DiD
- If geos are paired:
  - Compute pair-wise differences in post outcomes (or DiD using pre-post within pair).
  - Analyze geo-level means with pair FE and cluster-robust SEs (cluster = pair or geo as appropriate).

### 2) Panel DiD across geos
- Geo-by-time panel with geo FE and time FE; treatment indicator at geo×time.
- For staggered adoption, avoid naive TWFE with heterogeneity; use:
  - [[Callaway–Sant’Anna estimator]] for group-time ATTs,
  - [[Sun–Abraham estimator]] for robust event studies.

### 3) [[Synthetic Control]] / augmented SCM
- For one or a few treated geos, build a synthetic control from donor geos matching pre-period paths; inference via placebo (in-space) tests.
- For multiple treated geos, apply SCM per geo and summarize, or use synth-DiD.

> [!warning] Inference
> - Use [[clustered standard errors]] at the geo (or geo-pair) level for regression-based methods.
> - With few geos, prefer [[few-cluster corrections]] (CR2, wild cluster bootstrap) or SCM placebo-based inference.
> - Spatial correlation across nearby geos may warrant [[Conley standard errors]].

---

## Power and MDE

- [[power analysis]] should be at the geo level; account for between-geo variance and [[ICC|Intraclass Correlation (ICC)]] if sub-geo units roll up.
- Matched-pair designs can improve power by reducing between-geo variance.
- Variance reduction with geo-level [[Analysis of Covariance (ANCOVA)|ANCOVA]]/[[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] using pre-period geo averages (strictly pre-treatment).

---

## Instrumentation and logging

- [[exposure logging]] at geo level: confirm which geo/day is treated; record intensity (spend, impressions, dosage).
- Define analysis windows by geo; ensure consistent time zones and calendars.
- Track operational anomalies: outages, stock-outs, local events.

---

## Diagnostics

> [!check] Recommended checks
> - [ ] Balance on pre-period geo outcomes and covariates; if matched, verify pair balance  
> - [ ] [[Sample Ratio Mismatch (SRM)|SRM]] at the geo level (counts of geos per arm as planned)  
> - [ ] [[pre-trends]]/[[event study]] at geo aggregates (outcomes)  
> - [ ] Spillover proximity: near/far geo heterogeneity; border checks  
> - [ ] Seasonality alignment; exclude holidays/events or include controls  
> - [ ] Placebos: permutation tests (SCM), placebo dates (DiD)

---

## Minimal code snippets

> [!example] R: Panel DiD with geo/time FE and clustered SEs

```r
library(fixest)
# df: geo, time, Y, treat (0/1 at geo-time), plus controls and seasonality
est <- feols(Y ~ treat | geo + time, data = df, cluster = ~ geo)
etable(est)
```

> [!example] R: Staggered adoption ATT (Callaway–Sant’Anna)

```r
library(did)
# G = first treatment time per geo (Inf for never-treated)
att <- att_gt(yname="Y", idname="geo", tname="time", gname="G", data=df, panel=TRUE)
dyn <- aggte(att, type="dynamic")   # event-time effects
summary(dyn)
```

> [!example] R: Synthetic Control for one treated geo

```r
library(Synth)
# Build dataprep with treated geo and donor geos; include multiple pre-period outcomes as predictors
dat <- dataprep(foo = df, predictors = c("X1","X2"),
                dependent = "Y", unit.variable = "geo", time.variable = "time",
                treatment.identifier = treated_geo,
                controls.identifier = donor_geos,
                time.predictors.prior = pre_period,
                special.predictors = list(list("Y", t1, "mean"), list("Y", t2, "mean")),
                time.optimize.ssr = pre_period, time.plot = c(pre_period, post_period))
sout <- synth(dat)
gaps.plot(dataprep.obj = dat, synth.obj = sout)
```

> [!example] Stata: Geo DiD with cluster-robust SEs

```stata
* geo-time panel
xtset geo time
reghdfe Y i.treat, absorb(geo time) vce(cluster geo)
```

> [!example] Python: PanelOLS with entity/time effects and geo clustering

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['geo','time'])
res = PanelOLS.from_formula('Y ~ 1 + treat + EntityEffects + TimeEffects', data=df).fit(
    cov_type='clustered', cluster_entity=True)
print(res.summary)
```

---

## Common pitfalls

> [!warning]
> - Too few geos → underpowered; naive iid SEs → false positives  
> - Ignoring cross-geo [[spillovers]] (media bleed, travel)  
> - Seasonality/time-zone mismatches; partial-week windows  
> - Using already-treated geos as controls in staggered TWFE without robust methods  
> - Not accounting for geo size heterogeneity in matching/weighting  
> - Treating per-user metrics as iid when randomization is at geo (clustered dependence)

---

## Reporting essentials

- Geo definitions and counts; matching/stratification approach; assignment procedure
- Treatment schedule (staggered or parallel), intensity (if applicable)
- Pre-period balance and diagnostics (plots/tables)
- Estimator(s): DiD/SCM; FE structure; controls/seasonality; clustering level; small-sample corrections
- Results: effects with CIs (cluster-corrected or SCM placebo p-values); dynamic effects (event study)
- Robustness: alternative donor pools, near/far geos, excluding border geos, placebo dates, different windows
- Limitations: potential spillovers, external shocks/events, generalizability

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]
- [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]] · [[group-time average treatment effect]]
- [[clustered standard errors]] · [[few-cluster corrections]] · [[Conley standard errors]]
- [[seasonality]] · [[spillovers]] · [[exposure logging]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[switchback experiment]]