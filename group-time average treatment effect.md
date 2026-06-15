---
title: Group-Time Average Treatment Effect
aliases: [ATT(g,t), group-time ATT, GTATE]
tags: [econometrics, causal-inference, did, staggered-adoption, heterogeneous-effects]
updated: 2025-09-17
---

# Group-Time Average Treatment Effect

> [!summary] Quick definition
> The group-time average treatment effect, denoted $ATT(g,t)$, is the average causal effect for the cohort that first receives treatment in period $g$, measured at calendar time $t \ge g$. It is the core building block in modern DiD methods for [[staggered adoption]] such as the [[Callaway–Sant’Anna estimator]] and underlies robust [[event study]] aggregation.

## Definition and notation

- Cohort (group) by first treatment time: $G_i = g$ if unit $i$ first becomes treated at time $g$; $G_i=\infty$ if never treated.
- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1) - Y_t(0) \mid G = g\right], \quad t \ge g
$$

- Event-time version for cohort $g$ at relative time $k=t-g$:
$$
\theta_g(k) = \mathbb{E}\!\left[Y_{g+k}(1) - Y_{g+k}(0) \mid G = g\right], \quad k \ge 0
$$

> [!tip] Intuition
> Compute a valid DiD for each treated cohort and post period using appropriate controls (never- or not-yet-treated), then aggregate these effects to summarize dynamics or overall impact.

## Identification assumptions (by cell)

For each $(g,t)$:
- [[parallel trends assumption]] for untreated potential outcomes using valid comparisons at time $t$ (never- and/or not-yet-treated).
- Monotone adoption (no treatment reversals).
- [[No spillovers]]/[[interference]] or exposure properly modeled.
- No (or modeled) [[Anticipatory effects]].
- Overlap/positivity: cohort $g$ has comparable controls at $t$.
- Stable [[composition]] or adjustments (e.g., [[covariates]], reweighting).

## Valid comparison sets

- Not-yet-treated at time t: units with $G > t$.
- Never-treated: units with $G=\infty$.
- Many implementations allow choosing “notyet” vs. “nevertreated,” or combining both. The choice affects identification and precision; report it.

## Estimation approaches

- Outcome regression, inverse probability weighting (IPW), or doubly robust (DR) combine to estimate $ATT(g,t)$.
- Implementations:
  - [[Callaway–Sant’Anna estimator]] (R: `did::att_gt`, Stata: `csdid`)
  - Robust event-study variants (e.g., [[Sun–Abraham estimator]]) aggregate cohort-specific relative-time effects into valid averages.
  - Imputation/two-stage alternatives: [[Borusyak–Jaravel–Spiess (imputation)]], [[Gardner DID2S]].

## Aggregation of group-time ATTs

From the $ATT(g,t)$ grid, report transparent summaries with explicit weights.

- Overall/simple ATT:
$$
\text{ATT}^{\text{overall}} = \sum_{g} \sum_{t \ge g} w_{g,t} \, ATT(g,t), \quad \sum_{g,t} w_{g,t}=1
$$

- Dynamic (event-time) effects:
$$
\Theta(k) = \sum_{g} w_g(k)\, ATT(g,g+k), \quad \sum_{g} w_g(k)=1
$$

- Calendar-time effects:
$$
\Lambda(t) = \sum_{g \le t} w_g(t)\, ATT(g,t), \quad \sum_{g \le t} w_g(t)=1
$$

> [!note] Weights
> Default weights often use cohort sizes “at risk” in each cell; always report the chosen scheme (simple, cohort-size, exposure-time, etc.).

## Relationship to TWFE and event studies

- A single [[two-way fixed effects]] coefficient mixes many $(g,t)$ contrasts (and can assign negative weights with heterogeneity). Reporting the $ATT(g,t)$ grid and valid aggregations avoids this problem. See [[Goodman–Bacon decomposition]].
- Robust [[event study]] plots are constructed by aggregating cohort-specific relative-time effects into $\Theta(k)$ with valid comparison sets.

## Diagnostics

> [!check] For each $(g,t)$ and for aggregated results:
> - [ ] [[pre-trends]]: check leads near zero (cohort-wise or aggregated).
> - [ ] Overlap: verify comparable controls exist for each $(g,t)$.
> - [ ] Sensitivity to control choice (never vs. not-yet).
> - [ ] Stability to time windows and exclusion of small/early/late cohorts.
> - [ ] Appropriate [[clustered standard errors]]; use [[few-cluster corrections]] if needed.

## Common pitfalls

> [!warning] Avoid these
> - Aggregating $ATT(g,t)$ without revealing weights.
> - Using already-treated units as controls for later cohorts.
> - Ignoring anticipation when announcements precede implementation.
> - Failing to show dynamic paths and pre-period diagnostics.
> - Relying solely on a single TWFE β when heterogeneity is present.

## Minimal code snippets

> [!example] R: Callaway–Sant’Anna (ATT(g,t) grid and aggregations)

```r
library(did)

# Panel data with columns: Y, id, time, G (first treatment time; Inf or large for never-treated)
att <- att_gt(yname="Y", tname="time", idname="id", gname="G",
              data=df, panel=TRUE,
              control_group="notyet",   # or "nevertreated"
              est_method="dr",          # "dr", "ipw", or "reg"
              bstrap=TRUE, biters=999, clustervars="id")

# The grid of ATT(g,t)
head(att$att.gt)   # data.frame of group-time effects with SEs and t-stats

# Aggregations
overall  <- aggte(att, type="simple")
dynamic  <- aggte(att, type="dynamic")   # event-time Θ(k)
calendar <- aggte(att, type="calendar")  # Λ(t)
bygroup  <- aggte(att, type="group")     # average by cohort g
summary(dynamic)
```

> [!example] Stata: csdid

```stata
csdid Y, ivar(id) time(time) gvar(G) method(dripw) vce(cluster id)

estat group      // cohort-average effects
estat event      // dynamic event-time effects Θ(k)
estat calendar   // calendar-time effects Λ(t)

* Group-time cells are stored; see help csdid for accessing ATT(g,t).
```

> [!example] Robust event-study plot (R, Sun–Abraham via fixest)

```r
library(fixest)
es <- feols(Y ~ sunab(G, time, ref.p = -1) | id + time, cluster = ~id, data = df)
iplot(es)  # valid aggregated event-time coefficients with CIs
```

## Reporting essentials

- Define cohorts $G$, comparison set (never vs. not-yet), and whether panel or repeated cross-sections.
- Present $ATT(g,t)$ summaries: overall, dynamic (Θ(k)), and optionally calendar-time (Λ(t)).
- Show event-study plots with confidence bands and joint tests of leads.
- Report weighting scheme used for aggregation and provide counts “at risk” by $(g,t)$.
- State clustering level(s), number of clusters, and any small-sample corrections.

## Copy-ready formulas

- Group-time ATT:
$$
ATT(g,t) = \mathbb{E}\!\left[Y_t(1) - Y_t(0) \mid G=g\right], \quad t \ge g
$$

- Dynamic aggregation:
$$
\Theta(k) = \sum_{g} w_g(k)\, ATT(g,g+k)
$$

- Calendar-time aggregation:
$$
\Lambda(t) = \sum_{g \le t} w_g(t)\, ATT(g,t)
$$

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[staggered adoption]]
- [[two-way fixed effects]]
- [[Goodman–Bacon decomposition]]
- [[treatment effect heterogeneity]]
- [[parallel trends assumption]]
- [[event study]]
- [[pre-trends]]
- [[covariates]]
- [[composition]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Borusyak–Jaravel–Spiess (imputation)]]
- [[Gardner DID2S]]