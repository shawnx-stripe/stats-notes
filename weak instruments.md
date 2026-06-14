---
title: weak instruments
aliases: [weak IV, weak identification, instrument weakness, low first-stage, weak instruments problem]
tags: [econometrics, iv, inference, diagnostics, weak-iv, 2sls, liml, ar-test, clr]
updated: 2025-09-17
---

# weak instruments

> [!summary] Quick definition
> Instruments are weak when they have little explanatory power for the endogenous regressor(s). With weak [[Instrumental Variables (IV)|IV]], 2SLS/IV estimates are biased toward OLS, confidence intervals are misleading, and Wald/t tests severely over-reject. Use weak-IV diagnostics (first-stage F, KP rk F, Montiel–Olea–Pflueger F) and weak-IV-robust inference (Anderson–Rubin, Kleibergen’s K, Conditional LR), or stronger estimators (LIML/Fuller), and report instrument strength transparently.

- Symptoms: low first-stage F-statistics; small partial R²; many/weak instruments; clustered/heteroskedastic designs where standard F is invalid.

---

## Consequences of weak IV

- Bias: 2SLS biased toward OLS, especially with small samples or many/weak instruments.
- Size distortions: conventional t/Wald tests over-reject; standard CIs undercover.
- Instability: estimates sensitive to instrument set; large variance and sign flips.

> [!warning] Do not rely on standard 2SLS t-stats/CIs when instruments are weak.

---

## Diagnostics (single endogenous regressor unless noted)

- Staiger–Stock rule of thumb (homoskedastic i.i.d.):
  - First-stage F > 10 suggests acceptable strength; F < 10 indicates weakness. Not valid under heteroskedasticity/clustering.

- Kleibergen–Paap rk Wald F (heteroskedastic/cluster-robust):
  - Use KP rk F instead of classical F when using robust/clustered SEs; compare to [[Stock–Yogo|Stock–Yogo critical values]] (approximate).

- Montiel Olea–Pflueger (MOP) effective F:
  - Robust first-stage F with better finite-sample properties; report with confidence.

- Partial R² (Shea’s partial R²):
  - Share of variation in endogenous regressor explained uniquely by instruments (net of controls); small values indicate weakness.

- Multiple endogenous regressors:
  - Sanderson–Windmeijer (SW) conditional F for each endogenous regressor conditional on the others.

> [!tip] Clustered designs
> Report cluster-robust KP rk F (and/or MOP F). With few clusters, inference is especially fragile; complement diagnostics with robust tests and design discussion.

---

## Weak-IV-robust inference

- Anderson–Rubin (AR) test (valid even with weak IV)
  - Tests H0: β = β0 by regressing Y − β0 D on instruments and controls; uses F/χ² on instruments. Invert across β0 to get CIs (may be wide or disjoint).

- Kleibergen’s K (Score/LM-type) test
  - Robust to heteroskedasticity; valid under weak IV; invert to get CIs.

- Conditional Likelihood Ratio (CLR; Moreira 2003)
  - Often best power among weak-IV-robust tests; use where available (Stata ivreg2, some R packages).

- Confidence sets
  - Invert AR/K/CLR to form confidence sets for β; sets can be wide or even unbounded/disjoint when instruments are very weak.

> [!note]
> When instruments are weak, prefer reporting AR/K/CLR CIs and/or LIML/Fuller point estimates with weak-IV-robust p-values.

---

## Estimators better than 2SLS under weak IV

- LIML (Limited Information ML)
  - Less biased than 2SLS with many/weak instruments.

- Fuller-k modification (e.g., Fuller(1))
  - Bias-reduced LIML variant, often recommended in practice.

- JIVE (Jackknife IV)
  - Reduces bias in overidentified settings; variance can be large.

- Instrument selection/shrinkage
  - Lasso/“Post-Lasso” for instruments (Belloni et al.) to avoid many-weak-instruments bias; requires careful implementation and valid SEs.

> [!tip] Practice
> Report LIML (or Fuller) alongside 2SLS, with weak-IV-robust tests/CIs.

---

## Remedies and design advice

- Strengthen the design: find stronger/cleaner instruments; refine timing; exploit sharp rules; reduce measurement error.
- Reduce instrument count: avoid many weak instruments; use parsimonious sets or selection.
- Use valid robust tests: AR/K/CLR; avoid naive t-tests.
- Transparency: report strength (F/KP/MOP), first stage coefficients, partial R², number of instruments, and overidentification cautiously.

---

## Copy-ready formulas

- First-stage (one endogenous regressor):
$$
D = Z\pi + X\gamma + v.
$$

- Partial R² (of Z in D | X):
$$
R^2_{\text{partial}} = \frac{\text{SSR}_{\text{reduced}} - \text{SSR}_{\text{full}}}{\text{SSR}_{\text{reduced}}}.
$$

