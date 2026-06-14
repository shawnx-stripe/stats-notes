---
title: Hidden Markov Model (HMM)
aliases: [Hidden Markov Model, Hidden Markov Models, Markov-switching, HMM, hidden markov model]
tags: [time-series, probabilistic-models, state-space, em, inference, filtering, smoothing, viterbi, bayesian]
updated: 2025-09-21
---

# Hidden Markov Model (HMM)

> [!summary] Quick definition
> A Hidden Markov Model (HMM) is a discrete-state state-space model where an unobserved Markov chain Z_t governs observations Y_t via state-dependent emission distributions. Core tasks: filtering p(z_t|y_{1:t}), smoothing p(z_t|y_{1:T}), decoding (most probable state sequence via Viterbi), prediction p(y_{t+1}|y_{1:t}), and parameter learning (Baum–Welch EM).

- Parameters θ = {π, A, φ}: initial state π, transition matrix A, emission parameters φ.
- Related: [[Sequential Monte Carlo (SMC)|SMC]] (online inference), [[Markov Chain Monte Carlo (MCMC)|MCMC]] for Bayesian HMMs, [[Maximum Likelihood Estimation (MLE)|MLE]] via EM, [[Kalman filter]] for the linear‑Gaussian continuous‑state special case, [[Time Series (MOC)]].

---

## Model definition

- Latent states: Z_t ∈ {1, …, K}
- Initial and transitions:
$$
Z_1 \sim \operatorname{Cat}(\pi), \qquad
\Pr(Z_t=j \mid Z_{t-1}=i) = A_{ij}, \quad \sum_{j=1}^K A_{ij}=1
$$
- Emissions (examples):
  - Discrete: Y_t ∈ {1,…,V}, p(Y_t=v \mid Z_t=k) = b_{k,v}
  - Gaussian: Y_t ∈ \mathbb{R}^d, p(Y_t \mid Z_t=k) = \mathcal{N}(\mu_k, \Sigma_k)
- Joint distribution:
$$
p_\theta(z_{1:T}, y_{1:T})
= \pi_{z_1} \, b_{z_1}(y_1) \prod_{t=2}^T A_{z_{t-1}, z_t} \, b_{z_t}(y_t)
$$

---

## Inference (forward–backward)

Define emission likelihoods e_t(k) = p(y_t \mid Z_t=k; φ).

- Forward messages (α):
$$
\alpha_t(k) = p(y_{1:t}, Z_t=k), \quad
\alpha_1(k) = \pi_k \, e_1(k), \quad
\alpha_t(k) = e_t(k)\sum_{i=1}^K \alpha_{t-1}(i) A_{i k}
$$
- Backward messages (β):
$$
\beta_T(k) = 1, \qquad
\beta_t(i) = \sum_{j=1}^K A_{i j} \, e_{t+1}(j) \, \beta_{t+1}(j)
$$
- Posteriors:
$$
\gamma_t(k) = p(Z_t=k \mid y_{1:T}) = \frac{\alpha_t(k)\beta_t(k)}{\sum_{j}\alpha_t(j)\beta_t(j)}
$$
$$
\xi_t(i,j) = p(Z_t=i, Z_{t+1}=j \mid y_{1:T}) = \frac{\alpha_t(i) A_{i j} e_{t+1}(j)\beta_{t+1}(j)}{\sum_{a,b}\alpha_t(a) A_{a b} e_{t+1}(b)\beta_{t+1}(b)}
$$

> [!tip] Scaling for numerical stability
> Use normalized forward variables and scaling factors c_t:
> $$
> \tilde\alpha_1(k) = \frac{\pi_k e_1(k)}{c_1}, \quad c_1=\sum_k \pi_k e_1(k)
> $$
> $$
> \tilde\alpha_t(k) = \frac{e_t(k)\sum_i \tilde\alpha_{t-1}(i) A_{i k}}{c_t}, \quad c_t=\sum_k e_t(k)\sum_i \tilde\alpha_{t-1}(i) A_{i k}
> $$
> Then log p(y_{1:T}) = ∑_t log c_t. Alternatively, compute in log space with log‑sum‑exp.

- Complexity: O(T K^2); memory can be O(TK) (for γ, ξ) or O(K) (streaming).

---

## Decoding (Viterbi)

Most probable state sequence ẑ_{1:T} = argmax_z p(z_{1:T} \mid y_{1:T}).

