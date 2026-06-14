---
title: Structural models
aliases: [structural econometrics, structural modeling, SEM (econometrics), dynamic structural models, equilibrium models]
tags: [econometrics, structural, identification, gmm, mle, smm, mpec, counterfactuals, equilibrium, dynamic, bayesian]
updated: 2025-09-17
---

# Structural models

> [!summary] Quick definition
> Structural econometric models specify economic mechanisms (preferences, technologies, information sets, equilibrium/decision rules) to interpret parameters as primitives and to conduct counterfactuals. Identification relies on theory‑based restrictions (e.g., equilibrium conditions, exclusion/functional form, timing), and estimation uses [[Maximum Likelihood Estimation (MLE)|MLE]]/[[Generalized Method of Moments (GMM)|GMM]]/[[Simulated method of moments]]/[[indirect inference]] or Bayesian methods ([[Bayesian econometrics]] with [[Markov Chain Monte Carlo (MCMC)|MCMC]]). Structural models enable policy simulation and welfare analysis beyond reduced‑form effects.

- Typical domains: demand/supply (e.g., BLP demand), dynamic discrete choice (Rust, Hotz–Miller CCP), auctions, entry/exit and market structure, labor/search, household lifecycle, macro [[DSGE]], state‑space and expectations, industrial organization.

---

## When to use structural models (vs. reduced form)

> [!tip] Use when
> - You need counterfactuals (new taxes, prices, market design, policy rules) beyond observed “as‑is” shocks.  
> - You want primitives (elasticities, risk aversion, switching costs, information frictions), or to aggregate to welfare.  
> - Theory (optimization/equilibrium) meaningfully constrains behavior.

> [!warning] Consider reduced‑form (e.g., [[Difference-in-Differences (DiD)]], [[Regression Discontinuity Design (RDD)]], [[Instrumental Variables (IV)]]) when identification can be achieved without full structural assumptions and counterfactual mapping is not primary.

---

## Basic anatomy

- Economic environment: agents, state variables, information sets, timing.
- Preferences/technology: utility, costs, constraints.
- Behavior/equilibrium mapping: policy rules (best response/optimality), market‑clearing, rational expectations.
- Shocks and distributions: taste/productivity/measurement shocks; serial correlation; [[Kalman filter|state-space/Kalman filter]] if latent states.
- Data map: observables (choices, prices, outcomes) and unobservables; selection rules; sampling.

---

## Identification

- Sources: exclusion restrictions, functional forms, variation in instruments/markets, timing, shape constraints, equilibrium/complementarity conditions.
- Static vs dynamic: dynamic models often need additional variation (panel, timing instruments, exit/entry) and solve value functions.
- Partial identification: parameters set‑identified; report bounds (cf. [[Manski bounds]], [[Lee bounds]]) or sensitivity.
- Instruments/IV: many structural models need valid IV ([[relevance]], [[exclusion restriction]])—watch [[weak instruments]].
- Normalizations: scales, utility reference points, location/scale of errors; carefully document.

> [!check] Diagnostics
> - Overidentifying restrictions (J‑test in [[Generalized Method of Moments (GMM)|GMM]]), weak IV checks, falsification tests, auxiliary fit (micro‑moments).

---

## Estimation approaches

- Likelihood‑based
  - [[Maximum Likelihood Estimation (MLE)|MLE]] / simulated likelihood (SML) for discrete choice (random coefficients; importance/halton draws), [[EM algorithm|EM]] for latent classes.
  - State‑space likelihood via Kalman/particle filters (SV/TVP).
- Moment‑based
  - [[Generalized Method of Moments (GMM)|GMM]]: match sample moments to model moments; optimal weighting; J‑test.
  - [[Simulated method of moments]] (SMM/MSM): match micro‑moments using simulation from the model; pick moments that identify key mechanisms.
  - [[indirect inference]]: match auxiliary model coefficients (e.g., ARMA or reduced‑form regressions) between real and simulated data.
- Optimization frameworks
  - NFXP (Nested Fixed Point): inner loop solves dynamic program; outer loop searches parameters.
  - [[MPEC]] (Mathematical Programming with Equilibrium Constraints): estimate parameters subject to equilibrium conditions as constraints (often improves stability).
