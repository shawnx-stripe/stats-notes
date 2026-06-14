---
title: priors
aliases: [prior distributions, prior elicitation, weakly-informative priors, shrinkage priors]
tags: [bayesian, priors, elicitation, shrinkage, hierarchical, modeling, diagnostics]
updated: 2025-09-17
---

# priors

> [!summary] Quick definition
> In Bayesian inference, a prior p(θ) encodes information or regularization about parameters before observing data. Combined with the likelihood p(y|θ) it yields the posterior p(θ|y) ∝ p(y|θ)p(θ). Good priors stabilize estimation, improve predictive performance, and reflect domain knowledge; they are validated with prior-predictive checks and sensitivity analysis.

- Where used: across [[Bayesian econometrics]] (hierarchical panels, BVAR/SV/TVP in [[Time Series (MOC)]], state-space), causal models (Bayesian [[Difference-in-Differences (DiD)]], Bayesian [[Instrumental Variables (IV)]], Bayesian RDD), and product experimentation (Bayesian [[AB Testing (MOC)]], guardrails).
- Computation: via [[Markov Chain Monte Carlo (MCMC)|MCMC]] (Gibbs, MH, HMC/NUTS) or VI; priors shape posterior geometry and sampler behavior.

---

## Why priors matter

- Regularization: avoid overfitting, control tail behavior, aid weak identification (cf. frequentist [[weak instruments]]).
- Domain knowledge: encode signs, magnitudes, bounds, smoothness/persistence (e.g., time-series [[seasonality]] or AR stability).
- Identifiability: resolve symmetries (mixture label switching), stabilize latent scales in state-space.
- Decision-making: coherent posterior and posterior predictive for actions (e.g., targeting in [[policy learning]] / [[uplift]]).

> [!warning] Improper or overly diffuse priors can produce improper posteriors, degrade HMC (divergences), and make Bayes factors undefined.

---

## Prior → posterior → predictive (reminder)

- Posterior:
$$
p(\theta\mid y)\ \propto\ p(y\mid \theta)\,p(\theta).
$$
- Posterior predictive:
$$
p(y^{\text{new}}\mid y) = \int p(y^{\text{new}}\mid \theta)\,p(\theta\mid y)\,d\theta.
$$
See [[Bayesian econometrics]] for workflow and diagnostics; see [[Markov Chain Monte Carlo (MCMC)|MCMC]] for computation.

---

## Practical defaults (weakly-informative)

Assume predictors are standardized (mean 0, SD 1) and outcomes roughly scaled.

- Regression β (GLM/linear): Normal(0, 2) or Student‑t(ν=3, 0, 2).
- Intercept: Student‑t(3, 0, 10) or Normal(0, 5) depending on scale.
- Residual SD σ: half‑Normal(0, 1) or half‑Student‑t(3, 0, 1); place priors on SDs, not variances.
- Group-level SDs (hierarchies): half‑Normal(0, 1) / half‑t; prefer non-centered parameterization (see [[Markov Chain Monte Carlo (MCMC)|MCMC]]).
- Correlations: LKJ(η) prior (η≈1 weak; η>1 shrinks toward identity, e.g., LKJ(2)).

> [!tip] Standardize X or explicitly calibrate priors on raw units; weakly-informative priors are most interpretable on standardized scales.

---

## Shrinkage priors (high-dimensional/regularization)

- Ridge/Normal: β_j ∼ Normal(0, τ²) (global shrinkage).
- Laplace (Bayesian LASSO): β_j ∼ Laplace(0, b) (sparsity-friendly).
- Horseshoe (global–local):
$$
\beta_j \sim \mathcal{N}(0, \lambda_j^2 \tau^2),\ \ 
\lambda_j \sim \text{half‑Cauchy}(0,1),\ \ 
\tau \sim \text{half‑Cauchy}(0,1).
$$
- Spike‑and‑slab: mixture (1−π)·δ₀ + π·Normal(0, τ²) for explicit selection (heavier computation; label switching risks).

> [!tip] Horseshoe (or regularized horseshoe) is a robust default for sparse signals; Bayesian LASSO is simple; spike‑and‑slab is interpretable but mix-heavy.

---