- Recursions (log space):
$$
\delta_1(k) = \log \pi_k + \log e_1(k), \qquad
\delta_t(j) = \log e_t(j) + \max_i \left[ \delta_{t-1}(i) + \log A_{i j} \right]
$$
- Backpointers:
$$
\psi_t(j) = \arg\max_i \left[ \delta_{t-1}(i) + \log A_{i j} \right]
$$
- Backtrack from ẑ_T = argmax_j δ_T(j), then ẑ_{t-1} = ψ_t(ẑ_t).

---

## Learning (Baum–Welch EM; MLE)

- E-step: run forward–backward to compute γ_t(k) and ξ_t(i,j).
- M-step:
  - Initial distribution:
  $$
  \hat\pi_k = \gamma_1(k)
  $$
  - Transitions:
  $$
  \hat A_{i j} = \frac{\sum_{t=1}^{T-1} \xi_t(i,j)}{\sum_{t=1}^{T-1} \gamma_t(i)}
  $$
  - Emissions:
    - Discrete emissions:
    $$
    \hat b_{k,v} = \frac{\sum_{t=1}^T \gamma_t(k)\,\mathbf{1}\{y_t=v\}}{\sum_{t=1}^T \gamma_t(k)}
    $$
    - Gaussian emissions:
    $$
    \hat \mu_k = \frac{\sum_{t=1}^T \gamma_t(k) \, y_t}{\sum_{t=1}^T \gamma_t(k)}, \qquad
    \hat \Sigma_k = \frac{\sum_{t=1}^T \gamma_t(k)\,(y_t-\hat\mu_k)(y_t-\hat\mu_k)'}{\sum_{t=1}^T \gamma_t(k)}
    $$

> [!note] Regularization and priors
> Add pseudocounts (Dirichlet) to A rows and emission probabilities to avoid zeros. Bayesian HMMs place priors on π, A, φ; see sticky HDP‑HMM (unknown K) and fit via [[Markov Chain Monte Carlo (MCMC)|MCMC]].

---

## Prediction and state inference

- Filtering distribution p(Z_t|y_{1:t}) is proportional to α_t (with scaling).
- One‑step predictive state:
$$
p(Z_{t+1}=j \mid y_{1:t}) = \sum_{i=1}^K p(Z_t=i \mid y_{1:t}) A_{i j}
$$
- Predictive observation:
$$
p(y_{t+1} \mid y_{1:t}) = \sum_{j=1}^K p(Z_{t+1}=j \mid y_{1:t}) \, p(y_{t+1}\mid Z_{t+1}=j)
$$

---

## Model selection and diagnostics

- Choose K: BIC/AIC on fitted log‑likelihood, held‑out predictive likelihood/perplexity, cross‑validation; spectral/moment methods can initialize or suggest K.
- Stationarity and dwell times: expected duration in state k is 1/(1−A_{kk}); geometric dwell‑time may be too restrictive → consider HSMM.
- Label switching: state labels are exchangeable; order states post‑hoc (e.g., by means, occupancy).
- Fit checks: residuals within states, state occupancy and transition heatmaps, stability across restarts/seeds, decoded paths vs known events.

---

## Variants and extensions

- HSMM (hidden semi‑Markov): explicit duration distributions (non‑geometric).
- HMM with GMM emissions: each state has a Gaussian mixture emission (nested EM).
- IO‑HMM (input–output): transitions and/or emissions depend on exogenous covariates.
- Switching linear dynamical systems (SLDS): discrete HMM over continuous LDS regimes; combines HMM with [[Kalman filter]].
- Bayesian nonparametrics: HDP‑HMM and sticky‑HDP‑HMM for unknown K; inference via Gibbs/beam sampling ([[Markov Chain Monte Carlo (MCMC)|MCMC]]).
- Online/streaming: particle filtering for HMMs; see [[Sequential Monte Carlo (SMC)|SMC]].

---

## Practical guidance

> [!tip] Implementation checklist
> - Numerical stability: scaling c_t or log‑space with log‑sum‑exp  
> - Initialization: k‑means (for Gaussian μ_k), random A with Dirichlet rows, emissions from clustered data  
> - Restarts: run EM from multiple seeds; pick best log‑likelihood  
> - Smoothing zeros: add small ε to A and emissions; renormalize  
> - Constraints: tie/fix parameters for identifiability; diagonal Σ_k for speed if reasonable  
> - Complexity: O(TK^2); reduce K or exploit sparsity if justified

> [!warning]
> - Overfitting with large K; spurious states that split noise  
> - Degenerate Σ_k or zero‑probability emissions; enforce floors/priors  
> - Interpreting labels literally; remember permutation symmetry  
> - Geometric durations may be unrealistic; prefer HSMM in such cases

---

## Minimal forward–backward (pseudocode)

```python
def logsumexp(arr):
    import math
    m = max(arr)
    s = sum(math.exp(a - m) for a in arr)
    return m + math.log(s)

def hmm_forward_backward(y, pi, A, emission_logp):
    """
    Forward–backward with scaling.
    Inputs:
      - y: sequence of observations (only used by emission_logp)
      - pi: length-K initial state probs
      - A: KxK transition matrix
      - emission_logp(t, k): returns log p(y_t | z_t=k)
    Returns:
      - loglik: log p(y_{1:T})
      - gamma: T x K matrix with p(z_t=k | y_{1:T})
      - xi: (T-1) x K x K with p(z_t=i, z_{t+1}=j | y_{1:T})
    """
    import math

    T, K = len(y), len(pi)
    log_alpha = [[-1e300]*K for _ in range(T)]
    log_beta  = [[0.0]*K for _ in range(T)]
    c = [0.0]*T
    loglik = 0.0

    # Forward (with scaling)
    for k in range(K):
        log_alpha[0][k] = math.log(pi[k]) + emission_logp(0, k)
    c[0] = logsumexp(log_alpha[0])
    log_alpha[0] = [la - c[0] for la in log_alpha[0]]
    loglik += c[0]

    for t in range(1, T):
        for j in range(K):
            terms = [log_alpha[t-1][i] + math.log(A[i][j]) for i in range(K)]
            log_trans = logsumexp(terms)
            log_alpha[t][j] = emission_logp(t, j) + log_trans
        c[t] = logsumexp(log_alpha[t])
        log_alpha[t] = [la - c[t] for la in log_alpha[t]]
        loglik += c[t]

    # Backward (scaled)
    for k in range(K):
        log_beta[T-1][k] = 0.0

    for t in range(T-2, -1, -1):
        for i in range(K):
            terms = [
                math.log(A[i][j]) + emission_logp(t+1, j) + log_beta[t+1][j] - c[t+1]
                for j in range(K)
            ]
            log_beta[t][i] = logsumexp(terms)

    # Gamma (state posteriors)
    gamma = [[0.0]*K for _ in range(T)]
    for t in range(T):
        logs = [log_alpha[t][k] + log_beta[t][k] for k in range(K)]
        z = logsumexp(logs)
        gamma[t] = [math.exp(l - z) for l in logs]

    # Xi (pairwise posteriors)
    xi = [[[0.0]*K for _ in range(K)] for __ in range(T-1)]
    for t in range(T-1):
        log_xi_t = [
            [
                log_alpha[t][i]
                + math.log(A[i][j])
                + emission_logp(t+1, j)
                + log_beta[t+1][j]
                - c[t+1]
                for j in range(K)
            ]
            for i in range(K)
        ]
        flat = [val for row in log_xi_t for val in row]
        z = logsumexp(flat)
        for i in range(K):
            for j in range(K):
                xi[t][i][j] = math.exp(log_xi_t[i][j] - z)

    return loglik, gamma, xi
```

> [!example] Viterbi (sketch)
> Maintain δ_t(j) and backpointers ψ_t(j) as in the equations above, iterating t=2..T; backtrack from argmax δ_T.

---

## Related notes

- [[Sequential Monte Carlo (SMC)|SMC]] · [[Markov Chain Monte Carlo (MCMC)|MCMC]] · [[Time Series (MOC)]]  
- [[Kalman filter]] · [[state-space model]]  
- Estimation frameworks: [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Bayesian econometrics]] · [[priors]]

---

## References

- Baum & Petrie (1966); Baum et al. (1970): HMM and EM (Baum–Welch)
- Rabiner (1989): A tutorial on HMMs and selected applications
- Cappé, Moulines, & Rydén (2005): Inference in Hidden Markov Models
- Bishop (2006): Pattern Recognition and Machine Learning (HMM chapter)
- Murphy (2012): Machine Learning: A Probabilistic Perspective (HMMs)
- Fox et al. (2008, 2011): HDP‑HMM and sticky HDP‑HMM (Bayesian nonparametrics)

---
