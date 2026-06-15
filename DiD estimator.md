---
title: DiD Estimator
aliases: [Difference-in-Differences estimator, DID estimator]
tags: [econometrics, causal-inference, did, twfe, staggered-adoption]
updated: 2025-09-17
---

# DiD Estimator

> [!summary] Quick definition
> The Difference-in-Differences (DiD) estimator contrasts changes over time in a [[treated group]] with changes in a [[control group]]. Under the [[parallel trends assumption]], it identifies a causal effect (typically an ATT).

## Core formula (two groups, two periods)

- Copy-ready block math:
$$
\text{DiD} = \big(\bar{Y}_T^{\text{post}} - \bar{Y}_T^{\text{pre}}\big) - \big(\bar{Y}_C^{\text{post}} - \bar{Y}_C^{\text{pre}}\big)
$$

> [!example] Simple numbers
> - Treated: 10 → 15 (change = +5)
> - Control: 8 → 10 (change = +2)
> - DiD = 5 − 2 = 3

## Regression representation (TWFE, two periods)

- Copy-ready:
$$
Y_{it} = \alpha_i + \gamma_t + \beta \big(D_i \cdot Post_t\big) + \varepsilon_{it}
$$

- Interpretation:
  - $\beta$ is the DiD effect.
  - $\alpha_i$: unit fixed effects, $\gamma_t$: time fixed effects.
  - $D_i$: treated indicator; $Post_t$: post-treatment period indicator.
- This is a [[two-way fixed effects]] specification.

> [!tip] Equivalence
> With two groups and two periods, the OLS estimate $\hat{\beta}$ equals the sample DiD contrast above.

## Identification and estimands

- Main assumption: [[parallel trends assumption]] (treated and control would follow the same trend absent treatment).
- Typical estimand: [[Average Treatment Effect on the Treated (ATT)]].
- Potential outcomes view:
$$
ATT = \mathbb{E}\!\left[Y(1) - Y(0) \mid D=1\right]
$$
DiD identifies ATT if the change in $\mathbb{E}[Y(0)]$ for treated equals the change for controls.

## Standard errors and inference

- Cluster standard errors at the treatment-assignment level (often unit, region, firm).
- With few clusters, use [[few-cluster corrections]] or wild-cluster bootstrap.
- In panel settings with serial correlation, clustering at the unit level is typically essential.

## Diagnostics and good practice

> [!check] Pre-analysis checklist
> - [ ] Plot pre-trends and run an [[event study]] with leads to assess parallel trends.
> - [ ] Justify choice of [[control group]]; demonstrate covariate balance and similar pre-trends.
> - [ ] Check for [[spillovers]]/[[interference]] and [[Anticipatory effects]].
> - [ ] Verify stable sample [[composition]] and measurement across periods.

- Include [[covariates]] to improve precision; parallel trends may be assumed conditional on $X$.

## Variants and extensions

### Repeated cross-sections
- If units are not tracked over time, use group and time fixed effects:
$$
Y_{gt} = \alpha_g + \gamma_t + \beta \big(Treat_g \cdot Post_t\big) + \varepsilon_{gt}
$$
- Consider survey weights and ensure pre-period comparability across samples.

### Staggered adoption (multiple periods)
- Classic TWFE with heterogeneous effects can be biased due to negative weighting and contamination by already-treated units.
- Prefer cohort-time ATT estimators and proper aggregations:
  - [[Callaway–Sant’Anna estimator]] (group-time ATT, flexible aggregation)
  - [[Sun–Abraham estimator]] (interaction-weighted event study)
- Group-time ATT notation:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1) - Y_t(0) \mid G=g\right], \quad t \ge g
$$
Aggregate by cohort or calendar-time weights and report transparently.

### Dynamic effects (event study)
- Estimate leads/lags to visualize timing:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k \, \mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$
- Omit one lead (e.g., $k=-1$) as the reference. Pre-treatment leads should be near zero if parallel trends holds.

### Doubly robust / machine-learning aided DiD
- Augmented DiD with outcome regression and/or propensity weighting can improve robustness:
  - See [[Doubly Robust estimators]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[double machine learning]] for DiD.

## Common pitfalls

> [!warning] Watch out for
> - Violated parallel trends (different pre-trend slopes or shocks).
> - Contamination: treated units used as controls after adoption in naive TWFE with staggered timing.
> - [[spillovers|Spillovers]] to controls or interference across units.
> - Anticipation (effects start before “Post”).
> - Composition changes (entry/exit) correlated with treatment.
> - Functional form issues (e.g., logs with zeros; re-interpretation of percentage effects).

## Reporting essentials

- Describe design, timing, unit of analysis, and control selection.
- Present the DiD point estimate with clustered SEs and 95% CIs.
- Show pre-trend/event-study plots with confidence bands.
- For staggered adoption: report cohort-time ATTs, aggregation weights, and compare multiple estimators.
- Sensitivity: alternative windows, control sets, functional forms, and placebo tests.

## Minimal code snippets

> [!example] Two-group, two-period DiD

```r
# R (fixest)
library(fixest)
est <- feols(Y ~ D:Post | id + time, cluster = ~id, data = df)
etable(est)
```

```stata
* Stata (reghdfe)
xtset id time
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)
```

```python
# Python (linearmodels)
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
df['DPost'] = df['D'] * df['Post']
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + DPost + EntityEffects + TimeEffects', data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)
```

> [!example] Staggered adoption (modern estimators)

```r
# R: Callaway–Sant’Anna (did)
library(did)
att <- att_gt(yname="Y", tname="time", idname="id", gname="G", data=df, panel=TRUE)
agg_simple <- aggte(att, type="simple")     # overall ATT
agg_dynamic <- aggte(att, type="dynamic")   # event-study style
summary(agg_simple); summary(agg_dynamic)
```

```stata
* Stata: Sun–Abraham style
* Install eventstudyinteract (if needed)
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) vce(cluster id) absorb(id time)
```

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[treated group]]
- [[control group]]
- [[parallel trends assumption]]
- [[two-way fixed effects]]
- [[event study]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[few-cluster corrections]]
- [[covariates]]
- [[Doubly Robust estimators]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[double machine learning]]
- [[spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[composition]]
