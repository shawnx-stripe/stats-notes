---
title: Instrumental Variables (IV)
aliases: [IV, instrumental variable, instruments, instrumental variables]
tags: [econometrics, causal-inference, iv, noncompliance, policy-evaluation, weak-instruments]
updated: 2025-09-17
---

# Instrumental Variables (IV)

> [!summary] Quick definition
> Instrumental Variables address endogeneity by using an external variable (the instrument) that shifts treatment but affects the outcome only through that treatment. With a valid instrument, IV identifies causal effects even when treatment is endogenous.

- Canonical use cases:
  - [[noncompliance]] in RCTs/encouragement designs → identify [[Local Average Treatment Effect (LATE)|LATE]]
  - Omitted variable bias, simultaneity, or measurement error in observational settings
  - “Fuzzy” designs: [[fuzzy RDD]] and [[fuzzy DiD]]

## Core ingredients and assumptions

Let Z be the instrument, D the endogenous regressor/treatment, Y the outcome, and X covariates.

- [[relevance]]: Z must affect D (non-zero first stage)
- [[exclusion restriction]]: Z affects Y only via D (no direct effect on Y)
- Independence/As-if random: Z ⟂ {Y(0), Y(1), D(0), D(1)} (or conditional on X)
- For binary Z and D with heterogeneity: [[monotonicity]] (no defiers) to interpret as [[Local Average Treatment Effect (LATE)|LATE]]

> [!warning] Exclusion and independence are design/substantive assumptions; they cannot be verified statistically.

## Estimands and interpretation

