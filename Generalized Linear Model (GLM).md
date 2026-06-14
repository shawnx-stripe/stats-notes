---
title: Generalized Linear Model (GLM)
aliases: [GLM, generalized linear model, generalized linear models, IRLS, quasi-likelihood]
tags: [econometrics, estimation, glm, likelihood, quasi-mle, inference, robust, count, binary, link, variance]
updated: 2025-09-17
---

# Generalized Linear Model (GLM)

> [!summary] Quick definition
> Generalized Linear Models (GLMs) model the conditional mean of a response via a link function and an exponential-family likelihood:
> - Systematic component: η = Xβ
> - Link: g(μ) = η, where μ = E[Y|X]
> - Variance: Var(Y|X) = V(μ)·φ
> Estimation typically uses [[Maximum Likelihood Estimation (MLE)|MLE]] via Iteratively Reweighted Least Squares (IRLS). Inference can use model-based or robust (sandwich) SEs; cluster/HAC/spatial variants apply when dependence exists.

- Common GLMs: Bernoulli–logit/probit (binary), Binomial–logit (proportions), Poisson–log (counts), Gamma–log (positive skew), Gaussian–identity (OLS as a GLM).
- See also: [[regularization]] (penalized GLMs), Bayesian GLMs (priors/[[Bayesian econometrics]]; fit via [[Markov Chain Monte Carlo (MCMC)|MCMC]]).

---

## Anatomy

- Exponential-family log-likelihood (single obs):
$$
\log f(y|\theta,\phi)=\frac{y\theta - b(\theta)}{a(\phi)} + c(y,\phi),
$$
with canonical parameter θ and scale φ. Mean and variance follow:
$$
\mu = b'(\theta), \quad \mathrm{Var}(Y|X) = b''(\theta)\,a(\phi) = V(\mu)\,\phi.
$$

- Link function: g(μ) = Xβ (canonical link if g(μ)=θ).
  - Canonical links: logit for Bernoulli, log for Poisson and Gamma, identity for Gaussian.
  - Noncanonical but common: probit for binary, cloglog for extremes, inverse link for Gamma.

---

## Estimation (IRLS)

- IRLS solves weighted least squares updates for β:
  1) Working response: z = η + (y − μ)·(dη/dμ)
  2) Weights: W = (dμ/dη)^2 / Var(Y|X) = 1 / [V(μ)·(dη/dμ)^2]
  3) Update: β ← argmin (z − Xβ)' W (z − Xβ) (i.e., weighted LS)
- Under correct specification, the IRLS MLE is consistent, asymptotically normal, and efficient. With misspecification, use QMLE (quasi-likelihood) and robust SEs.

See: [[Maximum Likelihood Estimation (MLE)|MLE]] for likelihood theory; [[Generalized Method of Moments (GMM)|GMM]] for moment-based perspective.

---

## Inference

