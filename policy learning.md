---
title: policy learning
aliases: [uplift policy, treatment assignment policy, individualized treatment rules, ITR, decision policy, contextual bandit policy]
tags: [causal-inference, policy-learning, uplift, bandits, off-policy-evaluation, a/b-testing, constraints, fairness]
updated: 2025-09-17
---

# policy learning

> [!summary] Quick definition
> Policy learning chooses a treatment assignment rule π(x) that maps context/covariates X to actions (e.g., treat vs. control) to maximize expected outcomes (or minimize loss), subject to constraints (budget, fairness, risk). It uses causal estimates (CATE/uplift) and/or off-policy evaluation to select near-optimal, deployable policies.

- Goals: maximize value V(π) = E[Y(π(X))], minimize regret vs. the best feasible policy, and satisfy constraints.
- Settings: personalization, marketing lift, targeting subsidies, clinical decision rules, ranking interventions.

---

## Problem setup

- Context X ∈ ℝ^p, action A ∈ 𝒜 (binary or multi-armed), outcome Y.
- Policy π: X → 𝒜.
- Value of a policy:
$$
V(\pi) = \mathbb{E}\big[Y(\pi(X))\big].
$$
- Regret against oracle policy π⋆:
$$
\text{Regret}(\pi) = V(\pi^\star) - V(\pi).
$$

> [!note] Estimands
> - Binary treatment: use CATE τ(x) = E[Y(1) − Y(0) | X=x] to define π(x) = 1{τ(x) > c} where c can encode costs/constraints.
> - Multi-action: argmax over action-specific conditional means m_a(x) = E[Y(a) | X=x] minus action costs.

---

## Two main approaches

### 1) CATE-first (uplift) + policy induction
- Estimate τ(x) (binary) or action-conditional m_a(x) via [[double machine learning]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], causal forests (grf), meta-learners (T-/S-/X-/R-/DR-).
- Induce a deployable policy:
  - Threshold: π(x)=1{τ̂(x) > c}.
  - [[policy tree]]/policy list (interpretable structures).
  - Score-and-budget: treat top B% by τ̂(x) to respect spend/capacity.

### 2) Direct policy optimization with off-policy evaluation (OPE)
- Define policy class Π (e.g., depth-limited trees).
- Optimize empirical value estimate Ŵ(π) using OPE (IPS/DR/SNIPS/WDR) under logged data with known propensities.
- Optionally incorporate constraints and regularization during optimization.

---

## Off-policy evaluation (OPE)

Assume logged data (X_i, A_i, Y_i, p_i) where p_i = P(A_i | X_i) under logging policy.

- Inverse propensity scoring (IPS):
$$
\widehat{V}_{IPS}(\pi) = \frac{1}{N}\sum_{i=1}^N \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\,Y_i.
$$

- Self-normalized IPS (SNIPS):
$$
\widehat{V}_{SNIPS}(\pi)= \frac{\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}Y_i}{\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}}.
$$

- Doubly robust (DR/AIPW):
$$
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i\Big[m_{\pi(X_i)}(X_i)+\frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\big(Y_i-m_{A_i}(X_i)\big)\Big],
$$
with m_a(x)=E[Y|A=a,X=x] estimated by ML.

> [!tip] Properties
> - IPS unbiased if propensities known; high variance with small p_i.
> - SNIPS stabilizes variance but is biased in finite samples.
> - DR is consistent if either propensities or outcome models are correct; often best practical choice.

---

## Constraints and objectives

- Budget/capacity: P(π(X)=1) ≤ b (treat only top-b proportion by τ̂ or via constrained optimization).
- Cost-sensitive: maximize E[Benefit − Cost(π(X))].
- Fairness: bounds on group-wise treatment rates or outcomes; add constraints such as |P(π=1 | G=g) − q_g| ≤ ε.
- Risk/variance: penalize high-variance policies; use confidence-bound or pessimistic (minimax) value estimates.

---

## Assumptions and identification

- Logged randomized experiments: known propensities (bucketing), independence → clean OPE.
- Observational data with [[Unconfoundedness]]/[[Overlap]]: can estimate CATE and use DR policy learning; OPE requires estimated propensities and careful diagnostics.
- Bandit/logging policy drift: ensure p_i correspond to logging policy; handle nonstationarity (time FE, reweighting).

> [!warning] Pitfalls
> - Unknown/incorrect propensities → IPS/DR invalid.
> - Poor overlap (tiny p_i or extreme weights) → high variance; trim or constrain policy class.
> - Data leakage: using post-treatment information in features.
> - Distribution shift: policy deployed to a different population than trained; monitor and adapt.

---

## Practical pipeline

1) Define candidate policy class Π (thresholds, policy trees, linear score, k rules).
2) Split data for cross-fitting:
   - Learn nuisances (propensity ê, outcomes m̂) on folds; predict out-of-fold.
3) Evaluate policies via OPE (DR preferred), with uncertainty (bootstrap or IF-based SEs).
4) Select π̂ maximizing Ŵ(π) under constraints; compute CIs for V(π̂) and regret.
5) Validate with an online experiment ([[AB Testing (MOC)]]), possibly as a bandit with guardrails.

