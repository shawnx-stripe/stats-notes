---
title: Callaway–Sant’Anna Estimator
aliases:
- CS estimator
- att_gt
- csdid
- Callaway-Sant'Anna estimator
- Callaway–Sant'Anna estimator
- Callaway–Sant’Anna
- Callaway-Sant'Anna
- Callaway–Sant’Anna estimator
tags:
- econometrics
- causal-inference
- did
- staggered-adoption
- heterogeneous-effects
updated: 2025-09-17
---

# Callaway–Sant’Anna Estimator

> [!summary] Quick definition
> A Difference-in-Differences approach for [[staggered adoption]] that estimates cohort- and time-specific treatment effects, then aggregates them transparently. It avoids the negative-weight problems of naive [[two-way fixed effects]] when there is [[treatment effect heterogeneity]].

- Core object: [[group-time average treatment effect]]s, denoted $ATT(g,t)$.
- Implementations: R package “did” (`att_gt()`, `aggte()`), Stata `csdid`.

## What it estimates

- Group (cohort) defined by first-treatment time $G=g$.
- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\big[Y_t(1) - Y_t(0) \mid G=g\big], \quad t \ge g
$$

- Aggregations you can report:
  - Overall/simple ATT across groups and post periods
  - Dynamic/event-time effects (relative time $k=t-g$)
  - Calendar-time effects (by $t$)
  - Group (cohort) averages

See: [[group-time average treatment effect]].

## Identification assumptions

- [[parallel trends assumption]] for untreated potential outcomes, using valid comparison units (never-treated and/or not-yet-treated).
- No treatment reversal (monotone adoption).
- [[No spillovers]]/[[interference]] or they are properly modeled.
- No (or modeled) [[Anticipatory effects]]; pre-treatment leads near zero.
- Overlap/positivity: treated cohorts have comparable controls in each $t$.
- Stable [[composition]] or appropriate adjustments (e.g., conditioning, weighting).

> [!tip] Controls choice
> You may use “never-treated” or “not-yet-treated” as the control group. The choice can affect identification and precision; report it.

## How it works (high level)

1) For each treated cohort $g$ and time $t \ge g$, compare outcomes for units in $G=g$ with valid controls at $t$ (never- or not-yet-treated).
2) Identify $ATT(g,t)$ under (conditional) parallel trends, using:
   - Outcome regression, or
   - Inverse probability weighting, or
   - Doubly robust (DR) combination (common default)
3) Aggregate $ATT(g,t)$ to overall or dynamic effects with explicit, user-chosen weights.

> [!note] Benefit
> By constructing valid comparisons for each $(g,t)$, the estimator avoids using already-treated units as controls and sidesteps negative weighting.

## Copy-ready notation

- Group-time effect:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1)-Y_t(0)\mid G=g\right], \quad t \ge g
$$

- Dynamic aggregation (event time $k=t-g$):
$$
\Theta(k) = \sum_{g} w_g(k)\, ATT(g,g+k)
$$
with reported weights $w_g(k)$ (e.g., cohort sizes).

## Practical workflow

> [!check] Steps
> - [ ] Define cohorts $G_i$ (first treatment time; set $G=\infty$ for never-treated).
> - [ ] Choose control set: never-treated and/or not-yet-treated.
> - [ ] Decide on estimation method: IPW, outcome regression, or doubly robust.
> - [ ] Produce $ATT(g,t)$ grid and aggregated effects (overall, dynamic, calendar, group).
> - [ ] Plot [[event study]] dynamics and inspect [[pre-trends]].
> - [ ] Use appropriate [[clustered standard errors]] and, if needed, [[few-cluster corrections]].

## Minimal code snippets

> [!example] R: did (panel data)

