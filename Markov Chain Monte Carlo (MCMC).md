---
title: Markov Chain Monte Carlo (MCMC)
aliases: [MCMC, Markov chain Monte Carlo, markov chain monte carlo, Metropolis–Hastings, Gibbs sampling, HMC, NUTS, slice sampling]
tags: [bayesian, mcmc, inference, sampling, posterior, diagnostics, hmc, nuts, gibbs, metropolis, state-space, hierarchical]
updated: 2025-09-17
---

# Markov Chain Monte Carlo (MCMC)

> [!summary] Quick definition
> Markov chain Monte Carlo (MCMC) generates dependent draws from a target distribution (typically a Bayesian posterior) by simulating a Markov chain whose stationary distribution equals the target. Popular algorithms include Metropolis–Hastings (MH), Gibbs sampling, Hamiltonian Monte Carlo (HMC/NUTS), and slice sampling. Correct parameterization, convergence diagnostics (R̂, ESS), and posterior predictive checks are essential.

- Where it fits: [[Bayesian econometrics]] (hierarchical models, BVAR/DSGE, state-space), causal models (Bayesian DiD/IV), and predictive pipelines (posterior predictive) across [[Econometrics (MOC)]] and [[Time Series (MOC)]].
- Complements frequentist inference (see [[Hypothesis testing]]); MCMC produces posterior distributions and credible intervals, not p-values.

---

## Why MCMC?

- Flexible posteriors: integrate complex priors/likelihoods that defy closed-form solutions.
- Hierarchies and partial pooling: borrow strength across groups (firms, regions), with principled uncertainty.
- Latent states and dynamics: state-space models (local level/trend/[[seasonality]]), stochastic volatility, time-varying parameters.
- Decision-making: posterior predictive for policy optimization; coherent uncertainty propagation into downstream [[policy learning]] or forecasting.

> [!note] Credible vs confidence intervals
> A 95% credible interval is Pr(θ ∈ interval | data)=0.95. It is distinct from frequentist 95% CIs in [[Hypothesis testing]].

---

## Target and notation

- Target posterior: π(θ) ∝ p(y|θ) p(θ), where p(y|θ) is the likelihood and p(θ) is the prior (see [[Bayesian econometrics]]).
- Goal: approximate E[g(θ)|y] and draw samples θ^(s) ~ π(θ|y) for summaries and posterior predictive.

---

## Core algorithms

### Metropolis–Hastings (MH)

- Propose θ' ~ q(·|θ) and accept with
$$
\alpha(\theta \to \theta') = \min\!\left\{1,\ \frac{\pi(\theta')\,q(\theta\mid\theta')}{\pi(\theta)\,q(\theta'\mid\theta)}\right\}.
$$

