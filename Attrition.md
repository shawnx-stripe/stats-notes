---
title: Attrition
aliases: [dropout, nonresponse, loss to follow-up, missing outcome, panel attrition]
tags: [causal-inference, missing-data, selection, panels, did, survival, robustness]
updated: 2025-09-17
---

# Attrition

> [!summary] Quick definition
> Attrition is loss of observations over time (dropout, nonresponse, censoring). When attrition depends on outcomes or their determinants, estimates can be biased. Handle with design, weighting/modeling (e.g., IPCW, DR methods), bounds (e.g., [[Lee bounds]]), or sensitivity analyses.

- Two stages where it bites:
  - Assignment/estimation: missing outcomes create [[selection bias]]
  - Composition: group/time composition changes (especially in [[Difference-in-Differences (DiD)]])

## Types and taxonomy

- Unit nonresponse (cross-sectional) vs. panel attrition (longitudinal)
- Item nonresponse (some variables missing) vs. outcome nonresponse
- Missingness mechanisms:
  - MCAR: missing unrelated to data → complete-case unbiased (rare)
  - MAR: missing depends only on observed variables → recoverable with weighting/modeling
  - MNAR: missing depends on unobserved outcomes/errors → needs instruments/structure/bounds

Let S indicate outcome observed (S=1). If $S$ depends on $Y(d)$ or unobserved causes of $Y$, then naive estimates using only $S=1$ are biased.

## Why attrition matters

- RCTs: compromises internal validity if differential by arm; ITT remains policy-relevant (with missing outcomes) but precision drops; MNAR can still bias even ITT unless handled.
- DiD/panels: differential exit/entry changes group composition, threatening [[parallel trends assumption]] and producing apparent “effects.” See [[composition]].

## Targets and estimands

- ITT (offer/assignment): average effect of assignment; report regardless of attrition; use consistent missing-data handling.
- ATT/TOT among survivors: risk of “truncation by death” if treatment affects survival/observability; total effect may not be defined for non-survivors; consider principal stratification or report bounds.
- Policy estimands: effect among those reachable/observed under the policy; define clearly.

## Identification strategies

### 1) Inverse probability of censoring/observation weighting (IPCW)

- Model observation $S$ as a function of baseline (and possibly time-varying) covariates/history; weight observed units by inverse of their observation probability.

Copy-ready:
$$
w_i^{IPCW} = \frac{1}{\hat P(S_i=1 \mid X_i)} \quad \text{(cross-section)},
$$
Time-varying (history $H_{it}$):
$$
w_{it}^{IPCW} = \prod_{s \le t} \frac{1}{\hat P(S_{is}=1 \mid H_{is})}.
$$

- Stabilized weights (variance reduction):
$$
\tilde w_{it} = \prod_{s \le t} \frac{\hat P(S_{is}=1)}{\hat P(S_{is}=1 \mid H_{is})}.
$$

- Use IPCW as analysis weights in outcome models (including FE/TWFE DiD). Under MAR given $X$ or history, yields consistent estimates.

### 2) Doubly robust and ML-aided methods

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] / [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] with missingness: combine an outcome regression and a missingness (observation) model; consistent if either is correct.
- Longitudinal g-methods (e.g., MSM with stabilized censoring weights), [[LTMLE]].

### 3) Structural selection models

- Heckman (selection on unobservables) with exclusion restrictions:
$$
\mathbb{E}[Y \mid X,S{=}1] = X\beta + \rho\sigma_\varepsilon \lambda(Z\gamma).
$$
- Requires valid exclusion(s) and distributional assumptions.

### 4) Bounds and sensitivity

- [[Lee bounds]] under monotone selection (treatment weakly increases or decreases selection).
- Pattern-mixture/selection models; delta-based “tipping point” analyses.
- Negative controls / [[placebo test]]s on outcomes that should not be affected.

## Attrition in DiD and event studies

> [!check] Good practice
> - [ ] Track counts per group×time; plot attrition rates by arm/cohort
> - [ ] Reweight controls (and/or treated) to balance pre-period composition; use IPCW if attrition depends on $X$ or history
> - [ ] Check [[pre-trends]] in both outcomes and selection S (event study of S)
> - [ ] Report balanced-panel robustness (restrict to units observed throughout) alongside IPCW- and DR-based estimates
> - [ ] Consider [[Lee bounds]] if differential attrition likely MNAR

