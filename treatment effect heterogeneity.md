---
title: Treatment Effect Heterogeneity
aliases:
- heterogeneous treatment effects
- HTE
- effect heterogeneity
- CATE
- dynamic heterogeneity
- Treatment Effect Heterogeneity
- conditional average treatment effect
tags:
- causal-inference
- econometrics
- did
- panels
- heterogeneity
- machine-learning
updated: 2025-09-17
---

# Treatment Effect Heterogeneity

> [!summary] Quick definition
> Treatment effect heterogeneity means the causal effect varies across units, time, cohorts, exposure intensity, or parts of the outcome distribution. Formally, the effect can depend on covariates X, cohort $G$, event time $k$, or other moderators. Heterogeneity is central in [[Difference-in-Differences (DiD)]], especially with [[staggered adoption]].

## Key estimands

- Conditional average treatment effect (CATE):
$$
\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]
$$

- Cohort-time ATT (staggered DiD):
$$
ATT(g,t) = \mathbb{E}[Y_t(1) - Y_t(0) \mid G = g], \quad t \ge g
$$

- Dynamic (event-time) effect for cohort g:
$$
\theta_g(k) = \mathbb{E}[Y_{g+k}(1) - Y_{g+k}(0) \mid G = g]
$$

- Distributional/quantile effects (illustrative):
$$
QTE_\tau = Q_{Y(1)}(\tau) - Q_{Y(0)}(\tau)
$$
See [[quantile treatment effects]].

> [!tip] Aggregation matters
> Report how you aggregate heterogeneous effects (by cohort, calendar time, or event time). See [[group-time average treatment effect]].

## Why heterogeneity matters in DiD

- With [[staggered adoption]], classic [[two-way fixed effects]] that report a single β can be biased when effects vary across cohorts or over time since treatment.
- Insight: the TWFE coefficient is a weighted average of many 2×2 contrasts, potentially with negative weights. See [[Goodman–Bacon decomposition]].
- Interpretation: even if every cohort’s effect is positive, the single TWFE β can be attenuated or even negative due to weighting artifacts.

## Types of heterogeneity

- Across covariates X (e.g., size, age, baseline level)
- Across cohorts G (early vs. late adopters)
- Dynamic/event-time k (build-up, persistence, fade-out)
- By intensity/dose (continuous or multi-valued treatment)
- Across the distribution of Y (e.g., impacts larger in the upper tail)
- By compliance type in IV settings (e.g., [[Local Average Treatment Effect (LATE)|LATE]] for compliers)

## Identification assumptions (by context)

- DiD: [[parallel trends assumption]] (often conditional on [[covariates]]), no [[Anticipatory effects]], and [[No spillovers]]/[[interference]].
- IV for heterogeneous effects: effects identified for compliers (LATE), not necessarily for the whole population. See [[Instrumental Variables (IV)]] and [[monotonicity]].
- Selection-on-observables: [[Unconfoundedness]] and [[Overlap]], possibly with [[double machine learning]] for robust CATE estimation.

## Estimation strategies

### 1) Covariate interactions (regression-based)
- Let Z be a moderator; estimate:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \delta (D_{it} \times Z_i) + X_{it}'\theta + \varepsilon_{it}
$$
- Interpret β as the effect at Z=0 (center Z), and δ as how the effect changes with Z.
- For DiD with binary timing, use $D_i \cdot Post_t$ and interactions with Z.

> [!warning] Avoid post-treatment moderators
> Do not interact treatment with variables affected by treatment unless you aim to study mechanisms explicitly (risk of [[bad controls]]).

### 2) Dynamic heterogeneity (event study)
- Estimate relative-time leads/lags to trace effects over k:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \ne -1} \beta_k\,\mathbf{1}\{t-G_i=k\} + \varepsilon_{it}
$$
- With staggered timing, prefer [[Sun–Abraham estimator]] or [[Callaway–Sant’Anna estimator]] to avoid contamination. See [[event study]].

### 3) Cohort-time effects (staggered DiD)
- Estimate $ATT(g,t)$ and aggregate transparently:
  - [[Callaway–Sant’Anna estimator]]: group-time ATTs and chosen aggregations (simple, dynamic, calendar-time).
  - Imputation/DID2S methods or cohort-valid event studies.

### 4) Distributional heterogeneity
- Quantile/Distributional DiD to learn effects across the outcome distribution. Link to [[quantile treatment effects]] and decomposition methods.

