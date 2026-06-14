---
title: Bayesian Testing
aliases: [Bayesian hypothesis testing, Bayes factors, posterior odds]
tags: [bayesian, testing, inference, decision-theory, bayes-factors, sequential, multiple-testing, ab-testing, model-selection]
updated: 2025-09-23
---

# Bayesian Testing

> [!summary] Quick definition
> Bayesian testing evaluates hypotheses by updating prior beliefs with data and taking decisions to minimize expected loss. Evidence is commonly summarized by posterior odds or Bayes factors, not p-values. Decisions can be based on posterior probabilities, loss/utility, or predefined Bayes‑factor thresholds. See also [[Hypothesis testing]] (frequentist) and [[Bayesian econometrics]].

- Core objects: prior p(θ|H), likelihood p(y|θ,H), marginal likelihood p(y|H), Bayes factor BF, posterior odds, expected loss.
- Related: [[sequential testing]] (Bayesian variants allow continuous monitoring), [[multiple testing control]] and [[False Discovery Rate (FDR)|FDR]] (Bayesian local fdr), [[AB Testing (MOC)]] for product experiments, [[Markov Chain Monte Carlo (MCMC)|MCMC]]/[[Sequential Monte Carlo (SMC)|SMC]] for computation, [[priors]].

---

## Posterior odds and Bayes factors

- Posterior odds:
$$
\frac{p(H_1\mid y)}{p(H_0\mid y)}
= \underbrace{\frac{p(y\mid H_1)}{p(y\mid H_0)}}_{\mathrm{BF}_{10}}
\cdot
\underbrace{\frac{p(H_1)}{p(H_0)}}_{\text{prior odds}}
$$

- Marginal likelihood (evidence) under a composite hypothesis:
$$
p(y\mid H_1)=\int p(y\mid \theta_1,H_1)\,p(\theta_1\mid H_1)\,d\theta_1
$$

- Decision with 0–1 loss generalized by costs C_10 (choose H1 when H0 true) and C_01 (choose H0 when H1 true):
$$
\text{Choose } H_1 \iff \frac{p(H_1\mid y)}{p(H_0\mid y)} > \frac{C_{10}}{C_{01}}
\quad\iff\quad
\mathrm{BF}_{10} > \frac{C_{10}}{C_{01}}\cdot \frac{p(H_0)}{p(H_1)}
$$

> [!note] Savage–Dickey density ratio (nested point null)
> For nested models with H0: θ=θ0 vs H1: θ free, under factorizing priors,
> $$
> \mathrm{BF}_{01} = \frac{p(\theta=\theta_0 \mid H_1)}{p(\theta=\theta_0 \mid y,H_1)}
> $$
> Useful for one‑parameter tests; check conditions (proper priors, separability).

---

## Alternative Bayesian decisions

- Posterior probability threshold: choose H1 if p(H1|y) > τ (e.g., τ=0.95).
- [[Region of Practical Equivalence (ROPE)|ROPE]] (region of practical equivalence): define |θ| < ε as “no practically important effect”; decide by posterior mass inside/outside ROPE.
- [[Highest Density Interval (HDI)|HDI]] (highest density interval) plus ROPE: declare effect if HDI entirely outside ROPE.
- One‑sided/directional beliefs: use posterior sign probability p(θ>0|y) and loss tuned to false‑sign costs (local false sign rate; see [[False Discovery Rate (FDR)|FDR]]).

---

## Simple worked example (Normal mean test)

Test H0: μ=0 vs H1: μ∼N(0,τ²), with data y_i∼N(μ, σ²) (σ² known), i=1..n. Let ȳ be the sample mean.

- Under H0: ȳ ∼ N(0, σ²/n). Under H1: ȳ ∼ N(0, σ²/n + τ²). Bayes factor:
$$
\mathrm{BF}_{10}
= \frac{\phi\!\left(ȳ; 0,\; \sigma^2/n + \tau^2\right)}
{\phi\!\left(ȳ; 0,\; \sigma^2/n\right)}
= \sqrt{\frac{\sigma^2/n}{\sigma^2/n + \tau^2}}
\exp\!\left\{\frac{ȳ^2}{2}\left(\frac{1}{\sigma^2/n + \tau^2}-\frac{1}{\sigma^2/n}\right)\right\}
$$
Choose τ to reflect plausible effect sizes; very large τ induces “Occam’s razor” and can favor H0 (Lindley’s paradox).

---

## Common tests and defaults

