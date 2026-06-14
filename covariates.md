---
title: Covariates
aliases:
- controls
- X
- regressors
- confounders
- Covariates
tags:
- econometrics
- causal-inference
- did
- panels
- regression
- design
updated: 2025-09-17
---

# Covariates

> [!summary] Quick definition
> Covariates (often denoted X) are observed characteristics included in a model to improve precision, adjust for differences between groups, or identify causal effects when assumptions (e.g., [[parallel trends assumption]]) are assumed to hold conditional on X.

- Roles in practice:
  - Precision: reduce residual variance and tighten CIs.
  - Adjustment: support conditional identification (e.g., conditional parallel trends).
  - Heterogeneity: interact with treatment to study effect variation.
- In design-based settings (e.g., strong [[Difference-in-Differences (DiD)]] or [[Regression Discontinuity Design (RDD)]]), covariates help but do not replace identification.

## Covariates in DiD and panels

### Baseline TWFE with covariates
- Copy-ready:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + X_{it}'\theta + \varepsilon_{it}
$$
- Here, $X_{it}$ are time-varying controls. With panel unit FEs ($\alpha_i$), time-invariant covariates are absorbed.

### Conditional parallel trends
- Require that untreated potential-outcome trends are equal given X:
$$
\mathbb{E}\!\big[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i, X_i\big] \text{ is equal across groups}
$$
- Practical implementation often interacts key covariates with time FE to allow their effects to vary over time:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \sum_j \phi_j \big(X_{ij} \times \gamma_t\big) + \varepsilon_{it}
$$

> [!tip] When to interact X with time
> If covariates’ effects change over time (common in macro/industry settings), allowing $X \times$ time FE makes “conditional trends” more plausible.

### Repeated cross-sections DiD
- Without tracking units, include group and time FE, and adjust for composition via X and weights:
$$
Y_{gt} = \alpha_g + \gamma_t + \beta \big(Treat_g \cdot Post_t\big) + X_{gt}'\theta + \varepsilon_{gt}
$$
- Consider survey weights and compositional reweighting (e.g., [[entropy balancing]], [[Inverse Probability Weighting (IPW)|IPW]]).

## What covariates to include

- Pre-treatment covariates plausibly related to outcomes and treatment selection.
- Flexible time controls (e.g., year FE), seasonality dummies, or group-specific trends if justified.
- Baseline outcomes in repeated cross-sections (not panel with unit FE; baseline levels are collinear with $\alpha_i$).
- Avoid post-treatment variables unless explicitly modeling mechanisms; see [[bad controls]] and [[post-treatment conditioning]].

> [!warning] Do not “control away” the effect
> Conditioning on mediators or variables affected by treatment can bias estimates. Prefer designs that isolate exogenous variation or use mediator analysis explicitly.

## Covariates vs. weighting/matching

- Conditioning (regression) and weighting/matching target similar goals under [[Unconfoundedness]]. In DiD:
  - Reweighting to align pre-treatment composition supports conditional parallel trends; see [[propensity score]], [[entropy balancing]].
  - Doubly robust DiD combines outcome regression with weighting; see [[Doubly Robust estimators]] and [[Augmented Inverse Probability Weighting (AIPW)|AIPW]].

## Effect heterogeneity with covariates

- Interact treatment with moderators Z to learn how effects vary:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \delta \,(D_{it} \times Z_{i}) + X_{it}'\theta + \varepsilon_{it}
$$
- Interpret $\delta$ as differential effect for a one-unit increase in $Z$ (relative to reference). Consider centering Z for interpretability.

## Good practice

> [!check] Checklist
> - [ ] Use pre-treatment covariates; document timing.
> - [ ] If relying on conditional trends, allow $X \times$ time FE.
> - [ ] Show covariate balance and distributional checks over time ([[composition]]).
> - [ ] Consider reweighting to a reference composition (treated-pre) and compare results.
> - [ ] Cluster SEs at the assignment level; see [[clustered standard errors]].
> - [ ] Pre-register which covariates and interactions you plan to include.

