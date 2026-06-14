---
title: Ordinary Least Squares (OLS)
aliases: [OLS, ordinary least squares, linear regression, Gauss–Markov, least squares]
tags: [econometrics, estimation, linear-models, inference, robust, clustering, diagnostics, fe, did]
updated: 2025-09-17
---

# Ordinary Least Squares (OLS)

> [!summary] Quick definition
> Ordinary Least Squares (OLS) estimates β in the linear mean model E[Y|X]=Xβ by minimizing the sum of squared residuals. Under exogeneity and full rank, the OLS estimator is consistent; under the classical homoskedastic i.i.d. errors it is efficient in the class of linear unbiased estimators (Gauss–Markov BLUE) and asymptotically normal. Inference should use robust/cluster/HAC covariances when assumptions are violated.

- Related estimators: [[Generalized Linear Model (GLM)|GLM]] (generalizes beyond Gaussian), [[Maximum Likelihood Estimation (MLE)|MLE]] (Gaussian case), [[Generalized Method of Moments (GMM)|GMM]] (moment view), [[regularization]] (ridge/lasso), Bayesian linear regression ([[Bayesian econometrics]] with [[priors]]).
- Panels/DiD: OLS underlies FE/TWFE and many [[Difference-in-Differences (DiD)]] implementations (see [[two-way fixed effects]], [[Sun–Abraham estimator]], [[Callaway–Sant’Anna estimator]]).

---

## Model and estimator

- Linear regression model:
$$
Y = X\beta + u,\quad X\in \mathbb{R}^{N\times k},\ \beta\in \mathbb{R}^k,\ u\in \mathbb{R}^N.
$$