## Hierarchical priors (partial pooling)

- Random intercepts/slopes:
  - Non-centered: θ_j = μ + τ z_j, z_j ∼ Normal(0,1); τ ∼ half‑t/half‑Normal.
- Correlated effects:
  - u ∼ MVN(0, Σ) with SD priors (half‑t) and LKJ prior on correlations.

Shrinkage across groups organically mitigates multiple comparisons, complementing frequentist [[multiple testing control]]/[[False Discovery Rate (FDR)|FDR]].

---

## Priors by econometric structure

### Time series and state-space (see [[Time Series (MOC)]])
- Local level/trend/[[seasonality]]: half‑t on state innovation SDs; stationarity priors for AR/VAR (e.g., stability transformation or Beta prior on AR roots).
- Stochastic volatility: priors on log‑variance AR(1) persistence (φ on (−1,1)) and innovation scales (half‑t).
- BVAR (Minnesota/SS/Litterman): global tightness λ, lag decay, cross-variable penalty; alternatives: SSVS, Normal‑Inverse‑Wishart.

### Causal models
- Bayesian DiD: shrinkage priors on event‑time paths (pre‑period centered near 0), hierarchical time/unit effects; report posterior event‑study with bands (compare to frequentist [[event study]]).
- Bayesian RDD: smoothness priors (splines/GP) on trends; prior on cutoff jump; monotonicity if warranted.
- Bayesian IV: priors on first stage and structural parameters to stabilize weak identification (still require [[exclusion restriction]] and [[relevance]]; compare to [[weak instruments]] issues).

### Structural / DSGE
- Informative priors on preference/technology (β, σ, ϕ), measurement errors; check prior predictive moments and identification.

### Product/AB
- Bayesian guardrail/OEC models: priors on rates/latencies; combine with [[sequential testing]] governance in dashboards (preregister in [[pre-registration]]).

---

## Prior predictive checks and sensitivity

> [!check] Workflow
> - [ ] Prior predictive: simulate θ∼p(θ), y∼p(y|θ) to ensure plausible ranges (levels, dispersion, tails, seasonality patterns).  
> - [ ] Posterior sensitivity: vary scales/structures (e.g., τ in horseshoe; λ in Minnesota) and report impact on key posteriors.  
> - [ ] Predictive validation: PPC and LOO/WAIC to assess fit (see [[Bayesian econometrics]]).

> [!warning] Bayes factors are highly prior-sensitive and invalid with improper priors; prefer LOO/WAIC and posterior predictive checks.

---

## Constraints and transformations

- Positive parameters: work on log scale (σ = exp η) or truncated priors; ensure samplers see unconstrained geometry (Stan auto-transforms).
- Probabilities/simplex: logit/softmax parameterizations.
- Signs/monotonicity: truncated priors or reparameterize to enforce constraints.

---

## Links to frequentist counterparts

- Priors as regularizers mirror L2/L1 penalties; Bayesian shrinkage delivers full posteriors.
- Hierarchical priors vs pooled/unpooled OLS/GLS; pool adaptively via τ’s posterior.
- For cluster/geo/switchback designs, Bayesian hierarchies can model cluster/time variation directly; frequentist alternatives rely on [[clustered standard errors]] / [[few-cluster corrections]] / [[wild cluster bootstrap]].

---

## Interactions with causal ML and policy

- Use priors in Bayesian CATE learners (Bayesian trees/forests/NTRP) or place shrinkage on heterogeneous effects; compare with [[causal forests]]/[[double machine learning]] (frequentist).
- Translate posterior predictive to decisions in [[policy learning]]; validate offline with [[off-policy evaluation]] and online with [[AB Testing (MOC)]] guardrails.

---

## Implementation snippets

> [!example] R (brms): weakly-informative & hierarchical

```r
library(brms)
fit <- brm(
  Y ~ X1 + X2 + (1|group),
  data = df,
  family = gaussian(),
  prior = c(
    prior(normal(0, 2), class = "b"),               # coefficients
    prior(student_t(3, 0, 10), class = "Intercept"),
    prior(exponential(1), class = "sd"),            # group SD
    prior(exponential(1), class = "sigma")          # residual SD
  ),
  chains=4, iter=2000, seed=123
)
pp_check(fit)   # prior/posterior predictive checks per [[Bayesian econometrics]]
```

