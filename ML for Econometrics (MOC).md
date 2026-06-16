---
title: ML for Econometrics (MOC)
aliases: [Machine Learning for Econometrics, ML for Emetrics]
tags: [moc, econometrics, machine-learning, causal-inference, prediction, diagnostics]
updated: 2025-09-17
---

# ML for Econometrics (MOC)

> [!summary] Scope
> How to integrate modern ML with econometric goals: prediction, causal estimation, policy learning, model selection, diagnostics, and uncertainty. Emphasis on orthogonalization, cross-fitting, regularization, and design-aware validation.

---

## Quick start

> [!tip] One-page workflow
> 1) Define goal: prediction vs. causal effect vs. counterfactual policy
> 2) Choose design: see [[Causal Inference (MOC)]] (DiD/RDD/IV/observational)
> 3) Decide ML’s role: feature engineering, nuisance models (PS/OR), heterogeneous effects, policy rules
> 4) Use orthogonal methods with cross-fitting for causal targets: [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
> 5) Validate appropriately: time-aware CV for series; clustered CV for panels; guard against leakage
> 6) Diagnose: stability, overlap, weight tails, influence; interpret via SHAP/PDP/ICE where appropriate
> 7) Report: estimand, design, nuisance learners, cross-fitting, inference, and robustness

---

## Prediction vs. Causal vs. Policy

- Prediction/forecasting
  - Optimize out-of-sample error (MAE/RMSE/MAPE); see [[Time Series (MOC)]] for temporal validation
- Causal effect estimation
  - Requires a design (e.g., [[Difference-in-Differences (DiD)]], [[Regression Discontinuity Design (RDD)]], [[Instrumental Variables (IV)]], [[Unconfoundedness]]) and causal estimators (orthogonal/DR)
- Policy learning/uplift
  - Learn treatment assignment rules maximizing expected outcomes; uplift trees/forests, policy gradients

> [!warning] Leakage
> Do not use post-treatment or future information in nuisance/feature construction; see [[bad controls]] and [[leakage]].

---

## Estimation toolbox (prediction)

- Linear/regularized
  - [[regularization|Lasso/ridge/elastic net]], GLM/GBM with regularization, grouped lasso
- Tree ensembles
  - [[random forests]], [[gradient boosting]] (XGBoost/LightGBM/CatBoost)
- Kernel and margin methods
  - SVM, [[Gaussian process|Gaussian processes]]
- Neural networks
  - MLP/CNN/RNN/LSTM/Transformers
- Model selection
  - Cross-validation, nested CV, information criteria for hybrids
- Interpretation
  - Partial dependence (PDP), ICE, SHAP/LIME; [[stability selection]]

---

## Causal ML toolbox

- Orthogonal / Neyman-orthogonal methods
  - [[double machine learning]]: orthogonal moments + [[cross-fitting]]
  - [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]: [[Doubly Robust estimators]] using ML nuisances; [[Super Learner]]
- Heterogeneous treatment effects (HTE)
  - [[treatment effect heterogeneity]]; CATE learners: T-/S-/X-/R-/DR-learners
  - [[causal forests|Causal trees/forests]] (grf/causal forest)
- Policy learning / uplift
  - [[uplift]], doubly robust [[policy value|policy evaluation]], [[policy learning]], and contextual bandits
- Design-aware ML
  - DiD with ML: DR-DiD (see [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]; [[Callaway–Sant’Anna estimator]] with ML nuisances), event-study regularization
  - IV with ML: ML for first-stage, weak-IV robust inference, DeepIV/IV-forest
  - RDD with ML: flexible estimation of conditional means; guard against overfitting near cutoff

> [!note] Nuisance estimation
> Use flexible learners for propensity scores, outcome regressions, censoring models. Cross-fit to avoid overfitting bias; check [[Overlap]] and weight tails.

---

## Validation and resampling

- Cross-fitting and sample splitting
  - K-fold [[cross-fitting]] for orthogonal estimators; nested CV for hyperparameters
- Time-aware validation
  - Rolling-origin and blocked CV; no shuffling for series; see [[Time Series (MOC)]]
- Cluster-aware validation
  - Leave-one-cluster-out for panels; avoid mixing clusters between train/test when clustering used in SEs
- Evaluation metrics
  - Prediction: MAE/RMSE/[[MASE]], sMAPE
  - CATE/Policy: [[policy value]], regret, [[uplift metrics|Qini/uplift metrics]]; influence-function-based SEs

---

## Feature engineering and preprocessing

- Encodings and interactions
  - One-hot, target encoding (guard leakage); learned interactions via trees/NNs
