---
title: off-policy evaluation
aliases: [OPE, offline policy evaluation, counterfactual evaluation, IPS, SNIPS, WDR]
tags: [policy-learning, bandits, uplift, causal-inference, evaluation, importance-sampling, doubly-robust, sequential]
updated: 2025-09-17
---

# off-policy evaluation

> [!summary] Quick definition
> Off-Policy Evaluation (OPE) estimates the value of a new policy π using logged data collected under another policy μ (the logging policy), without running π online. In contextual bandits and A/B-style logs with known propensities, OPE relies on inverse-propensity weighting (IPS), self-normalized IPS (SNIPS), direct modeling (DM), and doubly robust (DR/WDR) estimators. For sequential decisions (RL), OPE extends with per-decision importance sampling and DR estimators.

- Use cases: [[policy learning]] model selection, uplift targeting validation, comparison of multiple policies, safe deployment.
- Core requirement: logged propensities (or consistent estimators) and adequate overlap between μ and π.

---

## Setup and assumptions

- Logged data: {(X_i, A_i, Y_i, p_i)} for i=1..N
  - Context X_i, action A_i, outcome/reward Y_i, propensity p_i = P_μ(A_i | X_i) under logging policy μ.
- Target policy: π(a|x) (deterministic or stochastic).
- Value (contextual bandit):
$$
V(\pi) = \mathbb{E}\big[ Y \,\big|\, A \sim \pi(\cdot|X)\big].
$$
- Assumptions:
  - SUTVA (no interference across units) and correct timing (no [[leakage]]).
  - Positivity/overlap: if π(a|x) > 0, then μ(a|x) > 0 (observed support).
  - Known propensities p_i, or consistent estimates p̂_i (e(X)) from logging policy.
  - Stationarity within evaluation window (no unmodeled drift).

> [!warning] If overlap fails (tiny p_i) or propensities are unknown/mis-specified, IPS/DR become unstable or biased. Consider trimming, constraints, or model-based approaches.

---

## Canonical estimators (contextual bandit)

Let 1{·} be indicator. For deterministic π, define w_i = 1{π(X_i)=A_i}/p_i.

- Direct modeling (DM):
  - Fit outcome models m_a(x) = E\[Y | A=a, X=x]; estimate:
  $$
  \widehat{V}_{DM}(\pi)=\frac{1}{N}\sum_i m_{\pi(X_i)}(X_i).
  $$
  - Low variance; biased if models are misspecified.

- IPS (inverse propensity scoring):
$$
\widehat{V}_{IPS}(\pi)=\frac{1}{N}\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\,Y_i.
$$
  - Unbiased if p_i known; high variance with small p_i.

- SNIPS (self-normalized IPS):
$$
\widehat{V}_{SNIPS}(\pi)=\frac{\sum_i w_i Y_i}{\sum_i w_i}.
$$
  - Lower variance; biased in finite samples but consistent.

- DR (doubly robust / AIPW):
  - With m_a(x) and p_i:
  $$
  \widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \Big[m_{\pi(X_i)}(X_i) + \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\big(Y_i - m_{A_i}(X_i)\big)\Big].
  $$
  - Consistent if either m_a(x) or p_i is correct; often best practical choice.

- WDR/Weighted DR:
  - Normalize IPS weights inside DR for stability:
  $$
  \widehat{V}_{WDR}(\pi)=\sum_i \tilde w_i \, Y_i + \frac{1}{N}\sum_i \Big[m_{\pi(X_i)}(X_i) - \sum_a \pi(a|X_i)m_a(X_i)\Big],
  $$
  where $\tilde w_i = w_i / \sum_j w_j$ (implementation varies).

> [!tip] Cross-fitting
> Estimate m_a and (if needed) p with out-of-fold predictions (see [[double machine learning]]) to reduce overfitting bias.

---

## Sequential OPE (finite-horizon RL, trajectories)

- Logged trajectories τ = {(s_t, a_t, r_t)}_{t=0}^{H-1} with behavior policy μ and target π.
- Importance ratio up to time t: ρ_t = Π_{k=0}^{t} π(a_k|s_k) / μ(a_k|s_k).
- Per-Decision Importance Sampling (PDIS):
$$
\widehat{V}_{PDIS}(\pi)=\frac{1}{N}\sum_{i=1}^N \sum_{t=0}^{H-1} \gamma^t \,\rho_{i,t}\, r_{i,t}.
$$
- Weighted PDIS (WPDIS): normalize weights at each t.
- DR for RL (Jiang & Li, 2016): combines a learned Q/V-function with PDIS residuals; variants include MAGIC, WDR-RL.
- FQE (Fitted Q-Evaluation): model-based estimation of Q^π via Bellman backups on logged data; pessimistic/regularized variants for safety (e.g., CQL).

> [!warning] Variance explodes with horizon H; prefer per-decision ratios, weight clipping, normalization, or DR/FQE variants. Ensure Markov and stationarity assumptions are plausible.

---

## Confidence intervals and selection

- Asymptotics: use influence-function variance for IPS/DR; cluster or block bootstrap when there is clustering/time dependence.
- Multiple policies: hold out evaluation data or use nested cross-validation to avoid optimistic selection bias; control multiplicity (e.g., [[False Discovery Rate (FDR)|FDR]]) when screening many policies.
- Safety: pessimistic OPE (lower confidence bounds), risk constraints, or conservative policy optimization before deployment.

