---
title: bandits
aliases: [contextual bandits, exploration-exploitation, Thompson sampling, UCB]
tags: [experimentation, policy-learning, bandits, online-learning, sequential, off-policy-evaluation, constraints, fairness]
updated: 2025-09-17
---

# bandits

> [!summary] Quick definition
> Bandits are online decision algorithms that balance exploration and exploitation to maximize cumulative reward (or minimize regret). In multi-armed bandits (MAB), actions are context-free; in contextual bandits, actions depend on covariates X. Bandits adapt allocations over time, unlike fixed-split [[AB Testing (MOC)]], and need different inference, monitoring, and governance.

- Uses: content ranking, recommendations, ads, notifications, pricing promos, experimentation with rapid adaptation.
- Outputs: an adaptive policy π_t and cumulative reward; can also learn interpretable policies (e.g., [[policy tree]]) after logging.

---

## Core concepts

- Actions/arms A ∈ {1,…,K}; reward Y_t (binary or continuous); optional context X_t.
- Objective: maximize expected cumulative reward ∑ E[Y_t] or minimize expected (pseudo-)regret:
$$
\text{Regret}(T) = \sum_{t=1}^T \big(\mu^\star_t - \mu_{A_t,t}\big),
$$
where μ⋆_t is the best-arm expectation at t (given context for contextual cases).
- Exploration vs exploitation: try uncertain arms vs play estimated best arm.
- Logging propensities p_t = P(A_t | history, X_t): needed for off-policy evaluation (OPE).

---

## Classic algorithms

### Non-contextual (MAB)
- ε-greedy: with prob. ε explore uniform; else exploit best mean.
- Upper Confidence Bound (UCB1):
$$
\text{index}_a = \bar y_a + c\sqrt{\frac{\ln t}{n_a(t)}},
$$
pick argmax index (optimism in face of uncertainty).
- Thompson Sampling (TS):
  - Bernoulli arm a: Beta(α_a, β_a) posterior; sample θ_a ∼ Beta(α_a,β_a) and pick argmax.

### Contextual bandits
- LinUCB (linear reward): assume E[Y|X,a] = θ_a^⊤ X; index = θ̂_a^⊤ X + α√(X^⊤ A_a^{-1} X).
- Logistic/GLM-UCB: replace linear model with GLM, use confidence bounds.
- Thompson Sampling with linear/GLM models (sample parameters from approximate posterior).
- Policy-gradient or direct [[policy learning]] with OPE constraints (more advanced).

> [!tip] Practical defaults
> - If binary reward and few arms: Thompson Sampling (Beta-Bernoulli) is simple and strong.
> - With features: LinUCB or contextual TS; start with modest α to avoid over-exploration.

---

## Bandits vs A/B tests

- Allocation: bandits adapt; A/B is typically fixed-split.
- Goal: bandits maximize online reward; A/B estimates treatment effect with controlled Type I error.
- Inference: bandit logs are biased toward better arms; naive difference-in-means is biased. Use OPE (IPS/SNIPS/DR) or design an explicit post-hoc A/B.
- Governance: use [[guardrail metric]]s, sequential safety monitors, and roll-back plans; [[Sample Ratio Mismatch (SRM)|SRM]] notion does not apply since allocation is intentional.

---

## Off-policy evaluation (OPE)

Given logged (X_i, A_i, Y_i, p_i), evaluate a counterfactual policy π:

- IPS:
$$
\widehat{V}_{IPS}(\pi)=\frac{1}{N}\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}Y_i
$$
- SNIPS:
$$
\widehat{V}_{SNIPS}=\frac{\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}Y_i}{\sum_i \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}}
$$
- DR (recommended):
$$
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \big[m_{\pi(X_i)}(X_i) + \frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\big(Y_i - m_{A_i}(X_i)\big)\big]
$$

> [!warning] Diagnostics
> - Overlap: avoid tiny propensities (extreme weights); consider minimum exploration.
> - Clustering/time-dependence: use block/cluster bootstrap for CIs; see [[sequential testing]] for online monitoring.

---

## Constraints and safety

- Budget/capacity: constrain treatment rate P(A=1) ≤ b (e.g., top-b by score; constrained bandits).
- Guardrails: monitor latency/errors/churn using sequential rules; define halt criteria.
- Fairness: constrain group-level exposure or outcomes; fairness-aware bandits.
- Nonstationarity: use sliding windows/discounted updates (exp-decay) or change-point detectors.
- Delayed rewards: handle lagged outcomes (e.g., conversions) with proxy modeling or delayed-updates TS/UCB.

---