- AR test (linear IV, homoskedastic version intuition):
Regress $Y - \beta_0 D$ on $Z, X$; F-stat on Z → AR p-value for H0: β=β0.

- CLR/LM (no simple closed form here; use software).

---

## Code snippets

> [!example] Stata: diagnostics + weak-IV-robust tests

```stata
* 2SLS with robust/clustered SEs
ivregress 2sls Y (D = Z1 Z2) X1 X2, vce(cluster clusterid)
estat firststage                // first-stage stats (i.i.d.)

* Robust weak-IV diagnostics and tests (ivreg2)
* ssc install ivreg2, replace
ivreg2 Y X1 X2 (D = Z1 Z2), robust first
* Reports KP rk F, partial R2, Stock–Yogo; weak-instrument-robust tests available:
weakivtest ivreg2              // (if installed) additional tests

* Anderson–Rubin / CLR (ivreg2 provides AR/CLR p-values for β=0 by default)
ivreg2 Y X1 X2 (D = Z1 Z2), robust
```

> [!example] R: AER ivreg + diagnostics; wild tests via packages

```r
library(AER)
fit <- ivreg(Y ~ D + X1 + X2 | Z1 + Z2 + X1 + X2, data = df)
summary(fit, diagnostics = TRUE)  # includes weak IV diagnostics (i.i.d.)

# Cluster-robust vcov and KP rk F (approx): use ivpack/sandwich; for weak-IV-robust AR/CLR,
# consider packages like 'ivmodel' or implement AR via regression of (Y - beta0 D).
library(sandwich); library(lmtest)
coeftest(fit, vcov = vcovCL(fit, cluster = ~ clusterid))

# LIML/Fuller (ivreg supports method="liml")
fit_liml <- ivreg(Y ~ D + X1 + X2 | Z1 + Z2 + X1 + X2, data=df, method="liml")
summary(fit_liml)
```

> [!example] Python: linearmodels IV2SLS (diagnostics sketch)

```python
from linearmodels.iv import IV2SLS
import numpy as np

res = IV2SLS.from_formula('Y ~ 1 + X1 + X2 + [D ~ Z1 + Z2]', data=df).fit(cov_type='robust')
print(res.summary)

# First-stage F (manual)
import statsmodels.api as sm
fs = sm.OLS(df['D'], sm.add_constant(df[['Z1','Z2','X1','X2']])).fit(cov_type='HC1')
# Compute partial F for instruments via anova-like decomposition or use statsmodels linear_hypothesis
from statsmodels.stats.contrast import ContrastResults
# (Implementation of KP/MOP not built-in; use Stata/R for authoritative diagnostics.)
```

> [!example] Stata: LIML/Fuller and weak-IV-robust CI

```stata
ivregress liml Y (D = Z1 Z2) X1 X2, vce(cluster clusterid)
* Fuller(1)
ivreg2 Y X1 X2 (D = Z1 Z2), fuller(1) robust
```

---

## Reporting essentials

- Instrument list; mechanism (why relevant), and plausibility of [[exclusion restriction]]
- First-stage results: coefficients on Z, partial R², KP rk F (robust), MOP F; number of instruments; sample size
- Inference: cluster level, robust method, weak-IV-robust tests used (AR/K/CLR) and their p-values/CIs
- Point estimates: 2SLS and LIML/Fuller; discuss differences
- Sensitivity: alternative instrument subsets, selection/shrinkage, overid tests with caveats (only informative if at least one valid instrument)
- If weak: transparent admission; emphasize robust CIs/sets; consider design improvements

---

## Common pitfalls

> [!warning]
> - Relying on “F > 10” under heteroskedasticity/clustering (use KP/MOP)  
> - Ignoring weak-IV-robust inference (reporting only 2SLS t-stats)  
> - Many weak instruments inflating bias/variance; “overfitting the first stage”  
> - Treating overidentification tests (Sargan/Hansen) as proof of validity when instruments are weak  
> - No discussion of instrument strength in clustered panels or with few clusters  
> - Using standard LR/Wald tests instead of AR/CLR under weakness

---

## Related notes

- [[Instrumental Variables (IV)]] · [[Local Average Treatment Effect (LATE)|LATE]] · [[exclusion restriction]] · [[relevance]] · [[monotonicity]]
- [[Anderson–Rubin|Anderson–Rubin test]] · [[Kleibergen–Paap]] · [[Stock–Yogo|Stock–Yogo critical values]] · [[Montiel Olea–Pflueger F]]
- [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[Limited Information Maximum Likelihood (LIML)|LIML]] · [[Fuller estimator]] · [[Jackknife IV (JIVE)]]
- [[clustered standard errors]] · [[few-cluster corrections]] · [[wild cluster bootstrap]]
- [[Hypothesis testing]] · [[randomization inference]]

---