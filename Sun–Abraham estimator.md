---
title: Sun–Abraham Estimator
aliases:
- interaction-weighted event study
- SA estimator
- Sun-Abraham
- IWE
- Sun-Abraham estimator
tags:
- econometrics
- causal-inference
- did
- staggered-adoption
- event-study
- heterogeneous-effects
updated: 2025-09-17
---

# Sun–Abraham Estimator

> [!summary] Quick definition
> The Sun–Abraham estimator is an interaction-weighted event-study approach for [[staggered adoption]]. It estimates cohort-specific relative-time (lead/lag) effects and then aggregates them using valid comparisons (never-treated and/or not-yet-treated) to avoid the negative-weight bias of naive [[two-way fixed effects]] under [[treatment effect heterogeneity]].

- Purpose: produce valid dynamic (event-time) DiD estimates when adoption is staggered.
- Outputs: cohort-by-relative-time estimates and aggregated event-time paths with transparent weights.

## Why it’s needed

- Problem with naive TWFE event studies: already-treated units implicitly serve as controls for later-treated ones, causing contamination and possibly negative weights when effects vary across cohorts or over time since treatment. See [[Goodman–Bacon decomposition]].
- SA solution: estimate effects separately by cohort and relative time using valid controls (never- or not-yet-treated), then average across cohorts with explicit weights.

## Setup and notation

- First treatment time (cohort): $G_i \in \{t_0,\dots,t_T\}$ or $G_i=\infty$ if never-treated.
- Relative (event) time: $k = t - G_i$.
- Reference period: typically $k=-1$ is omitted for identification.

Cohort-specific model (conceptually):
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{g} \sum_{k \ne -1} \beta_{gk}\,\mathbf{1}\{G_i=g\}\,\mathbf{1}\{t-G_i=k\} + \varepsilon_{it}
$$
with comparisons restricted to valid controls (never-/not-yet-treated at time t).

Aggregation to interaction-weighted event-time effects:
$$
\beta^{\text{IWE}}_k = \sum_{g} w_g(k)\, \beta_{gk}
$$
where $w_g(k)$ reflect the at-risk cohort shares (report these weights).

## Identification assumptions

- [[parallel trends assumption]] for untreated potential outcomes using valid comparison sets at each (g,t).
- Monotone adoption (no reversals).
- [[No spillovers]]/[[interference]] or they are modeled.
- No or modeled [[Anticipatory effects]] (pre-treatment leads near zero).
- Sufficient overlap (enough never-/not-yet-treated units for each cohort-time).
- Stable [[composition]] or adjustments via [[covariates]]/reweighting.

## Interpretation

- Each $\beta^{\text{IWE}}_k$ is an average treatment effect at relative time k, compared to the omitted period (often $k=-1$).
- Pre-treatment leads ($k<0$) should be near zero if parallel trends and no anticipation hold.
- Post-treatment lags ($k \ge 0$) trace dynamic effects (onset, persistence, fade-out).

> [!warning] Common pitfall
> A standard TWFE event study that does not restrict comparisons to never-/not-yet-treated can be biased with staggered timing.

## Practical workflow

> [!check] Steps
> - [ ] Define cohorts $G_i$ and event time $k=t-G_i$; choose the reference period (commonly $k=-1$).
> - [ ] Use an SA implementation to estimate cohort-specific effects and validly aggregate them.
> - [ ] Plot the event-time path with confidence bands; inspect [[pre-trends]].
> - [ ] Choose binning for long leads/lags to stabilize estimates.
> - [ ] Use appropriate [[clustered standard errors]]; apply [[few-cluster corrections]] if G is small.

## Minimal code snippets

> [!example] R: fixest (sunab)

