---
title: Model Estimation (MOC)
aliases:
  - Estimation methods (MOC)
  - Statistical estimation (MOC)
  - Econometric estimation (MOC)
tags:
  - MOC
  - econometrics
  - statistics
  - estimation
  - optimization
  - inference
updated: 2025-09-26
---

# Model Estimation (MOC)

> [!summary] Start here
> A map of how we fit models to data: objectives, algorithms, assumptions, and diagnostics. Connects least squares, likelihood and Bayesian methods, moment-based estimators, penalization, latent-variable/state-space estimation, and non/semiparametrics. Links to the right inference and robustness tools.

Related starting points:
- Concepts: [[Econometrics (MOC)]], [[Causal Inference (MOC)]], [[Identification Strategies (MOC)]]
- Inference: [[Standard Errors and Inference (MOC)]], [[Wald, LM, and LR tests]]
- ML + Causal: [[Machine Learning for Causal Inference (MOC)]]

## Core estimation paradigms

- Least squares family
  - [[Ordinary Least Squares (OLS)|OLS]]: closed-form under exogeneity, homoskedastic iid errors
  - WLS/GLS: known/estimated error covariance; feasible GLS
  - [[Nonlinear Least Squares (NLS)|NLS]]: nonlinear mean function; Gauss–Newton/LM
  - Robust/quantile (to create): Huber, [[quantile regression]] for heavy tails/outliers

- Likelihood-based
  - [[Maximum Likelihood Estimation (MLE)|MLE]]: maximize likelihood; score/Hessian; asymptotic normality via Fisher information
  - [[Generalized Linear Model (GLM)|GLM]]: exponential family + link; IRLS algorithm
  - [[Bayesian econometrics]]: priors + likelihood → posterior; computation via [[Markov Chain Monte Carlo (MCMC)|MCMC]] / [[Sequential Monte Carlo (SMC)|SMC]]
  - Latent variable via EM: mixture models, incomplete data (see “EM algorithm” to create)

- Moment-based
  - Method of moments; [[Generalized Method of Moments (GMM)|GMM]]: match sample to population moments; optimal weighting; overidentification tests
  - IV/2SLS as special cases within GMM

- Penalized and regularized
  - [[regularization]]: ridge/L2, lasso/L1, elastic-net; coordinate descent / proximal methods
  - Model selection via penalty ↔ information criteria (AIC/BIC) or CV

- Nonparametric/semiparametric
  - [[kernel regression]], [[splines]]/series; partially linear models; sieve GMM
  - Tree/forest estimators (prediction) + causal variants ([[Generalized Random Forests (GRF)|GRF]], [[causal forests]])

- State-space and latent structure
  - [[Kalman filter]]/smoother (linear–Gaussian); EM for parameter learning
  - [[Hidden Markov Model (HMM)|HMM]] (discrete latent states): forward–backward, Viterbi, EM
  - Particle methods: [[Sequential Monte Carlo (SMC)|SMC]] for nonlinear/non-Gaussian

- Causal estimators (estimation-oriented)
  - [[Inverse Probability Weighting (IPW)|IPW]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]] (orthogonal scores + [[cross-fitting]])
  - Panel design estimators: [[drdid]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]

## Choosing an estimator

- Data and noise
  - Continuous Gaussian-like → OLS/GLM; counts/binary → [[Generalized Linear Model (GLM)|GLM]] with canonical link
  - Heavy tails/outliers → robust/quantile methods
  - Heteroskedasticity/correlation → WLS/GLS; sandwich/HAC variance

- Identification and structure
  - Endogeneity → IV/[[Generalized Method of Moments (GMM)|GMM]]
  - Discrete choices/limited dependent vars → likelihood-based (logit/probit), tobit
  - Latent variables/time dependence → Kalman/HMM/SMC

- Dimensionality and generalization
  - High p → [[regularization]] (ridge/lasso), dimension reduction
  - Flexible fits with validation → splines/forests + CV/[[cross-validation]]

- Objectives and constraints
  - Predictive vs causal targets (see [[Identification Strategies (MOC)]])
  - Constraints/priors → constrained MLE or Bayesian

## Objective functions and estimating equations

- M-estimation: minimize empirical loss
  - L(θ) = n⁻¹ Σ ρ(y_i, f(x_i; θ)); OLS with ρ(u)=u²; Huber for robustness
