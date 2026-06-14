---
title: Bayesian econometrics
aliases: [Bayesian methods in econometrics, Bayesian inference, Bayesian DSGE, BVAR, hierarchical Bayes]
tags: [econometrics, bayesian, mcmc, priors, posterior, predictive, diagnostics, hierarchical, bvar, state-space, glm, shrinkage]
updated: 2025-09-17
---

# Bayesian econometrics

> [!summary] Quick definition
> Bayesian econometrics combines a prior p(θ) with the data likelihood p(y|θ) to obtain the posterior p(θ|y) ∝ p(y|θ)p(θ). Inference summarizes the posterior (means/medians/credible intervals) and the posterior predictive, often via [[Markov Chain Monte Carlo (MCMC)|MCMC]] (Gibbs, MH, HMC/NUTS) or variational inference. It excels at hierarchical/shrinkage modeling, complex latent-state/time-series structures, principled uncertainty, and decision-making under a loss function.

- Where it’s used: panel/hierarchical models, [[Time Series (MOC)]] (state-space, BVAR/SV/TVP), structural models (DSGE), and causal models (Bayesian DiD/RDD/IV).
- Complements frequentist [[Hypothesis testing]] with posterior credible intervals and decision-theoretic summaries.

---

## Core building blocks

- Prior p(θ): regularization or genuine prior information (informative, weakly-informative, reference).
- Likelihood p(y|θ): model for data given parameters (linear/GLM/state-space/structural).
- Posterior:
$$
p(\theta\mid y)\ \propto\ p(y\mid \theta)\,p(\theta).
$$
- Posterior predictive:
$$
p(y^{\text{new}}\mid y) = \int p(y^{\text{new}}\mid \theta)\,p(\theta\mid y)\,d\theta.
$$
- Decision: choose a to minimize posterior expected loss E[L(a,θ)|y] (posterior mean under squared loss; median under absolute loss).

See also: [[Markov Chain Monte Carlo (MCMC)|MCMC]] for computation, [[Time Series (MOC)]] for forecast models.

---

## Why Bayesian?

- Hierarchical/partial pooling: stabilize noisy group effects (firms, regions, products).
- Flexible shrinkage: horseshoe/Laplace/spike–slab priors for high-dimensional regression.
- Latent states/dynamics: coherent handling of unobserved components, stochastic volatility, time-varying parameters.
- Coherent uncertainty propagation: from parameters to forecasts/decisions/[[policy learning]].
- Interpretability: posterior probabilities for hypotheses (“Pr(θ>0|y)=0.97”) vs p-values in [[Hypothesis testing]].

---

## Priors: elicitation, defaults, and sensitivity

- Weakly-informative priors (recommended defaults):
  - Coefficients (standardized X): Normal(0, 2) or Student-t(ν=3, 0, 2).
  - Scale parameters (σ): half-Normal(0,1) or half-Student-t(ν=3, 0, 1).
  - Group-level SDs (hierarchies): half-Normal/half-t; prefer non-centered parameterization.
- Shrinkage:
  - Ridge/Normal (Gaussian), Laplace (Bayesian LASSO), horseshoe/horseshoe+ (global–local), spike-and-slab (SSVS).
- Prior predictive checks: simulate y~p(y) before seeing data; rule out implausible ranges.
- Sensitivity: vary prior scale and structure; report material changes.

---

## Computation

- [[Markov Chain Monte Carlo (MCMC)|MCMC]]:
  - HMC/NUTS (Stan/PyMC/NumPyro): fast mixing for continuous/differentiable posteriors; monitor divergences/ESS/R̂.
  - Gibbs/MH/slice: conjugate blocks, mixtures, discrete components; Metropolis-within-Gibbs for intractable conditionals.
- Approximate:
  - Variational Inference (VI): fast but approximate; validate via simulation/PPC; good for large-scale screening.
  - SMC/Particle methods: state-space/online inference; robust to multimodality.

> [!check] Diagnostics
> - Convergence: R̂ ≤ 1.01; large bulk/tail ESS; stable traceplots.
> - HMC health: 0 divergences; reasonable E-BFMI; no tree-depth saturation.
> - Fit: posterior predictive checks (PPC); coverage/calibration; residual structure.

---

## Common Bayesian models in econometrics

