---
title: double machine learning
aliases: [DML, Double ML, orthogonal machine learning, orthogonalization & cross-fitting]
tags: [causal-inference, machine-learning, doubly-robust, nuisance-models, orthogonal, cross-fitting, plr, pliv, ate, cate, iv]
updated: 2025-09-17
---

# double machine learning

> [!summary] Quick definition
> Double Machine Learning (DML; Chernozhukov et al. 2018) uses Neyman-orthogonal scores plus cross-fitting to combine flexible ML for nuisance functions with valid √N inference for target causal parameters (ATE/ATT, partially linear regression coefficients, IV/LATE, etc.). Orthogonality makes the estimator insensitive to small nuisance errors; cross-fitting avoids overfitting bias.

- Works with many ML learners (forests/boosting/lasso/nets) for nuisance models.
- Covers ATE/ATT (AIPW-style), partially linear regression (PLR), IV (PLIV), and heterogeneous effects (meta-learners).

---

## Core ideas

- Orthogonal (Neyman-orthogonal) score ψ(θ, η) satisfies
$$
\left.\frac{\partial}{\partial \eta}\ \mathbb{E}\big[\psi(W;\theta_0,\eta)\big]\right|_{\eta=\eta_0} = 0,
$$
so small nuisance errors (η̂−η0) affect ψ only in higher order terms.

- Cross-fitting: split data into K folds; fit nuisances on K−1 folds, predict on held-out fold; stack residuals/scores across folds. This prevents using the same data for training and evaluation.

---

## Canonical models and scores

### 1) ATE with binary treatment (AIPW/DML)
- Nuisances: propensity $e(X)=P(D=1|X)$, outcomes $m_d(X)=E[Y|D=d,X]$.
- Cross-fitted score (per i):
$$
\psi_i = \big(m_1(X_i)-m_0(X_i)\big)
+ \frac{D_i\,[Y_i-m_1(X_i)]}{e(X_i)}
- \frac{(1-D_i)\,[Y_i-m_0(X_i)]}{1-e(X_i)}.
$$
- Estimator: $\hat\theta = \frac{1}{N}\sum_i \psi_i$; SE via IF variance.

Properties: doubly robust; orthogonal; √N if nuisances converge at $o_p(N^{-1/4})$.

---

### 2) Partially Linear Regression (PLR)
Structural model:
- $Y = \theta_0 D + g_0(X) + \xi$, with $E[\xi|X,D]=0$
- $D = m_0(X) + v$, with $E[v|X]=0$.

Orthogonal/partialling-out score:
$$
\psi_i(\theta) = \big(D_i - m_0(X_i)\big)\,\big(Y_i - g_0(X_i) - \theta\, (D_i - m_0(X_i))\big).
$$
Estimator (cross-fitted):
1) Fit $\hat g(X)$ and $\hat m(X)$; get residuals $\tilde Y=Y-\hat g(X)$, $\tilde D=D-\hat m(X)$ on held-out folds.
2) Regress $\tilde Y$ on $\tilde D$ by OLS:
$$
\hat\theta_{PLR} = \frac{\sum \tilde D_i \tilde Y_i}{\sum \tilde D_i^2}.
$$
SE from OLS on cross-fitted residuals (or IF).

---

### 3) Partially Linear IV (PLIV)
Structural:
- $Y = \theta_0 D + g_0(X)+\xi$, endogenous $D$.
- Instrument $Z$ with $E[\xi|Z,X]=0$.

Orthogonal score (one form):
- Let $r_0(X)=E[Z|X]$, and $g_0(X)=E[Y|X]$,
$$
\psi_i(\theta) = \big(Z_i - r_0(X_i)\big)\,\big(Y_i - g_0(X_i) - \theta D_i\big).
$$
Estimator (cross-fitted):
- Regress residualized $Y-ĝ(X)$ on $D$ using instrument $(Z-r̂(X))$ (2SLS on residuals).
- SE via sandwich with cross-fitted residuals.

Variants use optimal instrument $E[D|Z,X]-E[D|X]$ or two-stage residualized forms.

---

### 4) Heterogeneous effects (CATE / meta-learners)
- X-/R-/DR-learners and causal forests combine orthogonalization and cross-fitting to learn τ(x)=E[Y(1)−Y(0)|X=x].
- Policy learning builds treatment rules π(X) from τ̂(x); see [[policy learning]].

---

## Cross-fitting in practice

- K-fold (K=2,5) is typical; larger K gains efficiency at higher compute cost.
- Tune hyperparameters within the training folds only (nested CV).
- Stack fold-level predictions to form out-of-fold $\hat e,\hat m,\hat r$ etc. for every observation.

---

## Software

### Python
- doubleml (PLR/PLIV/IRM/IRM-ATE)
```python
from doubleml import DoubleMLData, DoubleMLPLR, DoubleMLPLIV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV, LogisticRegression

# PLR
dml_data = DoubleMLData(df, y_col='Y', d_cols='D', x_cols=['X1','X2','X3'])
ml_g = RandomForestRegressor(n_estimators=500, max_depth=5, random_state=0)
ml_m = RandomForestRegressor(n_estimators=500, max_depth=5, random_state=0)
plr = DoubleMLPLR(dml_data, ml_g=ml_g, ml_m=ml_m, n_folds=5)
plr.fit(); print(plr.summary)

# PLIV
dml_iv = DoubleMLData(df, y_col='Y', d_cols='D', x_cols=['X1','X2'], z_cols=['Z'])
ml_y = RandomForestRegressor(); ml_d = RandomForestRegressor(); ml_z = RandomForestRegressor()
pliv = DoubleMLPLIV(dml_iv, ml_g=ml_y, ml_m=ml_d, ml_r=ml_z, n_folds=5)
pliv.fit(); print(pliv.summary)
```
- econml (DRLearner / DMLATEIV for ATE/LATE and CATE)
```python
from econml.dr import DRLearner
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

dr = DRLearner(model_propensity=LogisticRegression(max_iter=2000),
               model_regression=RandomForestRegressor(random_state=0))
dr.fit(Y=df['Y'], T=df['D'], X=df[['X1','X2','X3']])
print('ATE:', dr.ate(df[['X1','X2','X3']]).mean())
```