- Likelihood/MLE: maximize ℓ(θ) = Σ log p(y_i | x_i; θ); score ∂ℓ/∂θ = 0
- GMM: choose θ to satisfy moment conditions
  - m̄_n(θ) = n⁻¹ Σ g(z_i, θ); θ̂ = argmin m̄_n(θ)' W m̄_n(θ)
- Penalized risk: L(θ) + λ J(θ) with J(θ)=||θ||₁/||θ||₂ or structured penalties

## Optimization toolbox

- Gradient/Newton
  - Gradient descent, Newton–Raphson, (L-)BFGS; line search; trust regions
- Second-order approximations
  - IRLS for GLMs; Gauss–Newton/Levenberg–Marquardt for [[Nonlinear Least Squares (NLS)|NLS]]
- EM and variants
  - E-step expected complete-data log-likelihood; M-step maximization
- Coordinate descent / proximal methods
  - Lasso/elastic-net; soft-thresholding; ADMM for constrained problems
- Practicalities
  - Initialization (multi-start for nonconvex), scaling/standardization, constraints/box bounds
  - Diagnostics: gradient norms, KKT conditions, Hessian check; reproducibility (seeds)

Related notes to create: [[EM algorithm]], [[BFGS]], proximal gradient, [[ADMM]], line search, [[trust region]]

## Asymptotics, uncertainty, and tests

- Consistency and asymptotic normality
  - θ̂ → θ₀; √n(θ̂−θ₀) → N(0, V); regularity and identification needed
- Variance estimators
  - Model-based (inverse Hessian / Fisher information)
  - Robust/sandwich for misspecification; HAC for time series; cluster-robust for grouped data
- Hypothesis testing
  - [[Wald, LM, and LR tests]]; joint tests; score tests for nested models
- Resampling
  - [[bootstrap]] for complex estimators, small samples, nonstandard limits

Links: [[clustered standard errors]], [[Conley standard errors]], [[wild cluster bootstrap]], [[Standard Errors and Inference (MOC)]]

## Model selection and validation

- Information criteria
  - AIC (K-L), BIC (Schwarz), small-sample corrections; for Bayesian: [[BIC]] proxy, WAIC/DIC (to create)
- Out-of-sample validation
  - [[cross-validation]]/OOS splits; time-series CV (rolling); nested CV for tuning
- Bayesian model comparison
  - [[Bayesian Testing]] via Bayes factors/posterior odds; posterior predictive checks
- Regularization paths
  - Penalty tuning via CV; stability selection (to create) for variable selection

Related notes: [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]]

## Diagnostics and robustness

- Misspecification and fit
  - Residual diagnostics; link/variance checks in [[Generalized Linear Model (GLM)|GLM]]; dispersion
  - Influence/leverage; outlier detection; goodness-of-fit tests
- Dependence and structure
  - Serial/spatial correlation → HAC/Conley; clusters → cluster-robust
- Overlap and extrapolation
  - Monitor support in covariates; leverage points; report effective sample size in weighted fits
- Sensitivity
  - Compare estimators (OLS vs robust; MLE vs QMLE); bootstrap; leave-one-cluster-out

Links: [[Robust Methods (MOC)]], [[Missing Data and Selection (MOC)]], [[Spillovers and Interference (MOC)]]

## Time-series and state-space specifics

- HAC/Newey–West; long-run variance; frequency-domain options
- State-space: [[Kalman filter]] (linear-Gaussian), extended/unscented variants; parameter EM
- Nonlinear/non-Gaussian: [[Sequential Monte Carlo (SMC)|SMC]] (particle filters); [[Hidden Markov Model (HMM)|HMM]] for discrete latent states
- Forecast evaluation: MSE/MAE; Diebold–Mariano (to create)

Links: [[Time Series (MOC)]], [[seasonality]], [[Prophet]]

## Non/semiparametric estimation

- Local methods: [[kernel regression]], [[local linear regression]], [[local polynomial regression]]
- Global smoothers: [[splines]], series (Fourier/polynomials), sieve MLE/GMM
- Causal semiparametric: [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]] with [[cross-fitting]]

## Minimal formulas (copy-ready)