### Linear/GLM and hierarchical
- Bayesian linear regression with weakly-informative priors or shrinkage (ridge/Laplace/horseshoe).
- GLM (logit/probit/Poisson/NB) with priors on coefficients; probit via latent-variable augmentation.
- Multilevel/hierarchical:
  - Random intercepts/slopes; non-centered parameterization; partial pooling across groups.

### Time series (see [[Time Series (MOC)]])
- State-space / unobserved components: local level/trend/[[seasonality]]; stochastic volatility (SV); fitted via HMC or FFBS+MH.
- BVAR / TVP-VAR:
  - Minnesota priors, SS/BGR priors; TVP with dynamic shrinkage; Bayesian IRFs with uncertainty.
- BSTS / Bayesian synthetic control: counterfactual impact of interventions (akin to [[Synthetic Control]]).

### Bayesian causal models
- Bayesian DiD: hierarchical time and unit effects with shrinkage; posterior event-study paths; better small-sample pooling than classic DiD.
- Bayesian IV:
  - Joint modeling of structural and first-stage with priors; alternative to weak instrument frequentist issues ([[weak instruments]]); still requires [[exclusion restriction]] and [[relevance]].
- Bayesian RDD: flexible trend priors (splines/GP) on both sides of cutoff; posterior of discontinuity.

### Structural (DSGE)
- Priors on technology/preferences; posterior via MH/HMC; model fit by predictive checks and (careful) marginal likelihood.

---

## Model comparison and selection

- Predictive criteria (preferred): LOO (PSIS-LOO), WAIC; select/stack models maximizing held-out predictive accuracy.
- Bayesian model averaging (BMA) or stacking: combine models by predictive weights; reduce model risk.
- Bayes factors: sensitive to priors and undefined with improper priors; if used, compute via bridge sampling/SMC and report prior sensitivity.

---

## Forecasting and decisions

- Posterior predictive forecasts: full predictive intervals; evaluate with MAE/RMSE/MAPE/[[MASE]].
- Decision-making: define loss L(a, y^new) and pick action minimizing posterior predictive loss; e.g., capacity planning, pricing, risk constraints.
- Online experiments ([[AB Testing (MOC)]]): Bayesian posteriors can guide early stopping, but pre-register [[sequential testing]] and guard against multiplicity ([[multiple testing control]]/[[False Discovery Rate (FDR)|FDR]]).

---

## Practical patterns and pitfalls

> [!check] Good practice
> - [ ] Use weakly-informative priors; run prior predictive checks  
> - [ ] Prefer HMC/NUTS when possible; reparameterize (non-centered); standardize predictors  
> - [ ] Multiple chains, adequate warmup, diagnostics (R̂/ESS/divergences/trace)  
> - [ ] PPC and predictive validation (LOO/WAIC); compare to baselines (ARIMA/ETS/OLS)  
> - [ ] Sensitivity to priors and parameterizations; report robustness  
> - [ ] Reproducibility: seeds, versions, code, data schema

> [!warning] Pitfalls
> - Ignoring HMC divergences; relying on a single chain; posteriors stuck in a mode  
> - Overly vague priors in high dimensions → pathologies/improper posteriors  
> - Blind use of Bayes factors with improper priors; no sensitivity  
> - Label switching in mixtures; non-identifiability in structural models  
> - Using post-treatment features in causal models ([[leakage]])  
> - Confusing MCMC MCSE with sample-size power ([[power analysis]]/[[Minimum Detectable Effect (MDE)|MDE]] are design-time, not posterior MC error)

---

## Minimal code

> [!example] R: hierarchical regression (brms/Stan)

```r
library(brms); library(loo); library(bayesplot)

fit <- brm(
  Y ~ X + (1|firm),
  data = df,
  family = gaussian(),
  prior = c(
    prior(normal(0, 2), class = "b"),
    prior(student_t(3, 0, 10), class = "Intercept"),
    prior(exponential(1), class = "sd")
  ),
  chains = 4, iter = 2000, seed = 123
)

summary(fit)
pp_check(fit)                     # posterior predictive checks
loo_res <- loo(fit)               # predictive comparison
```

> [!example] Python: PyMC hierarchical GLM

