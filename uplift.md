---
title: uplift
aliases: [uplift modeling, incremental response, incremental lift, CATE modeling]
tags: [uplift, causal-inference, treatment-effect-heterogeneity, personalization, policy-learning, evaluation, qini, auuc]
updated: 2025-09-17
---

# uplift

> [!summary] Quick definition
> Uplift is the incremental effect of a treatment for a specific context X, commonly the Conditional Average Treatment Effect (CATE):
> $$
> \tau(x) = \mathbb{E}[Y(1)-Y(0)\mid X=x].
> $$
> Uplift modeling ranks or segments units by τ(x) to target interventions to those most likely to benefit, and is evaluated by uplift-specific metrics (Qini, AUUC) or by policy value via off-policy evaluation.

- Use cases: marketing targeting, pricing/promo selection, churn interventions, clinical decision rules, feature rollouts.
- Outputs: scores τ̂(x), uplift segments, and deployable policies (e.g., treat top b%).

---

## Setup and notation

- Binary treatment D ∈ {0,1}, outcome Y (binary or continuous), covariates X.
- Individual uplift (CATE): τ(x) as above.
- Segmented uplift: expected lift within a group/leaf S: τ(S) = E[Y(1)−Y(0) | X∈S].
- Policy: π(x) = 1{τ̂(x) > c} or treat top-b% by τ̂ for a budget b.

> [!note] Identification
> - Randomized experiments: propensities known (P(D=1|X)=p), clean identification.
> - Observational data: requires [[Unconfoundedness]] and [[Overlap]]; prefer doubly robust + cross-fitting (see [[double machine learning]]).

---

## When to use uplift modeling

- You need to decide who to target, not just whether there is an average effect.
- Treatment has costs/constraints; uplift helps maximize value subject to budgets/fairness.
- Effects are heterogeneous and average treatment effect masks large differences.

---

## Learning uplift (modeling approaches)

### Meta-learners (two-stage)
- T-learner: fit separate models m̂1(x)=E\[Y|D=1,X], m̂0(x)=E\[Y|D=0,X]; τ̂(x)=m̂1−m̂0.
- S-learner: one model m̂(x,D); τ̂(x)=m̂(x,1)−m̂(x,0).
- X-learner: T-style + imputation of pseudo-outcomes; often strong with imbalance.
- R-/DR-learner: orthogonalized losses with propensity ê and outcome m̂; doubly robust, recommended with ML.
- Tips: always use cross-fitting for out-of-fold predictions to reduce bias.

### Tree- and forest-based
- Uplift trees: splits chosen to maximize uplift separation between leaves; simple and interpretable.
- Causal trees/forests (e.g., grf): estimate τ̂(x) nonparametrically; good default with uncertainty estimates.
- Policy trees: learn a tree that directly optimizes value (see [[policy tree]]).

### Doubly Robust / DML
- Use [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]-style scores or [[double machine learning]] for τ̂(x) with orthogonalization:
  - Nuisances: ê(X), m̂0(X), m̂1(X).
  - Cross-fitting prevents overfitting bias; robust to single-model misspecification.

---

## Evaluation (offline)

### Uplift curves and Qini
- Sort units by predicted uplift τ̂(x) descending; plot cumulative incremental outcome vs proportion targeted.
- Qini (incremental Gini-like) coefficient: area between uplift curve and baseline (random), larger is better.
- AUUC: Area Under the Uplift Curve; related to Qini (with different normalization).

### Policy value via Off-Policy Evaluation (OPE)
- When action-specific logging propensities $p_i(a)=\Pr(D_i=a\mid X_i)$ are known/logged:
  - IPS:
  $$
  \widehat{V}_{IPS}(\pi)=\frac{1}{N}\sum_i \frac{\mathbf{1}\{\pi(X_i)=D_i\}}{p_i(D_i)}Y_i
  $$
  - DR (recommended):
  $$
  \widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \left[m_{\pi(X_i)}(X_i)+\frac{\mathbf{1}\{\pi(X_i)=D_i\}}{p_i(D_i)}\big(Y_i-m_{D_i}(X_i)\big)\right].
  $$
- Use bootstrap or IF-based CIs; cluster-aware if data are clustered.

### Calibration and sanity
- Within score deciles, treatment propensity should match design (e.g., ≈ 50/50 in RCTs).
- Gain stability across folds/splits; uplift in top bins versus random baseline.

> [!warning] Offline metrics do not guarantee online lift—validate via A/B or switchback with guardrails.

---

## Practical workflow

> [!check]
> - [ ] Train/validation/test splits (or K-fold cross-fitting)  
> - [ ] Choose approach (DR-/R-learner; causal forest) and tune with CV  
> - [ ] Diagnose overlap (propensity tails), cap weights if needed  
> - [ ] Evaluate: uplift curve, Qini/AUUC on a holdout; OPE for candidate policies  
> - [ ] Select a policy (threshold/budgeted treatment; [[policy learning]])  
> - [ ] Validate in an online experiment; monitor guardrails and [[Sample Ratio Mismatch (SRM)|SRM]]

---

## Data requirements and identification

- Randomized experiments: best setting; use assignment propensities and ensure clean exposure (see [[exposure logging]]).
- Observational data:
  - Need [[Unconfoundedness]] and [[Overlap]]; include rich pre-treatment covariates.
  - Prefer doubly robust DML with cross-fitting; trim or restrict tails where ê(X) near 0/1.
