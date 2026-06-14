---
title: Relevance (IV)
aliases: [instrument relevance, first-stage relevance, rank condition]
tags: [econometrics, causal-inference, iv, weak-instruments, diagnostics]
updated: 2025-09-17
---

# Relevance (IV)

> [!summary] Quick definition
> In [[Instrumental Variables (IV)]], relevance means the instrument(s) $Z$ must affect the endogenous regressor(s) $D$. Formally, the first-stage effect is nonzero (and not vanishing), and with multiple instruments the instrument matrix has sufficient rank. Without relevance, IV cannot identify the causal parameter (e.g., [[Local Average Treatment Effect (LATE)|LATE]] or the 2SLS estimand).

- Minimal requirement (single endogenous regressor):
$$
\operatorname{Cov}(Z, D) \neq 0.
$$
- First-stage regression (with covariates $X$):
$$
D = \pi_0 + \pi_1 Z + X'\pi + v,\quad \pi_1 \ne 0.
$$

> [!note] Rank vs. order condition
> - Order condition: #instruments ≥ #endogenous regressors.
> - Rank condition (relevance): instruments shift the endogenous regressor(s) in the column space not spanned by $X$.

## Why relevance matters

- Without a sufficiently strong first stage, IV/[[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] estimates become biased and imprecise (tending toward OLS with weak instruments).
- In heterogeneous-effects settings (binary $Z,D$), relevance is the nonzero “first stage” needed for [[Local Average Treatment Effect (LATE)|LATE]]:
$$
\Delta_D = \mathbb{E}[D\mid Z=1]-\mathbb{E}[D\mid Z=0] \ne 0.
$$

## Diagnostics and tests

### First-stage F-statistics

- Homoskedastic i.i.d. (textbook): use the first-stage F on excluded instruments. Rule of thumb: F > 10 (Staiger–Stock) for one endogenous regressor.
- Heteroskedastic/clustered settings: use robust weak-IV diagnostics:
  - [[Kleibergen–Paap]] rk Wald F (robust to heteroskedasticity and clustering)
  - [[Montiel Olea–Pflueger F]] (MOP) for one endogenous regressor
- Multiple endogenous regressors:
  - Conditional F-statistics (Sanderson–Windmeijer) for each endogenous variable given the others
  - Shea’s partial $R^2$ to assess instrument relevance net of collinearity

> [!warning] Few clusters
> With clustered data and few clusters, conventional F can mislead. Report cluster-robust KP/MOP and consider [[few-cluster corrections]] or design-based [[randomization inference]].

### Partial R-squared (first stage)

- Report the partial $R^2$ of $Z$ in the first-stage for transparency:
$$
R^2_{\text{partial}} = \frac{\text{SSR}_{\text{reduced}} - \text{SSR}_{\text{full}}}{\text{SSR}_{\text{reduced}}}.
$$

### Weak-IV robust inference

- If diagnostics suggest weakness:
  - Use [[Anderson–Rubin|Anderson–Rubin test]] or conditional likelihood ratio tests for valid inference even under weak instruments.
  - Consider estimators less sensitive to weakness: [[Limited Information Maximum Likelihood (LIML)|LIML]], [[Fuller estimator]], [[Jackknife IV (JIVE)]].

## Equations and conditions (copy-ready)

- First stage (single endogenous regressor):
$$
D = \pi_0 + \pi_1 Z + X'\pi + v,\quad \pi_1\ne 0.
$$

- Relevance (single instrument):
$$
\operatorname{Cov}(Z, D \mid X)\ne 0.
$$

- LATE first stage (binary $Z,D$):
$$
\Delta_D = \mathbb{E}[D\mid Z=1]-\mathbb{E}[D\mid Z=0] \ne 0.
$$

- Rank condition (matrix form): with instruments $Z$ and regressors $[D\ X]$,
  the projection of $Z$ onto the space orthogonal to $X$ must span the column space of $D$ orthogonal to $X$.

## Practical workflow

> [!check] Steps
> - [ ] Justify that $Z$ shifts $D$ (institutional channel/mechanism).
> - [ ] Estimate the first-stage; report coefficients on $Z$, partial $R^2$, and F-stat(s).
> - [ ] Use robust diagnostics (KP/MOP; SW for multiple endogenous regressors).
> - [ ] If weak: apply weak-IV robust tests (Anderson–Rubin/CLR) and/or alternative estimators (LIML/Fuller).
> - [ ] Combine with validity checks for [[exclusion restriction]] and independence; relevance alone is not enough.

## Good practice and pitfalls

> [!tip] Good practice
> - Report: first-stage table, F-stat(s), partial $R^2$, and number of instruments.
> - In clustered panels: cluster at the assignment level; use KP rk F or MOP F.
> - If many instruments: consider instrument selection/shrinkage or LIML to mitigate many-IV bias.

> [!warning] Avoid these
> - Relying only on the i.i.d. F>10 rule when heteroskedasticity/clustering is present.
> - Using numerous weak instruments (bias, overfitting); test strength and consider parsimony.
> - Confusing relevance with validity: a strong $Z$ can still violate [[exclusion restriction]].

## Minimal code snippets

> [!example] R (AER ivreg; diagnostics)

```r
library(AER)
iv <- ivreg(Y ~ D + X1 + X2 | Z + X1 + X2, data = df)
summary(iv, diagnostics = TRUE)  # shows weak-instrument diagnostics (i.i.d.)

# First stage explicitly
fs <- lm(D ~ Z + X1 + X2, data = df)
summary(fs)  # coefficient on Z, partial R^2 (via anova), F-stat on Z

# fixest FE-2SLS (clustered)
library(fixest)
iv_fe <- feols(Y ~ X1 | id + time, iv = ~ D ~ Z, data = df, cluster = ~id)
etable(iv_fe)

# KP/MOP: use ivreg2 in Stata or advanced R packages (e.g., ivpack/ivmodel) for robust F.
```

> [!example] Stata

```stata
ivregress 2sls Y X1 X2 (D = Z), vce(robust)
estat firststage          // first-stage coefficients and F
* Robust weak-IV tests with ivreg2 (user-written)
* ssc install ivreg2, replace
ivreg2 Y X1 X2 (D = Z), robust first    // reports KP rk F, partial R2
weakivtest ivreg2                       // additional weak-IV tests (if installed)
```

> [!example] Python (linearmodels)

```python
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula('Y ~ 1 + X1 + X2 + [D ~ Z]', data=df).fit(cov_type='robust')
print(res.summary)

# First stage (manually)
fs = IV2SLS.from_formula('D ~ 1 + X1 + X2 + [Z ~ 0]', data=df).fit(cov_type='robust')
print(fs.summary)  # inspect coefficient on Z; compute F via statsmodels if needed
```

## Special topics

- Multiple endogenous regressors:
  - Check Sanderson–Windmeijer conditional F for each endogenous variable.
  - Use Shea’s partial $R^2$ to account for multicollinearity among instruments.

- Panel and clustered designs:
  - Clustered KP rk F is preferred; report number of clusters. With few clusters, add [[few-cluster corrections]] or wild bootstrap for tests on $Z$ in the first stage.

- Many instruments:
  - Risk of bias and overfitting the first stage; consider instrument selection, regularization, or LIML/Fuller.

- Designs:
  - [[fuzzy RDD]] relevance: the treatment probability must jump at the cutoff.
  - [[fuzzy DiD]] relevance: $Z\times Post$ must shift $D\times Post$.

## Reporting essentials

- Instrument(s) and mechanism of action on $D$.
- First-stage estimates: coefficients on $Z$, partial $R^2$, F-statistics (KP/MOP; SW if applicable).
- Number of instruments and endogenous regressors; any selection/shrinkage used.
- Clustering level and number of clusters; small-sample corrections when relevant.
- Complementary validity checks (exclusion, independence) and sensitivity analyses.

---

Related notes to create:
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]]
- [[weak instruments]]
- [[Kleibergen–Paap]]
- [[Montiel Olea–Pflueger F]]
- [[Sanderson–Windmeijer F]]
- [[Shea’s partial R^2]]
- [[Anderson–Rubin|Anderson–Rubin test]]
- [[Stock–Yogo|Stock–Yogo critical values]]
- [[Cragg–Donald]]
- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Fuller estimator]]
- [[Jackknife IV (JIVE)]]
- [[fuzzy RDD]]
- [[fuzzy DiD]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[randomization inference]]