- t‑tests and regression coefficients: default Bayes factors via Jeffreys–Zellner–Siow (JZS) priors or g‑priors; compute by closed forms or numerical integration.
- Two proportions (A/B): model conversion with Beta‑Binomial priors; compare posterior of Δ = p_B − p_A, or compute BF between H0: Δ=0 and H1 with a prior on Δ.
- Model comparison and variable selection: posterior model probabilities with spike‑and‑slab priors; [[BIC]] provides a large‑sample approximation to log BF.
- Equivalence tests: specify ROPE and evaluate posterior mass within equivalence region.

---

## Sequential use and design

- Optional stopping: With proper, pre‑specified priors, Bayes factors are invariant to stopping rules; sequential monitoring is coherent. In practice, pre‑register priors/thresholds and record looks; check robustness to prior choices.
- Thresholds: Common evidence categories (e.g., BF>3 “moderate”, >10 “strong”) are heuristics; calibrate to your decision costs.
- Planning: Simulate prior predictive data to assess expected evidence (distribution of BF) and choose sample sizes/rules targeting desired operating characteristics. For product [[AB Testing (MOC)]], set guardrails and stopping on BF or posterior loss.

---

## Multiplicity and discovery

- Multiple comparisons: Use priors that share information across tests (hierarchical shrinkage), or compute posterior inclusion probabilities and control Bayesian FDR (e.g., local fdr = p(H0 true | data) per test).
- Report posterior probabilities or BFs, not only indicators; avoid naive threshold shopping. See [[multiple testing control]] and [[False Discovery Rate (FDR)|FDR]].

---

## Computation

- Exact/closed form: conjugate models (Beta‑Binomial, Normal‑Normal, Normal‑Inverse‑Gamma).
- Approximations: Laplace approximation, BIC for log BF, Integrated nested Laplace (INLA) for latent Gaussian models.
- Monte Carlo:
  - [[Markov Chain Monte Carlo (MCMC)|MCMC]] for posteriors; Bayes factors via bridge sampling, thermodynamic integration, Chib’s method.
  - [[Sequential Monte Carlo (SMC)|SMC]]/annealed importance sampling for marginal likelihoods and sequential designs.
- Posterior predictive checks: simulate ỹ∼p(ỹ|y) for model adequacy (complementary to testing).

---

## Diagnostics and good practice

> [!check]
> - [ ] Prior sensitivity: vary prior scales (e.g., τ) and report BF/posterior robustness  
> - [ ] Model adequacy: posterior predictive checks; compare to held‑out predictive performance (WAIC/LOO) when testing models for prediction  
> - [ ] Computation: verify marginal likelihood estimates with multiple methods/seeds; monitor MCMC convergence  
> - [ ] Calibration: if stakeholders expect Type‑I/II style guarantees, simulate operating characteristics of your Bayesian decision rule

---

## Pitfalls

> [!warning]
> - Lindley’s paradox: diffuse priors can favor H0 even with small p‑values; use informed or weakly‑informative priors  
> - Improper priors invalidate Bayes factors (marginal likelihood undefined)  
> - Post‑hoc priors or data‑dependent prior tuning bias evidence upward  
> - Over‑interpreting Jeffreys’ BF scale; align thresholds with decision costs  
> - Equating credible intervals with decisions without considering loss/ROPE

---

## Reporting essentials

- Hypotheses and parameterization; priors (including hyperparameters) and rationale
- Decision rule: posterior odds threshold, BF threshold, or loss specification
- Computation: method for marginal likelihood/BF (closed form, bridge, SMC, etc.), diagnostics
- Results: BF, prior and posterior odds, posterior probabilities, and sensitivity to priors
- Robustness: alternative priors, alternative models, posterior predictive checks
- Reproducibility: code, seeds, software versions

---

## Related notes

- Foundations: [[Bayesian econometrics]] · [[priors]]  
- Computation: [[Markov Chain Monte Carlo (MCMC)|MCMC]] · [[Sequential Monte Carlo (SMC)|SMC]]  
- Comparisons and design: [[Hypothesis testing]] · [[sequential testing]] · [[multiple testing control]] · [[AB Testing (MOC)]]  
- Model selection: [[BIC]] · [[AIC]] · [[Maximum Likelihood Estimation (MLE)|MLE]]

---

## References

- Jeffreys (1939/1961). Theory of Probability (Bayesian testing and scales)  
- Kass & Raftery (1995). Bayes factors (classic review)  
- Berger (1985). Statistical Decision Theory and Bayesian Analysis  
- Rouder et al. (2009). Bayesian t tests for accepting and rejecting the null (JZS t‑test)  
- Robert (2007). The Bayesian Choice (marginal likelihoods and testing)  
- Gelman et al. (2013/2020). Bayesian Data Analysis (ROPE/HDI, posterior predictive checks)  
- Gronau et al. (2017). bridge sampling for marginal likelihoods

---