---

## Practical workflow

> [!check]
> - [ ] Confirm logging propensities (or estimate well) and evaluate overlap (propensity tails, ESS)  
> - [ ] Choose estimator(s): DR (plus IPS/SNIPS as sanity), optional DM as baseline  
> - [ ] Use cross-fitting for nuisance models; avoid leakage (strict pre-treatment features)  
> - [ ] Diagnose weight tails, consider clipping/trimming and report sensitivity  
> - [ ] For multiple policies: split data (train policies vs evaluate), or use nested CV; control multiplicity  
> - [ ] Compute CIs (IF or bootstrap); use block/cluster bootstrap for dependence  
> - [ ] For sequential settings: use PDIS/WPDIS/DR-RL with per-decision ratios; consider FQE/CQL for stability  
> - [ ] Validate best policy online with a small safe A/B and [[guardrail metric]]s; use [[sequential testing]]

---

## Diagnostics

- Overlap/weights:
  - Propensity histograms p_i; weights w_i = 1/p_i; Effective Sample Size (ESS) = (∑w)^2 / ∑w^2.
  - Share of weights above thresholds; sensitivity to clipping (e.g., cap w_i at c).
- Nuisance quality:
  - Out-of-fold AUC (propensity), R² (outcome models); calibration plots.
- Consistency checks:
  - Compare DM vs IPS vs DR; large discrepancies indicate misspecification or poor overlap.
  - Evaluate “do nothing” (treat-none) and “treat-all” policies as anchors.
- Stability:
  - Repeat with different seeds/folds; report variability; policy value by cohort/segment.

---

## Common pitfalls

> [!warning]
> - Missing/incorrect propensities → IPS/DR invalid  
> - Severe lack of overlap (tiny p_i) → high variance; no amount of modeling fixes missing support  
> - Data leakage: using post-treatment features to train m_a or e(X)  
> - Selecting a policy on the same data used to evaluate → optimistic bias  
> - Ignoring clustering/serial dependence in CIs  
> - In sequential settings: using trajectory-wise IS instead of per-decision; weight explosion with long horizons  
> - Comparing many policies without multiplicity control or proper holdout

---

## Minimal code snippets

> [!example] Python: IPS/SNIPS/DR (contextual bandit)

```python
import numpy as np

# X: (n,d), A: (n,), Y:(n,), p:(n,) logged propensities under mu
# pi(X): predicted action under target policy (0/1); or scores for multiple actions

def ips_value(A, Y, p, pi):
    w = (pi == A) / p
    return np.mean(w * Y)

def snips_value(A, Y, p, pi):
    w = (pi == A) / p
    return np.sum(w * Y) / np.sum(w)

def dr_value(X, A, Y, p, pi, m0, m1):
    # m0, m1 are arrays with m_a(X) out-of-fold predictions
    m_pi = np.where(pi == 1, m1, m0)
    m_a  = np.where(A == 1, m1, m0)
    w = (pi == A) / p
    return np.mean(m_pi + w * (Y - m_a))
```

> [!example] R: DR OPE

```r
dr_ope <- function(A, Y, p, pi, m0, m1){
  m_pi <- ifelse(pi==1, m1, m0)
  m_a  <- ifelse(A==1, m1, m0)
  w <- as.numeric(pi==A) / p
  mean(m_pi + w * (Y - m_a))
}
```

> [!example] Python: Per-decision IS (sequential)

```python
import numpy as np

def pdis_value(trajs, pi_prob, mu_prob, gamma=1.0):
    # trajs: list of trajectories; each traj is dict with keys 's','a','r' arrays
    vals = []
    for traj in trajs:
        G = 0.0
        rho = 1.0
        for t, (s,a,r) in enumerate(zip(traj['s'], traj['a'], traj['r'])):
            rho *= pi_prob(s,a) / mu_prob(s,a)
            G += (gamma**t) * rho * r
        vals.append(G)
    return np.mean(vals)
```

> [!example] Python: ESS and clipping sensitivity

```python
def ess(weights):
    w = np.asarray(weights)
    return (w.sum()**2) / (np.square(w).sum())

def dr_with_clipping(A, Y, p, pi, m0, m1, clip):
    w_raw = (pi == A) / p
    w = np.minimum(w_raw, clip)
    m_pi = np.where(pi == 1, m1, m0)
    m_a  = np.where(A == 1, m1, m0)
    return np.mean(m_pi + w * (Y - m_a)), ess(w)
```

---

## Reporting essentials

- Data and logging policy: how p_i were obtained; stationarity; inclusion/exclusion rules; time window
- Assumptions: overlap diagnostics, SUTVA, timing (pre/post definitions)
- Estimators used (IPS/SNIPS/DM/DR/WDR), cross-fitting scheme, nuisance learners and tuning
- Policy set: how policies were chosen (pre-specified vs learned), holdout/nested CV use, multiplicity handling
- Results: policy values with CIs; sensitivity to clipping, alternative nuisances; anchors (treat-all/none)
- Safety: guardrails and pessimistic bounds for deployment; online validation plan with [[sequential testing]]

---

## Related notes

- [[policy learning]] · [[uplift]] · [[bandits]]
- [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[AB Testing (MOC)]] · [[sequential testing]] · [[guardrail metric]]
- [[exposure logging]] · [[bucketing]]
- [[Unconfoundedness]] · [[Overlap]] · [[leakage]]

---
