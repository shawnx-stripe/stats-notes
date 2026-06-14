---
title: Multi-Armed Bandit (MAB)
aliases: [MAB, multi-armed bandit, multi-armed bandits]
tags: [bandits, online-learning, exploration-exploitation, sequential, decision-theory, ab-testing, contextual, thompson-sampling, ucb]
updated: 2025-09-23
---

# Multi-Armed Bandit (MAB)

> [!summary] Quick definition
> Multi‑Armed Bandits (MAB) are sequential decision problems that balance exploration (learning about arms) and exploitation (using the best‑known arm) to maximize cumulative reward or minimize regret over a horizon. Algorithms include ε‑greedy, UCB, Thompson sampling, and contextual variants (LinUCB, linear/GLM TS). See also [[AB Testing (MOC)]] for contrasts with fixed randomized experiments and [[off-policy evaluation]] for evaluation from logged data.

- Core elements: arms/actions A ∈ {1..K}, rewards r_t ∈ ℝ, horizon T, policy π(a|history, context), regret R_T.
- Related: [[bandits]] · [[sequential testing]] · [[Bayesian Testing]] · [[policy learning]] · [[uplift]] · [[off-policy evaluation]].

---

## Problem setup

- Stochastic K‑armed bandit (stationary):
  - Each arm i has an unknown mean reward μ_i; pulls yield i.i.d. rewards with that mean.
  - Optimal mean μ_* = max_i μ_i, gaps Δ_i = μ_* − μ_i.
- Regret over horizon T:
$$
R_T \;=\; \mathbb{E}\!\left[\sum_{t=1}^T (\mu_* - \mu_{A_t})\right]
\;=\; \sum_{i:\,\Delta_i>0} \Delta_i \,\mathbb{E}[N_i(T)]
$$
where N_i(T) is the number of pulls of arm i.
- Contextual bandit:
  - At time t, observe features x_t; choose arm A_t; observe reward r_t with
$$
\mathbb{E}[r_t \mid x_t, A_t=a] = f_a(x_t)
$$
Goal: learn a policy π(a|x) maximizing expected reward (or other utility).

> [!note] Practical objectives
> - Short‑run: cumulative reward (minimize regret)  
> - Long‑run: learn best policy quickly, respect guardrails and constraints (latency, quality, fairness)

---

## Core algorithms

### Simple baselines

- ε‑greedy
  - With probability ε_t explore uniformly; else exploit best empirical mean.
  - Use decay ε_t = min(1, cK/t) to get logarithmic regret.

- Softmax/Boltzmann
  - Choose arm with probability ∝ exp(η·x̄_i); anneal η over time.

### UCB family (optimism in the face of uncertainty)

- UCB1 (Auer et al., 2002):
$$
\text{UCB}_i(t) = \bar r_i(t) + \sqrt{\frac{2\ln t}{N_i(t)}}
$$
Pull arm with largest UCB; yields O(∑_i (ln T)/Δ_i) regret.

- KL‑UCB (for bounded/ Bernoulli rewards):
$$
\text{choose } i = \arg\max_i \; q \;\text{s.t.}\; N_i(t)\,\mathrm{KL}(\hat p_i \,\|\, q) \le \ln t + c\ln\ln t
$$
Sharper constants than UCB1.

### Thompson sampling (Bayesian exploration)

- Bernoulli rewards with Beta prior:
  - Prior per arm i: θ_i ∼ Beta(α_i, β_i).
  - At time t: sample $\tilde\theta_i \sim \text{Beta}(\alpha_i, \beta_i)$; pick argmax_i $\tilde\theta_i$; update α_i ← α_i + r_t, β_i ← β_i + (1−r_t).
- Gaussian rewards (known variance σ²):
  - Conjugate Normal prior per arm; sample arm means and pick the largest.

> [!tip] TS vs UCB
> TS is simple, robust, and often best in practice; UCB offers clean frequentist guarantees and is parameter‑free (except constants). Use batched updates in high‑throughput systems.

---

## Contextual bandits

- LinUCB (linear reward model r = x'θ_a + noise):
  - For each arm a, maintain V_a = λI + ∑ x x' and b_a = ∑ r x; θ̂_a = V_a^{-1} b_a.
  - Index:
$$
\text{UCB}_a(x) = x' \hat\theta_a + \alpha \sqrt{x' V_a^{-1} x}
$$

- Linear Thompson Sampling:
  - Posterior θ_a ∼ N(θ̂_a, v^2 V_a^{-1}); sample $\tilde\theta_a$ and pick argmax x'$\tilde\theta_a$.

- Logistic/GLM bandits:
  - Use Laplace‑approximate posteriors for TS, or confidence sets for UCB‑style indices.

> [!warning] Leakage and confounding
> Features x_t must be strictly pre‑treatment. Post‑treatment or outcome‑contaminated features cause bias (see [[leakage]]).

---

## Nonstationary and practical variants

- Nonstationary rewards: sliding‑window or discounted UCB/TS; change‑point detectors with resets.
- Delayed/attributed rewards: use pending‑aware algorithms; censoring adjustments.
- Multiple plays and positions: combinatorial/position‑biased bandits (e.g., ranked recommendation); use cascading/PL/UCB variants.
- Constraints and safety:
  - Conservative bandits: constrain regret relative to a baseline policy.
  - Knapsack/budgeted bandits: costs per pull; maximize value under budget.
  - Fairness/risk: add constraints to selection rates or CVaR.