### R
- DoubleML (PLR/PLIV/IRM, etc.)
```r
library(DoubleML); library(mlr3); library(mlr3learners)
dml_data <- DoubleMLData$new(df, y_col="Y", d_cols="D", x_cols=c("X1","X2","X3"))

lrn_g <- lrn("regr.ranger", num.trees=500, max.depth=5)
lrn_m <- lrn("regr.ranger", num.trees=500, max.depth=5)
plr <- DoubleMLPLR$new(dml_data, ml_g = lrn_g, ml_m = lrn_m, n_folds = 5)
plr$fit(); plr$summary()
```
- grf (causal forests) for CATE/meta-learning.

---

## Assumptions and requirements

- Design/identification:
  - ATE/ATT: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[Unconfoundedness]], [[Overlap]].
  - PLR: partially linear structure; $E[\xi|X,D]=0$ given $X$ sufficient; overlap in $D|X$.
  - PLIV: valid instrument ([[exclusion restriction]], [[relevance]]), and monotonicity for LATE if interpreting local effects.
- ML/nuisance quality:
  - Nuisances converge sufficiently fast on compact support; avoid gross misspecification.
  - No leakage: only pre-treatment covariates and correct timing.

---

## Inference

- Influence-function (IF) variance:
$$
\widehat{\text{Var}}(\hat\theta) = \frac{1}{N^2}\sum_{i} (\hat\psi_i - \bar\psi)^2
$$
- Clustered data: aggregate IF by cluster and use cluster-robust variance; apply [[few-cluster corrections]] if clusters are few.
- Bootstrap: pairs/bootstrap of IF scores (cluster bootstrap for panels).

---

## Diagnostics and good practice

> [!check]
> - [ ] Overlap/positivity: PS tails; effective sample size (ESS); trim or restrict if needed  
> - [ ] Out-of-fold performance: AUC for ê(X), R² for m̂(X); detect gross failures  
> - [ ] Weight/score stability: extreme $1/\hat e(X)$ weights? cap/clip or add regularization  
> - [ ] Sensitivity to learner class: RF vs GBM vs lasso; report robustness  
> - [ ] Placebos: pre-period “treatment” leads near zero; negative control outcomes  
> - [ ] Heterogeneity sanity: smooth τ̂(x); avoid overinterpretation without uncertainty bands

---

## Common variants at a glance

- IRM / DR-IRM (DML for ATE with orthogonal scores; equivalent to AIPW with cross-fitting).
- PLR (residual-on-residual OLS).
- PLIV (residualized 2SLS with ML instruments/controls).
- DMLATEIV / Local IV (econml) for LATE with IV and heterogeneous effects.
- CATE DML (R-/DR-learners) for uplift and [[policy learning]].

---

## Pitfalls

> [!warning]
> - Skipping cross-fitting (same data for training and prediction) → overfitting bias  
> - Using post-treatment covariates (see [[bad controls]])  
> - Severe lack of overlap (propensity near 0/1) → unstable; trim/redefine target  
> - Treating learned τ̂(x) as truth without uncertainty; report intervals or aggregated CATE with SEs  
> - Ignoring clustered/time dependence; use appropriate SEs  
> - Interpreting PLR as fully nonparametric—partial linear structure is an assumption

---

## Reporting essentials

- Design/estimand (ATE/ATT/PLR/PLIV/LATE/CATE) and identification assumptions
- Nuisance learners (algorithms, hyperparameters), K-fold cross-fitting scheme
- Overlap diagnostics (PS histograms, ESS) and any trimming/clipping
- Main estimate with IF-based SEs (and clustering level); sensitivity to learner choices
- Robustness: alternative learner sets, sample restrictions, placebo checks
- For IV: instrument strength (first-stage), [[relevance]]/[[exclusion restriction]] rationale
- For CATE/policy: policy value via OPE, fairness/constraints (see [[policy learning]])

---

## Copy-ready formulas

- AIPW/ATE score:
$$
\psi_i = (m_1-m_0) + \frac{D_i(Y_i-m_1)}{e} - \frac{(1-D_i)(Y_i-m_0)}{1-e}
$$
- PLR residual regression:
$$
\hat\theta = \frac{\sum (D-\hat m)(Y-\hat g)}{\sum (D-\hat m)^2}
$$
- PLIV orthogonal moment:
$$
\mathbb{E}\big[(Z-r_0(X))\,(Y-g_0(X) - \theta D)\big] = 0
$$

---

## References (quick)
- Chernozhukov et al. (2018), “Double/Debiased ML for Treatment and Structural Parameters”
- Nie & Wager (2021), “Quasi-Oracle Estimation of Heterogeneous Treatment Effects”
- Athey & Imbens (2016–2019), meta-learners and causal forests

---

## Related notes

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Doubly Robust estimators]]
- [[propensity score]] · [[Inverse Probability Weighting (IPW)|IPW]]
- [[Instrumental Variables (IV)]] · [[Local Average Treatment Effect (LATE)|LATE]] · [[exclusion restriction]] · [[relevance]] · [[monotonicity]]
- [[treatment effect heterogeneity]] · [[policy learning]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[Causal Inference (MOC)]] · [[ML for Econometrics (MOC)]]

---