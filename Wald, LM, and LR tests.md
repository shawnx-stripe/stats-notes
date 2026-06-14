---
title: Wald, LM, and LR tests
aliases: [Wald/LM/LR tests, Wald test, Lagrange Multiplier test, Score test, Likelihood Ratio test, LR test]
tags: [econometrics, statistics, inference, hypothesis-testing, wald, score, lm, likelihood-ratio, robust, clustering]
updated: 2025-09-17
---

# Wald, LM, and LR tests

> [!summary] Quick definition
> Wald, Lagrange Multiplier (LM/Score), and Likelihood Ratio (LR) tests are the three classical large-sample tests for (joint) hypotheses in parametric and semi-parametric models.
> - Wald: test using unrestricted (full) model estimates and their covariance.
> - LM/Score: test using restricted (null) model and score/Information at the null.
> - LR: test based on the log-likelihood difference between unrestricted and restricted models.
> Under regularity and correct specification, all three are asymptotically equivalent (same local power), but they differ in implementation and small-sample behavior.

Use for: linear/nonlinear restrictions, joint tests (e.g., event-study pre-leads), comparisons of nested models, and specification checks.

---

## Setup and notation

- Parameter vector θ ∈ ℝ^k; null H0: r(θ) = 0 with q restrictions (e.g., Rθ = r).
- Unrestricted MLE/M-estimator: θ̂ (maximize/estimate without constraints).
- Restricted estimator under H0: θ̃ (maximize with constraints).
- Sample size n; robust covariance V̂ (sandwich), possibly [[clustered standard errors]] or HAC.
- Log-likelihood ℓ(θ) for LR tests (exact LR requires likelihood-based estimation).

---

## Definitions (copy-ready)

### Wald test (unrestricted estimate + covariance)
For linear restrictions Rθ = r (q×k matrix R, vector r):
$$
W = (R\hat\theta - r)^\top\,[R\,\widehat{\mathrm{Var}}(\hat\theta)\,R^\top]^{-1}\,(R\hat\theta - r)
\ \ \overset{H_0}{\sim}\ \chi^2_q.
$$
- One-parameter case reduces to squared t-statistic.
- Use robust/cluster/HAC covariance consistent with your estimator/design.

### LM / Score test (restricted fit only)
Let S(θ) = ∂ℓ(θ)/∂θ be the score; 𝐼(θ) the expected information.
Evaluate at restricted θ̃:
$$
LM = S(\tilde\theta)^\top\, \widehat{I}(\tilde\theta)^{-1}\, S(\tilde\theta)
\ \ \overset{H_0}{\sim}\ \chi^2_q.
$$
- Requires only the null (restricted) fit; handy when unrestricted model is hard to estimate.
- For quasi-/GMM settings, use the appropriate score/weighting analog.

### Likelihood Ratio test (two likelihoods)
$$
LR = 2\big[\ell(\hat\theta)-\ell(\tilde\theta)\big]
\ \ \overset{H_0}{\sim}\ \chi^2_q.
$$
- Needs a well-defined likelihood (ML). For quasi-ML, LR may be less reliable; prefer Wald/LM.

> [!note] Asymptotic equivalence
> Under correct specification and regularity, Wald ≈ LM ≈ LR for large n. In small samples:  
> - Wald may be sensitive to nuisance scaling;  
> - LM favors the null (conservative) when unrestricted fit is unstable;  
> - LR often performs well with correctly specified likelihood.

---

## When to use which

- Unrestricted model is easy/robust → Wald (with robust/clustered V̂).
- Unrestricted model is hard/unstable, but restricted is easy → LM/Score.
- Exact ML likelihood available and both fits are stable → LR (often good finite-sample power).
- GMM/IV settings → Wald/score analogs via robust (sandwich) and J-tests; LR not directly applicable.

---

## Robust/clustered/HAC versions

- Always align the variance with the sampling scheme:
  - Heteroskedasticity: HC/White sandwich.
  - Clustered data: cluster-robust V̂; apply [[few-cluster corrections]] or [[wild cluster bootstrap]] when G is small.
  - Time dependence: HAC (e.g., [[Newey–West]]).
- For joint tests (e.g., many coefficients): use the χ² form with robust V̂; or use an F-form with small-sample corrections where available.

---

## Special topics

- Joint pre-trend tests (event study): Wald/χ² joint test that all pre-treatment coefficients = 0.
- Nonlinear restrictions r(θ)=0: linearize or use delta method; many packages support nonlinear Wald tests.
- IV/weak instruments: standard Wald tests on 2SLS can be invalid with weak IV; prefer weak-IV-robust tests (e.g., [[Anderson–Rubin|Anderson–Rubin test]], Kleibergen’s K, conditional LR).
- Non-nested models: LR is not valid; use Vuong tests (with caution) or information criteria.

