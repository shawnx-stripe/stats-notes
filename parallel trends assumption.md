---
title: Parallel Trends Assumption
aliases: [Parallel trends assumption, common trends, parallel-trends, PTA]
tags: [econometrics, causal-inference, did, assumptions, diagnostics]
updated: 2025-09-17
---

# Parallel Trends Assumption

> [!summary] Quick definition
> In the absence of treatment, the average outcome for the [[treated group]] and the [[control group]] would have followed the same trend over time (possibly after conditioning on covariates). This assumption underpins identification in [[Difference-in-Differences (DiD)]].

## Formal statements

### Unconditional parallel trends (two periods)
- Copy-ready:
$$
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=1\big]
=
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=0\big]
$$

### Multi-period version
$$
\mathbb{E}\big[Y_{it}(0) - Y_{is}(0) \mid D_i=1\big]
=
\mathbb{E}\big[Y_{it}(0) - Y_{is}(0) \mid D_i=0\big]
\quad \text{for relevant } s,t
$$

### Conditional parallel trends
- Allow differences in levels, require trends equal after conditioning on $X$:
$$
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=1, X_i\big]
=
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=0, X_i\big]
$$

> [!tip] Connection to DiD
> Under parallel trends, the [[DiD estimator]] identifies an [[Average Treatment Effect on the Treated (ATT)]].

## Intuition

- Treated and control may start at different levels; the key requirement is equal counterfactual changes over time.
- The control group’s observed change proxies the treated group’s unobserved change had treatment not occurred.

## How to assess plausibility

> [!check] Diagnostics (not proofs)
> - Plot pre-treatment outcome paths for treated vs. controls.
> - Estimate an [[event study]] with pre-treatment leads; leads should be near zero.
> - Use alternative control groups or windows; results should be stable.
> - Show balance on pre-treatment covariates and pre-trends; consider conditional trends with [[covariates]] or weighting/matching.
> - Run placebo tests (fake treatment dates, unaffected outcomes).

> [!warning] Caveat
> Failing to reject pre-trend differences does not prove the assumption; tests often have low power. Treat diagnostics as supporting evidence, not confirmation.

## Common threats to parallel trends

- Differential exposure to shocks (macro, sectoral, policy spillovers).
- [[spillovers]] / [[interference]] between groups (treated affects controls).
- [[Anticipatory effects]] shift behavior before treatment.
- Composition changes (entry/exit, migration, selection) correlated with treatment.
- Measurement changes or seasonality differences across groups.
- Nonlinear dynamics where a linear trend adjustment is insufficient.

## Strategies to improve credibility

- Narrow the time window to a stable period around the intervention.
- Refine the [[control group]] to more comparable units (e.g., same region/industry).
- Condition on rich [[covariates]] and allow flexible time interactions (e.g., interactions of key covariates with time fixed effects).
- Use unit-specific trends cautiously; they can help or hurt identification depending on context.
- Consider alternative designs:
  - [[Synthetic Control]] to closely match pre-treatment paths.
  - [[Interrupted Time Series (ITS)]] with a comparison series.
  - Triple differences ([[Triple Differences (DDD)|DDD]]) to difference out an additional confound.
  - Modern DiD estimators for [[staggered adoption]] (e.g., [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]).

## Implications for identification

- If parallel trends holds, DiD identifies ATT:
$$
ATT = \Big(\bar{Y}_T^{\text{post}} - \bar{Y}_T^{\text{pre}}\Big) - \Big(\bar{Y}_C^{\text{post}} - \bar{Y}_C^{\text{pre}}\Big)
$$
- With covariates $X$, interpret it as conditional parallel trends; then use regression adjustment, weighting, or doubly robust DiD.

## Minimal code for pre-trend checks

```r
# R: event-study style with fixest (Sun–Abraham)
library(fixest)
es <- feols(Y ~ sunab(G, time) | id + time, cluster = ~id, data = df)
iplot(es)  # visualize leads/lags; check pre-treatment leads ~ 0
```

```stata
* Stata: event-study with eventstudyinteract
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
* Inspect coefficients on pre-treatment leads
```

```python
# Python: sketch using linearmodels (manual leads/lags)
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
for k in range(-5,6):
    df[f'leadlag_{k}'] = ((df['time'] - df['G']) == k).astype(int)
formula = 'Y ~ 1 + ' + ' + '.join([f'leadlag_{k}' for k in range(-5,6) if k != -1]) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(formula, data=df).fit(cov_type='clustered', cluster_entity=True)
print(res)
# Check pre-treatment coefficients (k < 0) ~ 0
```

## Reporting essentials

- Describe why parallel trends is plausible in your context.
- Show pre-trend plots and event-study estimates with confidence bands.
- Document control-group choice and any adjustments (matching/weighting/covariates).
- Provide robustness with alternative controls/time windows and placebo exercises.

## Copy-ready snippets

- Unconditional:
$$
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=1\big] = \mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=0\big]
$$
- Conditional:
$$
\mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=1, X_i\big] = \mathbb{E}\big[Y_{i,t}(0) - Y_{i,t-1}(0) \mid D_i=0, X_i\big]
$$

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[treated group]]
- [[control group]]
- [[event study]]
- [[pre-trends]]
- [[spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[covariates]]
- [[staggered adoption]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[Synthetic Control]]
- [[Interrupted Time Series (ITS)]]
- [[Triple Differences (DDD)|DDD]]
- [[composition]]