## Interference and deployment

- Interference (marketplaces/shared resources): consider [[switchback experiment]] (time-sliced) or [[geo experiment]]; per-user bandits may be invalid if arms affect others.
- Cold start: forced exploration at launch; decaying ε or optimistic priors.
- Multiple concurrent bandits: coordinate via namespaces and mutual exclusion to avoid policy collisions (see [[bucketing]]).

---

## Minimal code snippets

> [!example] Python: Thompson Sampling (Bernoulli)

```python
import numpy as np

K = 3
alpha = np.ones(K); beta = np.ones(K)  # Beta(1,1) priors
success = np.zeros(K); trials = np.zeros(K)

def select_arm():
    theta = np.random.beta(alpha, beta)
    return np.argmax(theta)

def update(a, y):  # y in {0,1}
    global alpha, beta, success, trials
    alpha[a] += y; beta[a] += 1 - y
    success[a] += y; trials[a] += 1

# simulate one step
a = select_arm()
y = np.random.binomial(1, 0.1 + 0.1*a)  # dummy reward
update(a, y)
```

> [!example] Python: LinUCB (contextual, linear reward)

```python
import numpy as np

K, d, alpha = 2, 10, 0.5
A = [np.eye(d) for _ in range(K)]
b = [np.zeros(d) for _ in range(K)]

def select_arm(x):
    p = np.zeros(K)
    for a in range(K):
        Ainv = np.linalg.inv(A[a])
        theta = Ainv @ b[a]
        p[a] = theta @ x + alpha * np.sqrt(x @ Ainv @ x)
    return np.argmax(p)

def update(a, x, y):
    A[a] += np.outer(x, x)
    b[a] += y * x
```

> [!example] Python: Doubly robust OPE for a learned policy

```python
import numpy as np

# logged data: X, A, Y, p (propensities)
# fitted outcome models m0, m1 (e.g., via RF on A=0 and A=1)
pi = policy(X)  # 0/1 decisions for new policy
m0 = m0_model.predict(X)
m1 = m1_model.predict(X)

V_DR = np.mean((pi==1)*m1 + (pi==0)*m0 + ((pi==A)/p)*(Y - (A*m1 + (1-A)*m0)))
```

---

## Governance and reporting

> [!check] Checklist
> - [ ] Define objective and constraints (budget, fairness, guardrails)  
> - [ ] Choose algorithm (TS/UCB/LinUCB/TS-Linear); set priors/α; nonstationarity strategy  
> - [ ] Log propensities p_t and contexts X_t; ensure reproducible seeds/versions  
> - [ ] Monitor online with sequential safety and drift checks; rollback plan  
> - [ ] Offline OPE for policy variants; A/B validation before full deployment  
> - [ ] Document exploration share, regret, guardrail incidents, and changes over time

---

## Pitfalls

> [!warning]
> - Treating bandit outcomes as unbiased A/B estimates (allocation is adaptive → bias)  
> - No logging of propensities (precludes valid OPE)  
> - Ignoring nonstationarity (concept drift) → stale policies  
> - No guardrails → harmful arms persist during exploration  
> - Severe interference → per-user bandits invalid; prefer switchback/geo designs  
> - Delayed rewards mishandled → optimistic bias for quick-feedback arms

---

## Relation to policy learning

- Bandits learn online policies with exploration; [[policy learning]] learns policies offline with OPE.
- Hybrid: use bandit logs to train offline policies (e.g., [[policy tree]]), then validate with an A/B or a safer bandit.

---

## Copy-ready formulas

- UCB index:
$$
\text{UCB}_a(t) = \bar y_a(t) + c\sqrt{\frac{\ln t}{n_a(t)}}.
$$

- Thompson Sampling (Bernoulli arm):
$$
\theta_a \sim \text{Beta}(\alpha_a,\beta_a),\quad a^\star = \arg\max_a \theta_a.
$$

- DR OPE:
$$
\widehat{V}_{DR}(\pi)=\frac{1}{N}\sum_i \left[m_{\pi(X_i)}(X_i)+\frac{\mathbf{1}\{\pi(X_i)=A_i\}}{p_i}\big(Y_i-m_{A_i}(X_i)\big)\right].
$$

---

## Related notes

- [[AB Testing (MOC)]] · [[policy learning]] · [[policy tree]] · [[uplift]]
- [[sequential testing]] · [[guardrail metric]] · [[exposure logging]] · [[bucketing]]
- [[switchback experiment]] · [[geo experiment]]
- [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Unconfoundedness]] · [[Overlap]] · [[treatment effect heterogeneity]]

---
