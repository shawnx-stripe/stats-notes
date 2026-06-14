---
title: Controlled Experiments Using Pre-Experiment Covariates (CUPAC)
aliases: [CUPAC, Controlled Experiments Using Pre-Experiment Covariates, controlled experiments using pre-experiment covariates, contextual CUPED, multivariate CUPED, prognostic score adjustment]
tags: [experimentation, variance-reduction, ancova, cuped, ab-testing, power, mde, clustering, prognostic-score, ml]
updated: 2025-09-17
---

# Controlled Experiments Using Pre-Experiment Covariates (CUPAC)

> [!summary] Quick definition
> CUPAC (Controlled Experiments Using Pre-Experiment Covariates) generalizes [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] by using multiple pre-exposure covariates or a learned prognostic score to reduce outcome variance. It is equivalent to multivariate [[Analysis of Covariance (ANCOVA)|ANCOVA]] with strictly pre-treatment covariates. Variance reduction is roughly by a factor of (1 − R²), where R² is the predictive power of the covariates (or prognostic score) for the outcome.

- Goal: improve precision (smaller SE/MDE) without changing the ITT estimand.
- Safe if (and only if) covariates are strictly pre-treatment (no leakage).

---

## Intuition and core formula

Let Y be the post-exposure outcome, and Z be a vector of pre-exposure covariates (or a single prognostic score s(X), learned from pre-period/historical data).

- CUPAC-adjusted outcome:
$$
Y^\star = Y - \boldsymbol\theta^\top \big(Z - \mathbb{E}[Z]\big),
$$
where the optimal $\boldsymbol\theta$ (in population) is:
$$
\boldsymbol\theta^\star = \operatorname{argmin}_{\theta} \Var\big(Y - \theta^\top Z\big) = \Sigma_{ZZ}^{-1}\,\Sigma_{ZY}.
$$

- Estimate $\boldsymbol\theta$ using only control data or pre-exposure data (to avoid bias), then analyze treatment effect on $Y^\star$ via difference-in-means or regression on $D$.

> [!note] Equivalence to ANCOVA
> Regressing Y on treatment and Z (pre-treatment) is algebraically equivalent to CUPAC with $Y^\star$. CUPED is a special case with a single baseline covariate.

---

## Variance reduction and MDE

- If $R^2$ is the coefficient of determination from regressing Y on Z (estimated on control or pre-exposure data):
  - Variance reduction factor ≈ (1 − R²)
  - [[Minimum Detectable Effect (MDE)|MDE]] reduction ≈ √(1 − R²)

Example: $R^2 = 0.49$ ⇒ variance halves; MDE shrinks by ~30%.

---

## How to build Z (covariates)

- Direct multivariate covariates
  - Pre-period outcomes (levels, moving averages), traffic/engagement baselines, demographics, device, geo, seasonality indicators.
- Prognostic score (single scalar)
  - Learn $\hat s(X)$ to predict Y using only historical/pre-exposure data (or post-outcomes in controls), then use $Z = \hat s(X)$ as a single, powerful covariate.
  - Methods: ridge/lasso/elastic net, trees/forests/boosting. Cross-validate and restrict to pre-exposure features.

> [!tip] Dimensionality
> - Many covariates: prefer a prognostic score (reduce to 1–2 dimensions) or regularized ANCOVA (ridge).
> - Keep interpretable and robust; monitor $R^2$ out-of-sample.

---

## Estimation strategies

- CUPAC two-step (control-based θ)
  1) Regress Y on Z using control (or pre-exposure) data to get $\hat{\boldsymbol\theta}$.
  2) Compute $Y^\star = Y - \hat{\boldsymbol\theta}^\top (Z - \bar Z)$.
  3) Estimate ITT via difference-in-means/regression on $Y^\star$.

- ANCOVA
  - Regress $Y$ on $D$ and $Z$ directly. Equivalent to CUPAC; easier to implement; use robust/clustered SEs.

- CUPAC-ML (prognostic score)
  1) Train $\hat s(X)$ on pre-exposure/historical or control data only.
  2) Use $Z = \hat s(X)$ (single covariate) in CUPAC/ANCOVA.
  3) Gains often larger and more stable than many raw covariates.

> [!warning] No leakage
> Do not use any post-treatment information (features or labels) to build Z or to estimate $\hat{\boldsymbol\theta}$.

---

## Inference and clustering

