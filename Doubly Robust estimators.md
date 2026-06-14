---
title: Doubly Robust Estimators
aliases:
- double robust
- DR estimators
- augmented estimators
- orthogonal estimators
- doubly robust
- DR
tags:
- causal-inference
- doubly-robust
- ate
- att
- tmle
- aipw
- dml
- did
updated: 2025-09-17
---

# Doubly Robust Estimators

> [!summary] Quick definition
> Doubly robust (DR) estimators combine an outcome model and a treatment/propensity model so that the target effect is consistently estimated if either model is correctly specified (not necessarily both), under [[Unconfoundedness]], [[Overlap]], and [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]. Examples include [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] (augmented IPW), [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], and [[double machine learning]] (DML).

- Targets: typically [[Average Treatment Effect (ATE)]] and [[Average Treatment Effect on the Treated (ATT)]]; DR variants also exist for [[Difference-in-Differences (DiD)]] (DR-DiD).
- Advantages:
  - Model-robustness: consistent if either nuisance model is correct.
  - Asymptotic efficiency when both are correct.
  - Natural influence-function–based standard errors and compatibility with ML via orthogonalization/cross-fitting.

## Core setup and assumptions

- Treatment D ∈ {0,1}, outcome Y, pre-treatment [[covariates]] X.
- Outcome regressions: m_d(X) = E[Y | D=d, X]
- [[propensity score]]: e(X) = P(D=1 | X)
- Identification requires:
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
  - [[Unconfoundedness]]: {Y(1), Y(0)} ⟂ D | X
  - [[Overlap]]: 0 < e(X) < 1 a.s.

## Canonical DR estimators

### 1) AIPW (Augmented IPW)
- ATE (copy-ready):
$$
\widehat{ATE}_{AIPW} = \frac{1}{N}\sum_{i}\Big[
\hat m_1(X_i)-\hat m_0(X_i)
+\frac{D_i\,(Y_i-\hat m_1(X_i))}{\hat e(X_i)}
-\frac{(1-D_i)\,(Y_i-\hat m_0(X_i))}{1-\hat e(X_i)}
\Big].
$$
- Doubly robust: consistent if either m_d or e is correct. See [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] for ATT forms and details.

### 2) TMLE (Targeted MLE)
- Uses initial Q̂ and ĝ plus a targeted “fluctuation” step to solve the efficient score equation and produce a plug-in estimate with influence-function (IF) inference. See [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].

### 3) Double Machine Learning (DML)
- Orthogonal moments + sample splitting ([[cross-fitting]]) allow flexible ML for nuisances while retaining valid inference. Closely related to AIPW’s influence-function form. See [[double machine learning]].

## DR for Difference-in-Differences (DR-DiD)

- Goal: identify ATT under DiD with conditional [[parallel trends assumption]]. DR-DiD remains consistent if either:
  - The outcome model for untreated potential outcomes is correct, or
  - The propensity of being (not-yet-)treated is correct.
- Implementations:
  - R: `drdid` package (panel or repeated cross-sections)
  - Stata: `csdid, method(dripw)` (Callaway–Sant’Anna DR-IPW)
- Use robust [[event study]] diagnostics, appropriate [[clustered standard errors]], and [[few-cluster corrections]] if needed.

## Influence function and inference

- DR estimators are often derived from efficient influence functions (EIF). For ATE, the EIF contribution is:
$$
\phi_i = \big[m_1(X_i)-m_0(X_i)\big]
+ \frac{D_i\,(Y_i-m_1(X_i))}{e(X_i)}
- \frac{(1-D_i)\,(Y_i-m_0(X_i))}{1-e(X_i)} - ATE.
$$
- Variance: use the sample variance of $\hat\phi_i$ divided by N (with clustering if applicable).

## Practical workflow

> [!check] Steps
> - [ ] Define estimand (ATE vs. ATT) and target population.
> - [ ] Specify pre-treatment X; avoid [[bad controls]].
> - [ ] Fit e(X) and m_d(X) flexibly (GLMs or ML); ensure [[Overlap]]/weight stability.
> - [ ] Use orthogonal/DR estimator (AIPW, TMLE, DML); prefer [[cross-fitting]] with ML.
> - [ ] Compute IF-based SEs; cluster by assignment when appropriate.
> - [ ] Report diagnostics: balance after weighting, PS overlap, weight summaries (min/max/ESS).