---

## Implementation checklist

> [!check]
> - [ ] Define reward and horizon; align with OEC/guardrails (see [[Overall Evaluation Criterion (OEC)|OEC]])  
> - [ ] Choose algorithm (ε‑greedy/UCB/TS; contextual vs non‑contextual) and hyperparameters (α in UCB, priors in TS, λ in linear models)  
> - [ ] Warm start (uniform exploration or informative priors)  
> - [ ] Log at decision time: context x_t, available arms, chosen arm, reward, logging propensity p(A_t|x_t), constraints  
> - [ ] Handle delayed feedback and missing outcomes; avoid biased early updates  
> - [ ] Monitor arm counts, empirical means, regret proxies, and guardrails; set abort rules  
> - [ ] For offline tuning/evaluation, use [[off-policy evaluation]] (IPS/DR) with logged propensities

---

## Minimal pseudocode

> [!example] Thompson sampling (Bernoulli)

```python
def ts_bernoulli(K, alpha0=1.0, beta0=1.0):
    alpha = [alpha0]*K; beta = [beta0]*K
    def select():
        import random
        from random import betavariate
        samples = [betavariate(alpha[i], beta[i]) for i in range(K)]
        return max(range(K), key=lambda i: samples[i])
    def update(i, r):  # r in {0,1}
        alpha[i] += r
        beta[i] += 1 - r
    return select, update
```

> [!example] LinUCB (contextual)

```python
import numpy as np

class LinUCB:
    def __init__(self, K, d, alpha=1.0, lam=1.0):
        self.K, self.d = K, d
        self.alpha = alpha
        self.V = [lam*np.eye(d) for _ in range(K)]
        self.b = [np.zeros(d) for _ in range(K)]

    def select(self, x):  # x: d-vector
        vals = []
        for a in range(self.K):
            Va_inv = np.linalg.inv(self.V[a])
            theta = Va_inv @ self.b[a]
            ucb = x @ theta + self.alpha * np.sqrt(x @ Va_inv @ x)
            vals.append(ucb)
        return int(np.argmax(vals))

    def update(self, a, x, r):
        self.V[a] += np.outer(x, x)
        self.b[a] += r * x
```

---

## Bandits vs A/B testing

- A/B tests optimize for inference about a fixed contrast with pre‑specified error control (see [[AB Testing (MOC)]]); traffic splits are fixed, enabling clean estimation of long‑run effects and [[sequential testing]] control.
- Bandits optimize online reward; allocation adapts, complicating unbiased estimation and counterfactuals. Prefer bandits when:
  - reward is immediate and aligned with OEC,
  - you can tolerate exploration and potential instability,
  - you can log propensities to enable [[off-policy evaluation]] and auditing.
- For product rollouts: use bandits for targeting/tuning within guardrails; validate winning policies with a confirmatory experiment.

---

## Diagnostics and monitoring

- Learning dynamics: arm counts N_i(t), empirical means and CIs/credible intervals, regret proxy vs baseline.
- Safety/guardrails: latency, error rates, revenue per user; automatic abort thresholds.
- Nonstationarity: drift detectors; reset frequency.
- Fairness/constraints: selection rate parity, budget adherence.

---

## Common pitfalls

> [!warning]
> - Ignoring delayed outcomes or attribution → biased updates  
> - Using post‑treatment features (model [[leakage]])  
> - Deterministic policies early on → exposure bias and lack of exploration  
> - Comparing policies without logged propensities; invalid offline evaluation  
> - Optimizing click proxies misaligned with long‑run value (myopic OEC)

---

## Reporting essentials

- Objective and reward definition; horizon and traffic eligibility
- Algorithm and hyperparameters (priors/α/λ), warm‑start strategy
- Logging schema (context, action, reward, propensity), handling of delays/missing
- Monitoring plan: guardrails, abort rules, drift handling
- Results: cumulative reward/regret, arm trajectories, final policy
- Post‑hoc validation: OPE metrics and confirmatory [[AB Testing (MOC)]]

---

## Related notes

- Algorithms: [[bandits]] · [[policy learning]] · [[uplift]]  
- Evaluation: [[off-policy evaluation]] · [[sequential testing]] · [[Bayesian Testing]]  
- Design/causal: [[AB Testing (MOC)]] · [[Causal Inference (MOC)]]

---

## References

- Lai & Robbins (1985). Asymptotically efficient adaptive allocation rules  
- Auer, Cesa‑Bianchi, & Fischer (2002). Finite‑time analysis of the multiarmed bandit problem (UCB1)  
- Agrawal & Goyal (2012, 2013). Thompson sampling analysis; contextual TS (linear)  
- Bubeck & Cesa‑Bianchi (2012). Regret analysis of stochastic and adversarial bandits (survey)  
- Lattimore & Szepesvári (2020). Bandit Algorithms (book)  
- Russo et al. (2018). A tutorial on Thompson sampling  
- Li et al. (2010). A contextual‑bandit approach to personalized news (LinUCB)

---