---

## Diagnostics

> [!check]
> - [ ] Overlap: distribution of learned propensities p̂, effective sample size (ESS), weight tails  
> - [ ] OPE stability: compare IPS, SNIPS, DR; variance and bias diagnostics  
> - [ ] Policy complexity vs value (overfitting) via nested CV  
> - [ ] Group-wise effects and fairness metrics; constraint satisfaction checks  
> - [ ] Sensitivity to nuisance learners (RF vs boosted trees vs lasso) and feature sets

---

## Minimal code snippets

> [!example] Python: simple threshold policy via CATE + DR OPE (sketch)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

X = df[['X1','X2','X3']].to_numpy()
A = df['A'].to_numpy()  # 0/1
Y = df['Y'].to_numpy()
p = df['propensity'].to_numpy()  # known/logged; if randomized 0.5

# Cross-fit outcome models
kf = KFold(n_splits=5, shuffle=True, random_state=42)
m0hat = np.zeros(len(Y)); m1hat = np.zeros(len(Y))
for train, test in kf.split(X):
    m0 = RandomForestRegressor().fit(X[train][A[train]==0], Y[train][A[train]==0])
    m1 = RandomForestRegressor().fit(X[train][A[train]==1], Y[train][A[train]==1])
    m0hat[test] = m0.predict(X[test])
    m1hat[test] = m1.predict(X[test])

tauhat = m1hat - m0hat
# Budget b: treat top b quantile by tauhat
b = 0.3
thr = np.quantile(tauhat, 1-b)
pi_hat = (tauhat >= thr).astype(int)

# DR OPE of policy value
V_DR = np.mean(m0hat + pi_hat*(m1hat-m0hat) + ((pi_hat==A)/p)*(Y - (A*m1hat + (1-A)*m0hat)))
print(V_DR)
```

> [!example] R: policy tree with grf + policytree (binary treatment)

```r
# install.packages(c("grf","policytree"))
library(grf); library(policytree)

# 1) Train causal forest for CATE
cf <- causal_forest(as.matrix(df[,c("X1","X2","X3")]), df$Y, df$A)
tauhat <- predict(cf)$predictions

# 2) Fit policy tree (shallow for interpretability)
pt <- policy_tree(df[,c("X1","X2","X3")], tauhat, depth = 2)
print(pt)
# Induced policy: treat if tree routes to positive leaf

# 3) Off-policy evaluation (DR) can be done via grf::average_treatment_effect or custom
```

> [!example] Python: IPS/SNIPS value for a candidate policy

```python
# propensities p (logged), A, Y, policy pi(X)
pi = policy_predict(X)  # 0/1
w = (pi == A) / p
V_ips = np.mean(w * Y)
V_snips = np.sum(w * Y) / np.sum(w)
```

---

## Beyond binary treatment

- Multi-armed decisions: learn m_a(x) for each a, choose argmax subject to constraints.
- Continuous doses/prices: policy is a function a = g(x); use policy gradients, plug-in m̂(x,a), or bandit/RL methods.
- Sequential decisions (RL): states, actions, rewards; learn stationary or nonstationary policies with exploration (contextual bandits → RL).

---

## Relation to bandits and A/B testing

- Online A/B: evaluate π̂ with a controlled experiment; consider [[sequential testing]] and guardrails.
- Contextual bandits: explore while learning policy; OPE essential for offline replay; guardrails/fairness constraints often imposed.
- Switchback/geo: when interference prohibits per-user randomization, test policies via [[switchback experiment]] or [[geo experiment]].

---

## Fairness, safety, and governance

- Fairness constraints: demographic parity or equalized benefit; audit group-wise value and harms.
- Safety: impose risk constraints (e.g., lower CI of V(π) above threshold), conservative (pessimistic) OPE.
- Governance: document policy class, constraints, OPE method, uncertainties; pre-registration for online validation.

---

## Common pitfalls

> [!warning]
> - Using predictive models for Y (not causal) to form policies → biased selection  
> - Unknown/incorrect logging propensities in OPE  
> - Severe lack of overlap → unstable IPS/DR; fix with trimming/constraints  
> - Overfitting the policy to noisy OPE; use nested CV and simple policies first  
> - Ignoring constraints (budget/fairness) until after selection → infeasible deployment  
> - Distribution shift between training and deployment populations

---

## Reporting essentials

- Data source and logging policy; propensities known/estimated; overlap diagnostics
- Nuisance learners (algorithms, hyperparameters), cross-fitting scheme
- Policy class Π and constraint set; selection and optimization method
- OPE estimates (IPS/SNIPS/DR) with CIs; sensitivity across OPE/learners
- Expected budget/fairness outcomes; monitoring plan and rollout experiment design
- Limitations and risks (shift, fairness harms, uncertainty)

---

## Related notes

- [[treatment effect heterogeneity]] · [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[AB Testing (MOC)]] · [[sequential testing]] · [[guardrail metric]]
- [[switchback experiment]] · [[geo experiment]]
- [[Unconfoundedness]] · [[Overlap]] · [[propensity score]]
- [[policy tree]] · [[uplift]]