> [!tip] High-dimensional X
> Use regularization (lasso) or ML for nuisance components with orthogonalized targets; see [[double machine learning]].

## Common pitfalls

> [!warning] Avoid these
> - Including variables measured after treatment begins (post-treatment bias).
> - Over-controlling with colliders that open backdoor paths.
> - Interacting X with time without sufficient data, causing multicollinearity and imprecision.
> - Assuming covariate adjustment “fixes” violations of [[No spillovers]]/[[interference]] or mis-timed treatment.

## Minimal code snippets

> [!example] R: TWFE with time-varying covariates and X×time interactions

```r
library(fixest)
# Baseline with covariates
est1 <- feols(Y ~ D:Post + X1 + X2 | id + time, cluster = ~id, data = df)

# Allow effects of key covariates to vary over time (conditional trends)
est2 <- feols(Y ~ D:Post + i(time, X1) + i(time, X2) | id + time, cluster = ~id, data = df)

# Heterogeneity by Z
est3 <- feols(Y ~ D:Post + D:Post:Z + X1 + X2 | id + time, cluster = ~id, data = df)
etable(est1, est2, est3)
```

> [!example] Stata: covariates and interactions with time

```stata
* Baseline TWFE with covariates
reghdfe Y c.Post##i.D X1 X2, absorb(id time) vce(cluster id)

* Interact X with time FE (flexible conditional trends)
xi: reghdfe Y c.Post##i.D i.time#c.X1 i.time#c.X2, absorb(id time) vce(cluster id)

* Heterogeneity by Z
reghdfe Y c.Post##i.D c.Z#c.Post#i.D X1 X2, absorb(id time) vce(cluster id)
```

> [!example] Python: PanelOLS with covariates and manual time interactions

```python
from linearmodels.panel import PanelOLS
import pandas as pd

df = df.set_index(['id','time'])
# Create time dummies and interact with key covariates
time_d = pd.get_dummies(df.index.get_level_values('time'), prefix='t', drop_first=True)
for col in ['X1','X2']:
    for tcol in time_d.columns:
        df[f'{col}_{tcol}'] = df[col] * time_d[tcol].values

rhs = ['D', 'Post', 'D:Post', 'X1', 'X2'] + [c for c in df.columns if c.startswith('X1_t_') or c.startswith('X2_t_')]
formula = 'Y ~ 1 + ' + ' + '.join(rhs) + ' + EntityEffects + TimeEffects'
res = PanelOLS.from_formula(formula, data=df).fit(cov_type='clustered', cluster_entity=True)
print(res)
```

> [!example] Doubly robust DiD (R, sketch)

```r
# Outcome model + propensity for D (or not-yet-treated) then AIPW-style DiD
# See packages: drdid, did, grf (causal forests) for nuisance estimation and orthogonalization
library(drdid)
out <- drdid::drdid_rc(Y = df$Y, post = df$Post, treat = df$D, covariates = df[,c("X1","X2")])
summary(out)
```

## Copy-ready snippets

- TWFE with X and flexible time effects of X:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \sum_j \phi_j \big(X_{ij} \times \gamma_t\big) + \varepsilon_{it}
$$

- Conditional parallel trends:
$$
\mathbb{E}\!\big[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=1, X_i\big] = \mathbb{E}\!\big[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=0, X_i\big]
$$

- Treatment heterogeneity by Z:
$$
\frac{\partial \mathbb{E}[Y_{it}]}{\partial D_{it}} = \beta + \delta Z_i
$$

## Practical notes

- Standardize continuous covariates for stability in interactions.
- Handle missing X via explicit missing indicators or imputation; document the strategy.
- In panels, time-invariant X are absorbed by unit FE; their interactions with time or treatment can still be identified.
- For seasonality and calendar effects, include appropriate dummies (month, week-of-year) and consider interactions with geography/industry.

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[parallel trends assumption]]
- [[pre-trends]]
- [[event study]]
- [[matching]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[entropy balancing]]
- [[Doubly Robust estimators]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[double machine learning]]
- [[bad controls]]
- [[post-treatment conditioning]]
- [[composition]]
- [[clustering]]
- [[clustered standard errors]]