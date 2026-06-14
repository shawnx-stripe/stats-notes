---
title: Two-Way Fixed Effects (TWFE)
aliases:
- TWFE
- two way fixed effects
- entity and time fixed effects
- TWFE DiD
- Two-Way Fixed Effects
- Two-way fixed effects
tags:
- econometrics
- causal-inference
- panels
- did
- twfe
updated: 2025-09-17
---

# Two-Way Fixed Effects (TWFE)

> [!summary] Quick definition
> A panel regression that includes fixed effects for entities (units) and time periods to control for time-invariant unit characteristics and common time shocks. Commonly used to implement [[Difference-in-Differences (DiD)]].

## Core specification

- Copy-ready:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + X_{it}'\theta + \varepsilon_{it}
$$

- $\alpha_i$: unit (entity) fixed effects
- $\gamma_t$: time fixed effects
- $D_{it}$: treatment/exposure (binary or continuous)
- $X_{it}$: time-varying covariates
- $\beta$: effect of interest (often interpreted as a DiD effect)

> [!tip] Frisch–Waugh–Lovell view
> TWFE estimates the effect of $D_{it}$ after “partialing out” unit and time FE (and $X_{it}$): regress residualized $Y$ on residualized $D$.

## Relationship to DiD

- With two groups and two periods and binary $D_{it} = D_i \cdot Post_t$, $\hat{\beta}$ equals the [[DiD estimator]].
- With more periods and [[staggered adoption]], classic TWFE with a single $\beta$ can be biased if there is [[treatment effect heterogeneity]] across cohorts or over time.

> [!warning] Goodman–Bacon insight
> In staggered settings, TWFE implicitly averages many 2x2 DiD comparisons with possibly negative weights. See [[Goodman–Bacon decomposition]].

## Identification assumptions

- Unit FE remove time-invariant differences across units.
- Time FE remove shocks common to all units at each time.
- Parallel trends (conditional on FE and covariates) for the untreated potential outcomes:
$$
\mathbb{E}\big[Y_{it}(0) - Y_{is}(0) \mid i, X\big] \text{ is the same for treated and controls}
$$
- No interference/[[spillovers]] across units unless modeled.
- Correct treatment timing and no anticipatory effects, or model leads.
- Strict exogeneity for inference with covariates: $\mathbb{E}[\varepsilon_{it} \mid \alpha_i, \gamma_t, D_{is}, X_{is}] = 0$ for all s.

## When TWFE is safe for causal DiD

- Two groups, two periods (classic DiD).
- Homogeneous treatment effects over cohorts and event time.
- Or when you restructure to use valid comparison groups (e.g., only comparing treated to not-yet-treated) and verify assumptions.

Otherwise prefer modern estimators (below).

## Modern alternatives for staggered adoption

- [[Callaway–Sant’Anna estimator]]: estimates cohort-time ATT, aggregates transparently.
- [[Sun–Abraham estimator]]: interaction-weighted event study that guards against contamination.
- Software helpers:
  - R: `did::att_gt()`, `fixest::sunab()`
  - Stata: `csdid`, `eventstudyinteract`

## Event-study with TWFE

- Dynamic specification:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k \mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$
- Omit one lead (e.g., $k=-1$) as the reference. Inspect pre-treatment leads for near-zero effects to assess [[parallel trends assumption]].
- Use Sun–Abraham style or cohort-specific estimators if staggered timing is present.

## Standard errors and inference

- Cluster at the treatment-assignment level (often unit or higher-level cluster).
- With few clusters, use [[few-cluster corrections]] or wild-cluster bootstrap.
- If both unit and time shocks induce correlation, consider two-way clustering (e.g., Cameron–Gelbach–Miller) or HAC/Driscoll–Kraay as appropriate.

## Practical guidance

> [!check] Before estimating TWFE
> - [ ] Define treatment precisely (timing, intensity).
> - [ ] Choose credible controls (never- or not-yet-treated).
> - [ ] Plot pre-trends and run an [[event study]] with leads.
> - [ ] Check for [[spillovers]]/[[interference]] and [[Anticipatory effects]].
> - [ ] Decide clustering level and document it.

> [!warning] Common pitfalls
> - Using all treated units as controls after they are treated (contamination).
> - Interpreting a single TWFE coefficient with heterogeneous effects.
> - Collinearity when adding unit-specific trends and many dummies without enough variation.
> - Functional-form issues (logs with zeros, nonlinear outcomes).

## Within transformation (intuition)

- Entity demeaning:
$$
\tilde{Y}_{it} = Y_{it} - \bar{Y}_i,\quad \tilde{D}_{it} = D_{it} - \bar{D}_i
$$
- Time demeaning:
$$
\dot{Y}_{it} = \tilde{Y}_{it} - \bar{Y}_t^{\sim},\quad \dot{D}_{it} = \tilde{D}_{it} - \bar{D}_t^{\sim}
$$
- TWFE OLS is equivalent to regressing the twice-demeaned outcome on the twice-demeaned regressor (plus demeaned covariates).

## Minimal code snippets

```r
# R: TWFE with fixest
library(fixest)
est <- feols(Y ~ D + X1 + X2 | id + time, cluster = ~id, data = df)
etable(est)

# Sun–Abraham style event study in fixest
es <- feols(Y ~ sunab(G, time) + X1 | id + time, cluster = ~id, data = df)
iplot(es)  # event-study plot
```

```stata
* Stata: TWFE with reghdfe
xtset id time
reghdfe Y D X1 X2, absorb(id time) vce(cluster id)

* Sun–Abraham style (eventstudyinteract)
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
```

```python
# Python: linearmodels PanelOLS
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
mod = PanelOLS.from_formula('Y ~ 1 + D + X1 + X2 + EntityEffects + TimeEffects', data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res.summary)
```

## Reporting essentials

- State unit and time dimensions, treatment definition, and control selection.
- Show pre-trend plots and event-study estimates with confidence bands.
- Report clustering choice and number of clusters.
- In staggered designs, report cohort-time ATTs and aggregation method; compare TWFE to modern estimators.

## When to use TWFE vs. alternatives

- Use TWFE for:
  - Baseline panel models when treatment is randomized over time within units or effects are plausibly homogeneous.
  - Short panels with clear pre/post and a single adoption time across treated units.

- Prefer alternatives when:
  - Adoption is staggered and effects vary across cohorts or over time.
  - There is concern about negative weighting and contamination. Use [[Callaway–Sant’Anna estimator]] or [[Sun–Abraham estimator]].

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[staggered adoption]]
- [[treatment effect heterogeneity]]
- [[Goodman–Bacon decomposition]]
- [[event study]]
- [[parallel trends assumption]]
- [[spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[few-cluster corrections]]
- [[clustering]]
- [[within transformation]]
- [[demeaning]]