---
title: Targeted Maximum Likelihood Estimation (TMLE)
aliases: [TMLE, targeted maximum likelihood estimation, targeted learning, targeted MLE, tmle]
tags: [causal-inference, semiparametric, doubly-robust, ate, att, nuisance-ml, super-learner]
updated: 2025-09-17
---

# Targeted Maximum Likelihood Estimation (TMLE)

> [!summary] Quick definition
> TMLE is a semiparametric, doubly robust procedure that combines flexible machine learning for nuisance functions with a targeted “fluctuation” step to produce a plug-in estimate of a causal parameter (e.g., [[Average Treatment Effect (ATE)]], [[Average Treatment Effect on the Treated (ATT)]]) that is:
> - Consistent if either the outcome model or the propensity model is correct (doubly robust),
> - Asymptotically efficient if both are correct,
> - Respectful of parameter bounds (e.g., probabilities in [0,1]),
> - Equipped with influence-function–based standard errors.

TMLE is closely related to [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Doubly Robust estimators]], and pairs naturally with ensemble learning (e.g., [[Super Learner]]).

## Setup and assumptions

- Binary treatment A ∈ {0,1}, outcome Y (binary or continuous), pre-treatment covariates X.
- Nuisance functions:
  - Outcome regression: Q0(a,x) = E[Y | A=a, X=x]
  - Propensity score: g0(x) = P(A=1 | X=x) (a [[propensity score]])
- Target parameter (ATE):
$$
\psi_0 = \mathbb{E}\big[ Q_0(1,X) - Q_0(0,X) \big]
$$
- Identification requires:
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
  - [[Unconfoundedness]]: {Y(1), Y(0)} ⟂ A | X
  - [[Overlap]]: 0 < g0(X) < 1 almost surely

TMLE variants exist for [[Average Treatment Effect on the Treated (ATT)|ATT]], longitudinal/dynamic treatments (LTMLE), survival outcomes, missing data, and more.

## TMLE algorithm (binary treatment, ATE)

> [!check] High-level steps
> 1) Initial fits (flexible/ML allowed)
>    - Fit Q(a,x): estimate Q̂(1,x), Q̂(0,x)
>    - Fit g(x): estimate ĝ(x) ≈ P(A=1|X=x)
> 2) Clever covariate
>    - Define for each i:
> $$
> H_i(A_i, X_i) = \frac{A_i}{\hat g(X_i)} - \frac{1-A_i}{1-\hat g(X_i)}
> $$
> 3) Targeting (fluctuation) step
>    - Update Q̂ by fitting a low-dimensional regression of Y on the offset Q̂ with H as the only covariate:
>      - Binary Y (logistic fluctuation):
> $$
> \operatorname{logit}\big(\tilde Q(A_i,X_i)\big) = \operatorname{logit}\big(\hat Q(A_i,X_i)\big) + \epsilon \, H_i
> $$
>      - Continuous Y (least-squares fluctuation):
> $$
> \tilde Q(A_i,X_i) = \hat Q(A_i,X_i) + \epsilon \, H_i
> $$
>    - Estimate ε by MLE/OLS; obtain updated predictions ṼQ(1,X), ṼQ(0,X)
> 4) Plug-in estimate
> $$
> \hat\psi = \frac{1}{N}\sum_{i=1}^N \left\{ \tilde Q(1,X_i) - \tilde Q(0,X_i) \right\}
> $$
> 5) Inference via efficient influence function (EIF)
>    - EIF for ATE:
> $$
> \phi_i = \left[ \frac{A_i}{\hat g(X_i)}\big(Y_i-\tilde Q(1,X_i)\big) - \frac{1-A_i}{1-\hat g(X_i)}\big(Y_i-\tilde Q(0,X_i)\big) \right] + \tilde Q(1,X_i) - \tilde Q(0,X_i) - \hat\psi
> $$
>    - Var(ψ̂) ≈ Var(φ̂)/N; CIs by normal approximation or bootstrap. Use clustered versions for grouped data (see [[clustered standard errors]]).

> [!tip] Cross-fitting
> Use sample-splitting to estimate nuisances on one fold and evaluate on another, rotating across folds. Cross-fitting weakens Donsker conditions and improves validity with modern ML; see [[double machine learning]].

## Relationship to AIPW

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] applies the EIF directly using initial Q̂ and ĝ (“one-step”).
- TMLE performs a targeting step that solves the EIF estimating equation via a minimal update to Q̂, yielding:
  - A plug-in estimate (bounded in parameter space),
  - Small finite-sample gains, often better behavior with probabilities.

Both are doubly robust and asymptotically equivalent under regularity.

## Extensions

- ATT-TMLE: target ψ_ATT = E[Y(1)-Y(0) | A=1] by changing the fluctuation and clever covariate for the ATT estimand.
- Longitudinal TMLE (LTMLE): handles time-varying treatments, confounders, censoring; see R package ltmle.
- Survival TMLE: censoring-adjusted parameters (e.g., restricted mean survival time).
- Continuous/multi-valued A: requires generalized propensity scores and adapted clever covariates.
- TMLE for missing data, mediation, transportability, and stochastic interventions.