> [!example] Python (PyMC): horseshoe regression

```python
import pymc as pm, numpy as np

with pm.Model() as m:
    tau = pm.HalfCauchy('tau', beta=1)
    lam = pm.HalfCauchy('lam', beta=1, shape=p)
    beta = pm.Normal('beta', mu=0, sigma=tau*lam, shape=p)
    sigma = pm.HalfNormal('sigma', 1.0)
    mu = pm.math.dot(X, beta)
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=Y)
    idata = pm.sample(2000, tune=2000, target_accept=0.9, random_seed=123)
```

> [!example] R: BVAR Minnesota prior tuning

```r
library(BVAR)
fit_bvar <- bvar(y, lags = 4, n_draw = 20000, n_burn = 5000,
                 priors = bv_priors(specifications = bv_mn_priors(lambda = 0.2)))
```

> [!example] Stan: LKJ + half‑t on SDs (snippet)

```stan
parameters {
  vector[K] beta;
  real<lower=0> sigma;
  vector<lower=0>[K] tau;
  cholesky_factor_corr[K] L_Omega;
  matrix[K, N_groups] z;
}
transformed parameters {
  matrix[K, N_groups] u = diag_pre_multiply(tau, L_Omega) * z;
}
model {
  beta ~ normal(0, 2);
  sigma ~ normal(0, 1);           // half-normal via lower=0
  tau ~ normal(0, 1);             // half-normal for group SDs
  L_Omega ~ lkj_corr_cholesky(2); // LKJ(2) prior
  to_vector(z) ~ normal(0, 1);
  // likelihood ...
}
```

---

## Pitfalls and remedies

> [!warning]
> - Improper priors → improper posteriors; avoid unless posterior propriety is proven.  
> - Overly diffuse priors in high‑dim problems → divergent transitions in HMC; tighten to weakly‑informative.  
> - Priors on variances rather than SDs → awkward scales; prefer SDs with half‑t/half‑Normal.  
> - Heavy Cauchy tails everywhere → geometry issues; prefer Student‑t(ν=3) or Normal unless tails are justified.  
> - No prior predictive/sensitivity → undetected miscalibration.  
> - Using post‑treatment variables to set priors in causal models → [[leakage]].

---

## Reporting essentials

> [!check]
> - [ ] Priors per parameter class (β, σ, group SDs, correlations) with scales and rationale  
> - [ ] Standardization/transformations; link to how priors map to raw units  
> - [ ] Prior predictive checks and sensitivity analyses (quantify impact)  
> - [ ] Structural constraints (signs, monotonicity, stationarity) if any  
> - [ ] Reproducibility: code (brms/Stan/PyMC), seeds, software versions

---

## Related notes

- Foundations & computation: [[Bayesian econometrics]] · [[Markov Chain Monte Carlo (MCMC)|MCMC]]  
- Modeling domains: [[Time Series (MOC)]] · [[Prophet]] · [[seasonality]]  
- Causal: [[Difference-in-Differences (DiD)]] · [[Instrumental Variables (IV)]] · [[weak instruments]] · [[Synthetic Control]]  
- Experimentation: [[AB Testing (MOC)]] · [[sequential testing]] · [[multiple testing control]]/[[False Discovery Rate (FDR)|FDR]] · [[Overall Evaluation Criterion (OEC)|OEC]] · [[guardrail metric]]  
- Causal ML & policy: [[double machine learning]] · [[causal forests]] · [[policy learning]] · [[uplift]] · [[off-policy evaluation]]  
- Hygiene: [[leakage]] · [[pre-registration]]  
- Inference contrasts: [[Hypothesis testing]]; robust frequentist add‑ons (e.g., [[clustered standard errors]], [[few-cluster corrections]])

---

## Further reading

- Gelman et al., Bayesian Data Analysis (BDA3) — prior choices and predictive checks  
- Piironen & Vehtari (2017) — regularized horseshoe  
- Kastner — SV priors; Litterman — Minnesota priors (BVAR)  
- Stan/PyMC docs on priors, prior/posterior predictive checks, LKJ priors

---