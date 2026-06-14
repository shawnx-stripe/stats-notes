---
title: Maximum Likelihood Estimation (MLE)
aliases: [MLE, maximum likelihood estimation, likelihood]
tags: [estimation, inference, likelihood, asymptotics, optimization, glm, quasi-mle, sandwich]
updated: 2025-09-21
---

# Maximum Likelihood Estimation (MLE)

> [!summary] Quick definition
> Maximum Likelihood Estimation (MLE) chooses parameters θ to maximize the likelihood of the observed data under a parametric model. Under standard regularity conditions, the MLE is consistent, asymptotically normal and efficient, and supports inference via the score, Fisher information, and [[Wald, LM, and LR tests]].

- Core ingredients:
$$
\begin{aligned}
L_n(\theta) &= \prod_{i=1}^n f(y_i\mid x_i;\theta), \\
\ell_n(\theta) &= \sum_{i=1}^n \log f(y_i\mid x_i;\theta), \\
U_n(\theta) &= \frac{\partial \ell_n(\theta)}{\partial \theta}, \\
I(\theta) &= -\mathbb{E}\!\left[\frac{\partial^2 \ell(\theta)}{\partial\theta\partial\theta'}\right]
\end{aligned}
$$

- Related: [[Generalized Linear Model (GLM)|GLM]], [[Ordinary Least Squares (OLS)|OLS]] as Gaussian MLE, [[Nonlinear Least Squares (NLS)|NLS]], [[regularization]] (penalized likelihood), [[Bayesian econometrics]] (priors + likelihood = posterior).

---

## Setup and notation

- Data: $W_i=(Y_i, X_i)$, $i=1,\dots,n$, usually iid.
- Model: density/pmf $f(y\mid x;\theta)$, $\theta \in \Theta \subset \mathbb{R}^p$.
- Likelihood and log-likelihood:
$$
L_n(\theta) = \prod_{i=1}^n f(Y_i\mid X_i;\theta), \qquad
\ell_n(\theta) = \sum_{i=1}^n \log f(Y_i\mid X_i;\theta)
$$
- MLE:
$$
\hat\theta = \arg\max_{\theta \in \Theta}\, \ell_n(\theta)
$$
- Score and information:
$$
\begin{aligned}
U_n(\theta) &= \frac{\partial \ell_n(\theta)}{\partial \theta} = \sum_{i=1}^n s(W_i;\theta), \\
I(\theta) &= \operatorname{Var}[s(W;\theta)] = -\mathbb{E}\!\left[\frac{\partial^2 \ell(\theta)}{\partial\theta\partial\theta'}\right], \\
J_n(\theta) &= -\frac{\partial^2 \ell_n(\theta)}{\partial\theta\partial\theta'}
\end{aligned}
$$

---

## Properties (regular, correctly specified models)

- Consistency: $\hat\theta \xrightarrow{p} \theta_0$
- Asymptotic normality:
$$
\sqrt{n}(\hat\theta - \theta_0) \;\xrightarrow{d}\; \mathcal{N}\!\left(0,\; I(\theta_0)^{-1}\right)
$$
- Efficiency: attains the Cramér–Rao lower bound in regular parametric families.
- Invariance: if $\psi = g(\theta)$ (smooth, one-to-one), then $\hat\psi = g(\hat\theta)$ is the MLE of $\psi$.

> [!note] Sandwich under misspecification (quasi-MLE)
> If the model is misspecified but the score has zero mean at pseudo-true $\theta^\star$, then
> $$
> \sqrt{n}(\hat\theta - \theta^\star) \;\xrightarrow{d}\; \mathcal{N}\!\left(0,\; H^{-1} S H^{-1}\right),
> $$
> where
> $$
> H = \operatorname*{plim}_{n\to\infty}\left(-\frac{1}{n}\frac{\partial^2 \ell_n(\theta^\star)}{\partial\theta\partial\theta'}\right), \qquad
> S = \operatorname*{plim}_{n\to\infty}\left(\frac{1}{n} U_n(\theta^\star)U_n(\theta^\star)'\right).
> $$
> Use robust (Huber–White) or clustered variants (see [[clustered standard errors]]; [[wild cluster bootstrap]] for few clusters).

---

## Inference toolbox

- Standard errors
  - Model-based: $\operatorname{Var}(\hat\theta) \approx \frac{1}{n} I(\hat\theta)^{-1}$ or $\frac{1}{n} J_n(\hat\theta)^{-1}$ (observed info; often better finite-sample behavior).
  - Robust/sandwich: $\frac{1}{n} H^{-1} S H^{-1}$ (prefer when misspecification or heteroskedasticity is plausible).
- Tests and intervals
  - Wald, Score (LM), and Likelihood Ratio: see [[Wald, LM, and LR tests]].
  - CIs: $\hat\theta_j \pm z_{\alpha/2}\cdot \operatorname{SE}(\hat\theta_j)$; or profile-likelihood CIs (see [[profile likelihood]]).
- Prediction and transforms
  - Use invariance for $g(\theta)$; for nonlinear $g$, use the delta method or parametric bootstrap.

---

## When to use MLE

- Well-specified parametric models (e.g., GLMs, survival, limited dependent variables) with likelihood-based inference.
- Model comparison/selection via information criteria (see [[AIC]], [[BIC]]) or as input to Bayesian analysis ([[priors]]).
- Large-sample settings or quasi-MLE with robust SEs.

---

## Links to common models

- Gaussian linear model: [[Ordinary Least Squares (OLS)|OLS]] is MLE under Normal homoskedastic errors.
- [[Generalized Linear Model (GLM)|GLM]]: canonical link models maximize exponential-family likelihoods (logistic, Poisson, etc.).
- [[Nonlinear Least Squares (NLS)|NLS]]: equals Gaussian MLE when only the mean is modeled; otherwise NLS is quasi-MLE.
- Penalized MLE: maximize $\ell(\theta) - \lambda P(\theta)$ (ridge/lasso; see [[regularization]]).

---

## Optimization and implementation

> [!tip] Practical algorithm choices
> - Newton–Raphson: $\theta_{k+1} = \theta_k - H(\theta_k)^{-1} U(\theta_k)$
> - Fisher scoring: replace $H$ with $-\,\hat I(\theta_k)$ (expected information)
> - Quasi-Newton (BFGS/L-BFGS): robust, avoids explicit Hessian
> - Constrained problems: reparameterize or use projected/box-constrained solvers; ensure $\Theta$ is respected

Implementation checklist:
- Scale/standardize features to improve conditioning
- Good starts: method-of-moments, [[Ordinary Least Squares (OLS)|OLS]]/[[Generalized Linear Model (GLM)|GLM]] fits
- Convergence: monitor gradient norm, step size, and monotonic increase of $\ell(\theta)$; guard against divergence
- Numerical stability: log-sum-exp for probabilities; boundary-aware parameterizations (e.g., $\log \sigma$, logit for probabilities)

---

## Diagnostics and model adequacy

- Identification: flat/multi-modal likelihoods; boundary parameters (e.g., zero variance) → nonstandard inference
- Separation in logistic/Poisson: complete/quasi separation → infinite MLE; remedies: penalized likelihood (Firth), priors, or data augmentation
- Residuals and fit: deviance, Pearson residuals, leverage; outliers and overdispersion
- Misspecification: compare robust vs model-based SEs; specification tests; consider quasi-likelihood/alternative families
- Dependence: iid violations (clusters/panels/time series) → use clustered/HAC SEs; see [[Time Series (MOC)]], [[clustered standard errors]]

---

## Worked examples

> [!example] Normal location–scale
> $Y_i \sim \mathcal{N}(\mu, \sigma^2)$.
> $$
> \ell(\mu,\sigma^2) = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n (Y_i-\mu)^2
> $$
> MLEs:
> $$
> \hat\mu = \bar{Y}, \qquad
> \hat\sigma^2 = \frac{1}{n}\sum_{i=1}^n (Y_i-\bar{Y})^2
> $$
> (note: MLE uses $1/n$, not $1/(n-1)$).

> [!example] Logistic regression (binary GLM)
> $p_i = \Pr(Y_i=1\mid X_i) = \operatorname{logit}^{-1}(X_i'\beta)$.
> $$
> \ell(\beta)=\sum_{i=1}^n \left[y_i \log p_i + (1-y_i)\log(1-p_i)\right], \quad
> U(\beta)=\sum_{i=1}^n X_i (y_i-p_i), \quad
> J(\beta)=\sum_{i=1}^n X_i X_i' p_i(1-p_i)
> $$
> IRLS/Fisher scoring update:
> $$
> \beta_{k+1} = \beta_k + \left(X' W_k X\right)^{-1} X' (y - p_k),
> \quad W_k = \operatorname{diag}\big(p_k \odot (1-p_k)\big)
> $$

---

## Non-regular and advanced topics

- Non-regular cases: boundary parameters, weak identification, mixtures/latent-variable models (irregular Fisher info) → nonstandard LR/Wald limits; use bootstrap or specialized theory.
- EM algorithm for latent variables: maximize expected complete-data log-likelihood ([[EM algorithm]]).
- Profile likelihood: inference on subset $\psi$ with nuisance $\lambda$ profiled out; often better finite-sample behavior.
- Composite likelihood: use parts/margins when full likelihood is intractable; adjust SEs.
- Information equality: $\operatorname{Var}(\text{score})=I(\theta)$ under correct specification; violations indicate misspecification.

---

## Common pitfalls

> [!warning]
> - Using model-based SEs under misspecification; prefer robust/sandwich when unsure  
> - Ignoring identification/separation issues; infinite or unstable estimates  
> - Trusting optimizer convergence without checking gradients/curvature  
> - Using post-treatment variables as predictors (model [[leakage]])  
> - Small-sample overconfidence; prefer profile likelihood or bootstrap when feasible

---

## Reporting essentials

- Model $f(y\mid x;\theta)$, link/variance (for GLM), constraints
- Optimization: algorithm, starts, convergence criteria, any issues
- Estimates with SEs and CI method (model-based vs robust; clustered if used)
- Tests used: [[Wald, LM, and LR tests]], profile-likelihood if applicable
- Diagnostics: fit measures, residuals, misspecification checks
- Reproducibility: data filters, software versions, seeds

---

## Related notes

- Modeling: [[Generalized Linear Model (GLM)|GLM]] · [[Ordinary Least Squares (OLS)|OLS]] · [[Nonlinear Least Squares (NLS)|NLS]] · [[regularization]] · [[Bayesian econometrics]] · [[priors]]
- Inference: [[Wald, LM, and LR tests]] · [[Hypothesis testing]] · [[clustered standard errors]] · [[wild cluster bootstrap]]
- Robust/semiparametric: [[double machine learning]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- Design context: [[Experimental Design (MOC)]] · [[Causal Inference (MOC)]]

---

## References

- Fisher (1922, 1925) foundations of likelihood, information, scoring
- Cramér (1946); Rao (1945): Cramér–Rao bounds
- Wald (1949); Rao (1948); Wilks (1938): classical tests
- Huber (1967); White (1982): M‑estimation and robust/sandwich variance (QMLE)
- McCullagh & Nelder (1989): GLMs and likelihood
- Efron & Hinkley (1978): observed Fisher information and accuracy

---
