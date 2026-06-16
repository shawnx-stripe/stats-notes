---
title: Robust Methods (MOC)
aliases:
  - Robust causal methods
  - Robust estimation and inference (MOC)
  - Misspecification-robust methods
tags:
  - MOC
  - causal-inference
  - econometrics
  - robustness
  - doubly-robust
  - diagnostics
updated: 2025-09-26
---

# Robust Methods (MOC)

> [!summary] Start here
> Robust methods protect your conclusions against model misspecification, limited overlap, dependence structures, small samples, and weak identification. This MOC connects design-robust identification, doubly-robust estimation, and inference-robust standard errors and tests.

Related starting points:
- Identification: [[Identification Strategies (MOC)]]
- Estimation and ML: [[Machine Learning for Causal Inference (MOC)]]
- Inference: [[Standard Errors and Inference (MOC)]]
- Designs: [[Panel Data Methods (MOC)]], [[Spillovers and Interference (MOC)]], [[Regression Discontinuity Design (RDD)]]

## What “robust” means here

- Robust to outcome or propensity model misspecification (double robustness, orthogonalization).
- Robust to limited overlap (diagnostics, trimming, balancing).
- Robust to dependence (clustering, spatial correlation, serial correlation).
- Robust to small samples/few clusters (finite-sample corrections, wild cluster bootstrap, design-based tests).
- Robust to weak identification (weak IV tests, partial identification/bounds).
- Robust to boundary/bias at discontinuities (bias-corrected RD).
- Robust to unobserved confounding via sensitivity/bounds (when assumptions are in doubt).

## Core robust estimators

- Weighting and balancing
  - [[Inverse Probability Weighting (IPW)|IPW]]/stabilized weights; [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] for attrition/censoring
  - Overlap-focused weights; trimming on [[Overlap]]
  - Moment-balancing methods: [[entropy balancing]]; matching + reweighting [[matching]]
- Doubly-robust estimation
  - [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and influence-function based estimators (consistent if either model is correct)
  - [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] (targeted plug-in; valid CIs with data-adaptive learners)
  - [[double machine learning]] (orthogonal scores + [[cross-fitting]])
- Design-robust by construction
  - Modern DiD under heterogeneity: [[drdid]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]
  - RD with bias-corrected robust inference: [[Calonico-Cattaneo-Titiunik]] (CCT), multi-bandwidth checks; [[Imbens-Kalyanaraman]] for bandwidth selection
  - IV under nonparametric/ML first stages: estimation framed via orthogonal scores; see [[Local IV]], [[marginal treatment effect (MTE)]]

## Robust inference (SEs and tests)

- Dependence-robust standard errors
  - [[clustered standard errors]]; report number of clusters; beware the [[Moulton problem]]
  - Few clusters: [[few-cluster corrections]]; [[wild cluster bootstrap]]
  - Spatial dependence: [[Conley standard errors]]
- Design-based inference
  - [[randomization inference]] (exact or approximate under the assignment mechanism)
  - [[bootstrap]] variants aligned to structure (cluster/block/wild)
- Multiple testing and exploration
  - [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]] for many outcomes or subgroups

## Limited overlap and weight diagnostics

- Diagnose and remediate
  - Plot propensity score distributions; assess [[Overlap]]/common support
  - Trimming rules (e.g., e(x) ∈ [α, 1−α]); report trimmed share
  - Weight dispersion metrics (max weight, coefficient of variation) and effective sample size:
$$
\text{ESS} = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$
- Prefer overlap-emphasizing estimands (e.g., overlap weights) when tails dominate
- Use balancing diagnostics post-weighting (standardized differences, variance ratios)

Related notes: [[propensity score]], [[entropy balancing]], [[matching]], [[Overlap]]

## Weak identification and partial identification

- Weak instruments (IV)
  - Diagnose [[weak instruments]] (first-stage F, strength), ensure [[relevance]]
  - Prefer robust tests such as [[Anderson–Rubin]] and [[CLR test]]
  - Interpret as [[Local Average Treatment Effect (LATE)|LATE]]/local effects; use [[fuzzy RDD]] where applicable
- Partial identification when assumptions are weak
  - Worst-case bounds: [[Manski bounds]]
  - Monotone selection trimming: [[Lee bounds]]
  - Report identification regions with transparent assumptions

Related: [[Instrumental Variables (IV)]], [[Local IV]], [[marginal treatment effect (MTE)]]

## Robust RD and DiD at a glance

- RD
  - [[Calonico-Cattaneo-Titiunik]] robust bias-corrected CIs
  - Multiple bandwidths; donut RD; continuity of covariates; [[density test]]/[[McCrary test]]
