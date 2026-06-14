---
title: Nonlinear Least Squares (NLS)
aliases: [NLS, nonlinear least squares, nonlinear regression, Gauss–Newton, Levenberg–Marquardt, NL-WLS]
tags: [econometrics, estimation, nonlinear, least-squares, gauss-newton, optimization, inference]
updated: 2025-09-17
---

# Nonlinear Least Squares (NLS)

> [!summary] Quick definition
> Nonlinear least squares (NLS) estimates parameters θ of a nonlinear mean function f(x; θ) by minimizing the sum of squared residuals:
> $$
> \hat\theta = \arg\min_\theta S(\theta),\quad S(\theta)=\sum_{i=1}^N r_i(\theta)^2,\ \ r_i(\theta)=y_i-f(x_i;\theta).
> $$
> Under correct specification and homoskedastic iid errors, NLS is consistent and asymptotically normal; inference uses the Jacobian and a (robust/cluster/HAC) sandwich covariance. With normal errors, NLS coincides with Gaussian [[Maximum Likelihood Estimation (MLE)|MLE]]; more generally it is a special case of [[Generalized Method of Moments (GMM)|GMM]] (the FOC J'(θ)r(θ)=0 are moment conditions).

- Use for: nonlinear mean relationships (e.g., CES, logistic growth, Michaelis–Menten), nonlinear demand/supply links, production/engines, and when linearization would distort inference.
- Related: [[Maximum Likelihood Estimation (MLE)|MLE]] (normal errors), [[Generalized Method of Moments (GMM)|GMM]] (moment view), [[regularization]] (penalized NLS), [[clustered standard errors]], [[Newey–West]], [[Conley standard errors]].

---

## Model, Jacobian, and first-order conditions

- Mean model: $E[Y|X=x]=f(x;\theta)$, with $f$ nonlinear in θ.
- Residuals: $r(\theta) = y - f(X;\theta)$ (N×1).
- Jacobian (N×k): $J(\theta)=\partial f(X;\theta)/\partial\theta'$ with rows $J_i(\theta)=\partial f(x_i;\theta)/\partial\theta'$.
- FOC (Gauss–Newton normal equations):
$$
\nabla_\theta S(\theta) = -2 J(\theta)' r(\theta)=0 \quad \Rightarrow \quad J(\hat\theta)' r(\hat\theta)=0.
$$

Gauss–Newton step (one iteration):
$$
\hat\theta_{t+1} = \hat\theta_t + \big(J'J\big)^{-1} J' r,
$$
and Levenberg–Marquardt (LM) adds a damping term: $(J'J+\lambda I)^{-1} J'r$ to improve robustness.

---

## Asymptotic inference

Under standard regularity and homoskedastic iid errors with variance σ²:

- Asymptotic covariance (model-based):
$$
\widehat{\mathrm{Var}}(\hat\theta) = \hat\sigma^2\,(J'J)^{-1},\quad \hat\sigma^2=\frac{S(\hat\theta)}{N-k}.
$$

Robust (Eicker–White/HC) sandwich covariance:
$$
\widehat{\mathrm{Var}}_{HC}(\hat\theta) = (J'J)^{-1}\,J'\,\widehat\Omega\,J\,(J'J)^{-1},
$$
with $\widehat\Omega=\mathrm{diag}(r_i^2)$ for HC0; use HC1/HC2/HC3 variants analogously.

- Cluster-robust: $\widehat\Omega = \sum_g r_g r_g'$, where $r_g$ stacks residuals in cluster g and premultiply/postmultiply by the cluster Jacobians $J_g$ (see [[clustered standard errors]] and [[few-cluster corrections]]/[[wild cluster bootstrap]] if clusters are few).
- HAC (time series): replace Ω by HAC estimator (e.g., [[Newey–West]]) using $J_t$ and residuals; spatial: [[Conley standard errors]].

Wald tests for parameter restrictions use these covariances (see [[Wald, LM, and LR tests]]). With normal errors, LR tests via SSE differences are equivalent to likelihood-based LR.

---

## Weighted NLS and heteroskedasticity

If $\mathrm{Var}(\varepsilon_i)=\sigma^2 / w_i$ known up to weights, minimize
$$
S_W(\theta)=\sum_i w_i\,r_i(\theta)^2,
$$
with Jacobian replaced by $\tilde J=W^{1/2}J$ and residuals by $\tilde r=W^{1/2}r$. This yields feasible GLS for known variance function. If heteroskedasticity is unknown, prefer robust covariances.

---

## Identification, starting values, and optimization

- Identification: parameters should be uniquely determined; avoid parameter collinearity (Jacobian rank). Check for flat regions/near-singular $J'J$.
- Starting values: essential to avoid local minima; use transformations, linearized approximations, grid search, or domain knowledge.
- Constraints: enforce via reparameterization (e.g., positivity with exponentials) or bound-constrained solvers; ensure differentiability for Gauss–Newton/HMC.
- Scaling: standardize inputs/outputs or rescale parameters to improve conditioning.

> [!warning] Pitfalls
> - Poor starts → local minima; flat Jacobian → non-identification.
> - Ignoring heteroskedasticity/autocorrelation; use robust/HAC/cluster-robust covariances.
> - Overparameterization; consider [[regularization]] or simpler parameterizations.

---

## Relation to MLE and GMM

- With $\varepsilon_i\sim\mathcal{N}(0,\sigma^2)$ iid, NLS ≡ Gaussian [[Maximum Likelihood Estimation (MLE)|MLE]]; SSE-based LR/Wald tests align with likelihood tests.
- GMM perspective: FOC $J' r = 0$ are moments. Efficient GMM reweights moments when errors are heteroskedastic to improve efficiency relative to plain NLS.

---

## Prediction, marginal effects, and delta method

- Fit $\hat f(x)$; prediction intervals via parametric bootstrap or delta method.
- For a function $g(\theta)$ (e.g., elasticity, $g_\theta=\partial f/\partial x\cdot \partial x/\partial\theta$), use delta method with $\widehat{\mathrm{Var}}(g)\approx G\,\widehat{\mathrm{Var}}(\hat\theta)\,G'$, $G=\partial g/\partial\theta'$ (see [[Hypothesis testing]] for Wald CIs).

---

## Examples of NLS models

- Exponential growth: $y=a\exp(bx)+\varepsilon$
- Logistic/S-curve: $y = \frac{L}{1+\exp(-k(x-x_0))} + \varepsilon$
- CES production: $y=A \big(\delta K^{\rho}+(1-\delta)L^{\rho}\big)^{1/\rho}$ (nonlinear in parameters)
- Michaelis–Menten: $y=\frac{V_{\max}x}{K_M+x}+\varepsilon$

(Translog is linear in logs → OLS; choose NLS when parameters enter nonlinearly.)

---

## Code snippets

> [!example] R: nls and robust SEs

```r
# Exponential model: y = a * exp(b*x)
fit <- nls(y ~ a * exp(b * x), data = df, start = list(a = 1, b = 0.1))
summary(fit)  # model-based SEs

# More robust Levenberg–Marquardt (minpack.lm)
# install.packages("minpack.lm")
library(minpack.lm)
fit_lm <- nlsLM(y ~ a * exp(b * x), data = df, start = list(a = 1, b = 0.1))

# Robust (HC) variance via sandwich
library(sandwich); library(lmtest)
# Construct Jacobian at estimates
a_hat <- coef(fit_lm)["a"]; b_hat <- coef(fit_lm)["b"]
J <- cbind(exp(b_hat * df$x), a_hat * df$x * exp(b_hat * df$x))
resid <- df$y - a_hat * exp(b_hat * df$x)
V_hc <- solve(t(J)%*%J) %*% t(J) %*% diag(resid^2) %*% J %*% solve(t(J)%*%J)
se_hc <- sqrt(diag(V_hc))
se_hc
```

> [!example] Python: scipy curve_fit (LM) + robust covariance (sketch)

```python
import numpy as np
from scipy.optimize import curve_fit

def f(x, a, b):
    return a * np.exp(b * x)

popt, pcov = curve_fit(f, df['x'].values, df['y'].values, p0=(1.0, 0.1), method='trf')  # or 'lm'
a_hat, b_hat = popt

# Robust (HC0) covariance (manual)
x = df['x'].values
y_hat = f(x, a_hat, b_hat)
res = df['y'].values - y_hat
J = np.column_stack([np.exp(b_hat * x), a_hat * x * np.exp(b_hat * x)])  # N x 2
XtX_inv = np.linalg.inv(J.T @ J)
V_hc = XtX_inv @ (J.T @ np.diag(res**2) @ J) @ XtX_inv
se_hc = np.sqrt(np.diag(V_hc))
print("params:", popt, "HC0 SE:", se_hc)
```

> [!example] Stata: nl with robust/clustered SEs

```stata
* Exponential NLS
nl (y = {a} * exp({b}*x)), vce(robust)

* Cluster-robust
nl (y = {a} * exp({b}*x)), vce(cluster cluster_id)

* Wald tests for nonlinear hypotheses
testnl _b[a] > 0
```

> [!example] R: CES production function (NLS)

```r
ces_fun <- function(K, L, A, delta, rho) A * (delta*K^rho + (1-delta)*L^rho)^(1/rho)
fit_ces <- nls(y ~ ces_fun(K, L, A, delta, rho),
               data = df, start = list(A=1, delta=0.5, rho=-0.5))
summary(fit_ces)
```

> [!example] R: Delta method for elasticity

```r
library(car)
# Suppose elasticity wrt x at mean xbar: g = b * xbar for exp model
xbar <- mean(df$x)
est <- c(a=a_hat, b=b_hat)
V <- V_hc
deltaMethod(list(est=est, vcov.=V), "b * xbar", parameterNames = c("a","b"))
```

---

## Extensions

- Penalized NLS: add λ‖θ‖² or other penalties (see [[regularization]]).
- Nonlinear fixed effects: large-N panel with nonlinear FE can face incidental parameter issues; prefer random effects/hierarchical Bayes or within transforms when available.
- Nonlinear IV (NLIV): when regressors enter nonlinearly and are endogenous, use [[Generalized Method of Moments (GMM)|GMM]]/control functions/instrumental NLS (requires valid instruments; watch [[weak instruments]]).

---

## Diagnostics and good practice

> [!check]
> - [ ] Residual plots; heteroskedasticity checks; HAC/cluster where needed ([[Newey–West]], [[clustered standard errors]])  
> - [ ] Sensitivity to starting values; multiple restarts; profile the objective for key parameters  
> - [ ] Jacobian conditioning; parameter standard errors stability across robust options  
> - [ ] Outlier influence; consider robust loss functions (Huber) if appropriate (beyond pure NLS)  
> - [ ] Compare to linearized approximations and/or [[Maximum Likelihood Estimation (MLE)|MLE]] if likelihood known  
> - [ ] Document constraints/transformations and scaling

---

## Reporting essentials

- Model $f(x;\theta)$, parameter interpretations, and constraints/transformations
- Estimation algorithm (Gauss–Newton/LM), starting values, convergence criteria, number of iterations
- SSE/RSS, $\hat\sigma^2$, RSE; parameter estimates with SEs (model-based and robust/cluster/HAC as appropriate)
- Inference: Wald tests, CIs; if normal errors, LR tests
- Diagnostics: residual patterns, heteroskedasticity/autocorrelation, sensitivity to starts
- Reproducibility: code, seeds, software versions

---

## Related notes

- Estimators: [[Maximum Likelihood Estimation (MLE)|MLE]] · [[Generalized Method of Moments (GMM)|GMM]] · [[Simulated method of moments]]  
- Inference: [[Wald, LM, and LR tests]] · [[clustered standard errors]] · [[Newey–West]] · [[Conley standard errors]] · [[wild cluster bootstrap]]  
- Modeling: [[regularization]] · [[Bayesian econometrics]] (nonlinear models via [[Markov Chain Monte Carlo (MCMC)|MCMC]])  
- Applications: [[Time Series (MOC)]] (nonlinear dynamics), [[Structural models]]

---

## References

- Bates & Watts, Nonlinear Regression Analysis  
- Seber & Wild, Nonlinear Regression  
- Greene, Econometric Analysis (NLS, Gauss–Newton/LM; inference)  
- More, The Levenberg–Marquardt algorithm (optimization)

---