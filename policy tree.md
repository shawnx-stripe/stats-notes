---
title: policy tree
aliases: [policy trees, optimal policy tree, uplift tree, decision policy tree, treatment decision tree]
tags: [causal-inference, policy-learning, uplift, interpretable-ml, off-policy-evaluation, constraints, fairness]
updated: 2025-09-17
---

# policy tree

> [!summary] Quick definition
> A policy tree is an interpretable decision tree that maps covariates X to a treatment decision π(X) ∈ {0,1,…} to maximize expected value (e.g., outcome lift), often under constraints (budget, fairness). It is learned from causal signals (e.g., CATE/uplift or doubly-robust scores) and evaluated via off-policy evaluation (OPE).

- Goal: maximize $V(\pi)=\mathbb{E}[Y(\pi(X))]$ with simple rules (if-then splits) that are deployable and auditable.
- Typical use: personalized interventions, marketing lift targeting, clinical decision rules, subsidy targeting.

---

## Setup and objective

- Binary treatment (for simplicity), action set 𝒜 = {0,1}.
- CATE (uplift): $\tau(x) = \mathbb{E}[Y(1)-Y(0)\mid X=x]$.
- Tree T induces leaves $\mathcal{L}(T)$; within each leaf ℓ, assign treat (1) or control (0).
- Value of a policy tree (plug-in with CATE):
$$
V(T) \approx \frac{1}{N}\sum_{i=1}^N \big[\ \mathbf{1}\{\pi_T(X_i)=1\}\,\tau(X_i)\ +\ \mathbb{E}[Y(0)\mid X_i]\ \big],
$$
(often drop the constant baseline to optimize only the uplift term).
- Budget/capacity constraint b:
$$
\frac{1}{N}\sum_{i=1}^N \mathbf{1}\{\pi_T(X_i)=1\} \le b.
$$

> [!note] Scores instead of raw CATE
> Many implementations use doubly-robust individual scores
> $$
> \gamma_i = \big(m_1(X_i)-m_0(X_i)\big) + \frac{D_i(Y_i-m_1(X_i))}{e(X_i)} - \frac{(1-D_i)(Y_i-m_0(X_i))}{1-e(X_i)}
> $$
> and pick leaf assignments to maximize $\sum_{i\in \ell} \gamma_i$ (subject to constraints). See [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] / [[double machine learning]].

---

## How policy trees are learned

- CATE-first (uplift) + tree induction
  - Estimate $\hat\tau(x)$ (e.g., DR-/R-/X-learner, causal forests).
  - Fit a tree to maximize summed $\hat\tau$ in treated leaves (vs. classification error). Use min leaf size and pruning to avoid overfitting.
- Direct value maximization (OPE-driven)
  - Use per-unit DR scores $\gamma_i$ and dynamic programming to split and assign leaves to maximize estimated value, possibly with budget constraints (e.g., R package policytree).
- Budgeted policies
  - Choose a subset of leaves to treat such that total treated share ≤ b, maximizing the sum of scores in treated leaves.

> [!tip] Cross-fitting
> Always compute $\hat\tau$ or $\gamma_i$ out-of-fold (cross-fitting) to reduce overfitting; then train the policy tree on these scores.

---

## Constraints and extensions

- Budget/capacity: treat at most b% globally, or per segment.
- Fairness: bounds on group-wise treat rates or outcomes; add constraints at leaves (e.g., minimum/maximum treat share by group).
- Stability: min leaf size, max depth; prefer shallow trees (depth 2–3) for interpretability.
- Multi-action: action-specific outcome models $m_a(x)$; assign $\arg\max_a m_a(x)-\text{cost}(a)$ per leaf.
- Costs: define net effect as uplift minus action cost; threshold accordingly within leaves.

---

## Off-policy evaluation (OPE)

Given logged data $(X_i, A_i, Y_i, p_i)$ with logging propensity $p_i=P(A_i\mid X_i)$:

- IPS:
$$
\widehat{V}_{IPS}(\pi)=\frac{1}{N}\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i} Y_i
$$
- SNIPS: normalized IPS for stability.
- DR (recommended):
$$
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \left[m_{\pi(X_i)}(X_i)+\frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\big(Y_i-m_{A_i}(X_i)\big)\right]
$$

> [!warning] Diagnostics
> - Check propensity overlap and weight tails (ESS).
> - Use bootstrap/IF-based CIs. For clustered data, cluster the resampling.

---

## R: causal forest + policytree (interpretable tree)