- OLS closed form:
$$
\hat{\beta} = (X'X)^{-1} X'Y, \quad \hat{V}(\hat{\beta}) = \hat{\sigma}^2 (X'X)^{-1}, \quad \hat{\sigma}^2 = \frac{\|Y - X\hat{\beta}\|^2}{n-k}
$$

- GLM likelihood (canonical):
$$
\ell(\beta) = \sum_i \frac{y_i \theta_i - b(\theta_i)}{a(\phi)} + c(y_i,\phi), \quad \theta_i = x_i'\beta
$$

- MLE asymptotic variance:
$$
\sqrt{n}(\hat{\theta}-\theta_0) \xrightarrow{d} N\big(0,\, I(\theta_0)^{-1}\big), \quad I(\theta) = -\mathbb{E}\!\left[\frac{\partial^2 \ell(\theta)}{\partial \theta \partial \theta'}\right]
$$

- GMM objective:
$$
\hat{\theta} = \arg\min_{\theta}\; \bar{g}_n(\theta)' W \,\bar{g}_n(\theta), \quad \bar{g}_n(\theta) = \frac{1}{n}\sum_i g(z_i,\theta)
$$

- Penalized least squares (lasso):
$$
\hat{\beta} = \arg\min_{\beta}\; \frac{1}{2n}\|Y - X\beta\|^2 + \lambda \|\beta\|_1
$$

- EM (conceptual):
$$
Q(\theta \mid \theta^{(t)}) = \mathbb{E}\big[\ell_{\text{complete}}(\theta) \mid \text{data}, \theta^{(t)}\big], \quad \theta^{(t+1)} = \arg\max_\theta Q(\theta \mid \theta^{(t)})
$$

## Practical checklist

> [!check] Workflow
> - [ ] Define estimand + identification (causal vs predictive)
> - [ ] Choose estimation paradigm (LS / Likelihood / Moments / Penalized / Nonparametric)
> - [ ] Match algorithm to problem (convex? latent? high-dim?)
> - [ ] Validate: CV or information criteria; residuals and influence checks
> - [ ] Inference: robust SEs aligned to structure; resampling when needed
> - [ ] Sensitivity: alternative specs/penalties; bootstrap; leave-one-cluster-out
> - [ ] Report optimization details (convergence, tolerances), selection/tuning, and uncertainty

## Common pitfalls

> [!warning] Avoid these
> - Treating estimation as identification (omitting instrument/design issues)
> - Ignoring dependence (clustering/serial/spatial)
> - Overfitting with flexible models; no out-of-sample validation
> - Blind trust in default optimizers; unreported convergence failures
> - Using MLE without checking regularity/identifiability or separation
> - Weak instruments passed off as precise IV estimates

## Cross-links

- Least squares and GLM: [[Ordinary Least Squares (OLS)|OLS]], [[Nonlinear Least Squares (NLS)|NLS]], [[Generalized Linear Model (GLM)|GLM]]
- Likelihood/Bayes: [[Maximum Likelihood Estimation (MLE)|MLE]], [[Bayesian econometrics]], [[Markov Chain Monte Carlo (MCMC)|MCMC]], [[Sequential Monte Carlo (SMC)|SMC]]
- Moments/IV: [[Generalized Method of Moments (GMM)|GMM]], [[Instrumental Variables (IV)]], [[weak instruments]]
- Penalization/ML: [[regularization]], [[random forests]], [[kernel regression]], [[Generalized Random Forests (GRF)|GRF]], [[causal forests]]
- Latent/time/state-space: [[Kalman filter]], [[Hidden Markov Model (HMM)|HMM]], [[Time Series (MOC)]]
- Causal/semiparametric: [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]], [[drdid]]
- Inference/robustness: [[Standard Errors and Inference (MOC)]], [[clustered standard errors]], [[bootstrap]], [[Robust Methods (MOC)]]

---

Related notes to create:
- [[EM algorithm]]
- [[BFGS]]
- proximal gradient
- [[ADMM]]
- line search
- [[trust region]]
- [[Fisher information]]
- [[sandwich estimator]]
- [[influence function]]
- [[AIC]]
- WAIC
- DIC
- [[stability selection]]
- [[Diebold–Mariano test]]
- [[quantile regression]]
- [[robust regression]]
- [[identifiability]]
- log-sum-exp trick
- numerical stability