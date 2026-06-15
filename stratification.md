---
title: Stratification (Subclassification)
aliases:
- stratification
- subclassification
- blocking
- PS stratification
- post-stratification
- Stratification
tags:
- causal-inference
- unconfoundedness
- propensity-score
- matching
- weighting
- design
- surveys
updated: 2025-09-17
---

# Stratification (Subclassification)

> [!summary] Quick definition
> Stratification (subclassification) estimates causal effects by partitioning units into strata based on pre-treatment covariates or a balancing score (often the [[propensity score]]), computing treated–control differences within each stratum, and averaging those differences across strata. Under [[Unconfoundedness]], [[Overlap]], and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], this identifies [[Average Treatment Effect (ATE)]] or [[Average Treatment Effect on the Treated (ATT)]].

- Common implementations:
  - Propensity-score quintiles/deciles (Cochran: 5 strata often remove most bias).
  - Exact/near-exact strata on key covariates (a form of blocking).
  - Survey post-stratification (calibration to known margins; related to [[entropy balancing]]/raking).

## Why use stratification?

- Transparent and simple; balances covariates within strata.
- Less model-dependent than pure regression; more stable than naive [[Inverse Probability Weighting (IPW)|IPW]] when overlap is decent.
- Can increase precision in experiments via stratified randomization (blocking).

## Setup and notation

- Partition the sample into K strata S_k using $b(X)$ (e.g., $b(X)=\hat e(X)$, the PS), with $k=1,\dots,K$.
- Within each stratum, compare outcomes between treated and controls.
- Then average with appropriate weights.

### ATE via stratification (copy-ready)
- Within-stratum contrast:
$$
\hat\Delta_k = \bar Y_{1k} - \bar Y_{0k} = \mathbb{E}[Y \mid D=1, S_k] - \mathbb{E}[Y \mid D=0, S_k].
$$
- Weighted average:
$$
\widehat{ATE} = \sum_{k=1}^K w_k \, \hat\Delta_k, \quad w_k = \Pr(S_k) \approx \frac{N_k}{N}.
$$

### ATT via stratification
- Weight strata by the treated share:
$$
\widehat{ATT} = \sum_{k=1}^K w_k^{(T)} \, \hat\Delta_k, \quad w_k^{(T)} = \Pr(S_k \mid D=1) \approx \frac{N_{1k}}{N_1}.
$$

> [!tip] Choice of K
> - 5 strata (quintiles) often remove most linear PS-related bias (Cochran).
> - Use 5–10 strata in practice; ensure enough treated and controls per stratum and good within-stratum balance.

## Assumptions

- [[Unconfoundedness]]: {Y(1), Y(0)} ⟂ D | X (or given $b(X)$).
- [[Overlap]]: each stratum contains both treated and controls (drop strata that don’t).
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]: no hidden versions and [[No spillovers]].

## Creating strata

- Propensity score: compute $\hat e(X)$, then cut into K quantiles (e.g., qcut).
- Exact/near-exact: stratify by key categorical covariates (e.g., sex×race×age bins), optionally within PS bands.
- For DiD designs: stratify on pre-period outcomes/[[pre-trends]] or cohort, then estimate DiD within strata.

## Diagnostics

> [!check] After stratification
> - Balance within each stratum: standardized mean differences (target |SMD| < 0.1).
> - PS overlap within strata; ensure both groups present.
> - Outcome pre-trends (for DiD) are similar across groups within strata.
> - Stratum sizes: avoid tiny cells; merge adjacent strata if necessary.

> [!warning] Off-support strata
> - If a stratum has only treated or only controls, drop it from ATE (redefine target) or from ATT if it contains no treated. Document changes.

## Variance and inference

- Compute within-stratum variances and aggregate; or bootstrap with resampling at the appropriate level (unit/cluster).
- If clustered data or panel/DiD: use [[clustered standard errors]] or cluster-aware bootstrap; apply [[few-cluster corrections]] when clusters are few.

## Relation to other methods

- [[matching]]: pairs individuals; stratification pools sets of “similar” units.
- [[Inverse Probability Weighting (IPW)|IPW]]: weighting by inverse PS; stratification can be seen as coarse weighting by PS bins.
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]: doubly robust; can be applied within strata or without stratification.
- [[entropy balancing]]: continuous weights to achieve exact moment balance; stratification achieves discrete-bin balance.
- Experiments: “stratified randomization” (blocking) is design-stage stratification to improve precision.

## Stratification in Difference-in-Differences (DiD)

- Create strata using pre-treatment covariates and pre-period outcomes (levels/slopes).
- Estimate DiD within each stratum:
$$
\hat\beta_k = \big(\bar Y^{post}_{1k} - \bar Y^{pre}_{1k}\big) - \big(\bar Y^{post}_{0k} - \bar Y^{pre}_{0k}\big),
$$
then aggregate:
$$
\widehat{ATT}^{DiD} = \sum_k w_k^{(T)} \, \hat\beta_k.
$$
- Still requires [[parallel trends assumption]] within strata; check [[pre-trends]] by stratum.