- Randomized experiments: $\hat\tau$ remains unbiased; use robust or [[clustered standard errors]] at the randomization unit (user/session/geo/time-block).
- Few clusters: apply [[few-cluster corrections]] (CR2, wild cluster bootstrap).
- Triggered designs: define pre-trigger baselines; analyze triggered population but report ITT as well.

---

## Practical guidance

> [!check] Good practice
> - [ ] Define Z strictly pre-exposure; document window and features  
> - [ ] Estimate $\hat{\boldsymbol\theta}$ on control or pre-period data (not on treated)  
> - [ ] Prefer a single prognostic score when p is large; cross-validate out-of-sample $R^2$  
> - [ ] Use robust/clustered SEs; report number of clusters  
> - [ ] Report variance/MDE gains (1 − R²) and sensitivity to feature sets  
> - [ ] For ratio/log metrics, consider transforming Y or modeling numerator/denominator separately

> [!warning] Pitfalls
> - Leakage (post-treatment covariates or treated outcomes in training)  
> - Using the full (treated+control) post sample to estimate $\hat{\boldsymbol\theta}$ when effects are large  
> - Overfitting many covariates with small N (unstable θ)  
> - Mismatch of units (per-session features with per-user analysis)  
> - Seasonality drift between baseline and experiment window (unstable $R^2$)

---

## Minimal code snippets

> [!example] R: CUPAC via control-based θ and adjusted outcome

```r
# df: Y (post), D (0/1), and Z1..Zk pre-exposure covariates
ctrl <- subset(df, D == 0)
theta <- coef(lm(Y ~ Z1 + Z2 + Z3, data = ctrl))[-1]  # slopes only (drop intercept)
Zbar  <- colMeans(df[, c("Z1","Z2","Z3")])
Zmat  <- as.matrix(df[, c("Z1","Z2","Z3")])
df$Y_star <- df$Y - as.vector(Zmat %*% theta) + sum(theta * Zbar)

# ITT on adjusted outcome (robust SEs)
library(sandwich); library(lmtest)
fit <- lm(Y_star ~ D, data = df)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))
```

> [!example] R: ANCOVA (equivalent; with clustering)

```r
# Cluster by user_id/session_id/geo as needed
fit <- lm(Y ~ D + Z1 + Z2 + Z3, data = df)
library(clubSandwich)
coef_test(fit, vcov = vcovCR(fit, type = "CR2", cluster = df$user_id), test = "Satterthwaite")
```

> [!example] Python: Prognostic score (ridge) + ANCOVA

```python
import numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
import statsmodels.formula.api as smf

X = df[['Z1','Z2','Z3']].values
Y = df['Y'].values
D = df['D'].values

# Train prognostic model on controls only
ridge = RidgeCV(alphas=np.logspace(-3,3,20), cv=5).fit(X[D==0], Y[D==0])
df['s'] = ridge.predict(X)

# ANCOVA with prognostic score
res = smf.ols('Y ~ D + s', data=df).fit(cov_type='HC1')
print(res.summary())
```

> [!example] Stata: ANCOVA and control-based θ

```stata
* ANCOVA (robust)
reg Y D Z1 Z2 Z3, vce(robust)

* Control-based theta then CUPAC-adjusted outcome
reg Y Z1 Z2 Z3 if D==0
matrix b = e(b)
sum Z1 Z2 Z3
scalar Z1bar = r(mean1)
scalar Z2bar = r(mean2)
scalar Z3bar = r(mean3)
gen Y_star = Y - (_b[Z1]*(Z1 - Z1bar) + _b[Z2]*(Z2 - Z2bar) + _b[Z3]*(Z3 - Z3bar))
reg Y_star D, vce(robust)
```

---

## CUPAC for special metrics

- Ratios (e.g., revenue/user): log-transform or model numerator and denominator separately; or build a prognostic score for the ratio directly with care.
- Quantiles (e.g., p95 latency): consider quantile ANCOVA or bootstrap variance; guard against heavy-tail instability.
- Binary outcomes: logistic ANCOVA or linear probability model with robust SEs; CUPAC still valid.

---

## Reporting essentials

- Baseline/covariate definitions (windows, features), and how prognostic models were trained (data, algorithm, CV)
- Estimation details: CUPAC vs ANCOVA; control-only vs pre-period training; $R^2$ out-of-sample
- Main effect with robust/clustered SEs; variance/MDE gains
- Sensitivity: different feature sets, baseline windows, prognostic models
- Diagnostics: leakage checks, seasonality alignment, stability across cohorts/segments

---

## Related notes

- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[seasonality]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[double machine learning]] (for advanced prognostic modeling)
- [[triggered analysis]] · [[exposure logging]]

---