### 5) ML-based CATE (unconfoundedness designs)
- Meta-learners: T-/S-/X-/R-/DR-learners; [[double machine learning]].
- Tree/forest methods: causal forests; regularized methods for stability.
- Use cross-fitting; report honest performance and out-of-sample checks.

## Minimal code snippets

> [!example] R: DiD with moderating covariate Z (fixest)

```r
library(fixest)
# Binary treatment timing (D:Post) with heterogeneity by Z
est <- feols(Y ~ D:Post + D:Post:Z + X1 + X2 | id + time, cluster = ~id, data = df)
etable(est)
# Marginal effect at Z = z0: beta_hat + delta_hat * z0
```

> [!example] R: Heterogeneous dynamic effects (Sun–Abraham)

```r
library(fixest)
# Allow dynamics to differ by Z via interacted event-study terms (bin or split Z for parsimony)
es <- feols(Y ~ sunab(G, time, ref.p = -1):i(Z_bin) | id + time, cluster = ~id, data = df)
iplot(es)
```

> [!example] R: Group-time ATTs (Callaway–Sant’Anna)

```r
library(did)
att <- att_gt(yname="Y", tname="time", idname="id", gname="G",
              data=df, panel=TRUE, xformla=~ X1 + X2)
dyn <- aggte(att, type="dynamic")     # event-time aggregation
byZ  <- aggte(att, type="group", by="Z_bin")  # subgroup aggregation (if available)
summary(dyn); summary(byZ)
```

> [!example] Python: CATE with EconML (unconfoundedness)

```python
# pip install econml
from econml.dml import CausalForestDML
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV

Y = df['Y'].values
T = df['D'].values   # treatment indicator or continuous
X = df[['X1','X2','Z']].values

est = CausalForestDML(model_t=RandomForestRegressor(),
                      model_y=RandomForestRegressor(),
                      discrete_treatment=True, random_state=123)
est.fit(Y, T, X=X)
tau_hat = est.effect(X)  # CATE estimates tau(x)
```

> [!example] Stata: DiD with moderator

```stata
* TWFE DiD with heterogeneity by Z
reghdfe Y c.Post##i.D c.Z#c.Post#i.D X1 X2, absorb(id time) vce(cluster id)
* Marginal effect at Z=z0: _b[c.Post#1.D] + z0*_b[c.Z#c.Post#1.D]
```

## Diagnostics and reporting

> [!check] Good practice
> - [ ] Pre-specify moderators and aggregation plans to avoid fishing.
> - [ ] Plot [[event study]] dynamics; inspect heterogeneity across cohorts and k.
> - [ ] Report aggregation choices and weights; include cohort-level tables if feasible.
> - [ ] Validate that results are robust to alternative control sets, windows, and weighting.
> - [ ] Use appropriate [[clustered standard errors]]; apply [[few-cluster corrections]] if G is small.
> - [ ] For ML-CATE, use cross-fitting, honest sample splitting, and report out-of-sample fit.

> [!warning] Common pitfalls
> - Interpreting a single TWFE β as “the effect” under obvious heterogeneity.
> - Using already-treated units as controls in staggered designs.
> - Conditioning on post-treatment moderators (creates [[bad controls]]).
> - Overfitting heterogeneity models and cherry-picking subgroups (address with pre-specification and multiple-testing control).

## Copy-ready snippets

- CATE:
$$
\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]
$$

- Cohort-time ATT:
$$
ATT(g,t) = \mathbb{E}[Y_t(1) - Y_t(0) \mid G=g]
$$

- Event-time dynamics:
$$
\theta_g(k) = \mathbb{E}[Y_{g+k}(1) - Y_{g+k}(0) \mid G=g]
$$

## When to use which approach

- Need dynamic paths: robust event studies (Sun–Abraham) and $ATT(g,t)$.
- Need subgroup differences: interact treatment with pre-treatment Z; or subgroup-specific CS estimators.
- Need general CATE under unconfoundedness: ML meta-learners with cross-fitting.
- Need distributional insights: [[quantile treatment effects]] or distributional DiD.

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[staggered adoption]]
- [[Goodman–Bacon decomposition]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[group-time average treatment effect]]
- [[event study]]
- [[parallel trends assumption]]
- [[covariates]]
- [[bad controls]]
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[double machine learning]]
- [[quantile treatment effects]]
- [[composition]]
- [[No spillovers]]
- [[interference]]
- [[few-cluster corrections]]
- [[clustered standard errors]]