---
title: Augmented Inverse Probability Weighting (AIPW)
aliases: [AIPW, augmented inverse probability weighting, doubly robust estimator, augmented IPW, DR estimator]
tags: [causal-inference, ate, att, weighting, doubly-robust, tmle, dml]
updated: 2025-09-17
---

# Augmented Inverse Probability Weighting (AIPW)

> [!summary] Quick definition
> AIPW (also called a doubly robust estimator) combines an outcome regression with inverse probability weighting by the [[propensity score]] to estimate causal effects. It is consistent if either the outcome model or the propensity model is correctly specified (not necessarily both), under [[Unconfoundedness]], [[Overlap]], and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]].

- Targets: typically [[Average Treatment Effect (ATE)]] or [[Average Treatment Effect on the Treated (ATT)]].
- Strengths: “doubly robust” against single-model misspecification; often near-efficient with good nuisance models.
- Extensions: panel/[[Difference-in-Differences (DiD)]] variants (DR-DiD).

## Assumptions

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] (no interference; well-defined treatment)
- [[Unconfoundedness]]: {Y(1), Y(0)} ⟂ D | X
- [[Overlap]] (positivity): 0 < e(X) < 1 almost surely, with e(X)=P(D=1|X)
- Correct specification of at least one nuisance: the outcome regressions m_d(X) or the propensity score e(X)

## Notation

- D ∈ {0,1}: treatment
- X: pre-treatment [[covariates]]
- Y: outcome
- e(X) = P(D=1|X): [[propensity score]]
- m_d(X) = E[Y | D=d, X]: outcome regression for arm d ∈ {0,1}

## AIPW estimators (copy-ready)

### ATE (cross-sectional)
- Influence-function (IF) form:
$$
\widehat{ATE}_{AIPW} = \frac{1}{N}\sum_{i=1}^N \Bigg[
\underbrace{\hat m_1(X_i)-\hat m_0(X_i)}_{\text{OR term}}
+ \underbrace{\frac{D_i\,(Y_i-\hat m_1(X_i))}{\hat e(X_i)} - \frac{(1-D_i)\,(Y_i-\hat m_0(X_i))}{1-\hat e(X_i)}}_{\text{IPW correction}}
\Bigg].
$$

### ATT (cross-sectional)
- One common ATT-AIPW form:
$$
\widehat{ATT}_{AIPW} =
\frac{1}{N_1}\sum_{i:D_i=1}\!\big(Y_i - \hat m_0(X_i)\big)
- \frac{1}{N_1}\sum_{i:D_i=0}\!\frac{\hat e(X_i)}{1-\hat e(X_i)}\big(Y_i - \hat m_0(X_i)\big),
$$
where $N_1=\sum_i D_i$. Variants use augmentation around $\hat m_1(X)$; all are DR if constructed via the efficient influence function.

> [!note] Doubly robust property
> If either $\hat e(X)$ is consistent for $e(X)$ or $\hat m_d(X)$ is consistent for $m_d(X)$, the AIPW estimator is consistent for the target effect.

## Efficient influence function (EIF) and SEs

- ATE EIF contribution for unit i:
$$
\phi_i = \Big[m_1(X_i)-m_0(X_i)\Big]
+ \frac{D_i\,(Y_i-m_1(X_i))}{e(X_i)}
- \frac{(1-D_i)\,(Y_i-m_0(X_i))}{1-e(X_i)}
- ATE.
$$
- Variance estimate: $\widehat{\mathrm{Var}}(\widehat{ATE}) = \frac{1}{N^2}\sum_i (\hat\phi_i - \bar\phi)^2$; CIs via normal approximation or bootstrap. In panels/clusters, use [[clustered standard errors]] with the influence scores.

## Practical workflow

> [!check] Steps
> - [ ] Specify pre-treatment covariates X (avoid [[bad controls]]/post-treatment variables).
> - [ ] Fit $\hat e(X)$ using flexible models (logit/probit or ML) and check overlap.
> - [ ] Fit $\hat m_0(X)$ and $\hat m_1(X)$ (separate models or a single model with D×X).
> - [ ] Compute AIPW estimate; derive IF-based SEs (or use software).
> - [ ] Perform diagnostics: balance after weighting, weight stability (extremes), overlap plots.
> - [ ] Sensitivity: alternative PS/OR models, trimming, stabilized/overlap weights.

> [!tip] Cross-fitting and ML
> To reduce overfitting bias with ML nuisances, use sample splitting and cross-fitting (orthogonalized estimation). See [[double machine learning]] and [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].

## Relation to other estimators

- [[Inverse Probability Weighting (IPW)|IPW]]: uses only propensity weights; sensitive to extreme weights/misspecification.
- Outcome regression: uses only m_d(X); sensitive to model misspecification.
- AIPW: combines both; consistent if either is correct; often more stable.
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]: targeted update of outcome regressions to solve the EIF estimating equation; asymptotically equivalent under regularity, sometimes better finite-sample behavior.
- [[double machine learning]]: orthogonal moments + cross-fitting with ML for nuisances; closely related to AIPW.

