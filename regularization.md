---
title: regularization
aliases:
- shrinkage
- penalization
- ridge
- lasso
- elastic net
- Regularization
tags:
- econometrics
- machine-learning
- bayesian
- penalization
- shrinkage
- high-dimensional
- inference
- selection
updated: 2025-09-17
---

# regularization

> [!summary] Quick definition
> Regularization (shrinkage/penalization) adds constraints or penalties to estimation to control model complexity, prevent overfitting, and improve out-of-sample performance. In frequentist form it solves penalized optimization (e.g., ridge, lasso, elastic net); in Bayesian form it corresponds to informative or shrinkage [[priors]]. Regularization is essential in high-dimensional problems, in nuisance modeling for [[double machine learning]], and in many [[Time Series (MOC)]] and structural applications.

- Frequentist ↔ Bayesian duality: penalties ↔ priors (e.g., ridge ≡ Gaussian prior, lasso ≡ Laplace prior; see [[Bayesian econometrics]] and [[priors]]).
- In causal ML: regularize nuisance models (propensities/outcomes) with cross-fitting to stabilize [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[double machine learning]] estimators.

---

## Why regularize?

- Bias–variance tradeoff: small, controlled bias for large variance reduction → better predictive risk.
- High-dimensionality: p comparable to or larger than n; multicollinearity; variable selection.
- Stability and interpretability: shrink or select features; enforce smoothness or structure (e.g., monotonicity).
- Robust estimation of complex components (e.g., nuisance functions in [[double machine learning]] and [[off-policy evaluation]]).

> [!warning] Over-regularization can bias target parameters (e.g., treatment effects). Orthogonalization and [[cross-fitting]] mitigate, but you should still tune carefully and report sensitivity.

---

## Canonical penalties (frequentist)

- Ridge (L2):
$$
\hat\beta = \arg\min_\beta \ \|y - X\beta\|_2^2 + \lambda \|\beta\|_2^2
$$
Shrinks coefficients toward zero; no sparsity. Bayesian view: β ∼ Normal(0, τ²I).

- Lasso (L1):
$$
\hat\beta = \arg\min_\beta \ \|y - X\beta\|_2^2 + \lambda \|\beta\|_1
$$
Promotes sparsity (variable selection). Bayesian view: β ∼ Laplace(0, b).

- Elastic net (L1+L2):
$$
\hat\beta = \arg\min_\beta \ \|y - X\beta\|_2^2 + \lambda\left(\alpha \|\beta\|_1 + (1-\alpha)\|\beta\|_2^2\right)
$$
Combines selection (L1) and grouping stability (L2).

- Group lasso: L2 within group + L1 across groups → select/deselect groups of coefficients.

- Fused lasso / total variation (TV):
$$
\|D\beta\|_1
$$
Penalizes differences across ordered coefficients (change-point detection, smooth piecewise-constant effects).

- Smoothing splines: penalty on curvature,
$$
\lambda \int \big(f''(t)\big)^2\,dt
$$
equivalent to a Gaussian process prior on f (Bayesian link).

> [!tip] Standardize predictors before L1/L2 penalties so that penalty treats features comparably.

---

## Bayesian shrinkage (priors)

- Ridge ↔ Normal prior; Lasso ↔ Laplace prior.
- Horseshoe (global–local shrinkage) for sparse signals (robust alternative to lasso).
- Spike-and-slab for explicit selection (mixture prior).
- Minnesota prior for BVAR (ridge-like shrinkage toward random-walk) in [[Time Series (MOC)]].
- See [[priors]] and [[Bayesian econometrics]] for choices, prior predictive checks, and sensitivity.

---

## Tuning and validation

- Regularization path: solution as a function of λ; pick via K-fold CV / time-aware CV / information criteria (AICc/BIC) depending on goal.
- One-standard-error rule: prefer simpler model within 1 SE of best CV score.
- Nested CV or sample splitting: for honest evaluation and policy selection (avoid optimistic bias), especially in [[policy learning]] and [[uplift]].
- For time series: use blocked/rolling CV; don’t shuffle (avoid [[leakage]]).

---

## Regularization in causal inference

- Nuisance models with ML (propensity ê(X), outcome m̂(X), censoring ŝ(X)) require regularization (lasso/GBM/RF). Combine with [[cross-fitting]] and orthogonal scores in [[double machine learning]]/[[Augmented Inverse Probability Weighting (AIPW)|AIPW]] to protect the target parameter from nuisance overfitting.
- Double selection (Belloni–Chernozhukov): lasso select covariates in both treatment and outcome models; controls = union of selected features → valid partialling-out.
- High-dimensional IV: lasso for instrument selection; report weak-IV-robust tests (see [[weak instruments]]; [[Anderson–Rubin|Anderson–Rubin test]]). Post-lasso 2SLS and LIML/[[Fuller estimator]] help stability.

> [!warning] Target parameter shrinkage: If you penalize the coefficient of interest (e.g., treatment effect) directly, account for shrinkage bias or use debiased-lasso for valid CIs.

---

## Time series and panel applications

- VAR/BVAR: ridge-like shrinkage (Minnesota prior) for lag coefficients; reduces forecast error and improves IRF stability (see [[Time Series (MOC)]]).
- State-space smoothing: penalty on state innovations → Kalman smoother; Bayesian equivalence to GP/spline priors.
- Panel/event-study with many fixed effects or leads/lags: ridge/elastic net can stabilize estimates; combine with valid estimators (e.g., [[Sun–Abraham estimator]] for staggered DiD) and interpret with care.