> [!warning] Pitfalls
> - Conditioning on “survivors” only (post-treatment selection)
> - Ignoring that treatment affects observability (truncation by death)
> - Severe weight instability (poor [[Overlap]]); address via stabilization/trimming

## Diagnostics

- Attrition rates by group/time; reasons for missingness (tabulate)
- Covariate balance among stayers vs. leavers; model $S$ with baseline/history
- Weight diagnostics: min/median/max; effective sample size (ESS):
$$
ESS = \frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
$$
- Event study of $S$ to detect anticipatory exits or differential selection dynamics

## Minimal code snippets

> [!example] R: IPCW for missing outcomes (cross-section)

```r
# observed == 1 if Y observed
ipcw <- glm(observed ~ X1 + X2 + D + time, data = df, family = binomial())
pobs <- pmax(pmin(fitted(ipcw), 0.995), 0.005)
df$w_ipcw <- 1 / pobs

# Use IPCW in regression (e.g., DiD with FE)
library(fixest)
est <- feols(Y ~ D:Post | id + time, data = subset(df, observed==1),
             weights = ~ w_ipcw, cluster = ~ id)
etable(est)
```

> [!example] R: DR handling of missing outcomes (AIPW/DR learner)

```r
# AIPW-like: model missingness and outcomes; sketch (ate/att depends on design)
# Consider packages: drtmle, ltmle for principled TMLE/DR with missingness
```

> [!example] Stata: IPCW and DiD

```stata
* observed = 1 if Y observed
logit observed X1 X2 D i.time
predict phat, pr
gen w_ipcw = 1 / phat
* DiD with FE and IPCW (subset to observed)
reghdfe Y c.Post##i.D [pw=w_ipcw] if observed, absorb(id time) vce(cluster id)
```

> [!example] Python: IPCW weights

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

obs = df['observed'].astype(int).values
X = df[['X1','X2','D','time']].values
p = LogisticRegression(max_iter=2000).fit(X, obs).predict_proba(X)[:,1]
p = np.clip(p, 0.005, 0.995)
df['w_ipcw'] = 1.0 / p

# Use w_ipcw in your FE/DiD model; cluster SEs appropriately
```

> [!example] R: Lee bounds linkage

```r
# See [[Lee bounds]] page for trimming-based ATT bounds under monotone selection
```

## Copy-ready snippets

- IPCW (cross-section):
$$
w^{IPCW}_i = \frac{1}{\hat P(S_i=1 \mid X_i)}
$$

- IPCW (longitudinal stabilized):
$$
\tilde w_{it} = \prod_{s \le t} \frac{\hat P(S_{is}=1)}{\hat P(S_{is}=1 \mid H_{is})}
$$

- Heckman selected-sample expectation:
$$
\mathbb{E}[Y \mid X,S{=}1] = X\beta + \rho\sigma_\varepsilon \lambda(Z\gamma)
$$

## Reporting essentials

- Attrition rates and reasons by arm/group/time (flow diagrams in RCTs)
- Missingness mechanism assumptions (MCAR/MAR/MNAR); model for $S$ (variables used)
- Weight construction (IPCW), stabilization/trimming rules, and diagnostics (ESS)
- Main estimates (ITT/ATT) with and without IPCW; balanced-panel robustness
- Sensitivity/bounds (e.g., [[Lee bounds]]), and, if used, selection-model exclusions
- Inference details: clustering level; [[few-cluster corrections]] if small G

## Common pitfalls

> [!warning] Avoid these
> - Dropping missing outcomes without analysis (complete-case bias under MAR/MNAR)
> - Conditioning on post-treatment “survivors/users” when estimating total effects
> - Overly complex missingness models with poor overlap (huge weights) without stabilization/trimming
> - Presenting a single “survivor-only” effect as the main causal estimand without acknowledging truncation-by-death issues

---

Related notes to create:
- [[selection bias]]
- [[Lee bounds]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Difference-in-Differences (DiD)]]
- [[composition]]
- [[parallel trends assumption]]
- [[event study]]
- [[Intent-to-Treat (ITT)]]
- [[Treatment-on-the-Treated (TOT)]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Heckman selection]]
- [[truncation by death]]
- [[placebo test]]
- [[few-cluster corrections]]
- [[clustered standard errors]]