## AIPW in DiD (DR-DiD)

- For panel or repeated cross-sections, “doubly robust DiD” augments the DiD with OR and IPW components, yielding consistency if either the propensity of being (not-yet-)treated or the outcome model is correct (conditional parallel trends).
- Implementations:
  - R: [[drdid]] package (functions like `drdid_panel`/`drdid_rc`)
  - Stata: `csdid, method(dripw)` (DR IPW) alongside cohort-time aggregation; see [[Callaway–Sant’Anna estimator]]

> [!warning] DiD assumptions
> Need [[parallel trends assumption]] (possibly conditional on X), correct timing, and [[No spillovers]]/[[interference]].

## Diagnostics and good practice

- Check overlap and weight stability:
  - Summarize weights: min/median/max; effective sample size (ESS)
  - Consider trimming/truncation (e.g., PS in [0.01, 0.99]) or overlap weights
- Check residual fit for OR models; flexible forms and interactions
- Report both AIPW and companion IPW/OR results for robustness
- Cluster SEs when data are clustered; use [[few-cluster corrections]] if G is small

## Common pitfalls

> [!warning] Avoid these
> - Using post-treatment covariates or mediators in X (violates identification)
> - Severe lack of overlap leading to unstable estimates (trim or redefine target)
> - Relying on a single parametric form for both nuisances without checks
> - Ignoring clustering/serial correlation in SEs
> - Not using cross-fitting when nuisances are high-dimensional ML

## Minimal code snippets

> [!example] R: AIPW for ATE (manual)

```r
# Nuisance models
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
ps <- pmax(pmin(ps_mod$fitted.values, 0.995), 0.005)

m1 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==1))
m0 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==0))
m1hat <- predict(m1, newdata = df)
m0hat <- predict(m0, newdata = df)

# AIPW ATE
aipw <- mean((m1hat - m0hat) + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps))

# Influence-function SE (iid)
phi <- (m1hat - m0hat) + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps) - aipw
se  <- sqrt(var(phi) / nrow(df))
ci  <- aipw + c(-1,1)*1.96*se
```

> [!example] R: Doubly robust DiD (repeated cross-sections, drdid)

```r
# install.packages("drdid")
library(drdid)
out <- drdid::drdid_rc(yname = "Y", tname = "Post", idname = "id", dname = "D",
                       xformla = ~ X1 + X2 + X3, data = df)
summary(out)  # ATT-type DiD with DR properties
```

> [!example] Stata: AIPW (cross-sectional) and DR DiD

```stata
* Cross-sectional ATE via AIPW
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), ate vce(robust)

* ATT
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), atet vce(robust)

* DR DiD (Callaway–Sant’Anna style)
csdid Y, ivar(id) time(time) gvar(G) method(dripw) vce(cluster id)
estat event
```

> [!example] Python: DR learner (AIPW-like)

```python
# pip install econml
from econml.dr import DRLearner
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

Y = df['Y'].values
T = df['D'].values
X = df[['X1','X2','X3']].values

dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(random_state=123),
               random_state=123)
dr.fit(Y, T, X=X)
ate = dr.ate(X).mean()
print(ate)
```

## Copy-ready snippets

- ATE AIPW:
$$
\widehat{ATE}_{AIPW} = \frac{1}{N}\sum_i\left[\hat m_1(X_i)-\hat m_0(X_i) + \frac{D_i(Y_i-\hat m_1(X_i))}{\hat e(X_i)} - \frac{(1-D_i)(Y_i-\hat m_0(X_i))}{1-\hat e(X_i)}\right]
$$

- ATT AIPW (one form):
$$
\widehat{ATT}_{AIPW} =
\frac{1}{N_1}\sum_{i:D_i=1}\!\big(Y_i - \hat m_0(X_i)\big)
- \frac{1}{N_1}\sum_{i:D_i=0}\!\frac{\hat e(X_i)}{1-\hat e(X_i)}\big(Y_i - \hat m_0(X_i)\big)
$$

- EIF-based SE (iid):
$$
\widehat{\mathrm{Var}}(\hat\theta) = \frac{1}{N^2}\sum_i (\hat\phi_i - \bar\phi)^2
$$

## Reporting essentials

- Estimand (ATE/ATT) and target population
- Nuisance specifications for $\hat e(X)$ and $\hat m_d(X)$; whether ML and cross-fitting were used
- Overlap diagnostics and any trimming/stabilization
- Inference details (SE type, clustering, few-cluster corrections if applicable)
- Robustness to alternative nuisance models and specifications

---

Related notes to create:
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Doubly Robust estimators]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[double machine learning]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[covariates]]
- [[matching]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[drdid]]
- [[Callaway–Sant’Anna estimator]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[bad controls]]