## Diagnostics and good practice

> [!check] Recommended
> - [ ] Use rich, pre-treatment X; avoid [[bad controls]].
> - [ ] Employ [[Super Learner]] or strong ML for Q and g; report learners and tuning.
> - [ ] Inspect overlap: PS histograms, extreme ĝ; consider truncation (e.g., clip ĝ to [0.01, 0.99]).
> - [ ] Use cross-fitting; report number of folds and seeds.
> - [ ] Report EIF-based SEs; use clustering if design is clustered.
> - [ ] Sensitivity: alternative learners, PS truncation levels, with/without specific base learners.

> [!warning] Common pitfalls
> - Severe lack of overlap (extreme weights) → unstable estimates; consider trimming or redefining target (e.g., overlap weights).
> - Including post-treatment variables in X.
> - Not using cross-fitting when employing complex ML.
> - Ignoring cluster/time dependence in SEs.

## Minimal code snippets

> [!example] R: tmle (ATE, binary outcome)

```r
# install.packages(c("tmle","SuperLearner"))
library(tmle); library(SuperLearner)

# Y: outcome (0/1), A: treatment (0/1), W: data.frame of covariates
SL_lib <- c("SL.glmnet","SL.xgboost","SL.ranger","SL.glm")

fit <- tmle(Y = df$Y,
            A = df$A,
            W = df[, c("X1","X2","X3")],
            family = "binomial",
            Q.SL.library = SL_lib,
            g.SL.library = SL_lib,
            gbound = c(0.01, 0.99))  # PS truncation

fit$estimates$ATE$psi        # point estimate
fit$estimates$ATE$CI         # 95% CI
fit$estimates$ATE$var.psi    # variance estimate
```

> [!example] R: tmle (ATE, continuous outcome)

```r
fit <- tmle(Y = df$Y, A = df$A, W = df[,c("X1","X2","X3")],
            family = "gaussian",
            Q.SL.library = SL_lib, g.SL.library = SL_lib, gbound = c(0.01,0.99))
fit$estimates$ATE$psi; fit$estimates$ATE$CI
```

> [!example] R: Cross-validated TMLE

```r
# install.packages("cvtmle")
library(cvtmle)
# cvtmle provides cross-validated TMLE and inference utilities; see vignette
```

> [!example] R: Longitudinal TMLE

```r
# install.packages("ltmle")
library(ltmle)
# ltmle handles time-varying treatment/censoring; specify nodes and learners
```

> [!example] Python: zEpid TMLE (ATE)

```python
# pip install zepid statsmodels
from zepid import TMLE
import statsmodels.api as sm

tmle = TMLE(df, exposure='A', outcome='Y')
tmle.exposure_model('X1 + X2 + X3', model='logistic')   # g-model
tmle.outcome_model('A + X1 + X2 + X3', model='logistic')  # Q-model (Y binary)
tmle.fit()
print(tmle.summary())   # ATE estimate with CI
```

> [!example] Stata
Stata does not have a native TMLE command; users often rely on R (tmle/ltmle/tmle3) via interop or implement EIF-based one-step/AIPW.

## Copy-ready formulas

- Clever covariate:
$$
H(A,X) = \frac{A}{\hat g(X)} - \frac{1-A}{1-\hat g(X)}
$$
- Logistic fluctuation:
$$
\operatorname{logit}\big(\tilde Q(A,X)\big) = \operatorname{logit}\big(\hat Q(A,X)\big) + \epsilon \, H(A,X)
$$
- TMLE plug-in (ATE):
$$
\hat\psi = \frac{1}{N}\sum_i \left\{ \tilde Q(1,X_i) - \tilde Q(0,X_i) \right\}
$$
- EIF (ATE):
$$
\phi_i = \frac{A_i}{\hat g(X_i)}(Y_i-\tilde Q(1,X_i)) - \frac{1-A_i}{1-\hat g(X_i)}(Y_i-\tilde Q(0,X_i)) + \tilde Q(1,X_i)-\tilde Q(0,X_i) - \hat\psi
$$

## Reporting essentials

- Estimand (ATE/ATT), outcome family, treatment type
- Learners used for Q and g ([[Super Learner]] library or specific ML), tuning, and cross-fitting details
- Propensity truncation range; overlap diagnostics
- Point estimate, 95% CI, and SE method (EIF; clustered if applicable)
- Sensitivity: alternative libraries, truncation levels, with/without particular learners

## When to use TMLE

- You want doubly robust, efficient estimation with ML nuisances while preserving parameter bounds.
- Complex/high-dimensional X where parametric models are doubtful.
- Longitudinal/dynamic settings (LTMLE) with time-varying treatments and censoring.

---

## Related notes
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Doubly Robust estimators]]
- [[double machine learning]]
- [[propensity score]]
- [[Super Learner]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[bad controls]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Difference-in-Differences (DiD)]]
- [[LTMLE|Longitudinal TMLE]]
- [[influence function]]
- [[influence function|efficient influence function]]