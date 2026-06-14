---
title: Controlled Experiments Using Pre-Experiment Data (CUPED)
aliases: [CUPED, Controlled Experiments Using Pre-Experiment Data, controlled experiments using pre-experiment data, variance reduction (CUPED)]
tags: [experimentation, ab-testing, variance-reduction, ancova, power, mde]
updated: 2025-09-17
---

# Controlled Experiments Using Pre-Experiment Data (CUPED)

> [!summary] Quick definition
> CUPED (Controlled Experiments Using Pre-Experiment Data) reduces variance in experiment estimates by adjusting outcomes with a pre-exposure baseline covariate. It is equivalent to ANCOVA with a pre-treatment covariate and, under standard conditions, leaves the estimate unbiased while shrinking variance by roughly (1 − R²), where R² is the predictive power of the baseline for the outcome.

- Use in: [[AB Testing (MOC)]], field RCTs, geo/switchback experiments.
- Outcome remains ITT if the baseline is strictly pre-exposure (no leakage).

---

## Intuition

- Let Y be the post-exposure outcome, X a pre-exposure baseline (e.g., pre-period metric).
- Adjusted outcome:
$$
Y^\star = Y - \theta \,(X - \mathbb{E}[X])
$$
- Run the usual difference-in-means (or regression) on $Y^\star$. If $\theta$ is chosen as the regression coefficient of Y on X (estimated on pre-exposure data or control), the treatment estimate is unbiased and variance shrinks by ≈ (1 − R²).

> [!note] Equivalence to ANCOVA
> Regress Y on treatment indicator and pre-period baseline X (plus fixed effects as needed). CUPED with a scalar X is algebraically equivalent to including X as a covariate (ANCOVA), given consistent estimation of θ and pre-exposure X.

---

## Core formulas

- CUPED coefficient (population):
$$
\theta^\star = \frac{\operatorname{Cov}(Y, X)}{\operatorname{Var}(X)}.
$$

- Adjusted outcome:
$$
Y^\star = Y - \theta^\star (X - \mathbb{E}[X]).
$$

- Variance reduction factor (approx.):
$$
\frac{\Var(\hat\tau_{\text{CUPED}})}{\Var(\hat\tau)} \approx 1 - R^2,
$$
where $R^2$ is from regressing Y on X in a pre-exposure or control-based sample.

- Regression/ANCOVA form:
$$
Y_i = \alpha + \tau D_i + \beta X_i + \varepsilon_i \quad \Rightarrow \quad \hat\tau_{\text{ANCOVA}} \equiv \hat\tau_{\text{CUPED}}.
$$

> [!warning] Estimating θ
> - Estimate θ using only pre-exposure data or control-group post data to avoid bias.  
> - Do not use post-treatment information to learn θ (leakage).

---

## Practical steps

1) Define a pre-exposure baseline X (e.g., user’s pre-period mean of the metric).
2) Estimate θ:
   - On the control group: regress Y on X (post-period Y, baseline X) using only control units, or
   - On historical/pre-period data: regress post-like outcome on baseline X in earlier windows.
3) Compute adjusted outcome $Y^\star = Y - \hat\theta (X - \bar X)$.
4) Analyze as usual:
   - Difference-in-means on $Y^\star$, or
   - Regression of $Y^\star$ on treatment indicator (plus clustering as needed).
5) Inference:
   - Use correct SEs (cluster-robust for clustered/session/geo designs).  
   - For AB tests with ratios/logs, consider transforming outcome first or use multivariate CUPED (see below).

---

## Variants and extensions

- Multi-covariate CUPED (CUPAC): use a vector of pre-exposure covariates $X$; estimate $\boldsymbol\theta$ via OLS (on control or pre-exposure data):
$$
\boldsymbol\theta = \hat\Sigma_{XX}^{-1}\hat\Sigma_{XY},\quad Y^\star = Y - \boldsymbol\theta^\top (X - \bar X).
$$
- Triggered experiments: use pre-trigger baseline within the eligible population; avoid “post-trigger” covariates (leakage).
- Cluster/geo experiments: compute cluster-level baselines (e.g., pre-period average by geo) and run CUPED at cluster level; use clustered SEs.
- Time-varying outcomes: define a stable pre-period window long enough to capture seasonality; align by cohorts.

---

## Design and diagnostics

> [!check] Good practice
> - [ ] Baseline X is strictly pre-exposure, same scale as Y, and stable across cycles ([[seasonality]])  
> - [ ] θ estimated on control or pre-period data; document the sample used  
> - [ ] Report R² (or variance reduction) and sensitivity to θ estimation method  
> - [ ] Use appropriate SEs (e.g., [[clustered standard errors]]); consider [[few-cluster corrections]] if needed  
> - [ ] For ratio/log metrics, validate delta/log approximations or use multivariate CUPED