---

## Code snippets

> [!example] R: Wald (linear restrictions) with robust/clustered SEs

```r
library(sandwich); library(lmtest); library(clubSandwich)
fit <- lm(Y ~ X1 + X2 + X3, data = df)

# Robust Wald test: H0: X2 = X3 = 0
R <- rbind(c(0,0,1,0),  # Intercept, X1, X2, X3 -> adjust to your order
           c(0,0,0,1))
co <- vcovHC(fit, type = "HC1")
waldtest(fit, vcov = co, R = R)

# Cluster-robust Wald (clusters in df$cluster)
co_cr2 <- vcovCR(fit, cluster = df$cluster, type = "CR2")
W <- linearHypothesis(fit, c("X2 = 0", "X3 = 0"), vcov = co_cr2, test = "Chisq")
W
```

> [!example] R: LR and Score (GLM example)

```r
fit_full <- glm(Y ~ X1 + X2 + X3, family = binomial, data = df)
fit_rest <- glm(Y ~ X1, family = binomial, data = df)

# LR test
anova(fit_rest, fit_full, test = "LRT")

# Score/LM test (R's anova on single model with test="Rao")
anova(fit_rest, test = "Rao")   # Rao's score test
```

> [!example] Stata: Wald/LR/Score

```stata
* OLS with robust Wald test of joint restrictions
reg Y X1 X2 X3, vce(robust)
test X2 X3   // robust Wald χ2

* Cluster-robust
reg Y X1 X2 X3, vce(cluster cluster_id)
test X2 X3

* GLM LR vs Score
glm Y X1 X2 X3, family(binomial) link(logit)
est store full
glm Y X1, family(binomial) link(logit)
est store rest
lrtest rest full    // LR test
estat gof, rao      // Rao's score test (if supported)
```

> [!example] Python: Wald with robust/clustered SEs (statsmodels)

```python
import statsmodels.formula.api as smf
from statsmodels.stats.contrast import LinearConstraint

res = smf.ols('Y ~ X1 + X2 + X3', data=df).fit(cov_type='HC1')
# Wald test H0: X2 = X3 = 0
LC = LinearConstraint(res, R=['X2=0','X3=0'])
print(LC.wald_test())  # reports chi2 and p

# Clustered SEs
res_cl = smf.ols('Y ~ X1 + X2 + X3', data=df).fit(cov_type='cluster', cov_kwds={'groups': df['cluster']})
LC_cl = LinearConstraint(res_cl, R=['X2=0','X3=0'])
print(LC_cl.wald_test())
```

> [!example] Event-study pre-trend joint test (R/fixest)

```r
library(fixest)
es <- feols(Y ~ sunab(G,time) | id + time, cluster = ~ id, data = df)
# Joint test of all pre-treatment leads = 0
wald(es, keep = "sunab\\(G, time\\)::[-]")  # match negative k terms
```

---

## Interpretation and reporting

- State the hypothesis clearly (e.g., H0: β2 = β3 = 0).
- Report the test type (Wald/LM/LR), degrees of freedom q, statistic (χ² or F), and p-value.
- Report the covariance/inference choice (robust/cluster/HAC) and clustering level; mention small-sample corrections if used (CR2/CR3; [[wild cluster bootstrap]] for p-values with few clusters).
- For LR, report log-likelihoods and that the models are nested.
- For event-study/pre-trend tests, report the joint test and show coefficient plots with CIs.

---

## Good practice and caveats

> [!check]
> - [ ] Align the inference method with your design (clustered, HAC, robust)  
> - [ ] Use joint tests for families (e.g., pre-leads) rather than fishing individual p-values  
> - [ ] In few-cluster settings, complement Wald with [[wild cluster bootstrap]] or [[randomization inference]]  
> - [ ] LR requires proper likelihood; do not use LR for quasi-ML/GMM indiscriminately  
> - [ ] With weak IV, avoid naive Wald tests; use [[Anderson–Rubin|Anderson–Rubin test]] and weak-IV-robust methods

> [!warning] Pitfalls
> - Testing after model selection without accounting for selection (post-selection inference)  
> - Mis-specified covariance (e.g., iid when clustering is needed)  
> - Non-nested models with LR tests (invalid)  
> - Using χ² critical values in very small samples; prefer small-sample corrections or resampling

---

## Related notes

- [[clustered standard errors]] · [[few-cluster corrections]] · [[wild cluster bootstrap]] · [[randomization inference]]  
- [[Newey–West]] · [[Conley standard errors]]  
- [[Anderson–Rubin|Anderson–Rubin test]] · [[weak instruments]] · [[Instrumental Variables (IV)]]  
- [[event study]] · [[multiple testing control]] · [[False Discovery Rate (FDR)|FDR]]

---