- Bayesian
  - [[Bayesian econometrics]] with priors ([[priors]]), [[Markov Chain Monte Carlo (MCMC)|MCMC]] (HMC/NUTS/Gibbs) or SMC; natural for hierarchical structures, small samples, complex likelihoods; posterior predictive for model checking.

> [!tip] High‑dimensional components: apply [[regularization]] or shrinkage priors (e.g., horseshoe) to stabilize.

---

## Solution and numerical methods

- Static discrete choice: logit/probit, mixed logit; random coefficients with simulation; BLP contraction for demand.
- Dynamic discrete choice (Rust)
  - Value function iteration / policy iteration; contraction mapping; NFXP or [[Hotz–Miller CCP]] (invert CCPs); [[Hotz–Miller CCP]] reduces dimensionality using conditional choice probabilities.
- Continuous state/action:
  - Approximation (e.g., Chebyshev collocation, spline bases), endogenous grid (EGM), gradient‑based solution (adjoint).
- Equilibrium models (IO/macro)
  - Fixed‑point algorithms (tatonnement), Newton/Krylov solvers, linearization (for [[DSGE]]), occasionally [[MPEC]] for joint estimation and equilibrium conditions.
- State‑space:
  - Kalman filter/smoother; particle filtering for non‑Gaussian/nonlinear; SV/TVP estimation.

---

## Examples (by area)

- Demand estimation (BLP; differentiated products)
  - Random coefficients logit; IV for price endogeneity; contraction mapping; [[Generalized Method of Moments (GMM)|GMM]]/SMM; counterfactual prices, markups, welfare.
- Dynamic discrete choice (Rust bus engine; Hotz–Miller)
  - Replacement/maintenance; estimate cost parameters; counterfactual policies (subsidies/penalties).
- Auctions
  - First‑price sealed bid (Ackerberg–Haan–Tamer style); recover value distributions; reserve‑price optimization.
- Entry/exit and market structure
  - Two‑stage games; profit inequalities; CCP methods; bounds (Pakes et al.) for partial identification.
- Labor/search
  - Job‑finding/separation; wage posting/bargaining; offer distributions; policies (UI/benefits).
- Macro [[DSGE]]
  - Solve linearized or nonlinear models; estimate via [[Markov Chain Monte Carlo (MCMC)|MCMC]] (MH/NUTS) or SMC; shock decompositions; policy rules.

---

## Inference and uncertainty

- Frequentist: sandwich SEs for [[Generalized Method of Moments (GMM)|GMM]]; bootstrap (pairs/block/parametric) to capture solution/simulation variability; profile likelihood for [[Maximum Likelihood Estimation (MLE)|MLE]]; consider [[wild cluster bootstrap]] in clustered designs.
- Bayesian: posterior credible intervals; report priors and run sensitivity; check convergence (R̂, ESS), divergences (HMC) (see [[Markov Chain Monte Carlo (MCMC)|MCMC]]).
- Weak identification: rely on robust tests/intervals; report set estimates if needed.

---

## Validation and diagnostics

> [!check]
> - [ ] In‑sample fit and micro‑moment matching; out‑of‑sample prediction (where meaningful)  
> - [ ] Overidentifying restrictions (J‑test), IV strength (KP/MOP F for first stage)  
> - [ ] Posterior predictive checks (Bayesian); sensitivity to [[priors]]  
> - [ ] Model‑implied elasticities vs reduced‑form estimates (consistency)  
> - [ ] Falsification tests (e.g., placebo implications, moments that should be zero)  
> - [ ] Computational robustness: alternative solvers, starting values, seeds

---

## Counterfactuals and welfare

- Procedure
  1) Fix estimated parameters (with uncertainty); solve model under new policy/shocks  
  2) Simulate equilibrium/behavior; compute outcomes and welfare measures  
  3) Propagate uncertainty via bootstrap or posterior draws; report intervals and sensitivity
- Examples
  - Price/tax changes; merger simulations; reserve price rules; UI benefit rules; carbon policy; monetary rules in [[DSGE]].

> [!warning] Counterfactual validity hinges on correct behavioral/expectation assumptions; document where the model extrapolates beyond observed support.

---

## Practical guidance

