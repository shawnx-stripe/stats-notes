---
title: Sequential Monte Carlo (SMC)
aliases: [Sequential Monte Carlo, particle filter, particle filters, particle MCMC, PMCMC, SMC samplers, SMC, sequential monte carlo]
tags: [bayesian, monte-carlo, time-series, state-space, filtering, smoothing, resampling, pmcmc, inference]
updated: 2025-09-21
---

# Sequential Monte Carlo (SMC)

> [!summary] Quick definition
> Sequential Monte Carlo (SMC) methods approximate a sequence of probability distributions with weighted samples (particles) that are propagated and resampled over time. In state‑space models, SMC implements online filtering p(x_t | y_{1:t}), smoothing p(x_{0:t} | y_{1:t}), and unbiased likelihood estimation for [[Markov Chain Monte Carlo (MCMC)|MCMC]] via particle MCMC (PMCMC).

- Core ideas: importance sampling with sequential updates, weight degeneracy monitoring (ESS), resampling to control variance, and optional MCMC “move” steps for rejuvenation.
- Related: [[Markov Chain Monte Carlo (MCMC)|MCMC]], [[Bayesian econometrics]], [[Time Series (MOC)]], [[Synthetic Control]] (distinct), [[Kalman filter]] for the linear‑Gaussian special case.

---

## Setup and notation

- State‑space model (SSM):
$$
\begin{aligned}
x_0 &\sim p(x_0), \\
x_t \mid x_{t-1} &\sim f_\theta(x_t \mid x_{t-1}), \\
y_t \mid x_t &\sim g_\theta(y_t \mid x_t), \quad t=1,\dots,T.
\end{aligned}
$$
- Filtering recursion:
$$
p(x_t \mid y_{1:t}) \propto g_\theta(y_t \mid x_t)\int f_\theta(x_t \mid x_{t-1})\, p(x_{t-1} \mid y_{1:t-1})\,dx_{t-1}.
$$
- Particle approximation: a set {(x_t^{(i)}, w_t^{(i)})}_{i=1}^N with normalized weights ∑_i w_t^{(i)}=1.

---

## Bootstrap particle filter (SIR)

Proposal q equals the transition, q(x_t|x_{t-1},y_t)=f_\theta(x_t|x_{t-1}).

- Propagate:
$$
x_t^{(i)} \sim f_\theta(\cdot \mid x_{t-1}^{(a_i)}),
$$
where a_i is the ancestor index after resampling at t−1.
- Weights:
$$
\tilde w_t^{(i)} \propto g_\theta\!\left(y_t \mid x_t^{(i)}\right), \quad
w_t^{(i)} = \frac{\tilde w_t^{(i)}}{\sum_j \tilde w_t^{(j)}}.
$$
- Effective sample size (ESS):
$$
\operatorname{ESS}_t = \frac{1}{\sum_{i=1}^N (w_t^{(i)})^2}.
$$
- Resample if ESS_t < τN (e.g., τ=0.5). Prefer systematic/stratified over multinomial resampling.

> [!example] Minimal pseudocode (bootstrap PF)

```python
def particle_filter(y, N, theta, resample_threshold=0.5):
    # initialize
    x = [sample_p_x0(theta) for _ in range(N)]
    w = normalize([g_theta(y[0], xi, theta) for xi in x])
    loglik = math.log(sum([g_theta(y[0], xi, theta) for xi in x]) / N)

    for t in range(1, len(y)):
        ESS = 1.0 / sum(wi*wi for wi in w)
        if ESS < resample_threshold * N:
            a = systematic_resample(w)  # indices length N
            x = [x[i] for i in a]
            w = [1.0/N]*N

        # propagate
        x = [sample_f(xi, theta) for xi in x]

        # weight
        unnorm = [wi * g_theta(y[t], xi, theta) for wi, xi in zip(w, x)]
        Zt = sum(unnorm)
        w = [ui / Zt for ui in unnorm]
        loglik += math.log(Zt)

    return x, w, loglik  # final particles, weights, unbiased log-likelihood estimator
```

---

## General SMC update (with proposal q)

With proposal q(x_t|x_{t-1}, y_t):
$$
\tilde w_t^{(i)} \propto w_{t-1}^{(a_i)} \cdot \frac{g_\theta\!\left(y_t \mid x_t^{(i)}\right)\, f_\theta\!\left(x_t^{(i)} \mid x_{t-1}^{(a_i)}\right)}{q\!\left(x_t^{(i)} \mid x_{t-1}^{(a_i)}, y_t\right)}.
$$

- Auxiliary particle filter (APF): anticipates promising particles via look‑ahead weights; reduces variance (good for peaky likelihoods).
- Rao–Blackwellization: when a linear‑Gaussian substructure exists, integrate it with a [[Kalman filter]] inside the PF (RBPF).

---

## Smoothing

