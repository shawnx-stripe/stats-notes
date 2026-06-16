---
title: Econometrics (MOC)
aliases: [Econometrics, econometrics, Econometrics hub, Emetrics MOC]
tags: [moc, econometrics, statistics, inference, modeling]
updated: 2025-09-17
---

# Econometrics (MOC)

> [!summary] Scope
> Methods for empirical economic analysis: identification, estimation, inference, diagnostics, and reporting across cross-sectional, panel, time-series, structural, and causal frameworks.

---

## Quick start

> [!tip] One-page workflow
> 1) Specify the question and estimand (prediction vs. structural parameter vs. causal effect)  
> 2) Choose design/model family (cross-section, panel, time series, or [[Causal Inference (MOC)]])  
> 3) Select estimator (OLS/GLM/ML/GMM/IV/etc.) and robust inference method  
> 4) Diagnose fit and assumptions (misspecification, heteroskedasticity, serial correlation, stationarity)  
> 5) Validate with out-of-sample/cross-validation where relevant; perform robustness and sensitivity checks  
> 6) Report clearly: design, assumptions, estimator, clustering, diagnostics, limitations, and reproducibility

---

## Major domains

- Causal Inference
  - [[Causal Inference (MOC)]]
- Time Series and Forecasting
  - [[Time Series (MOC)]]
- Cross-Sectional and Microeconometrics
  - Discrete choice (logit/probit), counts (Poisson/NB), limited dependent vars (tobit), quantiles, non/semiparametrics
- Panel Data / Longitudinal
  - FE/RE, dynamic panels (Arellano–Bond/Blundell–Bond), clustered/HAC inference, panel causal designs
- Structural Econometrics
  - [[Structural models]]: [[Maximum Likelihood Estimation (MLE)|MLE]]/GMM/Simulated MLE/Method of Simulated Moments, identification and counterfactual analysis
- Bayesian Econometrics
  - [[Bayesian econometrics]]: [[priors]], [[Markov Chain Monte Carlo (MCMC)|MCMC]]/[[Sequential Monte Carlo (SMC)|SMC]], Bayesian VAR/DSGE
- Machine Learning for Econometrics
  - [[ML for Econometrics (MOC)]]: [[regularization]], [[ML for Econometrics (MOC)|Causal ML (MOC)]], [[cross-fitting]], [[double machine learning]]

---

## Estimation toolbox

- Classical/likelihood
  - [[Ordinary Least Squares (OLS)|OLS]], [[Generalized Linear Model (GLM)|GLM]], [[Maximum Likelihood Estimation (MLE)|MLE]], [[Nonlinear Least Squares (NLS)|NLS]]
- Moment-based
  - [[Generalized Method of Moments (GMM)|GMM]], [[Two-Stage Least Squares (2SLS)|2SLS]] / [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]], [[Instrumental Variables (IV)|IV]] → [[relevance]] · [[exclusion restriction]] · [[monotonicity]]
- Limited dependent variables
  - [[Generalized Linear Model (GLM)|Logit/Probit]], Tobit, [[Generalized Linear Model (GLM)|Poisson/NB]], zero-inflation
- Quantiles and distributional
  - [[quantile regression|Quantile regression]], conformalized quantile regression
- Nonparametric/Semiparametric
  - [[kernel regression|Kernel/local polynomial]], [[splines|Series/splines]], single-index models
- Penalized/ML
  - [[regularization|Lasso/ridge/elastic net]], [[random forests|Random forest/GBM]], neural nets, [[double machine learning]]
- Simulation-based
  - [[bootstrap|Bootstrap]], [[randomization inference|Permutation test]], [[Simulated method of moments]]

---

## Inference and standard errors

- Robust SEs and clustering
  - [[clustered standard errors]] · [[clustering]] · [[few-cluster corrections]] · [[wild cluster bootstrap]]
- Heteroskedasticity/Autocorrelation
  - White HC (heteroskedastic-robust), [[Newey–West]], [[Driscoll–Kraay]], [[Conley standard errors]]
- [[Hypothesis testing]]
  - [[Wald, LM, and LR tests]], [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]]