- DiD
  - Event-study for [[pre-trends]]; cohort/event-time heterogeneity
  - Modern estimators: [[drdid]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]
  - Account for [[composition]] changes and [[Anticipatory effects]]

Related: [[Difference-in-Differences (DiD)]], [[event study]], [[two-way fixed effects]]

## Sensitivity analysis (unobservables)

- Design-specific bounds
  - [[Lee bounds]] (monotone selection into sample)
  - [[Manski bounds]] (assumption-light outcome bounds)
- Randomization-based sensitivity (experiments)
  - [[randomization inference]] with interference/attrition adjustments
- Observational confounding sensitivity
  - Placebo outcomes/negative controls; falsification tests
  - [[E-value]] and [[Oster’s delta]]
  - Pattern-mixture/selection models (MNAR; see [[Missing Data and Selection (MOC)]])

Related: [[selection bias]], [[placebo test]], [[Missing Data and Selection (MOC)]]

## Outliers, heavy tails, and distribution-robust targets

- Median/quantile effects (less sensitive than means)
- Robust regression and losses (Huber/M-estimation)
- Winsorization/trimming protocols (pre-registered to avoid p-hacking)

Related notes: [[quantile regression]], [[Huber regression]], [[M-estimation]]; future note: winsorization

## Practical workflow for robustness

> [!check] Robust analysis checklist
> - [ ] Define estimand and primary identification strategy
> - [ ] Pre-specify overlap rules (trimming/weights) and exposure of interference risks
> - [ ] Choose doubly-/orthogonally-robust estimator (AIPW/TMLE/DML) with [[cross-fitting]]
> - [ ] Run weight and balance diagnostics; report ESS and max weight
> - [ ] Align SEs to structure (cluster/spatial/few cluster); report clusters
> - [ ] For RD/DiD: use bias-corrected/modern estimators; show pre-trends and covariate continuity
> - [ ] Sensitivity: bounds (Lee/Manski), placebos, alternative specs/bandwidths
> - [ ] Document all robustness decisions and their impact on estimates

## Minimal formulas (copy-ready)

- Doubly robust ATE (see [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]):
$$
\hat{\tau}_{\text{AIPW}} = \frac{1}{n}\sum_i \left[\big(\hat{m}_1(X_i)-\hat{m}_0(X_i)\big) + \frac{D_i\,(Y_i-\hat{m}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-D_i)\,(Y_i-\hat{m}_0(X_i))}{1-\hat{e}(X_i)}\right]
$$

- TMLE clever covariate (see [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]):
$$
H(X_i,D_i) = \frac{D_i}{\hat{e}(X_i)} - \frac{1-D_i}{1-\hat{e}(X_i)}
$$

- Stabilized IPW (variance control):
$$
w_i^{\text{stab}} = \frac{P(D=d)}{\hat{P}(D=d\mid X_i)} \quad \text{for unit with } D=d
$$

- Overlap weights (emphasize common support):
$$
w(x) \propto \hat{e}(x)\,\big(1-\hat{e}(x)\big)
$$

- Effective sample size under weights:
$$
\text{ESS} = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$

## Common pitfalls

> [!warning] Avoid these
> - Unreported trimming/weight capping decisions
> - Using TWFE in staggered settings without modern DiD corrections
> - Clustering at the wrong level; ignoring spatial correlation
> - Treating DR as a license to ignore overlap/positivity
> - Overfitting nuisances without [[cross-fitting]]; no out-of-fold diagnostics
> - Post-hoc bandwidth selection in RD; outcome-dependent re-centering
> - Ignoring weak IV warnings; overinterpreting LATE as ATE

## Cross-links

- Estimation: [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]], [[Inverse Probability Weighting (IPW)|IPW]], [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]], [[matching]], [[entropy balancing]]
- Designs: [[Regression Discontinuity Design (RDD)]], [[Difference-in-Differences (DiD)]], [[fuzzy RDD]], [[Local IV]], [[marginal treatment effect (MTE)]]
- Inference: [[clustered standard errors]], [[few-cluster corrections]], [[wild cluster bootstrap]], [[Conley standard errors]], [[randomization inference]], [[bootstrap]]
- Diagnostics: [[Overlap]], [[placebo test]], [[pre-trends]], [[density test]], [[McCrary test]]
- Complications: [[Missing Data and Selection (MOC)]], [[Spillovers and Interference (MOC)]]

---

## Related notes
- [[stabilized weights]]
- [[weight trimming and caps]]
- [[effective sample size]]
- [[Anderson–Rubin|Anderson–Rubin test]]
- [[CLR test]]
- [[quantile regression]]
- [[Huber regression]]
- [[M-estimation]]
- winsorization
- [[E-value]]
- [[Oster’s delta]]
- [[robust RD bandwidths]]
- [[overlap weights]]
- [[influence function]]