- Model-based covariance (Fisher information):
$$
\widehat{\mathrm{Var}}_{\text{MB}}(\hat\beta) = (X' \widehat{W} X)^{-1}.
$$
- Robust/“sandwich” covariance (QMLE):
$$
\widehat{\mathrm{Var}}_{\text{rob}}(\hat\beta) = (X' \widehat{W} X)^{-1} \left( \sum_i s_i s_i' \right) (X' \widehat{W} X)^{-1},
$$
where s_i are score contributions. Use:
  - [[clustered standard errors]] if observations are clustered (panel/geo); apply [[few-cluster corrections]] / [[wild cluster bootstrap]] if clusters are few.
  - [[Newey–West]] for serial correlation (time series).
  - [[Conley standard errors]] for spatial dependence.

- Tests: Wald/[[Wald, LM, and LR tests|LM|LR]]; LR relies on the likelihood (nested models, i.i.d.); Wald/Score support robust SEs.

---

## Common GLMs and links

- Gaussian, identity: OLS (Var(Y)=σ²); GLM reduces to linear regression.
- Bernoulli/Binomial:
  - logit link: log(μ/(1−μ)) = Xβ (canonical)
  - probit: Φ^{-1}(μ) = Xβ (noncanonical—still GLM)
- Poisson (counts):
  - log link: log μ = Xβ (canonical); Var(Y)=μ → overdispersion common.
  - Quasi-Poisson or Negative Binomial handle overdispersion; NB is ML outside strict GLM unless dispersion is treated appropriately.
- Gamma (positive continuous, skewed):
  - log or inverse links; Var(Y)=φμ².

> [!warning] Over/under-dispersion:
> For Poisson, if Var(Y) ≠ μ, use robust SEs (QMLE), quasi-Poisson, or NB. For binomial data, consider quasi-binomial if Var(Y) deviates from n·p·(1−p).

---

## Marginal effects and interpretation

- Link scale vs mean scale:
  - Coefficients β live on g(μ). To interpret on μ-scale, compute ∂μ/∂x_j = g'(μ)^{-1} β_j.
  - For logit, marginal effect: ∂μ/∂x_j = μ(1−μ) β_j.
  - For Poisson with log link, ∂μ/∂x_j = μ β_j (semi-elasticity); exp(β_j) ≈ multiplicative effect on μ.

- Average marginal effects: average ∂μ/∂x_j across observations.

---

## Robustness and QMLE

- If the conditional mean is correctly specified but the variance is misspecified, GLM QMLE β̂ is consistent for the pseudo-true parameter; use robust/cluster/HAC SEs for valid inference.

- With separation (binary):
  - Logit MLE may diverge under complete/quasi-complete separation; use penalized likelihood (Firth), [[regularization]] (ridge), or Bayesian priors (e.g., Normal(0,2) on scaled X).

---

## Regularization & Bayesian GLM

- Penalized GLM (MAP/Penalized MLE): add penalties [[regularization]]:
  - Ridge/Lasso/Elastic-net (e.g., `glmnet`).
  - Group penalties for categorical expansions.
- Bayesian GLM:
  - Place [[priors]] on β, σ/φ; compute via [[Markov Chain Monte Carlo (MCMC)|MCMC]] or variational inference.
  - Weakly informative priors stabilize small-sample / separability issues. See [[Bayesian econometrics]].

---

## Dependencies and panels

- Clustered panels: use [[clustered standard errors]], cluster FE, or GLMM (random effects) where appropriate.
- Time series GLMs: Poisson/NegBin for counts; account for serial correlation in variance (HAC or state-space/INGARCH), see [[Time Series (MOC)]].
- Spatial GLMs: use [[Conley standard errors]] or spatial random effects/INLA.

---

## Model selection and diagnostics

> [!check]
> - [ ] Link and variance: does g(μ) and V(μ) fit residual patterns?  
> - [ ] Residuals: deviance and Pearson residuals vs fitted; leverage/influence points.  
> - [ ] Overdispersion (counts/binary): test/inspect; switch to quasi/NB or use robust SEs.  
> - [ ] Goodness-of-fit: deviance, AIC/BIC; predictive checks (CV); ROC/PR for binary.  
> - [ ] Misspecification: consider alternative links; add interactions/nonlinearities (splines) with regularization.  
> - [ ] Small-sample/cluster issues: apply [[few-cluster corrections]] / [[wild cluster bootstrap]] when needed.

---

## Code snippets

> [!example] R: glm + robust/clustered SEs

```r
# Logistic regression
m <- glm(y ~ x1 + x2, family = binomial(link = "logit"), data = df)
summary(m)  # model-based SEs

# Robust (HC)
library(sandwich); library(lmtest)
coeftest(m, vcov = vcovHC(m, type = "HC1"))

# Cluster-robust (CR2)
library(clubSandwich)
coef_test(m, vcov = vcovCR(m, cluster = df$cluster_id, type = "CR2"), test = "Satterthwaite")
```

> [!example] Python: statsmodels GLM + robust/cluster

```python
import statsmodels.api as sm
X = sm.add_constant(df[['x1','x2']])
y = df['y']
mod = sm.GLM(y, X, family=sm.families.Binomial(link=sm.families.links.logit()))
res = mod.fit()
print(res.summary())

# Robust cov (HC1)
res_rob = mod.fit(cov_type='HC1')
print(res_rob.summary())

# Cluster-robust
res_cl = mod.fit(cov_type='cluster', cov_kwds={'groups': df['cluster_id']})
print(res_cl.summary())
```

> [!example] Stata: glm and margins

```stata
* Logit GLM
glm y x1 x2, family(binomial) link(logit) vce(robust)

* Clustered
glm y x1 x2, family(binomial) link(logit) vce(cluster cluster_id)

* Marginal effects
margins, dydx(*)   // average marginal effects
```

> [!example] R: Poisson vs NB (overdispersion)

```r
# Poisson
mp <- glm(y ~ x1 + x2, family = poisson(link = "log"), data = df)
# Overdispersion? Compare to NB
library(MASS)
mnb <- MASS::glm.nb(y ~ x1 + x2, data = df)  # ML NB2
AIC(mp, mnb)
```

> [!example] R: Penalized GLM (glmnet)

```r
library(glmnet)
X <- model.matrix(~ 0 + x1 + x2 + x3, data = df)
y <- df$y
cv <- cv.glmnet(X, y, family = "binomial", alpha = 1)   # lasso logit
coef(cv, s = "lambda.1se")
```

---

## Reporting essentials

- Family, link, and rationale (e.g., Poisson–log for counts)
- Estimation method (IRLS/ML), convergence criteria, iterations
- Coefficients with SEs and CIs; specify SE type (model-based vs robust/cluster/HAC) and clustering level
- Marginal effects (average or at means) on the μ-scale
- Overdispersion handling (quasi, NB, robust SEs)
- Diagnostics: residual plots, leverage/influence, goodness-of-fit (AIC/BIC), predictive metrics (ROC/AUC for binary)
- Sensitivity: alternative links/variance functions; penalized variants; Bayesian priors

---

## Related notes

- Estimation & inference: [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Generalized Method of Moments (GMM)|GMM]] · [[Wald, LM, and LR tests]] · [[Hypothesis testing]]  
- Robust covariance: [[clustered standard errors]] · [[few-cluster corrections]] · [[wild cluster bootstrap]] · [[Newey–West]] · [[Conley standard errors]]  
- Modeling choices: [[regularization]] · [[priors]] · [[Bayesian econometrics]] · [[Markov Chain Monte Carlo (MCMC)|MCMC]]  
- Applications: [[AB Testing (MOC)]] (logistic models for conversion), [[Time Series (MOC)]] (count GLMs/INGARCH)

---

## References

- McCullagh & Nelder, Generalized Linear Models  
- Cameron & Trivedi, Regression Analysis of Count Data (Poisson/NB)  
- Hardin & Hilbe, Generalized Linear Models and Extensions  
- Greene, Econometric Analysis (GLMs, QMLE, robust inference)