- Weak instruments and IV diagnostics
  - [[weak instruments]], [[Kleibergen–Paap]], [[Montiel Olea–Pflueger F]], [[Anderson–Rubin|Anderson–Rubin test]]

---

## Diagnostics and specification tests

- Model specification
  - [[RESET test]], link tests, functional-form checks, partial residuals
- Heteroskedasticity / leverage
  - Breusch–Pagan test, White test, influence/leverage (DFBETAs, Cook’s D)
- Serial correlation (cross-section/panel/time)
  - [[Durbin–Watson]], [[Breusch–Godfrey]]
- Outliers/anomalies
  - Robust regression, winsorization strategies (with care)
- Causal diagnostics (see hub)
  - [[event study]] · [[pre-trends]] · [[placebo test]] · [[selection bias]] · [[Attrition]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]

---

## Time series essentials

- Univariate
  - [[ARIMA|ARMA/ARIMA/SARIMA]], seasonal adjustment (X-13), [[seasonality]]; stationarity [[ADF test]], [[KPSS test]]
- Volatility
  - [[GARCH|ARCH/GARCH]], EGARCH/GJR, realized volatility
- Multivariate
  - [[VAR|VAR/SVAR]], [[VECM]], [[cointegration]] (Engle–Granger, Johansen)
- State-space / filtering
  - [[Kalman filter|Kalman filter/state-space]], unobserved components
- Local projections and IRFs
  - [[Local projections (Jordà)]]
- Structural breaks and regimes
  - [[Bai–Perron]], [[Markov switching]]

---

## Panel data essentials

- Fixed/random effects
  - [[Fixed effects]], [[random effects|Random effects]], Hausman test
- Dynamic panels
  - [[Arellano–Bond]], [[System GMM]]
- Inference
  - [[clustered standard errors]] · multiway clustering · [[Driscoll–Kraay]]
- Causal panels
  - [[Difference-in-Differences (DiD)]] and modern variants (see hub), [[Synthetic Control]]

---

## Causal designs (index)

- [[Causal Inference (MOC)]]
  - [[quasi-experimental design]] · [[Difference-in-Differences (DiD)]] · [[Regression Discontinuity Design (RDD)]] · [[Instrumental Variables (IV)]] · [[Synthetic Control]]
  - Estimands: [[Average Treatment Effect (ATE)]] · [[Average Treatment Effect on the Treated (ATT)]] · [[Local Average Treatment Effect (LATE)|LATE]]
  - Estimators: [[Inverse Probability Weighting (IPW)|IPW]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Doubly Robust estimators]]
  - Assumptions: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] · [[Unconfoundedness]] · [[Overlap]] · [[parallel trends assumption]] · [[exclusion restriction]] · [[relevance]] · [[monotonicity]]

---

## Structural and Bayesian

- Structural models
  - [[Structural models]]: identification, counterfactuals, discrete-continuous choice, auction models
  - Estimation: [[Maximum Likelihood Estimation (MLE)|MLE]], [[Generalized Method of Moments (GMM)|GMM]], [[Simulated method of moments]]
- Bayesian
  - [[Bayesian econometrics]]: priors, posterior computation (MCMC/SMC), Bayesian model comparison
  - Applications: Bayesian VAR, DSGE estimation

---

## Data handling and reproducibility

- Data workflows
  - Versioned datasets, codebooks, tidy design, missing-data handling (MCAR/MAR/MNAR)
- Reproducibility
  - Scripts/notebooks; set seeds; environment management; dynamic documents
- Transparency
  - Pre-analysis plans, code and data sharing, computational diagnostics

---

## Reporting essentials

- Question and estimand; identification strategy and assumptions
- Model specification; estimator and inference method (robust/cluster/HAC)
- Diagnostics and robustness (misspecification, selection, breaks)
- Uncertainty (CIs, bands, forecast intervals); small-sample caveats
- Limitations and external validity; sensitivity/bounds where relevant
- Reproducibility (software versions, seeds, code/data availability)

---

## Reading list

- General econometrics
  - Wooldridge, Greene, Hayashi
