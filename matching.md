---
title: Matching
aliases:
- matching estimators
- nearest neighbor matching
- Matching
tags:
- causal-inference
- unconfoundedness
- design
- weighting
- ATT
- diagnostics
updated: 2025-09-17
---

# Matching

> [!summary] Quick definition
> Matching pairs treated and control units with similar pre-treatment covariates to approximate a randomized experiment under [[Unconfoundedness]] (selection on observables) and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]. It is a design-stage tool to reduce imbalance and improve comparability before estimation.

- Typical goal: estimate [[Treatment-on-the-Treated (TOT)]] / ATT.
- Works best when there is good [[Overlap]] and rich covariates measured pre-treatment.

## Identification and estimand

- Assume Unconfoundedness: {Y(1), Y(0)} ⟂ D | X and [[Overlap]]: 0 < P(D=1|X) < 1.
- ATT via matching:
$$
\widehat{ATT} = \frac{1}{N_1}\sum_{i:D_i=1}\left(Y_i - \sum_{j \in \mathcal{C}(i)} w_{ij}\,Y_j\right)
$$
where C(i) are matched controls for treated i, and weights w_{ij} depend on the matching rule.

> [!note]
> Matching is primarily a design step. Regressions after matching can further adjust residual imbalance, but do not restore identification if unconfoundedness fails.

## Common matching methods

- Exact matching: identical values on key covariates (possible only in small/low-dimensional cases).
- Mahalanobis distance matching: based on covariance-scaled distance in X.
- [[propensity score]] matching (PSM): match on estimated e(X)=P(D=1|X).
- Hybrid: Mahalanobis within PS calipers (often better than PS alone).
- Nearest neighbor (NN): k matches, with or without replacement; common to use replacement.
- Caliper/radius: restrict matches to |distance| ≤ c to avoid poor matches.
- Kernel/Local linear: use many controls with distance-based weights.
- [[coarsened exact matching (CEM)]]: coarsen X into bins, match exactly within strata.
- Genetic/optimal matching: optimize a balance loss function (e.g., optmatch, GenMatch).

> [!tip] Bias–variance trade-offs
> - With replacement reduces bias (find closer matches) at the cost of higher variance.
> - Larger k reduces variance but can increase bias.
> - Calipers reduce bias; too tight calipers may drop many treated (external validity trade-off).

## Diagnostics and balance checks

> [!check] After matching, always report:
> - Standardized mean differences (SMD) for each covariate before vs. after (target |SMD| < 0.1 is common).
> - Variance ratios (treated/control) near 1.
> - eCDF or QQ plots for key covariates.
> - Love plot summarizing balance.
> - Propensity score overlap and common support; drop off-support observations as needed.
> - Effective sample sizes and proportion of treated dropped by calipers.

> [!warning] Pitfalls
> - PSM without checking balance (matching on PS is not sufficient).
> - Including post-treatment variables (creates [[bad controls]]).
> - Poor overlap: extrapolation masquerading as matching.
> - Overfitting PS model without cross-validation; omit key interactions/nonlinear terms.

## Matching plus estimation

- After matching, estimate ATT by:
  - Simple differences in matched pairs/sets (with matching weights), or
  - Outcome regression on the matched sample to improve precision, or
  - Combine with weighting/DR methods (see [[Doubly Robust estimators]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]).

- Standard errors:
  - Abadie–Imbens NN-matching SEs are available for certain algorithms.
  - Naive bootstrap can be invalid for NN matching; use analytic SEs or software that implements valid variance estimators.
  - If data are clustered, use cluster-robust approaches and match within clusters where design dictates.

## Matching in Difference-in-Differences (DiD)

- Use matching to select comparable controls based on pre-treatment covariates and [[pre-trends]] (e.g., match on baseline levels and slope).
- Then run DiD on matched sample:
$$
Y_{it} = \alpha_i + \gamma_t + \beta (D_i \cdot Post_t) + \varepsilon_{it}
$$
- Improves plausibility of [[parallel trends assumption]]; does not replace it.

## Design choices for propensity score

- Specify PS with rich pre-treatment X; allow nonlinearities and interactions (splines, polynomials).
- Check calibration: overlap, SMD balance after matching.
- Consider alternative estimators of e(X): logistic regression, gradient boosting, random forests. Prioritize balance, not PS predictive accuracy.

