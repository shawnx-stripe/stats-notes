---
title: switchback experiment
aliases: [switchback, time-sliced randomization, reversal design, ABBA design, crossover by time]
tags: [experimentation, ab-testing, switchback, time-series, interference, seasonality, hac, clustered, power]
updated: 2025-09-17
---

# switchback experiment

> [!summary] Quick definition
> A switchback experiment randomizes treatment over time blocks (e.g., hours/days) instead of across users, alternating assignment between variants (e.g., A→B→A→B). It’s used when user-level randomization suffers from strong interference or when the mechanism operates at a shared resource (marketplace, cache, ranking, pricing engine). Analysis must account for serial correlation, block effects, and [[seasonality]].

- Typical contexts: marketplaces, search/ranking, ads auctions, pricing throttles, caching, delivery/logistics, capacity-constrained systems.

---

## When to use

- Interference at user level (capacity, queueing, shared inventory) violates SUTVA.
- Treatment can be toggled globally or per shard/cluster, not per user.
- System learns over time (algorithm warm-up, equilibrium effects) and you can alternate conditions.
- You need operational safety while getting unbiased estimates.

See also: [[geo experiment]] for cluster-by-geo designs.

---

## Design

- Unit of randomization: time block (e.g., 15-min, hour, day), optionally per shard/geo (factorial: block × geo).
- Block schedule:
  - Balanced alternation (e.g., ABAB…) or randomized block labels with equal counts.
  - Include “washout” time between switches if carryover exists.
- Block length:
  - Should exceed typical auto-correlation or system response horizon.
  - Trade-off: shorter blocks → more switches (variance) but risk carryover; longer blocks → fewer effective observations.
- Duration:
  - Cover full calendar cycles (day-of-week, pay periods, holidays) to control [[seasonality]].

> [!tip] Randomization
> Randomize the treatment label per block (not just fixed ABAB order) and pre-generate the schedule with a seed for reproducibility.

---

## Threats and assumptions

- Serial correlation: adjacent blocks are correlated; naive iid SEs are invalid.
- Carryover: effects may persist into the next block; consider washout or model lagged effects.
- Seasonality and trends: align windows or include time FE, day-of-week/hour-of-day controls.
- Interference across shards/geos: if multiple streams run in parallel, analyze with cluster-aware methods.

---

## Analysis

- Basic model (single stream/time series):
$$
Y_t = \alpha + \tau D_t + \gamma_b + f(\text{calendar}_t) + \varepsilon_t,
$$
where $D_t$ is treatment-on block indicator, $\gamma_b$ are block fixed effects or coarser time controls. Use HAC/[[Newey–West]] SEs or block-robust SEs.

- With multiple concurrent entities (e.g., geos, shards) in panel form:
$$
Y_{it} = \alpha + \tau D_{it} + \eta_i + \gamma_t + \varepsilon_{it},
$$
cluster SEs by entity (and optionally time), or use HAC across time within entity. For staggered rollouts across entities, consider [[Difference-in-Differences (DiD)]] (and robust staggered estimators).

- Alternatives:
  - Paired/block differences (average of within-block treatment-control contrasts if blocks pair naturally).
  - Event-study style to check pre/post switching dynamics.

> [!warning] Inference
> - Use HAC (e.g., Newey–West) or cluster by block/time as appropriate.
> - If few blocks or few entities, apply [[few-cluster corrections]] or wild cluster bootstrap.

---

## Power and MDE (heuristics)

- Effective sample size under AR(1) correlation ρ:
$$
N_{\text{eff}} \approx N \cdot \frac{1-\rho}{1+\rho}.
$$
- Choose block length to reduce ρ between treated–control comparisons.
- Include variance reduction via pre-period baselines ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]]) on block-level aggregates.

See: [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]].

---

## Instrumentation and logging

- Log assignment per block (namespace, experiment_id, block_id, start/end timestamps).
- Log exposure/outcomes keyed by block_id; align time zones (UTC).
- Include shard/geo identifiers if running crossed designs (block × entity).
- Maintain [[bucketing]]-like reproducibility (seed/salt) for block schedule.
- Use [[exposure logging]] for triggered surfaces even in switchbacks; keep ITT and triggered cohorts well-defined.

---

## Diagnostics

