---
title: Sequential and Adaptive Experiments (MOC)
aliases:
  - Sequential experiments
  - Adaptive experiments
  - Online experimentation (sequential)
  - Group sequential designs
  - Bandits and adaptive randomization
tags:
  - MOC
  - experimental-design
  - sequential
  - bandits
  - online-experiments
  - off-policy-evaluation
  - monitoring
updated: 2025-09-26
---

# Sequential and Adaptive Experiments (MOC)

> [!summary] Start here
> How to design, monitor, and analyze experiments when you peek at data, stop early, or adapt allocation. Covers frequentist [[sequential testing]], Bayesian monitoring, group-sequential designs, multi-armed bandits, [[off-policy evaluation|off-policy evaluation]], and platform practices (logging, guardrails, SRM).

Related starting points:
- Foundations: [[Experimental Design (MOC)]], [[Causal Inference (MOC)]], [[Econometrics (MOC)]]
- ML + policy: [[Machine Learning for Causal Inference (MOC)]], [[policy learning|policy learning]], [[policy tree|policy tree]]
- Inference: [[Standard Errors and Inference (MOC)]], [[multiple testing control|multiple testing control]], [[False Discovery Rate (FDR)|FDR]]

## Why sequential/adaptive designs

- Practical need to make decisions quickly; stop for superiority/futility
- Ethical/resource constraints (avoid long exposure to inferior variants)
- Continuous delivery environments with ongoing A/B tests
- Optimize exploration vs exploitation (bandits) and evaluate learned policies (OPE)

Key risks to manage:
- Inflated type I error from peeking
- Bias from outcome-dependent stopping
- Allocation bias in adaptive randomization
- Interference/time effects in operational settings (see [[Spillovers and Interference (MOC)]], [[switchback experiment|switchback experiment]])

## Design space at a glance

- Fixed-sample A/B: classical baseline (analyze once)
- Group sequential: pre-planned looks, alpha-spending boundaries
- Always-valid procedures: anytime p-values, e-values, confidence sequences
- Bayesian monitoring: [[Bayesian Testing|Bayesian testing]] with proper priors and stopping rules
- Adaptive randomization: [[bandits|bandits]]/[[Multi-Armed Bandit (MAB)|MAB]], Thompson sampling, UCB
- Contextual/adaptive policies: [[policy learning|policy learning]], [[off-policy evaluation|OPE]]
- Operational alternation: [[switchback experiment|switchback]] and geo-experiments for platform-wide changes

## Platform and integrity basics

