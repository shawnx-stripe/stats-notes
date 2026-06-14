---
title: Inverse Probability of Censoring Weighting (IPCW)
aliases: [IPCW, inverse probability of censoring weighting, inverse probability of observation weighting, censoring weights]
tags: [causal-inference, missing-data, attrition, selection, panels, longitudinal, msm, did, survival]
updated: 2025-09-17
---

# Inverse Probability of Censoring Weighting (IPCW)

> [!summary] Quick definition
> IPCW reweights the observed data to account for outcome missingness or censoring. Each observed record gets weight equal to the inverse of its probability of being observed, given covariates/history. Under appropriate assumptions (e.g., MAR given observed history), weighted analyses recover the intended estimand in the presence of [[Attrition]]/missing outcomes.

- Use cases:
  - Cross-sectional nonresponse (missing $Y$)
  - Panel/[[Difference-in-Differences (DiD)]] with dropouts over time
  - Longitudinal settings with time-varying censoring (loss to follow-up)
  - Survival analysis with right-censoring (weights can be derived from censoring model/KM)

## Assumptions

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] (well-defined outcomes; no interference unless modeled)
- Missingness model:
  - Cross-section (MAR): $S \perp Y \mid X$ where $S=1$ if observed
  - Longitudinal (sequential MAR): $S_{t} \perp Y_{t} \mid H_t$ (history up to t)
- [[Overlap]]/positivity:
  - Observation probabilities bounded away from 0 and 1: $0 < P(S=1 \mid \cdot) < 1$
- Correctly specified observation/censoring model (or DR methods if using augmentation)

> [!warning] MNAR
> If missingness depends on unobserved outcomes even after conditioning, IPCW alone may not identify the target; consider bounds (e.g., [[Lee bounds]]) or sensitivity analyses.

## Notation

- $S$ (or $S_{it}$): indicator that outcome is observed (1) vs. missing/censored (0)
- $X$ (or $H_t$): baseline covariates (or time-varying history)
- $w^{IPCW}$: inverse probability weight for observation
- In panels, define by unit i and time t.

## Weights (copy-ready)

### Cross-sectional IPCW
- Weight for observed unit $i$:
$$
w_i^{IPCW} = \frac{1}{\hat P(S_i=1 \mid X_i)}.
$$

### Longitudinal IPCW (sequential)
- Cumulative product up to t:
$$
w_{it}^{IPCW} = \prod_{s \le t} \frac{1}{\hat P(S_{is}=1 \mid H_{is})}.
$$

### Stabilized IPCW (variance reduction)
- Cross-sectional stabilized:
$$
\tilde w_i = \frac{\hat P(S_i=1)}{\hat P(S_i=1 \mid X_i)}.
$$
- Longitudinal stabilized:
$$
\tilde w_{it} = \prod_{s \le t} \frac{\hat P(S_{is}=1)}{\hat P(S_{is}=1 \mid H_{is})}.
$$

> [!tip] Weight management
> - Truncate/clamp extreme weights (e.g., to [0.01, 0.99] for probabilities; or cap weights at 99th percentile).
> - Monitor effective sample size (ESS):
> $$
> ESS = \frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
> $$

## How to use IPCW

- Estimate $P(S=1 \mid \cdot)$ with logistic/Probit or ML (cross-fitting optional).
- Compute (stabilized) weights for observed records.
- Fit your outcome model using these weights:
  - Cross-section: weighted mean/regression
  - Panels/DiD: include FE/TWFE with weights; cluster SEs appropriately
  - Longitudinal MSM: combine with treatment weights if needed (product of treatment and censoring weights)

> [!warning] Do not model $S$ using post-outcome variables contemporaneously (avoid leakage); use variables available before or at the time of observation.

## Relation to other methods

- [[Inverse Probability Weighting (IPW)|IPW]] for treatment vs. IPCW for observation; in longitudinal MSMs, combine both (treatment × censoring weights).
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] provide doubly robust handling of missing outcomes by augmenting IPCW with outcome regression.
- [[Lee bounds]] give identification-robust bounds under monotone selection when MNAR attrition is plausible.

## IPCW in DiD and panels

> [!check] Good practice
> - [ ] Model $S_{it}$ using pre-treatment $X$ and history (lags), not future outcomes
> - [ ] Use stabilized weights; truncate extremes
> - [ ] Report counts and attrition rates by group/time; event-study of $S$
> - [ ] Show robustness: balanced panel (complete cases) vs. IPCW vs. DR methods
> - [ ] Cluster SEs at the assignment level; consider [[few-cluster corrections]] if G is small

> [!note] Composition
> IPCW addresses missingness but not all [[composition]] changes (e.g., true entry/exit); consider reweighting controls to treated composition (e.g., [[entropy balancing]]) in tandem.

## Survival/time-to-event context

- If $T$ is failure time and $C$ is censoring time, censoring weights can be built from $\hat G(t)=\Pr(C \ge t)$:
$$
w(t) = \frac{1}{\hat G(t \mid X)}.
$$
- Practical implementations use KM or Cox models for censoring; common in MSMs for longitudinal data.

