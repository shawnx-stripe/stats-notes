---
title: Machine Learning for Causal Inference (MOC)
aliases:
  - ML for Causal Inference
  - Causal ML (MOC)
  - ML4CI
tags:
  - MOC
  - causal-inference
  - machine-learning
  - treatment-effects
  - policy-learning
  - uplift
updated: 2025-09-26
---

# Machine Learning for Causal Inference (MOC)

> [!summary] Start here
> How to use modern machine learning to estimate causal effects, discover heterogeneity, and learn policies—without confusing prediction with identification. This MOC links design, identification, estimation, and evaluation across experiments and observational studies.

Related starting points:
- Conceptual: [[Causal Inference (MOC)]], [[Econometrics (MOC)]], [[Experimental Design (MOC)]]
- Heterogeneity: [[Treatment Effect Heterogeneity (MOC)]]
- Inference: [[Standard Errors and Inference (MOC)]]

## Why ML in causal inference

- High-dimensional covariates and complex function classes
- Flexible modeling of nuisance components (propensity, outcomes)
- Discovery of heterogeneous effects (CATE) and optimal policies
- Improved precision in experiments (variance reduction: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]], [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]], [[Analysis of Covariance (ANCOVA)|ANCOVA]])

Caution:
- Identification still relies on causal assumptions and design (e.g., [[Unconfoundedness]], [[Instrumental Variables (IV)|Instrumental Variables (IV)]], [[Regression Discontinuity Design (RDD)|RDD]], [[Difference-in-Differences (DiD)]])
- Avoid [[bad controls]] and data [[leakage]]

## Core tasks and estimands

- Average causal effects: [[Average Treatment Effect (ATE)]], [[Average Treatment Effect on the Treated (ATT)]], [[Treatment-on-the-Treated (TOT)]], [[Local Average Treatment Effect (LATE)|LATE]]
- Conditional effects: CATE τ(x); see [[Treatment Effect Heterogeneity (MOC)]]
- Selection-margin effects: [[marginal treatment effect (MTE)]], [[Local IV]]
- Policy/value: optimal rules and off-policy value; see [[policy learning|policy learning]] and [[off-policy evaluation|off-policy evaluation]]

## Identification and design first

- Randomized experiments: ensure logging, balance, and integrity
  - [[randomized controlled trial (RCT)]], [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]], [[exposure logging]], [[triggered analysis]], [[bucketing]], [[stratification]]
- Observational studies:
  - Selection on observables: [[Unconfoundedness]], [[propensity score]], [[Overlap]]
  - IV: [[exclusion restriction]], [[relevance]], [[weak instruments]], [[monotonicity]], [[Local IV]]
  - Discontinuities: [[Regression Discontinuity Design (RDD)|Regression Discontinuity Design (RDD)]], [[fuzzy RDD]]
  - Panels: [[Difference-in-Differences (DiD)]], [[two-way fixed effects]], [[staggered adoption]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[drdid]]
- Interference and spillovers: see [[Spillovers and Interference (MOC)]]

## Nuisance-robust estimation

Principle: Learn nuisance functions flexibly; plug them into orthogonal/double-robust scores with [[cross-fitting]] for valid inference.

- Weighting: [[Inverse Probability Weighting (IPW)|IPW]], [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- Outcome modeling: regression with ML
- Doubly robust: [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- Orthogonalization: [[double machine learning]]
  - Prototype partially linear model score:
$$
\hat{\tau} = \arg\min_{\tau} \frac{1}{n}\sum_i \left[(Y_i - \hat{m}(X_i)) - \tau(X_i)\,(D_i - \hat{e}(X_i))\right]^2
$$
  - Properties: Neyman orthogonality, bias reduction, valid CLTs with ML under mild rates

Good practice:
- Cross-fitting and honest sample splitting
- Tune nuisance models within folds; avoid reusing validation data
- Report robustness to alternative nuisance learners (trees, boosting, nets, GLMs)

## Learning heterogeneous effects (CATE)

- Tree-/forest-based: [[causal forests]], [[Generalized Random Forests (GRF)|GRF]], [[random forests]]
- Meta-learners: S-, T-, X-, R-learners; see [[double machine learning]] (R-learner perspective)
- Smooth methods: [[kernel regression]], splines
- Bounds and selection-based: [[marginal treatment effect (MTE)]], [[Local IV]], [[Local Average Treatment Effect (LATE)|LATE]]
- Diagnostics and validation: [[Treatment Effect Heterogeneity (MOC)]]
  - Global tests of heterogeneity, calibration (BLP), sorted/group effects (GATES), targeting performance

Pitfalls:
- Poor overlap; mitigate with trimming, [[entropy balancing]], [[matching]]
- Post-treatment covariates (see [[bad controls]])
- Data drift between training/deployment contexts

## Policy learning and uplift

- Objective: learn d*(x) that maximizes expected utility (value)
  - See [[policy learning|policy learning]], [[policy tree|policy tree]], [[uplift]]
- Estimation strategies:
  - Plug-in: threshold CATE against cost
  - Direct uplift objectives (e.g., Qini/uplift AUC)
  - Off-policy value estimation: [[off-policy evaluation|off-policy evaluation]] (IPS, DR, SNIPS)
- Practical additions:
  - Guardrails: [[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]
  - Budget/constraints: cost-sensitive policies
  - Online adaptation: [[bandits]], [[Multi-Armed Bandit (MAB)|MAB]]; ensure exploration logging for OPE

## ML within specific designs

- RCTs: variance reduction and diagnostics
  - [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]], [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]], covariate-adjusted ANCOVA, pre-trends checks, [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]]
