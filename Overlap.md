---
title: Overlap
aliases: [overlap, positivity, positivity assumption, overlap assumption]
tags: [causal-inference, identification, propensity-score, weighting, matching, diagnostics]
updated: 2025-09-17
---

# Overlap

> [!summary] Quick definition
> Overlap (positivity) requires that for every covariate profile $x$ used for adjustment, each treatment status has a non-zero probability:
> $$
> 0 < \Pr(D=1 \mid X=x) < 1.
> $$
> Together with [[Unconfoundedness]] and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], overlap is necessary to identify effects like [[Average Treatment Effect (ATE)]] and [[Average Treatment Effect on the Treated (ATT)]].

- Intuition: there must be comparable treated and control units for each relevant $X=x$. Without overlap, you must extrapolate or redefine the target population.

## Formal statements

- Binary treatment:
$$
0 < e(x) = \Pr(D=1\mid X=x) < 1 \quad \text{for all } x \text{ with positive density.}
$$

- Multi-valued/continuous treatment (generalized propensity):
$$
f_{D\mid X}(d \mid x) > 0 \ \text{on the support where effects are targeted.}
$$

- Panel/DiD (conditional trends): require overlap of $X$ distributions across treated vs. control in the pre-period(s), often within each time or cohort slice.

## Why it matters

- No overlap ⇒ impossible to learn counterfactuals for some $x$ without modeling assumptions outside the data (extrapolation).
- Practically, severe non-overlap leads to:
  - Instability in [[Inverse Probability Weighting (IPW)|IPW]] (huge weights)
  - Poor matches in [[matching]]
  - High variance and sensitivity in [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]

## Diagnostics

> [!check] What to examine
> - Propensity score (PS) overlap by $D$: histograms/densities of $\hat e(X)$ for treated vs. control.
> - Weight diagnostics (IPW/DR):
>   - Min/median/max of weights; tail proportions above thresholds.
>   - Effective sample size (ESS): 
> $$
> ESS = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}.
> $$
> - Balance after matching/weighting: standardized mean differences (target |SMD| < 0.1).
> - Common support plots: PS vs. outcome or key covariates by group.
> - For DiD: overlap and balance in pre-period(s) and by cohort/time cells.

> [!warning] Red flags
> - Many treated units with $\hat e(X)$ near 1 or controls near 0 (or vice versa).
> - Extreme weights (e.g., > 20 or 50) concentrated in a few observations.
> - Balance fails even after reweighting/matching.

## Remedies and design choices

### 1) Restrict the target population
- Trimming/truncation of PS: keep units with $\alpha \le \hat e(X) \le 1-\alpha$ (e.g., $\alpha \in [0.01, 0.05]$).
- Common support rules in [[matching]] (calipers) or dropping off-support strata in subclassification.

### 2) Stabilize weights
- Stabilized IPW (for ATE): 
$$
SW_i=\begin{cases}
\frac{\hat p}{\hat e(X_i)}, & D_i=1 \\[2pt]
\frac{1-\hat p}{1-\hat e(X_i)}, & D_i=0
\end{cases},
\quad \hat p=\frac{1}{N}\sum_i D_i.
$$
- Truncate extreme weights at chosen percentiles (report thresholds).

### 3) Alternative weighting schemes
- Overlap weights (ATE on the overlap population): treated weights $\propto 1-\hat e(X)$; control weights $\propto \hat e(X)$ (emphasizes regions with good overlap).
- [[entropy balancing]] (calibration to match covariate moments deterministically).

### 4) Modeling choices
- Richer PS models (interactions, nonlinearities; ML) to better map overlap.
- Switch estimand: prefer [[Average Treatment Effect on the Treated (ATT)]] if overlap is poor on the control side (or vice versa).
- Use alternative designs (e.g., [[Regression Discontinuity Design (RDD)]], [[Instrumental Variables (IV)]]) if overlap is fundamentally absent.

### 5) For DiD
- Narrow time windows; choose comparable [[control group]]s (e.g., same region/industry).
- Reweight controls to match treated pre-period composition; see [[propensity score]] and [[covariates]] with time interactions.

## Minimal code snippets

> [!example] R: PS overlap, trimming, weights, ESS

```r
# PS
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
ps <- ps_mod$fitted.values

# Trim to common support
alpha <- 0.02
keep <- ps >= alpha & ps <= 1 - alpha
df_trim <- df[keep, ]; ps_trim <- ps[keep]

# ATE-IPW weights and ESS
w <- ifelse(df_trim$D == 1, 1/ps_trim, 1/(1-ps_trim))
ESS <- sum(w)^2 / sum(w^2)
summary(w); ESS
```

> [!example] Python: PS overlap and overlap weights

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = df[['X1','X2','X3']].values
ps = LogisticRegression(max_iter=2000).fit(X, df['D']).predict_proba(X)[:,1]
df['ps'] = ps

# Trimming
alpha = 0.02
keep = (ps >= alpha) & (ps <= 1 - alpha)
df_t = df.loc[keep].copy()

# Overlap weights (ATE on overlap population)
df_t['w'] = np.where(df_t['D']==1, 1 - df_t['ps'], df_t['ps'])
ESS = (df_t['w'].sum()**2) / (df_t['w']**2).sum()
print(df_t['w'].describe(), ESS)
```

> [!example] Stata: visualize overlap and trim

```stata
logit D X1 X2 c.X3##c.X3 c.X1#c.X2
predict ps, pr
kdensity ps if D==1, addplot(kdensity ps if D==0) legend(order(1 "Treated" 2 "Control"))

* Trimming
gen keep = (ps >= 0.02 & ps <= 0.98)
keep if keep
```

## Copy-ready snippets

- Positivity (binary treatment):
$$
0 < \Pr(D=1\mid X=x) < 1 \ \text{for all } x \text{ in support.}
$$

- Effective sample size (weights $w_i$):
$$
ESS = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}.
$$

- Overlap weights (heuristic, ATE on overlap population):
$$
w_i \propto 
\begin{cases}
1 - \hat e(X_i), & D_i=1 \\
\hat e(X_i), & D_i=0
\end{cases}
$$

## Common pitfalls

> [!warning] Avoid these
> - Proceeding with huge/unbounded weights without trimming or stabilization.
> - Declaring success from high PS AUC; prediction is not balance. Check balance and overlap.
> - Including post-treatment variables in the PS (see [[bad controls]]).
> - Ignoring overlap cell-by-cell in staggered/[[staggered adoption]] DiD (need overlap for each $(g,t)$ comparison).

## Reporting essentials

- Overlap diagnostics: PS plots by group; weight distributions; ESS; trimming rules.
- Estimand and target population (ATE vs. ATT; overlap population for overlap weights).
- Post-weighting/matching balance (SMDs, variance ratios).
- Inference details (SEs; [[clustered standard errors]] if clustered).
- Sensitivity to trimming thresholds, weight schemes (stabilized, overlap), and PS models.

---

## Related notes
- [[Unconfoundedness]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[matching]]
- [[entropy balancing]]
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[Difference-in-Differences (DiD)]]
- [[staggered adoption]]
- [[control group]]
- [[bad controls]]
- [[clustered standard errors]]