- With binary Z and D:
$$
LATE = \frac{\mathbb{E}[Y \mid Z=1] - \mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1] - \mathbb{E}[D \mid Z=0]}
$$
- With heterogeneity and general Z, linear IV/[[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] identifies a Z-specific weighted average of local effects (local to the instrument); see [[Local IV]] and [[marginal treatment effect (MTE)]].

- Relation to [[Intent-to-Treat (ITT)]]: ITT = LATE × first stage.

## 2SLS (two-stage least squares)

> [!equation] Basic setup
> 1st stage: D = π0 + π1 Z + X'π + v
> 
> 2nd stage: Y = α + β D̂ + X'γ + u

- β is the IV estimate.
- Use the same X in both stages.
- For panels, include fixed effects in both stages (FE-2SLS) and cluster errors appropriately; see [[clustered standard errors]].

> [!tip] Just-identified vs. overidentified
> - Just-identified: number of instruments = number of endogenous regressors
> - Overidentified: more instruments than endogenous regressors; can test overidentifying restrictions (Sargan/Hansen J) with caution (invalid if any instrument is invalid)

## Diagnostics: strength and validity

- Strength (first-stage):
  - Report the first-stage coefficient(s) on Z and an F-statistic.
  - Homoskedastic iid: rule-of-thumb F > 10 (Staiger–Stock).
  - Heteroskedastic/clustered: report Kleibergen–Paap rk F and/or Montiel Olea–Pflueger F. See [[weak instruments]] and [[few-cluster corrections]].

- Validity:
  - Substantive argument for [[exclusion restriction]] and independence.
  - Overid tests (Sargan/Hansen J) only informative if at least one instrument is valid; failing to reject is not proof of validity.

> [!warning] Many/weak instruments
> Many or weak instruments inflate variance and bias 2SLS toward OLS. Consider [[Limited Information Maximum Likelihood (LIML)|LIML]]/Fuller, Anderson–Rubin tests, or regularized/selection methods for instruments.

## Weak-instrument robust inference

- Tests: Anderson–Rubin confidence sets, Kleibergen’s K, conditional likelihood ratio
- Estimators: [[Limited Information Maximum Likelihood (LIML)|LIML]], Fuller-k class, [[Jackknife IV (JIVE)]]
- Always report: first-stage strength (F-stat) and, where relevant, Stock–Yogo critical values (iid) or robust alternatives.

## Designs using IV

- Encouragement/noncompliance:
  - Z = assignment/offer; D = take-up; estimate [[Intent-to-Treat (ITT)|ITT]] and [[Local Average Treatment Effect (LATE)|LATE]]
- [[fuzzy RDD]]:
  - Z = indicator for being above cutoff; use local Wald ratio
- [[fuzzy DiD]]:
  - Instrument D×Post with Z×Post under [[parallel trends assumption]] relative to assignment groups
- Measurement error:
  - Use an instrument correlated with true D but not error in Y

## Nonlinear and alternative estimators

- Binary outcomes: IV-Probit/structural models or 2SRI (two-stage residual inclusion) as a control-function approach; interpret with care.
- Control function:
  - Add residuals from first stage in outcome equation to control for endogeneity; connects to structural models.

## Practical workflow

> [!check] Steps
> - [ ] Justify instrument: source, mechanism, why exclusion holds, why monotonicity (if LATE)
> - [ ] Show strong first stage (coefficients, F-stat, KP/MOP)
> - [ ] Estimate 2SLS; cluster at assignment level; apply [[few-cluster corrections]] if needed
> - [ ] Report ITT, first stage, IV estimate (LATE interpretation if relevant)
> - [ ] Sensitivity: alternative instruments, windows, controls; overid tests (if overidentified)
> - [ ] Discuss external validity (LATE is for compliers/local movers)

## Minimal code snippets

> [!example] R

```r
# 2SLS with AER
library(AER)
iv_res <- ivreg(Y ~ D + X1 + X2 | Z + X1 + X2, data = df)
summary(iv_res)             # includes diagnostics, weak-instrument tests (iid)

# Panel FE-2SLS (fixest)
library(fixest)
iv_fe <- feols(Y ~ X1 | id + time, iv = ~ D ~ Z, data = df, cluster = ~id)  # cluster at id or assignment level
etable(iv_fe)
```

> [!example] Stata

```stata
* Basic 2SLS
ivregress 2sls Y X1 X2 (D = Z), vce(robust)
estat firststage
estat overid

* Heteroskedastic-robust weak-IV tests (Kleibergen–Paap)
ivreg2 Y X1 X2 (D = Z), robust first  // user-written ivreg2

* FE-2SLS (panel)
ivreghdfe Y X1 X2 (D = Z), absorb(id time) vce(cluster id)
```

> [!example] Python

```python
from linearmodels.iv import IV2SLS
# Simple 2SLS
res = IV2SLS.from_formula('Y ~ 1 + X1 + X2 + [D ~ Z]', data=df).fit(cov_type='robust')
print(res.summary)

# Panel with FE via dummies (large designs may be heavy)
res_fe = IV2SLS.from_formula('Y ~ C(id) + C(time) + X1 + [D ~ Z]', data=df).fit(cov_type='clustered', clusters=df['id'])
print(res_fe.summary)
```

## Copy-ready formulas

- Wald (binary Z and D):
$$
\widehat{LATE} = \frac{\bar Y_{Z=1} - \bar Y_{Z=0}}{\bar D_{Z=1} - \bar D_{Z=0}}
$$

- 2SLS:
$$
\hat\beta_{2SLS} = \big(X'P_Z X\big)^{-1} X'P_Z Y, \quad P_Z = Z(Z'Z)^{-1}Z'
$$

- First stage F (iid, single endogenous regressor):
$$
F = \frac{R^2 / q}{(1-R^2)/(N-K)} \quad \text{(q = number of instruments)}
$$

## Common pitfalls

> [!warning] Avoid these
> - Weak instruments (low F/KP/MOP): biased and imprecise IV
> - Violated exclusion via channels other than D (e.g., Z changes Y directly)
> - Interference/[[No spillovers]] of Z across units
> - Overusing many instruments (overfitting, finite-sample bias)
> - Treating overid tests as proofs of validity

## Reporting essentials

- Instrument definition, mechanism, and threats to exclusion
- ITT and first stage (coefficients, F-stat, KP/MOP)
- IV estimate with interpretation (LATE/complier population)
- SEs and clustering level; [[few-cluster corrections]] if applicable
- Overid tests (if overidentified) and sensitivity to instrument choice
- External validity and local nature of estimates

---

Related notes to create:
- [[Intent-to-Treat (ITT)]]
- [[noncompliance]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Treatment-on-the-Treated (TOT)]]
- [[exclusion restriction]]
- [[relevance]]
- [[monotonicity]]
- [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]]
- [[weak instruments]]
- [[Anderson–Rubin|Anderson–Rubin test]]
- [[Kleibergen–Paap]]
- [[Stock–Yogo|Stock–Yogo critical values]]
- [[Montiel Olea–Pflueger F]]
- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Fuller estimator]]
- [[Jackknife IV (JIVE)]]
- [[Local IV]]
- [[marginal treatment effect (MTE)]]
- [[fuzzy RDD]]
- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy DiD]]
- [[Difference-in-Differences (DiD)]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[No spillovers]]
- [[interference]]
- [[control function]]
- [[2SRI]]
- [[overidentification test]]
- [[Sargan test]]
- [[Hansen J test]]