> [!tip] Overlap and stabilization
> - Clip/truncate extreme PS (e.g., to [0.01, 0.99]) or use stabilized/overlap weights.
> - Check effective sample size (ESS) and tail weights.

## Common pitfalls

> [!warning] Avoid these
> - Including post-treatment mediators (violates identification).
> - Severe lack of overlap (unstable weights) without trimming/redefining target.
> - Omitting [[cross-fitting]] when using high-capacity ML for nuisances.
> - Ignoring clustering/serial correlation in SEs (esp. DiD/panels).
> - Treating DR as a cure for design violations (e.g., breach of [[No spillovers]] or timing errors).

## Minimal code snippets

> [!example] R: AIPW (ATE) manual

```r
# Nuisance models
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, family = binomial(), data = df)
ps <- pmax(pmin(ps_mod$fitted.values, 0.995), 0.005)

m1 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==1))
m0 <- lm(Y ~ X1 + X2 + poly(X3,2) + X1:X2, data = subset(df, D==0))
m1hat <- predict(m1, newdata = df); m0hat <- predict(m0, newdata = df)

aipw <- mean( (m1hat - m0hat) + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps) )

# IF-based SE (iid)
phi <- (m1hat - m0hat) + df$D*(df$Y - m1hat)/ps - (1-df$D)*(df$Y - m0hat)/(1-ps) - aipw
se  <- sqrt(var(phi) / nrow(df))
```

> [!example] R: TMLE with Super Learner

```r
library(tmle); library(SuperLearner)
SL_lib <- c("SL.glm","SL.glmnet","SL.ranger")
fit <- tmle(Y=df$Y, A=df$D, W=df[,c("X1","X2","X3")],
            Q.SL.library=SL_lib, g.SL.library=SL_lib, gbound=c(0.01,0.99))
fit$estimates$ATE$psi; fit$estimates$ATE$CI
```

> [!example] R: DR DiD (repeated cross-sections)

```r
library(drdid)
out <- drdid_rc(yname="Y", tname="Post", idname="id", dname="D",
                xformla=~ X1 + X2 + X3, data=df)
summary(out)  # ATT-type DR-DiD
```

> [!example] Stata

```stata
* AIPW ATE
teffects aipw (Y X1 X2 c.X3##c.X3) (D X1 X2 c.X3##c.X3), ate vce(robust)

* DR DiD (Callaway–Sant’Anna)
csdid Y, ivar(id) time(time) gvar(G) method(dripw) vce(cluster id)
estat event
```

> [!example] Python: EconML DRLearner (ATE)

```python
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
\widehat{ATE}_{AIPW}=\frac{1}{N}\sum_i\left[\hat m_1(X_i)-\hat m_0(X_i)+\frac{D_i(Y_i-\hat m_1(X_i))}{\hat e(X_i)}-\frac{(1-D_i)(Y_i-\hat m_0(X_i))}{1-\hat e(X_i)}\right]
$$

- EIF variance (iid):
$$
\widehat{\mathrm{Var}}(\hat\theta)=\frac{1}{N^2}\sum_i(\hat\phi_i-\bar\phi)^2
$$

- DR-DiD intuition: consistent if either conditional trends (OR) or selection (PS) is correct.

## Reporting essentials

- Estimand (ATE/ATT), target population, and design (cross-section vs. DiD).
- Nuisance specifications (Q and g models), whether ML and [[cross-fitting]] were used.
- Overlap diagnostics (PS histograms, weight summaries, ESS) and any trimming/clipping.
- Inference details (IF-based, bootstrap, clustered SEs; [[few-cluster corrections]] if needed).
- Robustness to alternative nuisance models and specifications.

---

Related notes to create:
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[double machine learning]]
- [[cross-fitting]]
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[bad controls]]
- [[Difference-in-Differences (DiD)]]
- [[drdid]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[event study]]
- [[clustered standard errors]]
- [[few-cluster corrections]]