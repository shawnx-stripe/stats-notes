---
title: Event Study
aliases:
- dynamic DiD
- event-time analysis
- leads and lags
- Event Study
- Event study
tags:
- econometrics
- causal-inference
- did
- panels
- dynamics
- visualization
updated: 2025-09-17
---

# Event Study

> [!summary] Quick definition
> An event study estimates and visualizes dynamic treatment effects by regressing outcomes on relative-time indicators (leads and lags) around the treatment event. Often used with [[Difference-in-Differences (DiD)]] to assess [[pre-trends]] and post-treatment dynamics.

- Typical use: confirm the [[parallel trends assumption]] (pre-treatment leads near zero) and show how effects evolve after treatment.
- Works with single adoption time or [[staggered adoption]] (use modern estimators in the latter).

## Core specification (relative time)

- Let $G_i$ be unit i’s first treatment time; relative time $k = t - G_i$.
- Omit one pre-period, commonly $k=-1$, as reference.
- Copy-ready:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k \,\mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$

- Interpretation:
  - For $k<0$ (leads), $\beta_k$ should be near zero under no [[Anticipatory effects]] and parallel trends.
  - For $k \ge 0$ (lags), $\beta_k$ traces the effect path relative to the reference period $k=-1$.

> [!tip] Binning distant times
> Improve precision and readability by binning tails, e.g., use indicators for $k \le -K$ and $k \ge L$.

## Event study and TWFE DiD

- Implemented within [[two-way fixed effects]] by adding relative-time dummies.
- Caution with [[staggered adoption]]:
  - Naive TWFE event studies can be biased with [[treatment effect heterogeneity]] and when already-treated units act as controls.
  - Prefer robust approaches such as [[Sun–Abraham estimator]] or cohort-time ATT methods like [[Callaway–Sant’Anna estimator]].

> [!warning] Common pitfall
> Using all treated units as controls after they are treated contaminates the comparison and distorts both leads and lags. Use never-treated or not-yet-treated comparisons, or modern estimators.

## What coefficients mean

- Each $\beta_k$ is a difference relative to the omitted period ($k=-1$), not a cumulative effect.
- In logs, $\beta_k$ approximates percentage differences; for count/limited outcomes, interpret carefully or consider alternative links.
- Dynamic average: with staggered timing, plot cohort-specific paths or use interaction-weighted/event-study corrections.

## Diagnostics and design checks

> [!check] Use event studies to:
> - Inspect [[pre-trends]]: leads near zero support parallel trends.
> - Detect [[Anticipatory effects]]: significant pre-period coefficients or breaks at announcements.
> - Characterize dynamics: persistence, fade-out, overshooting.
> - Guide window choice and robustness (e.g., excluding transition periods).

> [!note] Not a proof
> Pre-trend tests have low power; treat them as diagnostics, not confirmation.

## Practical choices

- Reference period: commonly $k=-1$; alternatives okay but be explicit.
- Window: choose symmetric windows around treatment; report robustness to alternatives.
- Weights: for survey/repeated cross-sections, include design weights.
- Inference: cluster SEs at the treatment-assignment level; for few clusters, use [[few-cluster corrections]] or wild bootstrap. Consider multiway or spatial clustering when appropriate. See [[clustering]].

## Robust event-study options for staggered adoption

- Sun–Abraham (interaction-weighted):
  - Estimates cohort-specific relative-time effects and aggregates validly.
- Callaway–Sant’Anna (group-time ATTs):
  - Build an “event-study” by aggregating $ATT(g,t)$ by relative time.

## Minimal code snippets

> [!example] R: Sun–Abraham via fixest

```r
library(fixest)
# G = first treatment time; time = period index
es <- feols(Y ~ sunab(G, time) | id + time, cluster = ~id, data = df)
iplot(es)  # plots leads/lags with CI
```

> [!example] Stata: eventstudyinteract

```stata
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
* Use estat to summarize or export coefficients; plot with coefplot, etc.
```

> [!example] Python: manual relative-time dummies (linearmodels)

```python
from linearmodels.panel import PanelOLS
import numpy as np
df = df.set_index(['id','time'])
rel = df.index.get_level_values('time') - df['G']
K = 5
for k in range(-K, K+1):
    if k != -1:
        df[f'rt_{k}'] = (rel == k).astype(int)
# Bin tails
df[f'rt_le_{-K}'] = (rel <= -K).astype(int)
df[f'rt_ge_{K}']  = (rel >=  K).astype(int)

rhs = ['rt_'+str(k) for k in range(-K, K+1) if k != -1] + [f'rt_le_{-K}', f'rt_ge_{K}']
formula = 'Y ~ 1 + ' + ' + '.join(rhs) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(formula, data=df).fit(cov_type='clustered', cluster_entity=True)
print(res)
```

## Visualization best practices

- Show a zero reference line and 95% confidence bands.
- Mark the treatment start (k=0) clearly.
- Label binned tails (e.g., k ≤ −5, k ≥ 5).
- Keep y-axis scale consistent across related plots for comparability.

## Extensions and variants

- Multiple events per unit: ensure spacing or use only first event; or model overlapping effects with care.
- Announcements vs. implementation: use event time defined by the first economically relevant date; see [[Anticipatory effects]].
- Alternative designs:
  - [[Synthetic Control]] for a single treated aggregate with a dynamic gap plot.
  - [[Triple Differences (DDD)|DDD]]/[[triple differences]] when an additional unaffected dimension can difference out confounders.
- Interference:
  - If [[interference]]/[[No spillovers]] is violated, augment with exposure-based event studies (near vs. far controls; exposure bins).

## Copy-ready formulas

- Baseline event-study:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k \,\mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$

- With binned tails:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k=-K}^{K} \mathbf{1}\{k \ne -1\}\beta_k \,\mathbf{1}\{t-G_i=k\}
+ \beta_{-K^-}\mathbf{1}\{t-G_i \le -K\} + \beta_{K^+}\mathbf{1}\{t-G_i \ge K\} + \varepsilon_{it}
$$

## Reporting essentials

- Specify event definition (e.g., first implementation or announcement), reference period, and window/bins.
- Describe the comparison group (never-treated or not-yet-treated) and justify.
- Document estimator choice (TWFE, Sun–Abraham, Callaway–Sant’Anna) and why.
- Report clustering level and number of clusters.
- Provide pre-trend diagnostics and sensitivity to windows/control sets.

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[parallel trends assumption]]
- [[pre-trends]]
- [[Anticipatory effects]]
- [[staggered adoption]]
- [[Sun–Abraham estimator]]
- [[Callaway–Sant’Anna estimator]]
- [[treated group]]
- [[control group]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]
- [[Synthetic Control]]
- [[interference]]
- [[No spillovers]]
- [[treatment effect heterogeneity]]
- [[Goodman–Bacon decomposition]]
- [[clustering]]
- [[few-cluster corrections]]