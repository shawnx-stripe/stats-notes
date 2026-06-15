---
title: Two-Stage Least Squares (2SLS)
aliases:
- 2SLS
- Two stage least squares
- two-stage least squares (2SLS)
- IV-2SLS
- TSLS
- two-stage least squares
tags:
- econometrics
- causal-inference
- instrumental-variables
- estimation
updated: 2025-09-26
---

# Two-Stage Least Squares (2SLS)

> [!summary] Quick definition
> The canonical estimator for linear [[Instrumental Variables (IV)]] models. It projects endogenous regressors onto the space spanned by instruments and exogenous controls (stage 1), then regresses the outcome on these fitted values (stage 2). Consistent when instruments satisfy [[relevance]] and the [[exclusion restriction]].

## Model and notation

- Structural outcome equation (linear):
$$
y = X_1\beta_1 + X_2\beta_2 + u
$$
where:
  - y is n×1 outcome
  - X1 is n×k1 exogenous regressors (included controls)
  - X2 is n×k2 endogenous regressors
  - u is error with E[Z'u]=0

- Instruments:
$$
Z = [\,X_1,\ W\,]
$$
where W (n×m) are excluded instruments; Z is n×L with L=k1+m.

- First-stage (reduced form for endogenous regressors):
$$
X_2 = Z\Pi + V
$$

Assumptions:
- Relevance: rank(Z'X2)=k2 (instruments correlate with X2)
- Exogeneity: E[Z'u]=0 (exclusion + independence conditional on X1)
- Rank condition: L ≥ k1 + k2 and instruments not collinear with included exogenous variables

## The 2SLS estimator

- Projection matrix onto instrument space: P_Z = Z(Z'Z)^{-1}Z'
- Compact formula:
$$
\hat{\beta}^{2SLS} = (X'P_Z X)^{-1} X'P_Z y
$$
with X = [X1 X2]. Intuition: regress y on the part of X that is explainable by Z.

- Practical two-stage steps:
  1) For each column of X2, regress it on Z (i.e., on X1 and W) and save fitted values X̂2.
  2) Regress y on X1 and X̂2 by OLS. Coefficients on X̂2 are 2SLS estimates of β2.

- Just-identified vs over-identified:
  - Just-identified: number of excluded instruments = number of endogenous regressors (m=k2)
  - Over-identified: m>k2 (enables over-ID tests)

## Relationship to other estimators

- [[Wald estimator]]: with a single binary instrument and one endogenous regressor, 2SLS collapses to the Wald ratio ΔY/ΔD.
- [[Generalized Method of Moments (GMM)|GMM]]: 2SLS is GMM with weighting matrix W = (Z'Z)^{-1}. Efficient two-step GMM uses an optimal weighting matrix to account for heteroskedasticity.
- LIML and k-class: [[Limited Information Maximum Likelihood (LIML)|LIML]] (k-class with k=λ̂) is often less biased than 2SLS under [[weak instruments]]/many instruments.

## Standard errors and inference

- Homoskedastic SEs (textbook) are rarely appropriate.
- Robust (Eicker–White) 2SLS variance:
$$
\widehat{V}_{\text{rob}}(\hat{\beta}^{2SLS})
= (X'Z(Z'Z)^{-1}Z'X)^{-1}\, X'Z(Z'Z)^{-1}\, \hat{S}\, (Z'Z)^{-1}Z'X \,(X'Z(Z'Z)^{-1}Z'X)^{-1}
$$
where Ŝ = Z' diag(ê^2) Z (or its clustered/spatial analog). Software will deliver HC/HAC/cluster variants.

- Cluster/spatial dependence: use [[clustered standard errors]] or [[Conley standard errors]]; report number of clusters.

- Tests:
  - Overidentification: Sargan (homoskedastic) or Hansen J (robust) to assess joint instrument exogeneity.
  - Endogeneity: Durbin–Wu–Hausman test compares OLS vs 2SLS; rejects if regressors are endogenous.
  - Weak-IV robust inference: [[Anderson–Rubin|Anderson–Rubin test]] and [[CLR test]] provide valid CIs under weak instruments.

## Diagnostics and weak instruments

- First-stage strength:
  - One endogenous regressor (homoskedastic): first-stage F ≥ 10 (rule of thumb).
  - General/robust: use Kleibergen–Paap rk Wald F; compare to [[Stock–Yogo]] critical values.
  - Report: partial R² of instruments for each endogenous regressor; F-statistics (Cragg–Donald, Kleibergen–Paap).

- Many instruments:
  - Risk: finite-sample bias toward OLS; inflated variance; weak-ID pathologies.
  - Remedies: limit instruments; collapse/group; use LIML/JIVE; regularization (post-lasso instruments in high-dim settings).

- Exclusion restriction:
  - Substantive justification; over-ID tests are not definitive.
  - Include rich X1; assess robustness to alternative instrument sets and windows.

## Interpretation with heterogeneity

- With binary treatment and valid instruments:
  - Just-identified (one Z): 2SLS estimates [[Local Average Treatment Effect (LATE)|LATE]] for compliers.
  - Over-identified (multiple Z): 2SLS recovers a weighted average of instrument-specific LATEs, with weights proportional to each instrument’s covariance with treatment (Angrist–Imbens).
- With continuous D or multiple endogenous regressors: interpret as linear projection parameter; causal interpretation requires stronger structure (e.g., [[Local IV]] or [[marginal treatment effect (MTE)]]).

## Good practice

- Always show first-stage regressions and strength metrics (F, partial R²).
- Report overidentification tests (Sargan/Hansen J) when over-identified.
- Use robust/cluster SEs aligned to assignment level; state number of clusters.
- Pre-specify instrument set; avoid instrument proliferation; justify exclusion.
- Provide weak-IV robust CIs (AR/CLR) when strength is borderline.
- Sensitivity: alternate instrument subsets; bandwidths/windows for policy instruments; falsification tests on placebo outcomes.

## Copy-ready formulas

- 2SLS estimator:
$$
\hat{\beta}^{2SLS} = (X'P_Z X)^{-1} X'P_Z y, \quad P_Z = Z(Z'Z)^{-1}Z'
$$

- Just-identified single endogenous regressor (partition X=[X1 D], Z=[X1 Z1]):
$$
\hat{\beta}_D^{2SLS}
= \frac{(y - X_1\hat{\beta}_1)' \, \hat{D}}{\hat{D}' \hat{D}}, \quad \hat{D} = P_Z D
$$

- Overidentification (Hansen J):
$$
J = n \cdot \hat{g}(\hat{\beta})' \,\hat{W}\, \hat{g}(\hat{\beta}), \quad \hat{g} = \frac{1}{n}Z'(y - X\hat{\beta}),\ \ \hat{W} = (Z' \hat{u}\hat{u}' Z / n)^{-1}
$$
Under H0 (valid instruments), J ~ χ² with df = L − (k1+k2).

- First-stage F (one endogenous regressor):
$$
F = \frac{R^2 / q}{(1-R^2)/(n - k)}, \quad \text{where } q=\text{# excluded instruments}
$$

## Minimal implementations (optional)

R
- AER::ivreg, fixest::feols with iv, ivreg::ivreg
- Example:
```r
library(AER)
fit <- ivreg(y ~ x1 + x2 | x1 + z, data = df)  # x2 endogenous, z excluded IV
summary(fit, diagnostics = TRUE)               # Shows 1st-stage F, Wu-Hausman, Sargan
```

Stata
- ivregress 2sls; ivreg2 (extended diagnostics)
```stata
ivregress 2sls y (x2 = z) x1, vce(cluster clusterid)
estat firststage
estat overid
ivreg2 y (x2 = z) x1, cluster(clusterid) first robust
```

Python
- linearmodels.iv.IV2SLS
```python
from linearmodels.iv import IV2SLS
mod = IV2SLS.from_formula('y ~ 1 + x1 + [x2 ~ z]', data=df)
res = mod.fit(cov_type='robust')
print(res.summary)
```

## Common pitfalls

> [!warning] Avoid these
> - Weak instruments (low F, low partial R²): biased, wide/invalid CIs; use LIML/AR/CLR, strengthen design.
> - Too many instruments: overfit first stage; bias toward OLS; use parsimonious/regularized sets.
> - Mis-specified controls: omit key X1 or include [[bad controls]] (post-treatment).
> - Ignoring clustering when instruments/treatments vary at group level (see [[Moulton problem]]; use [[clustered standard errors]]).
> - Overreliance on over-ID tests to “prove” exclusion; they have low power and test joint validity only.


## Cross-links

- Strategy: [[Instrumental Variables (IV)]], [[Identification Strategies (MOC)]]
- Assumptions: [[exclusion restriction]], [[relevance]], [[weak instruments]], [[monotonicity]]
- Estimands: [[Local Average Treatment Effect (LATE)|LATE]], [[Local IV]], [[marginal treatment effect (MTE)]], [[Wald estimator]]
- Estimation/inference: [[Generalized Method of Moments (GMM)|GMM]], [[Limited Information Maximum Likelihood (LIML)|LIML]], [[k-class estimator]] (to create), [[Anderson–Rubin|Anderson–Rubin test]], [[CLR test]], [[Stock–Yogo]], [[Durbin–Wu–Hausman test]]
- Panels/RD: [[fuzzy RDD]], [[Panel Data Methods (MOC)]]
- Inference: [[clustered standard errors]], [[Conley standard errors]], [[wild cluster bootstrap]]

---

## Potential future notes

- [[k-class estimator]]
- [[Jackknife IV (JIVE)|JIVE]]
- [[Cragg–Donald statistic]]
- [[Kleibergen–Paap]] rk Wald F
- [[Sargan test]]
- [[Hansen J test]]
- [[Durbin–Wu–Hausman test]]
- [[post-lasso instruments]]