## Diagnostics

> [!check] Inspect
> - Weight distributions (min/median/max; tail mass)
> - ESS before/after truncation
> - Balance of covariates among observed after weighting
> - Stability of main estimates to weight truncation and alternative $S$ models
> - Event study of $S$ to detect pre-trend selection differences

> [!warning] Red flags
> - Very small predicted observation probabilities for many units (positivity violation)
> - Highly unstable estimates that flip with small truncation changes
> - Using outcome-informed variables to predict $S$ (post-outcome bias)

## Minimal code snippets

> [!example] R: Cross-sectional IPCW

```r
# observed == 1 if Y observed
ipcw_mod <- glm(observed ~ X1 + X2 + D, family = binomial(), data = df)
p_obs <- pmax(pmin(fitted(ipcw_mod), 0.995), 0.005)
df$w_ipcw <- 1 / p_obs

# Weighted outcome model
library(sandwich); library(lmtest)
fit <- lm(Y ~ D + X1 + X2, data = subset(df, observed==1), weights = w_ipcw)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))
```

> [!example] R: DiD with IPCW (panel FE)

```r
library(fixest)
# observed = 1 if outcome is present for (i,t)
ipcw <- glm(observed ~ X1 + X2 + D + factor(time), family = binomial(), data = df)
p <- pmax(pmin(fitted(ipcw), 0.995), 0.005)
df$w_ipcw <- 1/p

est <- feols(Y ~ D:Post | id + time,
             data = subset(df, observed==1),
             weights = ~ w_ipcw, cluster = ~ id)
etable(est)
```

> [!example] Stata: Cross-sectional/DiD IPCW

```stata
* observed = 1 if Y observed
logit observed X1 X2 D i.time
predict phat, pr
gen w_ipcw = 1/phat
sum w_ipcw, detail

* DiD with FE and IPCW (restrict to observed)
reghdfe Y c.Post##i.D [pw=w_ipcw] if observed, absorb(id time) vce(cluster id)
```

> [!example] Python: IPCW (cross-section)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

obs = df['observed'].astype(int).values
X = df[['X1','X2','D']].values
p = LogisticRegression(max_iter=2000).fit(X, obs).predict_proba(X)[:,1]
p = np.clip(p, 0.005, 0.995)
df['w_ipcw'] = 1.0 / p

# Use weights in regression; for panels, include FE with appropriate package
```

> [!example] R: Longitudinal stabilized IPCW (cumulative)

```r
library(dplyr)
# Assume panel df with id, time, observed, and history vars H...
ipcw_t <- glm(observed ~ lag_observed + X1 + X2 + factor(time),
              family = binomial(), data = df)
p_it <- pmax(pmin(fitted(ipcw_t), 0.995), 0.005)

df <- df %>%
  mutate(p_it = p_it) %>%
  group_by(id) %>%
  arrange(time, .by_group = TRUE) %>%
  mutate(w_ipcw_cum = 1/ cumprod(p_it)) %>%
  ungroup()
```

## Copy-ready snippets

- Cross-sectional IPCW:
$$
w_i^{IPCW} = \frac{1}{\hat P(S_i=1 \mid X_i)}
$$

- Longitudinal IPCW:
$$
w_{it}^{IPCW} = \prod_{s \le t} \frac{1}{\hat P(S_{is}=1 \mid H_{is})}
$$

- Stabilized IPCW:
$$
\tilde w_{it} = \prod_{s \le t} \frac{\hat P(S_{is}=1)}{\hat P(S_{is}=1 \mid H_{is})}
$$

- Effective sample size:
$$
ESS = \frac{(\sum_i w_i)^2}{\sum_i w_i^2}
$$

## Reporting essentials

- Definition of missingness/censoring (what is S=0 vs S=1)
- Variables and timing used in the observation model; whether time dummies/history used
- Weight type (stabilized or not), truncation rules, and diagnostics (ESS, range)
- Main estimates with/without IPCW; sensitivity to truncation/specification
- Inference details: SE type, clustering level; [[few-cluster corrections]] if needed
- If combined with treatment weights (MSM), specify combined weight construction

## Common pitfalls

> [!warning] Avoid these
> - Using future information (post-outcome) in the observation model
> - Proceeding with severe positivity violations (tiny observation probabilities) without addressing them
> - Treating IPCW as a panacea under MNAR without sensitivity/bounds
> - Forgetting to restrict the analysis to observed outcomes (S=1) when applying weights

---

Related notes to create:
- [[Attrition]]
- [[selection bias]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Difference-in-Differences (DiD)]]
- [[composition]]
- [[event study]]
- [[Lee bounds]]
- [[entropy balancing]]
- [[Doubly Robust estimators]]
- [[Marginal Structural Models (MSM)]]
- [[LTMLE]]
- [[clustered standard errors]]
- [[few-cluster corrections]]