```python
import pymc as pm, numpy as np, arviz as az

with pm.Model() as model:
    sigma_group = pm.Exponential('sigma_group', 1.0)
    group_raw   = pm.Normal('group_raw', 0, 1, shape=n_groups)
    group_eff   = pm.Deterministic('group_eff', sigma_group * group_raw)

    beta0 = pm.Normal('beta0', 0, 5)
    beta  = pm.Normal('beta', 0, 2, shape=X.shape[1])
    mu    = beta0 + group_eff[group_idx] + pm.math.dot(X, beta)

    sigma = pm.HalfNormal('sigma', 1.0)
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=Y)

    idata = pm.sample(2000, tune=1000, chains=4, target_accept=0.9, random_seed=123)

az.summary(idata, var_names=['beta0','beta','sigma','sigma_group'])
az.plot_ppc(idata)
```

> [!example] R: BVAR with Minnesota prior

```r
library(BVAR)
y <- as.matrix(df[, c("gdp","cpi","ffr")])
fit_bvar <- bvar(y, lags = 4, n_draw = 20000, n_burn = 5000,
                 priors = bv_priors(specifications = bv_mn_priors(lambda = 0.2)))
summary(fit_bvar)    # posterior of coefficients, IRFs via bvar::irf()
```

> [!example] R: Bayesian DiD (hierarchical partial pooling; sketch with brms)

```r
library(brms)
# Y_it ~ unit FE + time FE + treatment effect with partial pooling over event-time k
fit_did <- brm(
  Y ~ 0 + factor(unit) + 0 + factor(time) + z_k,   # z_k: event-time design columns
  data = df,
  prior = c(prior(normal(0, 0.2), class='b')),     # shrinkage on event-time effects
  chains = 4, iter = 2000, seed = 123
)
# Posterior over dynamic treatment path; report credible bands and PPC
```

---

## Comparison to frequentist tools

- CIs vs credible intervals: interpretation differs; both valuable.
- Robust/clustered inference: frequentist [[clustered standard errors]]/[[wild cluster bootstrap]] vs Bayesian hierarchical modeling of cluster variation.
- Multiplicity: still manage practical multiplicity; use predictive performance, hierarchical shrinkage, or transparent [[multiple testing control]] policies.

---

## Reporting essentials

> [!check]
> - [ ] Model and likelihood; hierarchical structure; priors (forms, scales, rationale)  
> - [ ] Computation: sampler (HMC/NUTS/Gibbs/VI), chains, warmup, iterations, seeds; software and versions  
> - [ ] Diagnostics: R̂, bulk/tail ESS, divergences/tree depth (HMC), traceplots, PPCs  
> - [ ] Posterior summaries: means/medians, 50/95% credible intervals; posterior predictive intervals  
> - [ ] Predictive comparison (LOO/WAIC); sensitivity to priors/parameterization  
> - [ ] Reproducibility: code and data artifacts; registry links if [[pre-registration]] used

---

## Related notes

- Foundations and computation: [[Markov Chain Monte Carlo (MCMC)|MCMC]] · [[Hypothesis testing]] (contrast)  
- Time series: [[Time Series (MOC)]] · [[Prophet]] · BVAR (above) · state-space (placeholder) · [[seasonality]]  
- Causal: [[Difference-in-Differences (DiD)]] · [[Regression Discontinuity Design (RDD)]] · [[Instrumental Variables (IV)]] · [[weak instruments]] · [[Synthetic Control]]  
- Experimentation: [[AB Testing (MOC)]] · [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]]/[[multiple testing control]] · [[Overall Evaluation Criterion (OEC)|OEC]] · [[guardrail metric]]  
- Modeling hygiene: [[leakage]] · [[pre-registration]] · [[clustered standard errors]] · [[few-cluster corrections]]

---

## References and resources

- Gelman, Carlin, Stern, Dunson, Vehtari, Rubin — Bayesian Data Analysis (BDA3)  
- McElreath — Statistical Rethinking (applied Bayesian modeling)  
- Stan, PyMC, NumPyro documentation; ArviZ and bayesplot for diagnostics  
- Vehtari, Gelman, Gabry — Practical Bayesian model evaluation (LOO/WAIC, PPC)  
- Karlsson, Villani — Bayesian VARs; Primiceri — TVP-VAR; Kastner — SV priors

---