> [!check] Recommended
> - [ ] Balance of covariates and pre-period outcomes across block-level treatment vs control
> - [ ] Autocorrelation diagnostics (ACF/PACF) and block-length sensitivity
> - [ ] Placebo “pseudo-switches” in pre-period (should yield ~0)
> - [ ] Seasonality controls adequate (hour/day/week FE)
> - [ ] Carryover check (treatment lag terms or washout blocks)
> - [ ] [[AA test]] on switchback schedule (no systematic drift), [[Sample Ratio Mismatch (SRM)|SRM]] on block counts

---

## Minimal code snippets

> [!example] R: Build schedule and analyze with HAC SEs

```r
set.seed(42)
# Build hourly blocks for 14 days
blocks <- seq.POSIXt(as.POSIXct("2025-01-01 00:00:00", tz="UTC"),
                     as.POSIXct("2025-01-14 23:00:00", tz="UTC"), by="1 hour")
sched <- data.frame(block = seq_along(blocks), start = blocks)
sched$treat <- sample(c(0,1), nrow(sched), replace = TRUE)  # randomized switchback

# Merge with aggregated outcomes by hour (df has ts 'start', Y, controls)
df <- merge(out_by_hour, sched, by = "start")

# OLS with calendar controls and Newey–West SEs
library(sandwich); library(lmtest); library(lubridate)
df$dow <- wday(df$start, label = TRUE)
df$hod <- hour(df$start)
fit <- lm(Y ~ treat + dow + factor(hod), data = df)
# Choose lag via rule-of-thumb or ACF (e.g., 24)
nw <- NeweyWest(fit, lag = 24, prewhite = FALSE, adjust = TRUE)
coeftest(fit, vcov = nw)["treat", ]
```

> [!example] Python: OLS with Newey–West HAC

```python
import pandas as pd, numpy as np
import statsmodels.api as sm

df['dow'] = df['start'].dt.dayofweek
df['hod'] = df['start'].dt.hour
X = pd.get_dummies(df[['treat','dow','hod']], columns=['dow','hod'], drop_first=True)
X = sm.add_constant(X)
res = sm.OLS(df['Y'], X).fit(cov_type='HAC', cov_kwds={'maxlags':24})
print(res.summary().tables[1].as_text())
```

> [!example] R: Panel switchback (entity × time) with clustered SEs

```r
# df: entity, time (hour), Y, treat (per entity×hour), calendar FE
library(fixest)
est <- feols(Y ~ treat + i(dow) + i(hod) | entity + time, data = df, cluster = ~ entity)
etable(est)
```

> [!example] Stata: Time FE and cluster/HAC

```stata
* Single stream with hourly data; HAC SEs with 24 lags
reg Y treat i.dow i.hod, vce(hac 24)

* Panel (entity × hour) with entity and hour FE, cluster by entity
reghdfe Y treat i.dow i.hod, absorb(entity time) vce(cluster entity)
```

---

## Carryover handling

- Washout: insert neutral blocks between switches (e.g., 15-min buffer).
- Model dynamics: include lagged D or Y, or drop first k minutes of each block in sensitivity.
- Asymmetric effects: check treat→control blocks vs control→treat separately.

---

## Common pitfalls

> [!warning]
> - Blocks too short (carryover, auto-correlation) → biased or underpowered
> - Ignoring [[seasonality]] (e.g., weekday/weekend mix differs by treatment)
> - Fixed ABAB schedule without randomization → confounded with slow trends
> - Using iid SEs → anticonservative inference; prefer HAC or clustering
> - Mixing units (time-sliced run but per-user analysis without clustering)
> - Not logging assignment per block (hard to audit/reproduce)

---

## Reporting essentials

- Block definition and length; schedule generation (seed), washout rules
- Assignment counts by block and total treated vs control time; SRM check
- Calendar controls included (hour/day/week FE), lag length for HAC
- Main effect (τ) with HAC/clustered CIs; sensitivity to block length and washout
- Diagnostics: pre-period placebo switches, ACF/PACF, carryover checks
- Limitations: remaining interference, nonstationarity, unexpected events

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[bucketing]] (time-based keys) · [[exposure logging]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]]
- [[seasonality]] · [[sequential testing]]
- [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- [[geo experiment]]