## Practical workflow

> [!check] Steps
> - [ ] Choose estimand (ATE/ATT) and K.
> - [ ] Estimate PS (or define $b(X)$); form K strata (quantiles or exact bins).
> - [ ] Verify overlap; drop/merge sparse or one-sided strata.
> - [ ] Check within-stratum balance (SMDs); adjust K or $b(X)$ if needed.
> - [ ] Compute within-stratum effects and aggregate with proper weights.
> - [ ] Inference: robust/clustered SEs or bootstrap.

## Minimal code snippets

> [!example] R: PS quintiles and ATE via stratification

```r
# PS model
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
df$ps <- ps_mod$fitted.values

# Create K=5 strata by PS quintiles
K <- 5
df$stratum <- cut(df$ps, breaks = quantile(df$ps, probs = seq(0,1,length.out=K+1)),
                  include.lowest = TRUE, labels = FALSE)

# Within-stratum differences and ATE aggregation
library(dplyr)
ests <- df %>%
  group_by(stratum) %>%
  summarise(
    N = n(),
    y1 = mean(Y[D==1], na.rm = TRUE),
    y0 = mean(Y[D==0], na.rm = TRUE),
    diff = y1 - y0,
    .groups = "drop"
  )
ate_hat <- with(ests, sum((N/sum(N)) * diff))
ate_hat
```

> [!example] Stata: PS, quintiles, stratified ATE (manual)

```stata
logit D X1 X2 c.X3##c.X3 c.X1#c.X2
predict ps, pr
xtile S = ps, nq(5)     // 5 strata

* Within-stratum differences
collapse (count) N = Y (mean) Y1 = Y if D==1 (mean) Y0 = Y if D==0, by(S)
gen diff = Y1 - Y0
sum diff [pw=N]         // weighted average by stratum size (ATE)
```

> [!example] Python: PS quintiles, ATE

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

ps = LogisticRegression(max_iter=2000).fit(df[['X1','X2','X3']], df['D']).predict_proba(df[['X1','X2','X3']])[:,1]
df['ps'] = ps
df['stratum'] = pd.qcut(df['ps'], q=5, labels=False, duplicates='drop')

g = df.groupby('stratum')
ests = g.apply(lambda x: x.loc[x.D==1,'Y'].mean() - x.loc[x.D==0,'Y'].mean()).rename('diff')
weights = g.size() / len(df)
ate_hat = (ests * weights).sum()
print(ate_hat)
```

## Good practice

- Use PS plus key interactions/nonlinearities; consider ML for $b(X)$.
- Keep K modest to avoid tiny cells; merge sparse strata.
- Report balance by stratum and overall; include Love plots or tables.
- For surveys, incorporate base weights and post-stratify to known margins (related to raking/[[entropy balancing]]).

## Common pitfalls

> [!warning] Avoid these
> - Including post-treatment variables in $b(X)$ ([[bad controls]]).
> - Too many strata with tiny cells; unstable estimates and noisy SEs.
> - Poor overlap within strata (one-sided cells); handle by trimming/merging.
> - Assuming stratification alone proves ignorability; it supports but does not guarantee it.

## Copy-ready formulas

- ATE stratified:
$$
\widehat{ATE} = \sum_{k=1}^K \Pr(S_k)\left\{\mathbb{E}[Y \mid D=1,S_k]-\mathbb{E}[Y \mid D=0,S_k]\right\}.
$$

- ATT stratified:
$$
\widehat{ATT} = \sum_{k=1}^K \Pr(S_k \mid D=1)\left\{\mathbb{E}[Y \mid D=1,S_k]-\mathbb{E}[Y \mid D=0,S_k]\right\}.
$$

- DiD within strata:
$$
\hat\beta_k = (\bar Y^{post}_{1k}-\bar Y^{pre}_{1k}) - (\bar Y^{post}_{0k}-\bar Y^{pre}_{0k}),\quad
\widehat{ATT}^{DiD} = \sum_k \Pr(S_k \mid D=1)\,\hat\beta_k.
$$

## Reporting essentials

- Estimand (ATE/ATT), choice of $b(X)$ and K, and stratum construction.
- Overlap decisions (dropped/merged strata) and within-stratum balance diagnostics.
- Effect estimates within strata and aggregated; SEs and clustering level.
- Sensitivity to K, $b(X)$ specification, and overlap rules.

---

## Related notes
- [[propensity score]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[entropy balancing]]
- [[Difference-in-Differences (DiD)]]
- [[pre-trends]]
- [[bad controls]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[raking]]