- Triggered experiments: define and use pre-trigger baselines; avoid triggered bias by symmetric eligibility.

---

## Diagnostics and pitfalls

> [!warning] Common pitfalls
> - Training predictive models for Y (not causal) and treating differences as uplift  
> - No cross-fitting → overfitting spuriously inflates uplift metrics  
> - Severe lack of overlap → unstable IPS/DR and misleading τ̂(x)  
> - Data leakage (post-treatment features) in X or nuisance models  
> - Evaluating only by accuracy/AUC (irrelevant)—use uplift-specific metrics or OPE  
> - Nesting bias: using the same data to select policy and to evaluate without proper splits

> [!check] Diagnostics
> - Propensity histograms; effective sample size (ESS) of IPS weights  
> - Decile table of observed lift with CIs; random baseline check  
> - Placebo tests (pre-period “treatment” or negative outcomes)  
> - Stability across time, cohorts, and segments; fairness audits

---

## Minimal code snippets

> [!example] Python: DRLearner (econml) + uplift curve + policy value

```python
import numpy as np, pandas as pd
from econml.dr import DRLearner
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

X = df[['X1','X2','X3']].to_numpy()
T = df['D'].to_numpy().astype(int)
Y = df['Y'].to_numpy()
e = df.get('propensity_treated', pd.Series(np.full(len(Y), T.mean()))).to_numpy()

dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(n_estimators=500, random_state=0))
dr.fit(Y, T, X=X)
tauhat = dr.effect(X)

# Uplift curve (simple)
order = np.argsort(-tauhat)
cum_t = T[order].cumsum()
cum_y = Y[order].cumsum()
# For RCT with p≈0.5, estimate incremental lift vs baseline ~ p
# (Use a dedicated uplift metric package for precise Qini/AUUC.)

# Policy value via DR OPE (treat top 30%)
b = 0.3
thr = np.quantile(tauhat, 1-b)
pi = (tauhat >= thr).astype(int)
# Approximate m0,m1 via DRLearner's models (implementation-dependent)
# Here we refit simple models for demo
from sklearn.model_selection import train_test_split
idx0 = T==0; idx1 = T==1
m0 = RandomForestRegressor().fit(X[idx0], Y[idx0]).predict(X)
m1 = RandomForestRegressor().fit(X[idx1], Y[idx1]).predict(X)
p_logged = np.where(T == 1, e, 1 - e)
m_logged = np.where(T == 1, m1, m0)
m_policy = np.where(pi == 1, m1, m0)
V_DR = np.mean(m_policy + (pi == T) / p_logged * (Y - m_logged))
print("DR policy value:", V_DR)
```

> [!example] Python: uplift tree (scikit-uplift or causalml)

```python
# pip install scikit-uplift
from sklift.models import ClassTransformation
from sklift.metrics import qini_auc_score
from sklearn.ensemble import RandomForestClassifier

# For binary Y, ClassTransformation converts to uplift by modeling transformed target
model = ClassTransformation(RandomForestClassifier(n_estimators=500, random_state=0))
model.fit(X, y=Y, treatment=T)
uplift_score = model.predict_uplift(X)
print("Qini AUC:", qini_auc_score(Y, uplift_score, T))
```

> [!example] R: causal forest (grf) + binary policy tree

```r
# install.packages(c("grf","policytree"))
library(grf); library(policytree)
X <- as.matrix(df[, c("X1","X2","X3")]); Y <- df$Y; W <- df$D

cf <- causal_forest(X, Y, W)
tauhat <- predict(cf)$predictions

# Reward matrix columns are actions 0 and 1. Treat when estimated gain is positive.
Gamma <- cbind(control = 0, treat = tauhat)
pt <- policy_tree(X, Gamma, depth = 2, min.node.size = 200)
print(pt)
pi_hat <- predict(pt, X)
```

---

## Copy-ready formulas

- Uplift (CATE):
$$
\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x].
$$
- DR score (binary treatment):
$$
\gamma_i = (m_1 - m_0) + \frac{D_i(Y_i - m_1)}{e} - \frac{(1-D_i)(Y_i - m_0)}{1-e}.
$$
- Policy value (DR OPE):
$$
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \left[m_{\pi(X_i)}(X_i)+\frac{\mathbf{1}\{\pi(X_i)=D_i\}}{p_i(D_i)}(Y_i-m_{D_i}(X_i))\right].
$$

---

## Reporting essentials

- Data design (RCT vs observational), propensities (known/estimated), overlap diagnostics
- Model class (meta-learner/forest/tree), cross-fitting scheme, hyperparameters
- Uplift metrics (Qini/AUUC) with confidence intervals or bootstraps
- Policy definition (threshold/budget), OPE value and uncertainty; fairness/constraint checks
- Online validation plan (A/B or switchback), guardrails, and monitoring
- Sensitivity to learners, thresholds, and cohorts; stability over time

---

## Related notes

- [[treatment effect heterogeneity]] · [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[policy learning]] · [[policy tree]]
- [[AB Testing (MOC)]] · [[sequential testing]] · [[guardrail metric]]
- [[switchback experiment]] · [[geo experiment]]
- [[Unconfoundedness]] · [[Overlap]] · [[propensity score]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]

---