```r
library(fixest)
# Y: outcome, id: unit, time: period, G: first treatment time (Inf for never-treated)
# ref.p = -1 sets k=-1 as reference. You can bin tails via 'sunab()' options (e.g., 'cohort'/'periodize').
es <- feols(Y ~ sunab(G, time, ref.p = -1) | id + time, cluster = ~id, data = df)
iplot(es)  # dynamic plot with CIs

# Extract and jointly test pre-treatment leads ~ 0
coefs <- broom::tidy(es)
pre <- subset(coefs, grepl("sunab\\(G, time\\)::[-]", term))  # negative k terms
fixest::wald(es, keep = pre$term)  # joint test that leads = 0
```

> [!example] Stata: eventstudyinteract

```stata
* Requires: ssc install eventstudyinteract
* Y outcome, G cohort (first treatment time), time period index, id unit id
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)

* The command estimates cohort-specific leads/lags and aggregates them validly.
* Plot with coefplot or estat tools; jointly test leads near zero.
```

> [!example] Python (sketch)
Python’s mainstream packages don’t yet provide a turnkey SA estimator. Options:
- Use R from Python (rpy2) to call fixest::sunab.
- Implement cohort-valid comparisons manually (nontrivial); prefer R/Stata implementations for correctness.

## Practical choices

- Reference period: $k=-1$ is common; alternatives are fine if stated.
- Tails/binning: group distant times (e.g., $k \le -K$ and $k \ge L$) for precision.
- Control set: not-yet-treated is standard; include never-treated if available and comparable. Report the choice.
- Covariates: can be included; if relying on conditional parallel trends, allow time-varying effects of key X (e.g., X × time FE).

## Inference

- Cluster at the assignment-relevant level (often unit or higher-level cluster).
- With few clusters or few treated clusters, use [[few-cluster corrections]] (e.g., wild cluster bootstrap, CR2/CR3).
- Report number of clusters and treated clusters.

## Strengths and limitations

- Strengths:
  - Robust to [[treatment effect heterogeneity]] with staggered timing.
  - Transparent cohort-specific estimation and aggregation.
  - Clear diagnostics for [[pre-trends]] and dynamics.

- Limitations:
  - Requires sufficient untreated comparison units in each cohort-time cell.
  - Precision can be limited with many small cohorts or long event windows.
  - Still depends on (conditional) parallel trends and no interference.

## Relation to alternatives

- [[Callaway–Sant’Anna estimator]]: also cohort-time based; estimates [[group-time average treatment effect]]s and aggregates (overall, dynamic, calendar). Close in spirit; CS emphasizes ATT(g,t) grids and explicit aggregations.
- Imputation/Two-stage: [[Borusyak–Jaravel–Spiess (imputation)]], [[Gardner DID2S]] provide alternative robust paths.
- Avoid interpreting a single TWFE β as “the effect” when heterogeneity is likely.

## Copy-ready formulas

- Cohort-interacted event-study (conceptual):
$$
Y_{it} = \alpha_i + \gamma_t + \sum_g \sum_{k \ne -1} \beta_{gk} \,\mathbf{1}\{G_i=g\}\,\mathbf{1}\{t-G_i=k\} + \varepsilon_{it}
$$

- Interaction-weighted aggregation:
$$
\beta^{\text{IWE}}_k = \sum_{g} w_g(k)\, \beta_{gk}, \quad \sum_g w_g(k)=1
$$

- Pre-trend diagnostic (leads):
$$
\beta^{\text{IWE}}_k \approx 0 \quad \text{for } k<0
$$

## Reporting essentials

- Define event and reference period; specify binning.
- State control set (never vs. not-yet) and justify comparability.
- Show event-study plots with confidence bands; report joint tests of pre-leads.
- Document clustering and any small-sample corrections.
- If applicable, present cohort-specific results and the weights used in aggregation.

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[two-way fixed effects]]
- [[staggered adoption]]
- [[treatment effect heterogeneity]]
- [[Callaway–Sant’Anna estimator]]
- [[group-time average treatment effect]]
- [[Goodman–Bacon decomposition]]
- [[event study]]
- [[pre-trends]]
- [[parallel trends assumption]]
- [[covariates]]
- [[No spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Borusyak–Jaravel–Spiess (imputation)]]
- [[Gardner DID2S]]