- Path space degeneracy affects long‑horizon smoothing.
- Common smoothers:
  - FFBSi (forward filter backward simulator): sample trajectories with backward kernels.
  - Two‑filter smoother: combine forward and backward information.
  - Particle Gibbs with ancestor sampling (PGAS) provides high‑quality smoothing within PMCMC.

---

## Likelihood estimation and PMCMC

- The particle filter provides an unbiased likelihood estimator:
$$
\hat p_\theta(y_{1:T}) = \prod_{t=1}^T \left(\frac{1}{N}\sum_{i=1}^N \tilde w_t^{(i)}\right).
$$
- Particle marginal MH (PMMH): plug unbiased likelihood into MH to sample θ from p(θ|y).
- Particle Gibbs (PG) and PG with ancestor sampling (PGAS) alternate between θ and latent trajectories using conditional SMC.

---

## SMC for static targets (SMC samplers)

- Tempering sequence:
$$
\pi_t(\theta) \propto p(\theta)\, p(y\mid \theta)^{\phi_t}, \quad 0=\phi_0 < \cdots < \phi_T=1.
$$
- Incremental weights:
$$
\tilde w_t^{(i)} \propto w_{t-1}^{(i)} \left[p(y\mid \theta^{(i)})\right]^{\phi_t - \phi_{t-1}}.
$$
- After weighting, apply MCMC “move” kernels that leave π_t invariant to rejuvenate particles.

---

## Practical guidance

- Number of particles N: scale with state dimension and observation informativeness; for PMMH, increase N to keep Var(log-likelihood) ≈ 1–2.
- Resampling:
  - Schemes: systematic (fast, low variance), stratified, residual; avoid excessive multinomial resampling.
  - Trigger by ESS or always‑resample; always‑resample simplifies but can add noise.
- Proposals:
  - Bootstrap (q=f) is robust; APF or locally adapted q improves efficiency when g(y_t|x_t) is sharp.
- Degeneracy control:
  - Monitor ESS and diversity; consider “move steps” (short MCMC) or jittering in parameter SMC.
- Parallelization: propagation and weighting are embarrassingly parallel; resampling requires collective operations.

---

## Diagnostics and checks

> [!check]
> - [ ] ESS trajectory and resampling counts within expected range  
> - [ ] Stability of log-likelihood estimates across seeds and N  
> - [ ] Weight variance and particle diversity (unique ancestor counts)  
> - [ ] For PMCMC: acceptance rate, autocorrelation, variance of log-likelihood near 1–2  
> - [ ] Smoothing quality: compare marginal posteriors across horizons; path degeneracy not severe

---

## When to use SMC

- Online/streaming inference in non‑linear, non‑Gaussian SSMs.
- Computing p(y|θ) or p(θ|y) when the likelihood is intractable but simulable.
- Joint state and parameter inference via PMCMC or SMC^2.
- Alternatives: [[Kalman filter]] for linear‑Gaussian; [[Markov Chain Monte Carlo (MCMC)|MCMC]] for batch static models.

---

## Common pitfalls

> [!warning]
> - Too few particles → weight degeneracy and biased functionals  
> - Frequent multinomial resampling → high variance; prefer systematic/stratified  
> - Poor proposals in high signal‑to‑noise regimes → collapse; use APF/adapted q  
> - Ignoring path degeneracy for smoothing; use FFBSi/PGAS  
> - For PMMH: overly noisy likelihood → poor mixing; tune N and proposals

---

## Reporting essentials

- Model specification f, g, priors; whether filtering, smoothing, PMCMC, or SMC sampler
- Particle count N, resampling scheme and threshold, proposal choice
- Diagnostics: ESS, resampling frequency, log-likelihood variance, acceptance rates (PMCMC)
- Computational budget, seeds, and software versions
- Sensitivity to N, proposals, tempering schedule (if SMC sampler)

---

## Related notes

- [[Markov Chain Monte Carlo (MCMC)|MCMC]] · [[Bayesian econometrics]] · [[Time Series (MOC)]]  
- [[Kalman filter]] · [[state-space model]] · [[Hidden Markov Model (HMM)|HMM]]  
- [[Markov Chain Monte Carlo (MCMC)|MCMC]] links: [[priors]] · [[Sequential Monte Carlo (SMC)|SMC]] complements [[Markov Chain Monte Carlo (MCMC)|MCMC]] for dynamic latent variable models

---

## References

- Gordon, Salmond, & Smith (1993). Novel approach to nonlinear/non-Gaussian Bayesian state estimation (bootstrap PF).
- Pitt & Shephard (1999). Filtering via simulation (APF).
- Doucet, de Freitas, & Gordon (2001). Sequential Monte Carlo in Practice.
- Del Moral (2004). Feynman–Kac Formulae (SMC theory).
- Andrieu, Doucet, & Holenstein (2010). Particle MCMC.
- Chopin (2002); Chopin & Papaspiliopoulos (2020). SMC for static and dynamic models.
- Lindsten, Jordan, & Schön (2014). Particle Gibbs with ancestor sampling (PGAS).
- Doucet & Johansen (2011). A tutorial on particle filtering and smoothing.

---