---

## Implicit regularization

- Subsampling and honesty in [[causal forests]]; early stopping in boosting; dropout/noise injection in neural nets.
- Model constraints (e.g., monotonicity, non-negativity), shape constraints—regularization by design.

---

## Connections to multiplicity and shrinkage

- Hierarchical shrinkage partially addresses multiple comparisons by pooling (Bayesian alternative to [[multiple testing control]]/[[False Discovery Rate (FDR)|FDR]]).
- Post-selection inference: standard errors from unpenalized OLS ignore selection; use selective inference, debiased lasso, or sample splitting.

---

## Practical guidance

> [!check] Good practice
> - [ ] Standardize features; remove/leak-proof post-treatment variables ([[leakage]])  
> - [ ] Use CV (blocked/grouped as appropriate); adopt one-SE rule for simplicity  
> - [ ] In causal targets, regularize only nuisances; use orthogonalization + [[cross-fitting]]  
> - [ ] Report λ/α, selection stability, and sensitivity across learners  
> - [ ] For IV/high-dim, report weak-IV diagnostics, and use robust inference ([[weak instruments]])  
> - [ ] For time series, use time-aware CV and compare to classical baselines (ARIMA/ETS/BVAR)

> [!warning] Pitfalls
> - Penalizing the parameter of interest without correction → biased estimates  
> - Choosing λ on the same data used for policy comparison without holdout ([[off-policy evaluation]] requires careful splits)  
> - Using IID CV in presence of clustering/temporal dependence  
> - Ignoring standard error adjustments after selection

---

## Minimal code snippets

> [!example] R: glmnet (lasso/elastic net)

```r
# install.packages("glmnet")
library(glmnet)
X <- model.matrix(~ 0 + ., data = df[,features])
y <- df$Y
cvfit <- cv.glmnet(X, y, alpha = 1)         # lasso (alpha=1); alpha in [0,1]
coef(cvfit, s = "lambda.1se")               # one-SE rule
pred <- predict(cvfit, newx = X, s = "lambda.1se")
```

> [!example] Python: scikit-learn

```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV, ElasticNetCV, RidgeCV
from sklearn.pipeline import make_pipeline

X = df[features].to_numpy(); y = df['Y'].to_numpy()

lasso = make_pipeline(StandardScaler(with_mean=True, with_std=True),
                      LassoCV(cv=5, random_state=0))
lasso.fit(X, y)
coef = lasso.named_steps['lasso'].coef_

enet = make_pipeline(StandardScaler(with_mean=True, with_std=True),
                     ElasticNetCV(l1_ratio=[.1,.5,.9,1.0], cv=5, random_state=0))
enet.fit(X, y)
```

> [!example] R: double selection (sketch)

```r
# Belloni–Chernozhukov double selection
# 1) Lasso D ~ X; 2) Lasso Y ~ X; 3) OLS Y ~ D + X_selected_union, robust SEs
```

> [!example] R: BVAR shrinkage (Minnesota prior)

```r
library(BVAR)
fit_bvar <- bvar(y, lags = 4, n_draw = 20000, n_burn = 5000,
                 priors = bv_priors(specifications = bv_mn_priors(lambda = 0.2)))
```

> [!example] Python: debiased lasso (sketch)

```python
# Fit lasso → residualize → debias via nodewise regression (use specialized packages)
```

---

## Reporting essentials

- Penalty type (L1/L2/elastic net/group/TV), tuning (λ, α), and selection procedure (CV scheme)
- Feature preprocessing (standardization) and data splits; time-aware/grouped CV if relevant
- For causal targets: which parts are regularized (nuisances vs target), orthogonalization, [[cross-fitting]] folds
- Stability (selection frequency across folds/seeds), sensitivity to λ and learners
- For IV/high-dim: weak-IV diagnostics and robust tests (AR/CLR), LIML/Fuller alternatives
- For time series: block CV, comparison against ARIMA/ETS/BVAR; forecast metrics (RMSE/[[MASE]])

---

## Related notes

- Bayesian ↔ frequentist: [[priors]] · [[Bayesian econometrics]] · [[Markov Chain Monte Carlo (MCMC)|MCMC]]  
- Causal ML: [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[causal forests]] · [[uplift]] · [[policy learning]] · [[off-policy evaluation]]  
- Econometrics: [[weak instruments]] · [[Instrumental Variables (IV)]] · [[Difference-in-Differences (DiD)]] · [[Sun–Abraham estimator]] · [[Callaway–Sant’Anna estimator]]  
- Time series: [[Time Series (MOC)]] · BVAR (Minnesota prior) · state-space smoothing · [[Prophet]]  
- Inference and governance: [[multiple testing control]] · [[False Discovery Rate (FDR)|FDR]] · [[sequential testing]] · [[leakage]] · [[pre-registration]]

---

## Further reading

- Hastie, Tibshirani, Friedman — Elements of Statistical Learning (lasso/elastic net)  
- Tibshirani (1996) — Lasso; Zou & Hastie (2005) — Elastic Net  
- Belloni, Chernozhukov, Hansen — High-dimensional methods for causal inference  
- Koop & Korobilis — BVAR shrinkage; Giannone et al. — Bayesian VARs with priors  
- Piironen & Vehtari — Regularized horseshoe (Bayesian shrinkage)

---
