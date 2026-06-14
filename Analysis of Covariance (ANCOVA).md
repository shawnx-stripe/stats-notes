---
title: Analysis of Covariance (ANCOVA)
aliases: [ANCOVA, analysis of covariance, covariate adjustment, regression adjustment]
tags: [experimentation, ancova, variance-reduction, ab-testing, power, mde, rct, clustering]
updated: 2025-09-17
---

# Analysis of Covariance (ANCOVA)

> [!summary] Quick definition
> ANCOVA (Analysis of Covariance) estimates treatment effects while adjusting for pre-treatment covariates, typically a baseline of the outcome. In randomized experiments, ANCOVA yields an unbiased ITT estimate and can substantially reduce variance (roughly by a factor of 1 − R², where R² is the predictive power of covariates for the outcome). In online tests, ANCOVA with a baseline is equivalent to [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]].

- Primary use: precision gain in randomized experiments and [[AB Testing (MOC)]].
- Estimand: ITT (unless analyzing as-treated with endogeneity).
- Key rule: only include pre-treatment covariates (no leakage/post-treatment variables).

---

## Core model and estimand

- Two-arm post-outcome ANCOVA:
$$
Y_{i,\text{post}} = \alpha + \tau D_i + \beta^\top X_i + \varepsilon_i,
$$
where:
  - $D_i \in \{0,1\}$ is treatment assignment,
  - $X_i$ are pre-treatment covariates (often baseline $Y_{i,\text{pre}}$),
  - $\tau$ is the ITT.

- With a single baseline $X=Y_{\text{pre}}$, this is algebraically equivalent to [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]].

> [!tip] Precision
> Approximate variance reduction factor ≈ (1 − R²), where R² is from regressing $Y_{\text{post}}$ on $X$ using pre-exposure/control data. MDE shrinks by √(1 − R²). See [[Minimum Detectable Effect (MDE)|MDE]] and [[power analysis]].

---

## Best-practice specifications

- Baseline-only:
$$
Y_{\text{post}} = \alpha + \tau D + \beta Y_{\text{pre}} + \varepsilon.
$$

- Multiple covariates:
$$
Y_{\text{post}} = \alpha + \tau D + \beta^\top X + \varepsilon.
$$

- Lin (2013) robust adjustment for RCTs (allow heterogeneity in slopes):
$$
Y_{\text{post}} = \alpha + \tau D + \beta^\top X + \gamma^\top(D \cdot X) + \varepsilon.
$$

- Blocked/stratified randomization: include strata FE
$$
Y_{\text{post}} = \alpha + \tau D + \beta^\top X + \sum_s \delta_s \,\mathbf{1}\{\text{stratum}=s\} + \varepsilon.
$$

> [!warning] Clusters
> For cluster-randomized trials (schools, geos) or session-level randomization: use [[clustered standard errors]] at the randomization unit; consider [[few-cluster corrections]] when clusters are few.

---

## ANCOVA vs. alternatives

- Post-only difference in means: unbiased under randomization but less precise than ANCOVA when covariates predict outcomes.
- Change score (Δ = post − pre): can be less efficient and sensitive to measurement error; ANCOVA typically preferred.
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]: equivalent to ANCOVA with a single baseline covariate; CUPAC is multivariate ANCOVA in disguise.

---

## Assumptions and cautions

- Randomized experiments:
  - Unbiasedness of $\hat\tau$ does not require correct linear specification; covariates affect precision.
  - Use robust/cluster-robust SEs.
  - Include only pre-treatment covariates; no post-treatment [[bad controls]].
- Observational data:
  - Requires identification (e.g., [[Unconfoundedness]]/[[Overlap]]). ANCOVA alone doesn’t fix confounding.
- AB testing nuances:
  - Baseline must be strictly pre-exposure; for triggered tests, use pre-trigger baseline in the eligible population.
  - Ratio/log metrics: consider transforming outcome or use multivariate ANCOVA to model both numerator/denominator components.

---

## Precision, power, and MDE

- If the baseline explains R² of outcome variance, then:
  - Var reduction ≈ (1 − R²)
  - [[Minimum Detectable Effect (MDE)|MDE]] scales by √(1 − R²)
- Incorporate [[stratification]]/blocks and R² into [[power analysis]]; inflate for clustering via ICC/design effect if applicable.

---

## Multi-arm and factorial designs