- Temporal features
  - Lags, rolling stats, Fourier terms, holiday dummies; see [[seasonality]]
- Panels
  - Entity/time effects as features or dummies; demeaning; stratified interactions
- Missing data
  - Imputation (mice/softImpute/Kalman); [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] for missing outcomes; [[Inverse Probability Weighting (IPW)|IPW]]/[[entropy balancing]] for selection/design

---

## Inference and uncertainty

- Asymptotics with orthogonal scores
  - IF-based SEs for ATE/ATT/CATE aggregates (AIPW/DML/TMLE)
- Bootstrap
  - Cluster/bootstrap for panels; [[block bootstrap]] for series
- Conformal prediction
  - Conformal intervals for predictions and residuals; conformalized quantile regression

> [!warning] Few clusters
> Use [[few-cluster corrections]] or wild cluster bootstrap for clustered designs; see [[clustered standard errors]].

---

## Fairness, stability, and ethics

- Fairness
  - Group/individual fairness metrics and constraints
- Stability and transport
  - Covariate shift and domain adaptation; reweighting/importance sampling
- Transparency
  - Document design, features, hyperparameters, seeds, and software versions

---

## Software ecosystem (examples)

- R: tidymodels, mlr3, xgboost, lightgbm, ranger, glmnet; grf (causal forests); DoubleML; tmle3; SuperLearner
- Python: scikit-learn, xgboost/lightgbm/catboost; econml (DRLearner/DML); DoWhy/EconML; causalml; doubleml; zEpid (TMLE); statsmodels/linearmodels for FE/IV
- Julia/Stata: EconPDEs/MLJ (Julia); teffects/causal inference add-ons (Stata)

---

## Reporting essentials

- Estimand/design and why ML is used (nuisance, features, heterogeneity, policy)
- Learners for each nuisance (PS, OR, censoring), cross-fitting folds, hyperparams
- Validation protocol (time- or cluster-aware), leakage protections
- Diagnostics: overlap, weight distributions (ESS), balance, sensitivity to learners
- Inference method (IF-based vs. bootstrap), clustering level
- Limitations (external validity, data drift, missingness mechanisms)

---

## Reading list

- Orthogonal/DR: Chernozhukov et al. (DML), van der Laan & Rubin (TMLE), Athey & Imbens (ML for CI)
- HTE/Policy: Athey & Imbens (Causal Trees/Forests), Wager & Athey (grf), Zhao et al. (policy learning)
- Practice: Kuhn & Johnson (Feature Engineering), Hastie–Tibshirani–Friedman (ESL), Bishop (PRML)
- Tools: Hyndman & Athanasopoulos (forecasting), Hyndman et al. (tsfeatures)

---

## Index of topics (A–Z)

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Attrition]] · [[Average Treatment Effect (ATE)]] · [[Average Treatment Effect on the Treated (ATT)]]
- [[bad controls]] · [[Bayesian econometrics]] · [[bootstrap]]
- [[Callaway–Sant’Anna estimator]] · [[clustering]] · [[clustered standard errors]] · [[composition]] · [[Conley standard errors]]
- [[double machine learning]] · [[Doubly Robust estimators]] · [[meta-learners|DR-learner]]
- [[Econometrics (MOC)|econometrics]] (see [[Econometrics (MOC)]]) · [[entropy balancing]] · [[event study]]
- [[exclusion restriction]]
- [[few-cluster corrections]] · feature engineering · [[fairness]]
- [[Gardner DID2S]] · [[causal forests|grf/causal forest]] · [[group-time average treatment effect]]
- [[Instrumental Variables (IV)]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Inverse Probability Weighting (IPW)|IPW]]
- [[leakage]] · [[Lee bounds]] · [[Local IV]]
- [[matching]] · [[Manski bounds]] · [[monotonicity]] · [[Moulton problem]]
- [[Overlap]]
- [[parallel trends assumption]] · [[placebo test]] · [[policy learning]] · [[potential outcomes]] · [[pre-trends]] · [[Prophet]]
- [[Regression Discontinuity Design (RDD)]] · [[relevance]]
- [[seasonality]] · [[selection bias]] · [[stratification]] · [[Super Learner]] · [[Sun–Abraham estimator]] · [[Synthetic Control]] · [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Treatment-on-the-Treated (TOT)]] · [[two-way fixed effects]]
- [[weak instruments]]
- [[Gaussian process]] · [[LOESS]] · [[decision trees]] · [[distributed random forests]]

---

## Related hubs

- [[Econometrics (MOC)]]
- [[Causal Inference (MOC)]]
- [[Time Series (MOC)]]