> [!warning] Pitfalls
> - Using post-treatment covariates (leakage) to compute X or θ  
> - Estimating θ on the full post-period including treated (can bias under strong effects)  
> - Mismatched units (per-session baseline but per-user analysis)  
> - Short/seasonally unrepresentative baseline windows

---

## Impact on MDE and power

- If $R^2 = 0.5$, variance halves and MDE shrinks by √(1−R²) ≈ 0.707.
- Plan [[power analysis]] by replacing σ² with σ²(1−R²) in formulas. See also [[Minimum Detectable Effect (MDE)|MDE]].

---

## Minimal code snippets

> [!example] R: CUPED via control-based θ and adjusted outcome

```r
# df: columns Y (post), D (treatment 0/1), X (pre-exposure baseline)
# 1) Estimate theta on control
theta_hat <- coef(lm(Y ~ X, data = subset(df, D == 0)))[["X"]]

# 2) Adjusted outcome
Xbar <- mean(df$X)
df$Y_star <- df$Y - theta_hat * (df$X - Xbar)

# 3) Analyze with difference-in-means or regression
t.test(Y_star ~ D, data = df)

# or regression with robust/clustered SEs
library(sandwich); library(lmtest)
fit <- lm(Y_star ~ D, data = df)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))
```

> [!example] R: ANCOVA (equivalent)

```r
fit_ancova <- lm(Y ~ D + X, data = df)
coeftest(fit_ancova, vcov = vcovHC(fit_ancova, type = "HC1"))  # tau on D
```

> [!example] Python: CUPED with control-based θ

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

# df has columns: Y (post), D (0/1), X (pre)
ctrl = df[df['D']==0]
X_ctrl = sm.add_constant(ctrl['X'])
theta_hat = sm.OLS(ctrl['Y'], X_ctrl).fit().params['X']

Xbar = df['X'].mean()
df['Y_star'] = df['Y'] - theta_hat * (df['X'] - Xbar)

# Difference-in-means on Y_star
treated = df[df['D']==1]['Y_star']
control = df[df['D']==0]['Y_star']
diff = treated.mean() - control.mean()

# Regression with robust SEs
X = sm.add_constant(df['D'])
res = sm.OLS(df['Y_star'], X).fit(cov_type='HC1')
print(res.summary())
```

> [!example] Stata: CUPED and ANCOVA

```stata
* Estimate theta on control
reg Y X if D==0
scalar theta = _b[X]

* Adjust outcome
sum X
scalar Xbar = r(mean)
gen Y_star = Y - theta*(X - Xbar)

* Difference-in-means on Y_star
ttest Y_star, by(D)

* ANCOVA (equivalent)
reg Y D X, vce(robust)
```

> [!example] Multivariate CUPED (vector covariates) in R

```r
# Fit on control to get theta vector
ctrl <- subset(df, D==0)
theta <- coef(lm(Y ~ X1 + X2 + X3, data = ctrl))[-1]  # slopes only (drop intercept)
Xbar <- colMeans(df[, c("X1","X2","X3")])
df$Y_star <- df$Y - as.vector(as.matrix(df[,c("X1","X2","X3")]) %*% theta) + sum(theta * Xbar)
```

---

## CUPED vs. alternatives

- CUPED vs ANCOVA: algebraically equivalent (scalar X); ANCOVA is simpler and handles multi-covariate naturally.
- CUPED vs. matching/weighting: CUPED/ANCOVA reduces variance but does not alter the estimand (ITT); matching/weighting is for balance/selection concerns.
- CUPED vs. DiD: With a strong pre/post structure, DiD uses multiple pre-periods; CUPED uses a baseline summary. They can be complementary.

---

## Reporting essentials

- Baseline definition (window, metric, unit), θ estimation sample (control or pre), and R²
- Main effect with and without CUPED; % variance reduction/MDE gain
- Inference details: SE type (robust/clustered), unit of analysis, handling of clusters/sessions/geos
- Diagnostics: leakage checks, seasonality coverage, stability across subgroups
- Limitations: when baseline is weak (low R²) or unstable across time/segments

---

## Common pitfalls

> [!warning]
> - Baseline drift across arms (violates pre-exposure balance)  
> - Different baseline windows across variants/cohorts  
> - Using baseline correlated with treatment assignment mechanism (e.g., triggered eligibility differences) without clarity  
> - Ignoring clustering in session/geo designs; iid SEs understate uncertainty

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[stratification]] · [[seasonality]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[leakage]] · [[triggered analysis]]