## When to prefer weighting or balancing

- If overlap is strong and you want to retain all units, consider [[Inverse Probability Weighting (IPW)|IPW]] or [[entropy balancing]].
- Matching is appealing when there are many controls and relatively few treated, and you favor interpretability and design transparency.

## Sensitivity to unobserved confounding

- Matching addresses observed confounding only.
- Conduct sensitivity analysis (e.g., Rosenbaum bounds) to quantify how strong an unobserved bias would need to be to overturn conclusions. See [[Rosenbaum sensitivity]].

## Minimal code snippets

> [!example] R: MatchIt + cobalt

```r
# install.packages(c("MatchIt","cobalt"))
library(MatchIt); library(cobalt)

# Propensity score model
m <- matchit(D ~ X1 + X2 + X3 + I(X1^2) + X1:X2,
             data = df, method = "nearest", distance = "logit",
             replace = TRUE, caliper = 0.2)

summary(m)          # balance numbers
love.plot(m)        # Love plot

dfm <- match.data(m)
# ATT estimate (difference in means with weights)
with(dfm, weighted.mean(Y[D==1], weights[D==1]) - weighted.mean(Y[D==0], weights[D==0]))
```

> [!example] R: CEM

```r
# install.packages("cem")
library(cem)
c <- cem(treatment = "D", data = df, cutpoints = list(X1 = c(10,20,30)))
df$w <- c$w
with(df, weighted.mean(Y[D==1], w[D==1]) - weighted.mean(Y[D==0], w[D==0]))
```

> [!example] Stata: nearest-neighbor PSM and balance

```stata
* ssc install psmatch2, replace
psmatch2 D X1 X2 X3 c.X1#c.X1 c.X1#c.X2, outcome(Y) neighbor(1) caliper(0.2) common
pstest X1 X2 X3, both graph   // balance diagnostics

* Or built-in teffects
teffects psmatch (Y) (D X1 X2 X3), atet vce(robust)
```

> [!example] Python: simple PS + NN matching (sketch)

```python
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

X = df[['X1','X2','X3']].values
ps = LogisticRegression(max_iter=2000).fit(X, df['D']).predict_proba(X)[:,1]
df['ps'] = ps

treated = df[df.D==1].copy()
control = df[df.D==0].copy()
nbrs = NearestNeighbors(n_neighbors=1).fit(control[['ps']])
dist, idx = nbrs.kneighbors(treated[['ps']])
matched_ctrl = control.iloc[idx.flatten()].copy()
att = (treated['Y'].reset_index(drop=True) - matched_ctrl['Y'].reset_index(drop=True)).mean()
print(att)
# Add calipers, with-replacement, and balance checks in real use.
```

## Copy-ready checklists

> [!check] Matching workflow
> - [ ] Define estimand (ATT) and pre-treatment covariates X
> - [ ] Choose method (NN/Mahalanobis/PSM/CEM) and tuning (k, caliper, with-replacement)
> - [ ] Estimate PS if using PSM; include nonlinearities/interactions
> - [ ] Perform matching; ensure common support
> - [ ] Assess balance (SMDs, variance ratios, eCDF, Love plot)
> - [ ] Estimate ATT with valid SEs; consider outcome regression on matched sample
> - [ ] Sensitivity analysis to unobserved confounding

> [!warning] Common pitfalls
> - Matching on variables affected by treatment (post-treatment bias)
> - Declaring success based on PS overlap alone without balance tables
> - Ignoring units dropped by calipers (changes target population)
> - Using naive bootstrap for NN matching SEs

## Reporting essentials

- Describe covariates, method, tuning, replacement, calipers, and matching ratio.
- Provide balance tables/plots pre/post matching.
- State how many units were dropped and the target population implied.
- Report ATT with appropriate SEs and sensitivity analyses.
- If used with DiD, show [[pre-trends]] and justify [[parallel trends assumption]].

---

Related notes to create:
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[entropy balancing]]
- [[Doubly Robust estimators]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Rosenbaum sensitivity]]
- [[bad controls]]
- [[Difference-in-Differences (DiD)]]
- [[pre-trends]]
- [[covariates]]
- [[Treatment-on-the-Treated (TOT)]]
- [[clustered standard errors]]