```r
# install.packages(c("grf","policytree"))
library(grf); library(policytree)

# 1) Estimate CATE with causal forest
X <- as.matrix(df[, c("X1","X2","X3")])
Y <- df$Y; W <- df$D
cf <- causal_forest(X, Y, W)
tauhat <- predict(cf)$predictions

# (Optional) Cross-fitting: split data, fit cf on folds, get out-of-fold tauhat

# 2) Fit a shallow policy tree that maximizes binary-action rewards
# policytree expects one reward column per action: control vs treat.
depth <- 2
Gamma <- cbind(control = 0, treat = tauhat)
pt <- policy_tree(X, Gamma, depth = depth, min.node.size = 200)
print(pt)
# Predict treatment decisions
pi_hat <- predict(pt, X)

# 3) Off-policy evaluation (simple DR)
# Estimate m0, m1 (can use regression forests or cf's get_tree_predictions)
rf0 <- regression_forest(X[W==0,], Y[W==0])
rf1 <- regression_forest(X[W==1,], Y[W==1])
m0 <- predict(rf0, X)$predictions
m1 <- predict(rf1, X)$predictions
p_treated <- mean(W)  # if randomized; otherwise estimate e(X)
p_logged <- ifelse(W == 1, p_treated, 1 - p_treated)
m_logged <- ifelse(W == 1, m1, m0)
m_policy <- ifelse(pi_hat == 1, m1, m0)

V_DR <- mean(m_policy + ((pi_hat == W) / p_logged) * (Y - m_logged))
V_DR
```

---

## Python: econml CATE + PolicyTree + DR OPE (sketch)

```python
import numpy as np
from econml.dr import DRLearner
from econml.policy import PolicyTree
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

X = df[['X1','X2','X3']].to_numpy()
T = df['D'].to_numpy().astype(int)
Y = df['Y'].to_numpy()
p = df['propensity'].to_numpy()  # if randomized 0.5 else estimate via logit

# 1) CATE via DRLearner (with cross-fitting internally)
dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(random_state=0))
dr.fit(Y, T, X=X)
tauhat = dr.effect(X)

# 2) Policy tree (shallow)
pt = PolicyTree(max_depth=2)  # interpretable
pt.fit(X, tauhat)             # learns splits to maximize uplift
pi_hat = pt.predict(X).astype(int)

# 3) DR off-policy evaluation (with m0,m1 from DRLearner)
m0 = dr.const_marginal_effect(X, T0=0) * 0 + dr.model_regression[0].predict(X)
m1 = dr.const_marginal_effect(X, T0=1) * 0 + dr.model_regression[1].predict(X)

V_DR = np.mean( (pi_hat==1)*m1 + (pi_hat==0)*m0 + ((pi_hat==T)/p)*(Y - (T*m1 + (1-T)*m0)) )
print(V_DR)
```

> [!note] Depending on econml version, you may need to extract m0/m1 differently (e.g., via nuisance models). The DR OPE formula remains the same.

---

## Practical checklist

> [!check]
> - [ ] Use cross-fitted causal signals (τ̂ or γ) to train the tree (no leakage)  
> - [ ] Keep trees shallow (depth 2–3), enforce min leaf size for stability  
> - [ ] If budget/capacity constraints apply, use constrained tree or treat only top leaves by average score  
> - [ ] OPE with DR; report CIs; check overlap and weight tails  
> - [ ] Validate policy via an online A/B (with guardrails); consider [[sequential testing]]  
> - [ ] Audit fairness: group-wise treatment rates/outcomes under π̂; enforce constraints if needed

---

## Interpretation and reporting

- Present the tree with human-readable rules (feature thresholds per node).
- Report policy value (OPE), regret vs. baselines (treat-all / treat-none / score-threshold).
- Constraints: spend share achieved, fairness metrics.
- Robustness: alternative depths, min leaf sizes, different learners for τ̂/γ, sample splits.
- Limitations: overlap gaps, distribution shift, stability across time/cohorts.

---

## Common pitfalls

> [!warning]
> - Optimizing classification accuracy instead of value (uplift)  
> - Using predictive models (not causal) to form policies → biased targeting  
> - No cross-fitting → overfitting to noise in τ̂/γ  
> - Ignoring budget/fairness until after training (infeasible policies)  
> - Evaluating with plain ATE methods instead of OPE; ignoring propensities  
> - Overly deep trees with unstable small leaves

---

## Copy-ready formulas

- DR score (binary treatment):
$$
\gamma_i = (m_1 - m_0) + \frac{D_i(Y_i - m_1)}{e} - \frac{(1-D_i)(Y_i - m_0)}{1-e}.
$$
- IPS/SNIPS/DR policy value:
$$
\widehat{V}_{IPS}(\pi)=\frac{1}{N}\sum_i \frac{\mathbb{1}\{\pi(X_i)=A_i\}}{p_i}Y_i,\quad
\widehat{V}_{SNIPS}=\frac{\sum \frac{\mathbb{1}\{\pi(X)=A\}}{p}Y}{\sum \frac{\mathbb{1}\{\pi(X)=A\}}{p}},\quad
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \Big[m_{\pi(X_i)}(X_i)+\frac{\mathbb{1}\{\pi(X_i)=A_i\}}{p_i}(Y_i-m_{A_i}(X_i))\Big].
$$

---

## Related notes

- [[policy learning]] · [[treatment effect heterogeneity]] · [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[AB Testing (MOC)]] · [[sequential testing]] · [[guardrail metric]]
- [[switchback experiment]] · [[geo experiment]]
- [[Unconfoundedness]] · [[Overlap]] · [[propensity score]]

---