> [!check] Workflow
> - [ ] Write economic environment clearly (states, timing, equilibrium)  
> - [ ] Map to observables; specify selection/measurement processes  
> - [ ] Identify: list instruments/exclusions, moments, normalizations; discuss support  
> - [ ] Choose estimator (MLE/GMM/SMM/II/Bayesian) and solver (NFXP/CCP/MPEC); set simulation design (draws, seeds)  
> - [ ] Validate with auxiliary/reduced‑form evidence (DiD/RD/IV); cross‑check parameters/elasticities  
> - [ ] Run counterfactuals with uncertainty and sensitivity (alternative moments/priors/functional forms)

> [!warning] Pitfalls
> - Weak instruments or poor support → fragile parameters; see [[weak instruments]]  
> - Over‑parameterization without shrinkage; no regularization ([[regularization]])  
> - Equilibrium selection issues; multiple equilibria ignored  
> - Solvers stuck in local optima; unreported sensitivity to starting values  
> - Mis‑specified error processes; ignoring serial correlation/[[Kalman filter|state-space/Kalman filter]] needs  
> - Using post‑treatment information in moments (model‑based [[leakage]])

---

## Minimal code sketches

> [!example] Python: SMM skeleton

```python
import numpy as np

def simulate_model(theta, draws, T):
    # simulate outcomes/moments under parameter theta
    # return simulated moments m_sim(theta)
    pass

def objective(theta, m_data, W, draws, T):
    m_sim = simulate_model(theta, draws, T)
    diff = m_sim - m_data
    return diff.T @ W @ diff

# Optimize objective; update W to optimal (two-step GMM/SMM)
```

> [!example] R: Indirect inference (auxiliary AR(1))

```r
auxiliary <- function(y){ coef(lm(y[-1] ~ y[-length(y)]))["y[-length(y)]"] }
m_data <- auxiliary(y_obs)
simulate_model <- function(theta){ # ... return simulated y
}
obj <- function(theta){
  ysim <- simulate_model(theta)
  m_sim <- auxiliary(ysim)
  (m_sim - m_data)^2
}
# Optimize obj(theta)
```

> [!example] R: Bayesian structural (Stan/brms) sketch

```r
# Encode structural likelihood in Stan; use HMC/NUTS
# Posterior draws -> re-solve counterfactual policy for each draw
```

---

## Reporting essentials

- Economic structure: agents, timing, equilibrium/expectations, information sets
- Identification: instruments, exclusions, normalizations, moments used; support and potential violations
- Estimation: method (MLE/GMM/SMM/II/Bayesian), objective/likelihood, weighting, simulation design (draws, seeds), solver (NFXP/CCP/MPEC)
- Inference: SE/CI method (robust/bootstrap/posterior), [[weak instruments]] diagnostics if IV
- Validation: auxiliary fits, overid tests, PPC, sensitivity to moments/priors/functional forms
- Counterfactuals: policy scenarios, solution methods, uncertainty bands, welfare definitions
- Reproducibility: code, seeds, versions, hardware/runtime

---

## Related notes

- Estimation and inference: [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Generalized Method of Moments (GMM)|GMM]] · [[Simulated method of moments]] · [[indirect inference]] · [[MPEC]] · [[EM algorithm|EM]] · [[regularization]]  
- Identification and IV: [[Instrumental Variables (IV)]] · [[weak instruments]] · [[exclusion restriction]] · [[relevance]]  
- Dynamic/IO/macro: dynamic discrete choice (placeholder) · [[Hotz–Miller CCP]] · NFXP (placeholder) · Auctions (placeholder) · BLP (placeholder) · [[DSGE]] · [[Kalman filter|state-space/Kalman filter]]  
- Validation and robustness: [[Hypothesis testing]] · [[randomization inference]] · [[multiple testing control]] (for many moments) · [[leakage]]  
- Time series: [[Time Series (MOC)]]

---

## References (selected)

- Rust (1987): Dynamic discrete choice/NFXP; Hotz & Miller (1993): CCP.  
- Berry, Levinsohn, Pakes (1995): BLP demand; Nevo (2000): implementation.  
- Pakes, Ostrovsky, Berry (2007): Indirect inference/BLP refinements.  
- Gourieroux, Monfort, Renault (1993): Indirect inference.  
- Keane & Wolpin; Aguirregabiria & Mira: dynamic discrete choice solutions.  
- Ackerberg, Benkard, Berry, Pakes (2015): demand IO survey.  
- Deaton & Muellbauer; Pakes & Pollard; Train: discrete choice/demand.  
- Fernández-Villaverde et al.: Bayesian [[DSGE]].  

---