- Causal inference
  - [[Angrist and Pischke]] · [[Imbens and Rubin]] · [[Hernán and Robins]] · [[Cunningham (Mixtape)]]
- Time series
  - Hamilton, Hyndman & Athanasopoulos
- Bayesian/structural
  - Gelman et al., DeJong & Dave, Canova

---

## Index of topics (A–Z)

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[GARCH|ARCH/GARCH]] · [[Attrition]] · [[Average Treatment Effect (ATE)]] · [[Average Treatment Effect on the Treated (ATT)]]  
- [[Bai–Perron]] · [[Bayesian econometrics]] · [[bootstrap|Bootstrapping]] · [[Breusch–Godfrey]] · Breusch–Pagan test  
- [[Causal Inference (MOC)]] · [[clustered standard errors]] · [[clustering]] · [[cointegration]] · [[Conley standard errors]]  
- [[Difference-in-Differences (DiD)]] · [[DiD estimator]] · [[Driscoll–Kraay]] · [[Durbin–Watson]] · [[Doubly Robust estimators]]  
- [[entropy balancing|Entropy balancing]] · [[event study]] · [[exclusion restriction]]  
- [[few-cluster corrections]] · [[Fixed effects]] · [[fuzzy RDD]]  
- [[Generalized Method of Moments (GMM)|GMM]] · [[Goodman–Bacon decomposition]] · [[group-time average treatment effect]]  
- [[Instrumental Variables (IV)]] · [[Intent-to-Treat (ITT)]] · [[interference]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Inverse Probability Weighting (IPW)|IPW]]  
- [[Kalman filter|Kalman filter/state-space]] · [[KPSS test]]  
- [[Local Average Treatment Effect (LATE)|LATE]] · [[Lee bounds]] · [[Limited Information Maximum Likelihood (LIML)|LIML]] · [[Local projections (Jordà)]] · [[Generalized Linear Model (GLM)|Logit/Probit]] · [[regularization|Lasso/ridge/elastic net]]  
- [[Manski bounds]] · [[Markov switching]] · [[matching]] · [[Maximum Likelihood Estimation (MLE)|MLE]] · [[monotonicity]] · [[Moulton problem]]  
- [[Newey–West]] · [[Nonlinear Least Squares (NLS)|NLS]] · [[noncompliance]] · [[No spillovers]]  
- [[Overlap]]  
- [[Panel Data Methods (MOC)|Panel Data]] · [[parallel trends assumption]] · [[placebo test]] · [[Generalized Linear Model (GLM)|Poisson/NB]] · [[potential outcomes]] · [[pre-trends]]  
- [[quantile regression|Quantile regression]] · [[Regression Discontinuity Design (RDD)]] · [[relevance]] · [[RESET test]]  
- [[seasonality]] · [[selection bias]] · [[Simulated method of moments]] · [[staggered adoption]] · [[stratification]] · [[Sun–Abraham estimator]] · [[Synthetic Control]] · [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]  
- [[Time Series (MOC)]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Treatment-on-the-Treated (TOT)]] · [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[two-way fixed effects]]  
- [[VAR|VAR/SVAR]] · [[VECM]] · [[weak instruments]] · [[wild cluster bootstrap]]
- [[Bertrand–Duflo–Mullainathan (2004)]] · [[DFL reweighting]] · [[DSGE]] · [[Durbin–Wu–Hausman test]] · [[Fuller estimator]] · [[Hansen J test]] · [[Hotz–Miller CCP]] · [[Interrupted Time Series (ITS)]] · [[Jackknife IV (JIVE)]] · [[MIV]] · [[MPEC]] · [[MTR]] · [[MTS]] · [[Oaxaca–Blinder decomposition]] · [[Sargan test]] · [[Stock–Yogo]] · [[control function]] · [[exogeneity]] · [[first stage]] · [[indirect inference]] · [[k-class estimator]] · [[overidentification test]]  

---

## Related hubs

- [[Causal Inference (MOC)]]
- [[Time Series (MOC)]]
- [[ML for Econometrics (MOC)]]