```r
library(did)

# df columns: Y (outcome), id (unit), time (period), G (first treatment time; Inf or large value for never)
att <- att_gt(yname = "Y",
              tname = "time",
              idname = "id",
              gname = "G",
              data = df,
              panel = TRUE,
              control_group = "notyet",     # or "nevertreated"
              est_method = "dr",            # "dr", "ipw", or "reg"
              bstrap = TRUE, biters = 999,  # bootstrap for SEs
              clustervars = "id")           # cluster level

# Aggregations
overall <- aggte(att, type = "simple")     # overall ATT
dynamic <- aggte(att, type = "dynamic")    # event-time effects
calendar <- aggte(att, type = "calendar")  # by calendar time
bygroup  <- aggte(att, type = "group")     # by cohort

summary(overall); summary(dynamic)
```

> [!example] R: did (repeated cross-sections)

```r
att_rc <- att_gt(yname = "Y", tname = "time", gname = "G", data = d_rc,
                 panel = FALSE, xformla = ~ X1 + X2,
                 control_group = "notyet", est_method = "dr",
                 bstrap = TRUE, biters = 999)
dyn_rc <- aggte(att_rc, type = "dynamic")
summary(dyn_rc)
```

> [!example] Stata: csdid

```stata
* Panel or repeated cross-sections
csdid Y, ivar(id) time(time) gvar(G) method(dripw)  vce(cluster id)
estat simple     // overall ATT
estat event      // dynamic (event-time) effects
estat group      // cohort averages
estat calendar   // calendar-time effects

* Controls choice (notyet vs never) and bootstrap options exist; see help csdid
```

## Interpretation and reporting

- Report:
  - Control set used: “not-yet-treated” vs “never-treated”
  - Estimation method (IPW, REG, DR)
  - Aggregation scheme(s) and weights
  - Event-study plots with confidence bands
  - Clustering level and number of clusters; small-sample corrections if applicable
- Provide robustness:
  - Alternative control sets and time windows
  - Different covariate sets or weighting schemes
  - Excluding early/late adopters or small cohorts

## Diagnostics

> [!check] What to examine
> - [[pre-trends]]: event-study leads near zero
> - [[Anticipatory effects]]: breaks around announcement vs. implementation
> - Overlap: support for treated vs. controls at each $(g,t)$
> - Sensitivity to control set (“notyet” vs. “never”)
> - [[composition]] stability (entry/exit; reweight if needed)

## Strengths and limitations

- Strengths:
  - Handles [[staggered adoption]] with [[treatment effect heterogeneity]]
  - Transparent comparisons and aggregations
  - Works with panels and repeated cross-sections
- Limitations:
  - Requires sufficient untreated observations for each $(g,t)$
  - Precision can drop with many small cohorts or narrow windows
  - Still relies on (conditional) parallel trends and no interference

## Relation to other estimators

- [[Sun–Abraham estimator]]: robust event study using cohort interactions; conceptually close, focuses on dynamic paths.
- Imputation/Two-stage alternatives: [[Borusyak–Jaravel–Spiess (imputation)]], [[Gardner DID2S]]
- Avoid relying solely on naive [[two-way fixed effects]] when heterogeneity is likely.

## Copy-ready formulas

- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1)-Y_t(0)\mid G=g\right], \ t \ge g
$$

- Dynamic aggregation (event time):
$$
\Theta(k) = \sum_{g} w_g(k)\, ATT(g,g+k)
$$

- Calendar-time aggregation:
$$
\Lambda(t) = \sum_{g \le t} w_{g}(t)\, ATT(g,t)
$$

## Obsidian tips

- Use `$$...$$` for formulas and callouts for summaries.
- Link to related notes with standard wikilinks for quick navigation (see below).

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[staggered adoption]]
- [[group-time average treatment effect]]
- [[Sun–Abraham estimator]]
- [[two-way fixed effects]]
- [[treatment effect heterogeneity]]
- [[parallel trends assumption]]
- [[event study]]
- [[pre-trends]]
- [[Anticipatory effects]]
- [[No spillovers]]
- [[interference]]
- [[composition]]
- [[covariates]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Borusyak–Jaravel–Spiess (imputation)]]
- [[Gardner DID2S]]