- OLS estimator (full rank X):
$$
\hat\beta = (X'X)^{-1}X'Y.
$$

- Fitted values and residuals:
$$
\hat Y = X\hat\beta = HY,\quad e = Y - \hat Y = MY,
$$
where $H = X(X'X)^{-1}X'$ (hat matrix), $M = I - H$ (residual maker).

- Sample variance of residuals (homoskedastic model-based):
$$
\hat\sigma^2 = \frac{e'e}{N - k}.
$$

- Model-based covariance of $\hat\beta$ (i.i.d. Gaussian errors):
$$
\widehat{\mathrm{Var}}(\hat\beta) = \hat\sigma^2\,(X'X)^{-1}.
$$

FWL (Frisch–Waugh–Lovell) theorem (partialling-out): the coefficient on a regressor equals the OLS of residualized Y on residualized regressor after projecting out controls; central to FE/TWFE and [[double machine learning]]’s PLR.

---

## Assumptions and properties

- Exogeneity: $\mathbb{E}[u\mid X]=0$ (or moment exogeneity $X'u/N \to 0$) ⇒ consistency.
- Full column rank of X (no perfect multicollinearity).
- Homoskedasticity and no serial correlation (classical OLS) ⇒ Gauss–Markov BLUE among linear unbiased estimators; model-based SEs valid.
- Normality (optional) ⇒ exact finite-sample t/F inference; not required asymptotically.

When homoskedasticity/independence fail, use robust covariances:
- Heteroskedasticity: HC/White sandwich (see below).
- Cluster dependence: cluster-robust (see [[clustered standard errors]]; use [[few-cluster corrections]]/[[wild cluster bootstrap]] if clusters are few).
- Serial correlation (time series): [[Newey–West]] HAC.
- Spatial correlation: [[Conley standard errors]].

Best Linear Predictor interpretation: even under misspecification (nonlinear mean), OLS estimates the projection of Y onto the linear span of X—interpret accordingly; causal interpretation requires exogeneity and no [[bad controls]]/[[leakage]].

Endogeneity (E[u|X] ≠ 0) ⇒ OLS biased/inconsistent; use [[Instrumental Variables (IV)]] (mind [[weak instruments]]) or design-based methods (DiD/RD).

---

## Robust/cluster/HAC covariances

- Sandwich (HC0; QMLE):
$$
\widehat{\mathrm{Var}}_{HC}(\hat\beta) = (X'X)^{-1}\Big(\sum_i x_i x_i' e_i^2\Big)(X'X)^{-1}.
$$
HC1/HC2/HC3 variants adjust for leverage/small-sample.

- Cluster-robust:
$$
\widehat{\mathrm{Var}}_{CL}(\hat\beta) = (X'X)^{-1} \Big(\sum_g X_g'e_g e_g' X_g\Big) (X'X)^{-1},
$$
with $g$ indexing clusters. Use [[few-cluster corrections]] or [[wild cluster bootstrap]] if cluster count is small.

- HAC (time series): use [[Newey–West]]; spatial: [[Conley standard errors]].

See [[Wald, LM, and LR tests]] and [[Hypothesis testing]] for t/F/Wald tests based on these covariances.

---

## Weighted/Feasible GLS

- Weighted Least Squares (known heteroskedasticity structure): minimize $\sum w_i (y_i - x_i'\beta)^2$; $\hat\beta_{WLS} = (X'WX)^{-1}X'WY$.
- Feasible GLS: estimate variance structure (e.g., AR(1), groupwise heteroskedasticity) and apply GLS. In practice, robust SEs are often preferred unless the structure is well-specified.

---

## Panels, fixed effects, and DiD

- Entity/time fixed effects (within estimator) are OLS on demeaned data:
  - With entity FE: regress $Y - \bar Y_i$ on $X - \bar X_i$ to get FE coefficients.
  - TWFE (entity + time FE) underlies canonical DiD:
    - Beware staggered adoption heterogeneity; prefer [[Sun–Abraham estimator]] / [[Callaway–Sant’Anna estimator]] for robust DiD.
- Inference: cluster by entity (and/or time) as appropriate; see [[clustered standard errors]].

---

## Diagnostics and specification

> [!check]
> - [ ] Residual plots vs fitted; heteroskedasticity tests (Breusch–Pagan/White)  
> - [ ] Serial correlation: ACF/Ljung–Box (time series), use HAC if needed  
> - [ ] Multicollinearity: VIF/condition number (inflates SEs; may use [[regularization]] if prediction is goal)  
> - [ ] Outliers/leverage: hat values, Cook’s D; robust regression for sensitivity  
> - [ ] Functional form: Ramsey RESET; add interactions/splines where theory suggests  
> - [ ] Goodness-of-fit: $R^2$, adjusted $R^2$ (interpret with caution); predictive metrics via CV

Omitted-variable bias and post-treatment conditioning: avoid [[bad controls]] and [[leakage]]; for causal interpretation, ensure identification via design or exogeneity.

---

## Relation to other frameworks

- Gaussian [[Maximum Likelihood Estimation (MLE)|MLE]] ≡ OLS; with non-Gaussian outcomes use [[Generalized Linear Model (GLM)|GLM]].
- [[Generalized Method of Moments (GMM)|GMM]]: OLS FOC $X'(Y-X\beta)=0$ are moment conditions; efficient GMM can improve with heteroskedasticity.
- [[regularization]]: ridge/lasso shrinkage when p is large or multicollinearity is severe (interpretation changes).
- [[Bayesian econometrics]]: priors on β,σ define posterior; uncertainties via [[Markov Chain Monte Carlo (MCMC)|MCMC]].

---

## Code snippets

> [!example] R: OLS + robust/cluster/HAC SEs

```r
# OLS
fit <- lm(Y ~ X1 + X2, data = df)
summary(fit)  # model-based SEs

# Robust (HC1)
library(sandwich); library(lmtest)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))

# Cluster-robust (CR2)
library(clubSandwich)
coef_test(fit, vcov = vcovCR(fit, cluster = df$cluster_id, type = "CR2"), test = "Satterthwaite")

# Newey–West HAC (time series)
library(lmtest); library(sandwich)
coeftest(fit, vcov = NeweyWest(fit, lag = 4, prewhite = FALSE, adjust = TRUE))
```

> [!example] Python: statsmodels OLS + robust/cluster/HAC

```python
import statsmodels.formula.api as smf

res = smf.ols('Y ~ X1 + X2', data=df).fit()
print(res.summary())

# Robust HC1
res_hc = smf.ols('Y ~ X1 + X2', data=df).fit(cov_type='HC1')
print(res_hc.summary())

# Clustered by group
res_cl = smf.ols('Y ~ X1 + X2', data=df).fit(cov_type='cluster',
                                            cov_kwds={'groups': df['cluster_id']})
print(res_cl.summary())

# Newey–West HAC
res_hac = smf.ols('Y ~ X1 + X2', data=df).fit(cov_type='HAC',
                                             cov_kwds={'maxlags': 4})
print(res_hac.summary())
```

> [!example] Stata: regress + robust/cluster

```stata
* OLS
reg Y X1 X2

* Robust HC
reg Y X1 X2, vce(robust)

* Clustered
reg Y X1 X2, vce(cluster cluster_id)

* HAC (newey)
newey Y X1 X2, lag(4)
```

> [!example] R: Fixed effects (within) with fixest

```r
library(fixest)
fe <- feols(Y ~ X1 + X2 | id + time, cluster = ~ id, data = df)
etable(fe)
```

> [!example] R: Weighted least squares

```r
wls <- lm(Y ~ X1 + X2, data = df, weights = w)  # known weights
coeftest(wls, vcov = vcovHC(wls, type = "HC1"))
```

---

## Hypothesis testing and CIs

- Single coefficient: t-test $t = \hat\beta_j / \mathrm{se}(\hat\beta_j)$.
- Joint restrictions $R\beta=r$: Wald/F-test (see [[Wald, LM, and LR tests]]).
- Confidence intervals: $\hat\beta_j \pm t_{N-k,1-\alpha/2}\cdot \mathrm{se}(\hat\beta_j)$ with appropriate SE (robust/cluster/HAC as needed).

---

## Practical guidance

> [!check]
> - [ ] Align inference with data structure: robust/cluster/HAC/spatial SEs  
> - [ ] Report number of clusters and apply [[few-cluster corrections]] / [[wild cluster bootstrap]] if G small  
> - [ ] Avoid post-treatment variables ([[bad controls]]/[[leakage]]); motivate exogeneity or use IV/DiD/RD  
> - [ ] For panels/DiD, prefer modern estimators when staggered adoption with heterogeneity is present  
> - [ ] Scale/center predictors for numerical stability; consider interactions/splines where theory supports  
> - [ ] Provide diagnostics (heteroskedasticity, leverage) and sensitivity analyses

> [!warning] Pitfalls
> - Using i.i.d. SEs in clustered/serially correlated data  
> - Overinterpreting $R^2$ and significance without economic magnitude  
> - Multicollinearity inflating SEs; remedy is not dropping theoretically important variables blindly  
> - Causal claims without design/identification  
> - Ignoring Moulton problem (group-level regressors with individual outcomes—cluster at group; see [[Moulton problem]])

---

## Reporting essentials

- Specification: dependent and regressors, fixed effects (if any)
- Estimation details: sample, weights (if WLS), FE structure
- Inference: SE type (model-based/robust/cluster/HAC), clustering level, small-sample corrections
- Results: coefficients with CIs; marginal effects if appropriate
- Diagnostics: omitted variable discussion, heteroskedasticity tests, leverage/outliers, RESET/functional form
- Sensitivity: alternative SEs (robust vs cluster), subsamples, functional forms

---

## Related notes

- Estimation frameworks: [[Generalized Linear Model (GLM)|GLM]] · [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Generalized Method of Moments (GMM)|GMM]]
- Robust inference: [[clustered standard errors]] · [[few-cluster corrections]] · [[wild cluster bootstrap]] · [[Newey–West]] · [[Conley standard errors]]
- Causal designs: [[Difference-in-Differences (DiD)]] · [[two-way fixed effects]] · [[Sun–Abraham estimator]] · [[Callaway–Sant’Anna estimator]] · [[Regression Discontinuity Design (RDD)]] · [[Instrumental Variables (IV)]] · [[weak instruments]]
- Modeling hygiene: [[bad controls]] · [[leakage]] · [[regularization]] · [[Bayesian econometrics]]  
- Time/panels: [[Time Series (MOC)]] · [[Moulton problem]]

---

## References

- Greene, Econometric Analysis (OLS theory, diagnostics)
- Wooldridge, Introductory & Advanced Econometrics (robust/cluster/HAC; panels)
- Angrist & Pischke, Mostly Harmless Econometrics (causal OLS, FE/TWFE)
- Davidson & MacKinnon (hypothesis testing; robust inference)

---