- Multi-arm: include multiple treatment indicators (or factors); τ’s are contrasts.
- Factorial: include main effects and interactions of factors; keep pre-treatment covariates (and optionally factor×covariate interactions).
- Stepped-wedge/staggered rollout: ANCOVA with cohort/time FE is akin to short-horizon DiD; for general staggered adoption, see [[staggered adoption]] and modern DiD estimators.

---

## Diagnostics and good practice

> [!check]
> - [ ] Covariates are pre-treatment; define baseline windows to cover [[seasonality]] cycles  
> - [ ] Document how θ (CUPED) or regression coefficients were estimated (control/pre-period vs. full-sample)  
> - [ ] Use robust/clustered SEs; report number of clusters  
> - [ ] Sensitivity: with/without ANCOVA; alternative baseline definitions; add/remove key covariates  
> - [ ] For AB tests: monitor [[AA test]] and [[Sample Ratio Mismatch (SRM)|SRM]]; ensure exposure logging integrity

---

## Minimal code snippets

> [!example] R

```r
# Simple ANCOVA (robust SEs)
library(sandwich); library(lmtest)
fit <- lm(Y_post ~ D + Y_pre, data = df)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))  # tau on D

# With interactions (Lin 2013)
fit_lin <- lm(Y_post ~ D*(Y_pre + X1 + X2), data = df)
coeftest(fit_lin, vcov = vcovHC(fit_lin, type = "HC1"))

# Cluster-robust SEs (cluster = cluster_id)
library(clubSandwich)
fit_cl <- lm(Y_post ~ D + Y_pre + factor(stratum), data = df)
coef_test(fit_cl, vcov = vcovCR(fit_cl, type = "CR2", cluster = df$cluster_id), test = "Satterthwaite")
```

> [!example] Stata

```stata
* Robust ANCOVA
reg Y_post D Y_pre, vce(robust)

* Lin (2013) style with interactions and clusters
reg Y_post c.D##c.Y_pre c.D##c.X1 c.D##c.X2, vce(cluster cluster_id)

* Include strata fixed effects if blocked
reg Y_post D Y_pre i.stratum, vce(cluster cluster_id)
```

> [!example] Python (statsmodels)

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Robust ANCOVA
fit = smf.ols('Y_post ~ D + Y_pre', data=df).fit(cov_type='HC1')
print(fit.summary())

# Lin (2013) with interactions
fit_lin = smf.ols('Y_post ~ D*(Y_pre + X1 + X2)', data=df).fit(cov_type='HC1')
print(fit_lin.summary())

# Cluster-robust
fit_cl = smf.ols('Y_post ~ D + Y_pre + C(stratum)', data=df).fit(
    cov_type='cluster', cov_kwds={'groups': df['cluster_id']})
print(fit_cl.summary())
```

---

## Common pitfalls

> [!warning]
> - Using post-exposure covariates (leakage) → bias  
> - Ignoring clustering in CRTs/switchback/geo tests → anticonservative SEs  
> - Very short/seasonal baseline windows → unstable adjustment  
> - Overfitting many covariates with tiny samples; prefer parsimonious baselines  
> - In observational studies, mistaking ANCOVA for identification (needs [[Unconfoundedness]]/design)

---

## Reporting essentials

- Estimand (ITT), covariates used (definitions, timing), and rationale
- Specification (with/without interactions; strata FE; cluster level)
- Effect estimate with robust/clustered SEs and CIs
- Precision gains: R² and % MDE reduction
- Sensitivity (different baselines, with/without ANCOVA)
- Data quality: exposure logging, SRM/AA for AB tests; seasonality coverage

---

## Copy-ready snippets

- Model:
$$
Y_{\text{post}} = \alpha + \tau D + \beta^\top X + \varepsilon
$$

- Variance reduction:
$$
\Var(\hat\tau_{\text{ANCOVA}}) \approx (1 - R^2)\,\Var(\hat\tau_{\text{diff}})
$$

- CUPED equivalence (scalar baseline):
$$
Y^\star = Y - \theta (X - \bar X), \quad \hat\tau_{\text{diff on }Y^\star} \equiv \hat\tau_{\text{ANCOVA}}
$$

---

## Related notes

- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[stratification]] · [[clustered standard errors]] · [[few-cluster corrections]]
- [[seasonality]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[Unconfoundedness]] · [[Overlap]] · [[bad controls]]