- DiD and panels with ML:
  - Flexible outcome models, synthetic controls ([[Synthetic Control]]), matrix completion
  - Heterogeneity by cohort/event-time: [[event study]], [[staggered adoption]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[drdid]]
- RDD:
  - Nonparametric fits ([[kernel regression]], [[local linear regression]], [[local polynomial regression]])
  - Robust bandwidth selection: [[bandwidth selection]]
  - Fuzzy designs tie to IV: [[fuzzy RDD]], [[Wald estimator]]
- IV with ML:
  - First-stage and reduced-form with ML; interpret via [[Local IV]]/[[marginal treatment effect (MTE)|MTE]]
  - Diagnose [[weak instruments]] and ensure [[relevance]]; use robust inference

## Uncertainty and inference

- Sandwich/robust SEs: [[clustered standard errors]], [[few-cluster corrections]], [[Cameron–Gelbach–Miller]], [[Conley standard errors]], [[wild cluster bootstrap]]
- Resampling: [[bootstrap]]; beware dependence and clustering
- Influence-function-based CIs for AIPW/TMLE/DML
- Multiple testing and exploration: [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]]

Reporting:
- Number of clusters, trimming/overlap diagnostics, nuisance learners, cross-fitting scheme, hyperparameters
- Sensitivity to nuisance choices and trimming thresholds

## Data integrity, logging, and pitfalls

- Logging and attribution: [[exposure logging]], [[leakage]]
- Randomization integrity: [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]]
- Triggered and conditional exposure: [[triggered analysis]]
- Sample definition and bucketing: [[bucketing]], [[stratification]]
- Overlap and positivity: [[Overlap]]; report common support and trimming rules
- Post-treatment controls: [[bad controls]]

## Practical workflow

1) Define estimand and design
- Choose ATE/ATT/CATE/LATE/MTE/Policy target
- Justify identification (RCT/[[Unconfoundedness]]/[[Instrumental Variables (IV)|IV]]/[[Regression Discontinuity Design (RDD)|RDD]]/[[Difference-in-Differences (DiD)|DiD]])

2) Prepare data and validate design
- Logging checks (AA/SRM), attrition ([[Attrition]], [[selection bias]])
- Overlap diagnostics ([[Overlap]], common support)
- Pre-analysis plan and [[pre-registration]] when possible

3) Choose estimation strategy
- Average effects: [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[double machine learning]]
- Heterogeneity: [[causal forests]], meta-/R-/X-learners
- Policy: [[policy learning|policy learning]], [[off-policy evaluation|off-policy evaluation]], [[uplift]]

4) Fit with robust practice
- [[cross-fitting]], honest splitting, hyperparameter tuning inside folds
- Trimming/reweighting for overlap: [[matching]], [[entropy balancing]]

5) Inference and validation
- SEs/CIs with appropriate dependence structure (cluster/spatial)
- Calibration (BLP) and sorted effects (GATES); targeting value
- Placebos and sensitivity: [[placebo test]], [[power analysis]], [[Minimum Detectable Effect (MDE)|MDE]]

