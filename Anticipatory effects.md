---
title: Anticipatory Effects
aliases: [anticipation, no-anticipation assumption, pre-treatment effects, Ashenfelter's dip]
tags: [causal-inference, did, timing, policy-evaluation, assumptions, dynamics]
updated: 2025-09-17
---

# Anticipatory Effects

> [!summary] Quick definition
> Anticipatory effects occur when units change behavior before the official treatment start because they expect the intervention. This violates the “no-anticipation” assumption often invoked in [[Difference-in-Differences (DiD)]] and related designs.

- Classic example: job seekers reduce earnings just before entering training (the "Ashenfelter's dip").
- Why it matters: If pre-period outcomes already respond to future treatment, the [[parallel trends assumption]] fails and the [[DiD estimator]] is biased.

## Formal statement

### No-anticipation assumption (event time)
- Let $G_i$ be the adoption time (first treatment time) and $k = t - G_i$ be event time.
- No anticipation means all pre-treatment leads have zero effect:
$$
\beta_k = 0 \quad \text{for all } k < 0
$$
in an [[event study]] that includes relative-time indicators.

### Potential outcomes view
- Potential outcomes may depend on current treatment $D_{it}$ and on information about future treatment $F_{it}$ (e.g., announcement):
$$
Y_{it} = Y_{it}\big(D_{it}, F_{it}\big)
$$
- No anticipation implies $Y_{it}(0,1) = Y_{it}(0,0)$ for $t < G_i$ (future treatment info does not affect current outcomes).

## How it biases DiD

- If treated units “pre-adjust” upwards (or downwards) relative to controls before $Post_t=1$, the pre-treatment difference is already affected, so the post-minus-pre contrast misattributes part of the change to treatment.
- Direction:
  - Positive pre-effects for treated shrink estimated impacts toward zero.
  - Negative pre-effects (e.g., dips) inflate estimated impacts.

## Diagnosing anticipatory effects

> [!check] Diagnostics (suggestive, not proofs)
> - Event-study leads: estimate and plot coefficients for $k<0$; look for statistically and substantively non-zero effects.
> - Announcement vs. implementation: check for breaks at the announcement date, not only at implementation.
> - Placebos: fake policy dates; unaffected outcomes that should not respond to anticipation.
> - Heterogeneity: stronger pre-effects where advance information is more salient (e.g., media exposure, compliance incentives).

## Design and modeling strategies

### 1) Align the treatment date to information
- Define $Post_t$ from the earliest economically relevant date (e.g., public announcement or eligibility notification), not just implementation.
- Mark an “anticipation window” and code it as treated if theoretical channels suggest effects.

### 2) Exclude ambiguous windows (“donut” around treatment)
- Drop observations within a short window around announcement/implementation to avoid transitional dynamics, then test robustness to window size.

### 3) Use event-study and dynamic DiD
- Include relative-time leads/lags:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k \,\mathbf{1}\{t - G_i = k\} + \varepsilon_{it}
$$
- Interpret non-zero pre-treatment $\beta_k$ as evidence of anticipation or non-parallel trends.

### 4) Instrument or exploit surprise shocks
- Prefer “surprise” policy changes or plausibly exogenous announcement timing.
- Use [[Instrumental Variables (IV)]] if you can isolate unexpected variation in the information arrival process.

### 5) Alternative designs / adjustments
- [[Synthetic Control]] at the announcement date to track pre/post gaps.
- [[Triple Differences (DDD)|DDD]]/[[triple differences]] to difference out a dimension unaffected by anticipation.
- Model explicit exposure to information (e.g., media reach, proximity to HQ) and interact with time.

## Practical guidance

> [!tip] Good practice
> - Pre-register the event date definition and anticipation window.
> - Show main results at implementation and robustness with announcement-defined $Post_t$.
> - Report event-study plots with confidence bands and clearly labeled pre-period leads.
> - Discuss mechanisms for anticipation (eligibility rules, media, incentives).

> [!warning] Common pitfalls
> - Using only implementation as $Post_t$ when announcement effects are likely.
> - Treating pre-trend deviations as “noise” rather than potential anticipation or selection.
> - Post-treatment control selection that amplifies pre-dips (creates [[bad controls]]).

## Minimal code snippets

> [!example] Event-study with leads (R, fixest Sun–Abraham)

```r
library(fixest)
# G = first treatment time; event-study handles leads/lags
es <- feols(Y ~ sunab(G, time) | id + time, cluster = ~id, data = df)
iplot(es)  # inspect pre-treatment leads (k < 0)
```

```stata
* Stata: event-study with eventstudyinteract
* ssc install eventstudyinteract
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id)
* Check coefficients for pre-treatment leads
```

```python
# Python (linearmodels): manual relative-time dummies
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
for k in range(-6,7):
    df[f'rt_{k}'] = ((df.index.get_level_values('time') - df['G']) == k).astype(int)
formula = 'Y ~ 1 + ' + ' + '.join([f'rt_{k}' for k in range(-6,7) if k != -1]) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(formula, data=df).fit(cov_type='clustered', cluster_entity=True)
print(res)
# Inspect rt_k for k < 0
```

> [!example] Coding announcement vs. implementation (pseudo)

```r
df$Post_impl <- as.integer(df$time >= df$impl_date)
df$Post_announce <- as.integer(df$time >= df$announce_date)
# Option A: treat anticipation window as treated
df$Post_any <- as.integer(df$time >= pmin(df$announce_date, df$impl_date))
```

```python
df["Post_impl"] = (df["time"] >= df["impl_date"]).astype(int)
df["Post_announce"] = (df["time"] >= df["announce_date"]).astype(int)
df["Post_any"] = (df["time"] >= df[["announce_date","impl_date"]].min(axis=1)).astype(int)
```

## Copy-ready definitions

- No-anticipation (relative time):
$$
\beta_k = 0 \quad \text{for all } k<0
$$

- Potential outcomes with information:
$$
Y_{it} = Y_{it}\big(D_{it}, F_{it}\big), \quad \text{with no-anticipation: } Y_{it}(0,1)=Y_{it}(0,0)\ \text{for } t<G_i
$$

## When to suspect anticipatory effects

- Publicly announced rollouts, phased eligibility, or compliance campaigns.
- Outcomes that can be quickly adjusted (prices, hours, inventories).
- Settings with strong incentives to time behavior (income tests, thresholds, exams).

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[parallel trends assumption]]
- [[event study]]
- [[Synthetic Control]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]
- [[Instrumental Variables (IV)]]
- [[bad controls]]
- [[policy endogeneity]]
- [[announcement vs implementation]]
- [[staggered adoption]]
- [[pre-trends]]
- [[composition]]