- Randomization checks: [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]]
- Correct unit of analysis (user, session, household), [[bucketing]] stability, [[stratification]]
- Exposure/accounting: [[exposure logging]], [[triggered analysis]], delayed conversions, repeat exposures
- Guardrails and objectives: [[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]
- Data hygiene: prevent [[leakage]] across variants; define analysis windows a priori
- Pre-commitment: [[pre-registration]] of stopping/monitoring plans

## Sequential testing (frequentist)

- Group sequential designs
  - Information times and boundaries (e.g., Pocock, O’Brien–Fleming)
  - Alpha spending functions to control type I error with multiple looks
- Always-valid inference
  - Anytime p-values via nonnegative supermartingales (e-values) and confidence sequences
  - Mixture Sequential GLR (mSPRT) for continuous monitoring

Related notes: [[sequential testing|sequential testing]], [[power analysis|power analysis]], [[Minimum Detectable Effect (MDE)|MDE]]

### Minimal formulas (copy-ready)

- Wald SPRT log-likelihood ratio for hypotheses H0 vs H1:
$$
\log \Lambda_t = \sum_{i=1}^t \log \frac{f_{1}(X_i)}{f_{0}(X_i)} \quad \text{stop if } \log\Lambda_t \ge \log A \text{ or } \log\Lambda_t \le \log B
$$

- Alpha-spending (cumulative error α(t) at information time t ∈ [0,1]):
$$
\alpha(t) = \text{spend}(t), \quad \text{reject at look k if } Z_k \text{ exceeds boundary } c_k(\alpha(t_k))
$$

- Anytime-valid e-value E_t (nonnegative supermartingale):
$$
\mathbb{P}_{H_0}\!\left(\sup_{t} E_t \ge 1/\alpha\right) \le \alpha, \quad \text{reject when } E_t \ge 1/\alpha
$$

- Mean confidence sequence (conceptual):
$$
\Pr\left(\forall t: \mu \in \text{CS}_t\right) \ge 1-\alpha \quad \text{(width shrinks with t, valid under continuous monitoring)}
$$

## Bayesian sequential monitoring

- Proper priors + likelihood → posterior odds; Bayes factors valid under [[Optional stopping]] (with correct model and proper priors)
- Decision-theoretic stopping: stop when expected value of information < cost, or posterior P(effect > δ) passes threshold
- Practical defaults: JZS priors for t-tests; Beta–Binomial for binary

Related notes: [[Bayesian Testing|Bayesian testing]], [[Region of Practical Equivalence (ROPE)|ROPE]], [[priors|priors]], [[Optional stopping]]

## Adaptive allocation (bandits)

- Goals and settings
  - Minimize regret; identify best arm; maximize cumulative reward
- Algorithms
  - Epsilon-greedy, UCB family, Thompson sampling
  - Contextual bandits for personalization (features X)
- Considerations
  - Nonstationarity; delayed outcomes; batched updates
  - Regret vs inference trade-offs; post-experiment unbiased estimation

Related notes: [[bandits|bandits]], [[Multi-Armed Bandit (MAB)|MAB]], [[off-policy evaluation|off-policy evaluation]], [[policy learning|policy learning]]

## Off-policy evaluation (OPE) and policy learning

- Estimating value of new policies from logged data
  - IPS/SNIPS, Doubly Robust (DR), model-based estimators
- Logging requirements
  - Known propensities; exploration logging; stable policies
- Policy improvement loops
  - Learn → evaluate via OPE → deploy → re-learn; guardrails/[[Overall Evaluation Criterion (OEC)|OEC]] to prevent regressions

Related notes: [[off-policy evaluation|off-policy evaluation]], [[uplift]], [[policy tree|policy tree]]

## Time and interference-aware designs

- [[switchback experiment|Switchback]] across time/regions to mitigate spillovers and temporal autocorrelation
- Geo-cluster randomization with buffers (see [[geo experiment|geo experiment]])
- Saturation/partial-population designs when peer effects exist

Related notes: [[Spillovers and Interference (MOC)]]

## Power, MDE, and planning under sequential/adaptive use

- Sequential power analysis: account for multiple looks/boundaries
- MDE inflation under group sequential vs fixed-sample
- Bandits: define regret budgets and stopping criteria; ensure minimal exploration mass
- Practical advice
  - Fix maximum sample horizon
  - Pre-specify stopping for efficacy/futility
  - Simulate operating characteristics (type I error, power, expected sample size)

Related notes: [[power analysis|power analysis]], [[Minimum Detectable Effect (MDE)|MDE]]

## Multiple metrics and multiplicity

- Many outcomes/segments → control family-wise error or [[False Discovery Rate (FDR)|FDR]]
- Sequential multiplicity:
  - Alpha spending across outcomes/time
  - Alpha investing procedures for streams of tests
- Pre-specify primary/secondary metrics; treat guardrails descriptively unless adjusted

Related notes: [[multiple testing control|multiple testing control]]

## Diagnostics and governance

> [!check] Operational checklist
> - [ ] Randomization integrity: [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]]
> - [ ] Correct exposure unit: [[exposure logging]], [[triggered analysis]]
> - [ ] Pre-registered monitoring/stopping plan: [[pre-registration]]
> - [ ] Guardrails and OEC clearly defined: [[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]
> - [ ] Sequential procedure chosen (group sequential/always-valid/Bayesian) and justified
> - [ ] If adaptive: logging propensities for [[off-policy evaluation|OPE]]
> - [ ] Handling of delays, repeats, contamination, seasonality
> - [ ] Post-hoc bias audit and reproducibility plan

## Common pitfalls

> [!warning] Avoid these
> - Peeking with fixed-sample p-values (inflates type I error)
> - Changing metrics/stopping rules midstream
> - Ignoring delayed outcomes and triggered eligibility
> - Not logging propensities in adaptive experiments (OPE becomes impossible)
> - Confounding time/seasonality with treatment; prefer [[switchback experiment|switchback]] or block randomization
> - Ignoring interference between units or regions

## Minimal formulas (copy-ready)

- Two-arm z-stat under normal approximation (sequentially monitored):
$$
Z_t = \frac{\bar{Y}_{1,t} - \bar{Y}_{0,t}}{\sqrt{s_{1,t}^2/n_{1,t} + s_{0,t}^2/n_{0,t}}}
$$
Use only with group-seq/alpha-spending boundaries pre-specified.

- IPS/SNIPS/DR for OPE (see linked page):
  - IPS: $\hat{V} = \frac{1}{n}\sum_i \frac{\pi(a_i\mid x_i)}{\mu(a_i\mid x_i)} r_i$
  - SNIPS: self-normalized IPS
  - DR: model-assisted with bias reduction

- Thompson sampling (conceptual):
  - Sample parameter from posterior; play arm that maximizes sampled value; update with outcome

## When to use what

- Need valid continuous monitoring without pre-planned looks → anytime-valid (e-values/confidence sequences) or Bayesian with proper priors
- Limited scheduled looks and regulatory reporting → group sequential with alpha-spending
- Goal is optimization of cumulative reward or fast winner ID → bandits/adaptive randomization
- Strong temporal/spatial correlation → [[switchback experiment|switchback]] or geo designs

## Cross-links

- Monitoring and testing: [[sequential testing|sequential testing]], [[Bayesian Testing|Bayesian testing]]
- Optimization and deployment: [[bandits|bandits]], [[Multi-Armed Bandit (MAB)|MAB]], [[policy learning|policy learning]], [[off-policy evaluation|off-policy evaluation]]
- Platform: [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]], [[exposure logging]], [[triggered analysis]], [[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]
- Designs for time/space: [[switchback experiment|switchback experiment]], [[geo experiment|geo experiment]], [[Spillovers and Interference (MOC)]]
- Planning and inference: [[power analysis|power analysis]], [[Minimum Detectable Effect (MDE)|MDE]], [[Standard Errors and Inference (MOC)]], [[multiple testing control|multiple testing control]]

---

Related notes to create:
- [[alpha spending]]
- [[O’Brien–Fleming boundary]]
- [[Pocock boundary]]
- [[anytime p-values]]
- [[confidence sequence]]
- [[mixture SPRT]]
- [[sequential FDR]]
- [[delayed outcomes]]
- propensity logging
- [[batched bandits]]
- [[nonstationary bandits]]