> [!tip] Practice
> - Symmetric random-walk (q(θ'|θ)=q(θ|θ')) reduces to π(θ')/π(θ).
> - Tune proposal scale for reasonable acceptance (e.g., 0.2–0.5; ≈0.234 asymptotically for Gaussian targets).
> - Use covariance-informed proposals (pre-adaptation or adaptive MH with diminishing adaptation).

### Gibbs sampling (and Metropolis-within-Gibbs)

- Sample blocks from full conditionals when available:
$$
\theta_j \sim \pi(\theta_j\mid \theta_{-j},y).
$$
- Conjugate structures (Normal-inverse-gamma, Dirichlet-multinomial) enable efficient cycles.
- With intractable conditionals, embed MH within Gibbs for that block.

### Slice sampling

- Introduce auxiliary height u and sample uniformly from {θ: f(θ) ≥ u}. Self-tuning step sizes; robust to some tail issues.

### Hamiltonian Monte Carlo (HMC) and NUTS

- Use gradients ∇ log π(θ) to simulate Hamiltonian dynamics; long-distance, high-acceptance proposals; strong in moderate/high dimensions.
- NUTS (No-U-Turn Sampler) adaptively chooses trajectory length and tunes step size/mass matrix during warmup.

> [!warning] HMC diagnostics
> - Divergences → reparameterize (non-centered), tighten priors, increase `target_accept`, re-scale parameters.
> - Max tree depth → increase depth or smooth posterior geometry.

---

## Practical workflow

> [!check] End-to-end checklist
> - [ ] Specify model and priors (weakly informative by default); run prior predictive checks ([[Bayesian econometrics]])  
> - [ ] Choose sampler: HMC/NUTS for continuous/differentiable; Gibbs/MH for conjugate or discrete blocks; particle methods for non-conjugate state-space  
> - [ ] Parameterize well: non-centered hierarchies, transform constraints (log σ, logit p), standardize predictors  
> - [ ] Run multiple chains with warmup (adaptation) and sufficient draws; set seeds; record versions  
> - [ ] Diagnose: R̂ ≤ 1.01, bulk/tail ESS large, stable traceplots, low autocorrelation; for HMC: 0 divergences and adequate E-BFMI  
> - [ ] Posterior predictive checks (PPC): replicated data match salient features (level, dispersion, tails, seasonality)  
> - [ ] Sensitivity: alternative priors/scales, reparameterizations; report impact on key quantities  
> - [ ] Summarize posteriors (means/medians/credible intervals), and (if relevant) compare across models via LOO/WAIC

---

## Parameterization patterns

- Constrained parameters
  - Sample on unconstrained scale: σ = exp(η), p = logistic(η), Cholesky factors for covariances.
- Non-centered hierarchies
  - Centered: θ_j ~ N(μ, τ^2) can mix poorly when τ small; prefer θ_j = μ + τ z_j with z_j ~ N(0,1).
- Scaling & standardization
  - Standardize predictors to O(1) to help HMC geometry; scale priors accordingly.

---

## Diagnostics in detail

- Convergence
  - Split R̂ (target ≤ 1.01), bulk/tail ESS, MCSE (Monte Carlo SE).
- Visuals
  - Traceplots (stationarity, mixing), rank plots, ACF.
- HMC-specific
  - Divergences (should be zero), treedepth saturations, energy/BFMI (should be reasonable).
- Fit adequacy
  - PPC: compare replicated vs observed via discrepancy metrics; residual-like checks; calibration curves.

> [!tip] Thinning is rarely needed. Prefer longer chains and report ESS/MCSE.

---

## Posterior predictive and decisions

- Posterior predictive distribution:
$$
p(y^{\text{new}}\mid y) = \int p(y^{\text{new}}\mid \theta)\,p(\theta\mid y)\,d\theta
$$
- Use for predictive metrics (MAE/RMSE), uncertainty bands, and decision rules (minimize expected loss).
- In experimentation ([[AB Testing (MOC)]]), Bayesian posterior predictive can complement frequentist [[sequential testing]]; pre-register if used ([[pre-registration]]).

---

## Common econometric models with MCMC

- Hierarchical linear/GLM
  - Partial pooling of coefficients across groups (firms/regions/products); random intercepts/slopes with priors on SDs.
- Time series and [[Time Series (MOC)]]
  - State-space (local level/trend/[[seasonality]]), stochastic volatility; HMC or Gibbs/FFBS; BSTS-like interventions (Bayesian synthetic control).
- BVAR/DSGE
  - Shrinkage priors (Minnesota, horseshoe) with Gibbs/MH/HMC; posterior predictive for IRFs and out-of-sample.
- Causal models
  - Bayesian [[Difference-in-Differences (DiD)]] (hierarchical trends), Bayesian RDD (GP priors), Bayesian IV (joint structural models). Report posterior for treatment effects with PPC.

---

## Relation to other topics

- [[Bayesian econometrics]]: conceptual foundation (priors, posterior, predictive, decision theory)
- Frequentist comparison: [[Hypothesis testing]] (p-values/Type I error) vs credible intervals and posterior decisions
- Experimental pipelines: [[AB Testing (MOC)]], [[sequential testing]], [[False Discovery Rate (FDR)|FDR]]/[[multiple testing control]] (if combining many Bayesian decisions, still mind multiplicity governance)
- Modeling toolkits: [[Prophet]] (additive trend/holidays; Bayesian-ish), [[Time Series (MOC)]]
- Causal toolkits: [[Difference-in-Differences (DiD)]], [[Instrumental Variables (IV)]], [[weak instruments]] (Bayesian alternatives exist)
- Policy and uplift: [[policy learning]], [[uplift]] (Bayesian learners/policy posteriors)
- Data hygiene: avoid [[leakage]] (post-treatment features), use time-aware splits and reproducible seeds

---

## Minimal code snippets

> [!example] Python: Random-Walk Metropolis (toy)

```python
import numpy as np

def logpi(theta):  # target log-density; std normal example
    return -0.5 * theta**2

def rw_metropolis(n=20000, sigma=1.0, x0=0.0, seed=1):
    rng = np.random.default_rng(seed)
    x = np.empty(n); x[0] = x0; acc = 0
    for t in range(1, n):
        prop = x[t-1] + rng.normal(0, sigma)
        loga = logpi(prop) - logpi(x[t-1])
        if np.log(rng.uniform()) < loga:
            x[t] = prop; acc += 1
        else:
            x[t] = x[t-1]
    return x, acc/(n-1)

samples, acc = rw_metropolis(sigma=1.0)
print("Acceptance:", acc)
```

> [!example] Python: HMC/NUTS with PyMC

```python
# pip install pymc arviz
import pymc as pm, arviz as az

with pm.Model() as model:
    beta0 = pm.Normal('beta0', 0, 10)
    beta  = pm.Normal('beta', 0, 2, shape=X.shape[1])
    mu    = beta0 + pm.math.dot(X, beta)
    sigma = pm.HalfNormal('sigma', 1)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=Y)
    idata = pm.sample(2000, tune=1000, chains=4, target_accept=0.9, random_seed=123)
az.summary(idata, var_names=['beta0','beta','sigma'])
az.plot_trace(idata); az.plot_ppc(idata)
```

> [!example] R: brms/Stan (hierarchical model)

```r
library(brms)
fit <- brm(
  Y ~ X + (1|group),
  data = df,
  prior = c(prior(normal(0, 5), class="b"),
            prior(student_t(3, 0, 10), class="Intercept"),
            prior(exponential(1), class="sd")),
  chains = 4, iter = 2000, seed = 123
)
summary(fit)
pp_check(fit)
```

> [!example] R: JAGS (Gibbs-friendly)

```r
library(rjags); library(coda)
model_string <- "
model {
  for (i in 1:N) {
    y[i] ~ dnorm(mu, tau)
  }
  mu ~ dnorm(0, 1.0E-4)
  tau <- pow(sigma, -2)
  sigma ~ dunif(0, 100)
}
"
jm <- jags.model(textConnection(model_string), data=list(y=Y,N=length(Y)), n.chains=4, n.adapt=1000)
update(jm, 2000)
samps <- coda.samples(jm, c("mu","sigma"), n.iter=5000)
summary(samps)
plot(samps)
```

---

## Tuning & adaptation

- MH: adapt proposal covariance during warmup (diminishing adaptation), then fix; target acceptance in a reasonable band.
- HMC/NUTS: use warmup (mass matrix/step size adaptation); increase `target_accept` (e.g., 0.9–0.99) if divergences arise; reparameterize hierarchies.
- Gibbs: block updates for correlated parameters; use parameter expansion if mixing is slow.

---

## Power vs MCSE

- [[power analysis]]/[[Minimum Detectable Effect (MDE)|MDE]] belong to design-time questions about detecting effects in new data (frequentist).
- MCMC Monte Carlo error (MCSE) is simulation accuracy for posterior summaries conditional on observed data; reduce MCSE by increasing ESS (longer chains / better mixing).
- Avoid conflating MCSE with statistical power; report both where relevant (e.g., in preregistered Bayesian analyses; see [[pre-registration]]).

---

## Common pitfalls and remedies

> [!warning]
> - Using MCMC outputs without diagnostics (R̂/ESS/trace); ignoring divergences in HMC  
> - Poor parameterization (centered hierarchies when non-centered needed; unscaled predictors) → slow mixing  
> - Overly vague priors → unstable posteriors; prefer weakly informative priors  
> - Label switching in mixtures; impose identifiability or post-process  
> - Treating PPC as “nice plots only”—use quantitative checks and calibration  
> - [[leakage]]: including post-treatment information in Bayesian causal models

---

## Reporting essentials

- Model specification (likelihood, hierarchies), priors (forms/scales), and rationale
- Sampler (MH/Gibbs/HMC/NUTS), software/versions, chains, warmup, iterations, seeds
- Diagnostics: R̂, bulk/tail ESS, MCSE, divergences/max treedepth (HMC), trace/ACF
- Posterior summaries (means/medians, 50/95% credible intervals), posterior correlations
- Posterior predictive checks and predictive performance (LOO/WAIC; [[Bayesian econometrics]])
- Sensitivity to priors and parameterizations
- Reproducibility: code and environment details

---

## Related notes

- [[Bayesian econometrics]] · [[Econometrics (MOC)]] · [[Time Series (MOC)]]
- [[Hypothesis testing]] · [[sequential testing]] · [[multiple testing control]]
- [[Difference-in-Differences (DiD)]] · [[Instrumental Variables (IV)]] · [[weak instruments]]
- [[policy learning]] · [[uplift]]
- [[Prophet]]
- [[leakage]] · [[pre-registration]]

---