6) Report and ship
- Assumptions, diagnostics, sensitivity, and deployment constraints
- Guardrails ([[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]), monitoring, and re-training plan

## Common pitfalls and how to avoid them

- Confusing prediction with causation: secure identification first
- Using post-treatment variables: see [[bad controls]]
- Violating overlap/positivity: diagnose and act; see [[Overlap]]
- Ignoring clustering/interference: see [[clustered standard errors]] and [[Spillovers and Interference (MOC)]]
- Data leakage and mis-logging: see [[leakage]], [[exposure logging]]
- Overfitting heterogeneity: use honest trees/[[cross-fitting]] and out-of-fold evaluation
- Weak instruments in ML-IV: check [[relevance]] and [[weak instruments]]

## Measuring success

- Estimand accuracy: bias/variance via simulation or placebo
- Heterogeneity quality: calibration (BLP), stability across folds/samples
- Policy value: DR/IPS estimates with CIs; regret vs benchmark
- Reliability: guardrails met, invariant metrics stable, robustness to perturbations

## Connections and extensions

- Bayesian approaches: [[Bayesian econometrics]], [[Bayesian Testing]], [[Region of Practical Equivalence (ROPE)|ROPE]], priors/posteriors ([[priors]])
- Time series and panels: [[Time Series (MOC)]], [[seasonality]], [[Prophet]]
- Structure and learning: [[Structural models|Structural models]]
- Bounds when assumptions are weak: [[Lee bounds]], [[Manski bounds]]

## Minimal formulas (copy-ready)
- Doubly-robust ATE (see [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]):
$$
\hat{\tau}_{\text{AIPW}} = \frac{1}{n}\sum_i \left[\big(\hat{m}_1(X_i)-\hat{m}_0(X_i)\big) + \frac{D_i\,(Y_i-\hat{m}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-D_i)\,(Y_i-\hat{m}_0(X_i))}{1-\hat{e}(X_i)}\right]
$$

- Orthogonal score (partially linear model; see [[double machine learning]]):
$$
\psi_i(\tau) = \big(Y_i - \hat{m}(X_i)\big) - \tau\,\big(D_i - \hat{e}(X_i)\big), \quad \hat{\tau} = \arg\min_\tau \frac{1}{n}\sum_i \psi_i(\tau)^2
$$

- R-learner objective for CATE τ(x):
$$
\hat{\tau}(\cdot) = \arg\min_{f \in \mathcal{F}} \frac{1}{n}\sum_i \left(\big[Y_i - \hat{m}(X_i)\big] - f(X_i)\,\big[D_i - \hat{e}(X_i)\big]\right)^2 + \lambda \,\mathcal{J}(f)
$$

- TMLE fluctuation update (ATE; see [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]):
  - Clever covariate: $H(W_i) = \frac{D_i}{\hat{e}(X_i)} - \frac{1-D_i}{1-\hat{e}(X_i)}$
  - Logistic fluctuation: $\text{logit}\,Q^\star = \text{logit}\,\hat{Q} + \hat{\varepsilon}\, H(W)$
  - Updated plug-in: $\hat{\tau}_{\text{TMLE}} = \frac{1}{n}\sum_i \big(Q^\star_1(X_i) - Q^\star_0(X_i)\big)$

- Off-policy value estimators (see [[off-policy evaluation|off-policy evaluation]]):
  - IPS: $\hat{V}_{\text{IPS}} = \frac{1}{n}\sum_i \frac{\pi(a_i\mid x_i)}{\mu(a_i\mid x_i)}\, r_i$
  - SNIPS: $\hat{V}_{\text{SNIPS}} = \frac{\sum_i \frac{\pi}{\mu} r_i}{\sum_i \frac{\pi}{\mu}}$
  - DR: $\hat{V}_{\text{DR}} = \frac{1}{n}\sum_i \left[\hat{q}(x_i,\pi) + \frac{\pi(a_i\mid x_i)}{\mu(a_i\mid x_i)}\big(r_i - \hat{q}(x_i,a_i)\big)\right]$

- Uplift/Qini (see [[uplift]]):
  - Rank by $\hat{\tau}(x)$; Qini curve plots cumulative outcome gain by rank; Qini coefficient = area between uplift and baseline curves.

- Overlap and balancing weights (see [[entropy balancing]], [[matching]], [[Overlap]]):
  - Overlap weights: $w(x) \propto \hat{e}(x)\,[1-\hat{e}(x)]$ (emphasize regions with good overlap)
  - Entropy balancing: choose $w_i$ to match moments $\sum_i w_i X_i = \bar{X}$ subject to $w_i > 0$ and entropy regularization

- IV/Wald link for fuzzy RDD and policy learning (see [[fuzzy RDD]], [[Wald, LM, and LR tests]]):
$$
\text{Wald} = \frac{\Delta Y}{\Delta D} \quad \text{(local to instrument-induced change)}
$$

## Tools and ecosystem

- R
  - [[Generalized Random Forests (GRF)|GRF]] and [[causal forests]] for CATE and policy gradients
  - [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] (tmle3/tlverse) for targeted inference; super learner (sl3) for nuisances
  - [[double machine learning]] (DoubleML), [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Inverse Probability Weighting (IPW)|IPW]], [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
  - [[policy tree]] for interpretable rules; value-based selection via [[policy learning|policy learning]]
  - [[matching]] (MatchIt, optmatch), [[entropy balancing]] (WeightIt, ebalance)
  - Panel/DiD: [[drdid]], [[Sun–Abraham estimator]], [[Callaway–Sant’Anna estimator]], [[two-way fixed effects]]
  - RDD: [[kernel regression]], [[local linear regression]], [[bandwidth selection]]

- Python
  - econml: DML, DRLearner, XLearner, CausalForestDML (forest-based CATE), IVLearner for [[Local IV]]
  - causalml: meta-learners, uplift trees/forests, Qini metrics
  - DoWhy / EconML-DoWhy: causal graphs and identification checks
  - statsmodels/linearmodels: IV, panel DiD with robust inference
  - OPE: bandit libraries; custom IPS/DR/SNIPS implementations

- Design, logging, integrity
  - [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]], [[exposure logging]], [[triggered analysis]], [[bucketing]], [[stratification]], [[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]

## Reading roadmap

- Identification and design
  - Rubin (1974); Rosenbaum & Rubin (1983) on [[propensity score]] and [[Unconfoundedness]]
  - Angrist & Imbens on [[Instrumental Variables (IV)]], [[Local Average Treatment Effect (LATE)|LATE]], [[monotonicity]]
  - Imbens & Lemieux on [[Regression Discontinuity Design (RDD)|RDD]]; modern robust RD

- Orthogonalization and DR
  - Robins & Rotnitzky on IPW; van der Laan & Rubin on [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
  - Chernozhukov et al. (2018) on [[double machine learning]]

- Heterogeneity and forests
  - Athey & Imbens (2016) on recursive partitioning
  - Wager & Athey (2018) on [[causal forests]] and asymptotics
  - Künzel et al. (2019) on meta-learners (S/T/X)

- Policy learning and OPE
  - Athey & Wager (2021), Kitagawa & Tetenov on regret and optimal rules
  - Dudík et al., Swaminathan & Joachims on DR and SNIPS for [[off-policy evaluation|OPE]]
  - Uplift modeling surveys for ranking-based targeting ([[uplift]])

- Selection margins and IV with ML
  - Heckman & Vytlacil on [[marginal treatment effect (MTE)]] and [[Local IV]]

## Checklist

> [!check] ML for Causal Inference
> - [ ] Estimand defined (ATE, ATT, CATE, LATE, MTE, policy value)
> - [ ] Valid design/assumptions (RCT, Unconfoundedness, IV, RDD, DiD)
> - [ ] Overlap/common support assessed; trimming rules pre-set
> - [ ] Nuisance models with [[cross-fitting]]; hyperparameters tuned within folds
> - [ ] Multiple nuisance learners compared (trees, boosting, GLMs)
> - [ ] Diagnostics: calibration (BLP), GATES, residual plots
> - [ ] Proper SEs: [[clustered standard errors]] / [[wild cluster bootstrap]] as needed
> - [ ] Sensitivity to trimming, nuisance specs, bandwidths
> - [ ] Policy value estimated with OPE (DR/SNIPS) + CIs where applicable
> - [ ] Guardrails ([[guardrail metric]], [[Overall Evaluation Criterion (OEC)|OEC]]) and monitoring documented

## FAQ

- When should I prefer DR/DML over naive ML on outcomes?
  - When aiming for causal effects, not predictions; DR/DML protect against misspecification and use orthogonalization to reduce bias.

- Can I do CATE with weak overlap?
  - Diagnose first. Use trimming/reweighting ([[Overlap]], [[entropy balancing]]) and report target population of inference. Extrapolation is risky.

- Are uplift models causal?
  - Only under valid identification (e.g., randomized treatment). For observational data, use DR/DML-based uplift and OPE.

- How do I pick between S/T/X/R learners?
  - Start with R-/DR-based methods for robustness; X-learner can help with imbalanced treatment; forests are strong baselines with uncertainty.

## Connections and extensions

- Experiments with ML variance reduction: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]], [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]], [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- Panels and DiD with ML: [[drdid]], [[Sun–Abraham estimator]], [[Callaway–Sant’Anna estimator]]
- RDD with ML smoothers: [[kernel regression]], [[local linear regression]], [[bandwidth selection]]
- IV with ML: [[Local IV]], [[marginal treatment effect (MTE)]], diagnose [[weak instruments]]
- Interference-aware learning: see [[Spillovers and Interference (MOC)]]

## Reporting template

- Estimand and identification strategy
- Data and logging integrity checks (AA/SRM), handling of missing/attrition ([[Missing Data and Selection (MOC)]])
- Overlap diagnostics and any trimming/weights
- Nuisance learners, cross-fitting scheme, hyperparameters
- Primary effect estimates (ATE/ATT/CATE), uncertainty, calibration
- Policy value (IPS/SNIPS/DR) with CIs; guardrails met
- Sensitivity analyses and robustness checks
- Limitations and assumptions

---

## Related notes
- [[meta-learners]]
- [[meta-learners|R-learner]]
- [[meta-learners|S-learner]]
- [[meta-learners|T-learner]]
- [[uplift metrics]]
- [[overlap weights]]
- [[Super Learner|super learner]]
- [[honest inference]]
- [[policy value]]
- [[targeting with constraints]]