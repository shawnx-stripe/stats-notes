---
title: cross-fitting
aliases: [crossfitting, out-of-fold prediction, sample-splitting, K-fold orthogonalization]
tags: [causal-inference, machine-learning, dml, aipw, tmle, uplift, policy-learning, nuisance-models, validation]
updated: 2025-09-17
---

# cross-fitting

> [!summary] Quick definition
> Cross-fitting (sample-splitting with out-of-fold prediction) is a procedure that fits nuisance functions (e.g., propensity e(X), outcome models m(X)) on a training fold and uses their predictions on a held-out fold. Stacking the out-of-fold predictions across K folds removes overfitting bias and enables √N-consistent inference with flexible ML in orthogonal estimators such as [[double machine learning]] (DML), [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], and [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].

- Goal: prevent “using the same data twice” (train + evaluate), which biases plug-in/DR estimators.
- Result: orthogonal scores behave as if nuisances were “fixed,” delivering valid asymptotics and robust inference.

---

## Why cross-fit?

- Nuisance models estimated with ML can overfit; evaluating scores on the same data leaks information, causing bias.
- Cross-fitting ensures each observation’s nuisance predictions come from a model that never saw that observation.
- With Neyman-orthogonal scores, cross-fitting yields √N rates under mild nuisance rates (often $o_p(N^{-1/4})$), enabling valid CIs.

See: [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].

---

## Core procedure (generic K-fold)

1) Split indices {1,…,N} into K roughly equal folds $I_1,\dots,I_K$.
2) For each fold ℓ:
   - Fit nuisances η̂^{(-ℓ)} on the complement $I_{-ℓ}=\{1,\dots,N\}\setminus I_\ell$.
     - Examples: $e(X)$, $m_0(X)$, $m_1(X)$; or $g(X)=E[Y|X]$, $m(X)=E[D|X]$ in PLR.
   - Predict η̂^{(-ℓ)} on the held-out fold $I_\ell$ to obtain out-of-fold predictions for those observations.
3) Stack all folds’ out-of-fold predictions into full-length vectors (each row predicted by a model trained without it).
4) Compute the orthogonal score ψ(W_i; θ, η̂_oof) and estimate θ (e.g., solve $\frac{1}{N}\sum_i\psi_i=0$, or run residual-on-residual OLS).
5) Get SEs from the influence function (IF) using the out-of-fold ψ_i (cluster-aware if needed).

> [!tip] K=2 (simple split) is OK; K=5 typically reduces variance with similar bias protection.

---

## Common use cases

- ATE/ATT (AIPW/DML): out-of-fold $\hat e(X), \hat m_0(X), \hat m_1(X)$ in the AIPW score.
- PLR (partialling out): out-of-fold residuals $\tilde Y=Y-\hat g(X)$ and $\tilde D=D-\hat m(X)$, then OLS of $\tilde Y$ on $\tilde D$.
- IV/PLIV: residualize $Y,D$ on $X$ out-of-fold; instrument residualized D with $(Z-\hat r(X))$ trained out-of-fold.
- CATE/[[uplift]]: meta-learners (R-/DR-/X-) compute pseudo-outcomes with out-of-fold nuisances; forests (e.g., econml’s CF-DML) do this internally.
- [[off-policy evaluation]] (OPE/DR): fit $m_a(X)$ and propensities out-of-fold; compute DR value scores with those predictions.

---

## Math snapshots (copy-ready)

- AIPW / DML ATE score (binary treatment):
$$
\psi_i =
\big(\hat m_1(X_i)-\hat m_0(X_i)\big)
+ \frac{D_i\big(Y_i-\hat m_1(X_i)\big)}{\hat e(X_i)}
- \frac{(1-D_i)\big(Y_i-\hat m_0(X_i)\big)}{1-\hat e(X_i)}.
$$

- PLR (partialling-out):
$$
\tilde Y_i = Y_i - \hat g(X_i),\quad
\tilde D_i = D_i - \hat m(X_i),\quad
\hat\theta = \frac{\sum_i \tilde D_i \tilde Y_i}{\sum_i \tilde D_i^2}.
$$

- IF variance:
$$
\widehat{\mathrm{Var}}(\hat\theta) = \frac{1}{N^2}\sum_i (\hat\psi_i - \bar\psi)^2,
$$
with cluster aggregation if clustered (see [[clustered standard errors]]).

---

## Practical guidance

> [!check] Best practices
> - [ ] Use out-of-fold predictions for every nuisance used in the score  
> - [ ] Tune ML hyperparameters using only training folds (nested CV); do not peek at held-out fold  
> - [ ] In time series: use blocked/rolling folds (no future leakage)  
> - [ ] In clustered data: use GroupKFold/leave-one-cluster-out folds to prevent cross-cluster leakage; cluster IFs for SEs  
> - [ ] Check overlap (propensity tails) and stabilize weights (trim/clip) if needed  
> - [ ] Report K, learners, tuning scheme, and random seeds

> [!warning] Pitfalls
> - Tuning hyperparameters on all data (leakage)  
> - Using the same out-of-fold nuisance for multiple estimands with mismatch in timing  
> - Ignoring group/time structure (users in both train and test folds)  
> - Small folds with high-capacity learners → unstable nuisances; reduce model complexity or K

---

## Minimal code snippets

> [!example] Python: K-fold cross-fitting for AIPW ATE

```python
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

X = df[['X1','X2','X3']].to_numpy()
D = df['D'].to_numpy().astype(int)
Y = df['Y'].to_numpy()
n = len(Y)

m0_hat = np.zeros(n); m1_hat = np.zeros(n); e_hat = np.zeros(n)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train, test in kf.split(X):
    # propensities
    prop = LogisticRegression(max_iter=2000).fit(X[train], D[train])
    e_hat[test] = prop.predict_proba(X[test])[:,1]
    # outcome models
    m0 = RandomForestRegressor(n_estimators=500, random_state=0).fit(X[train][D[train]==0], Y[train][D[train]==0])
    m1 = RandomForestRegressor(n_estimators=500, random_state=0).fit(X[train][D[train]==1], Y[train][D[train]==1])
    m0_hat[test] = m0.predict(X[test])
    m1_hat[test] = m1.predict(X[test])

e = np.clip(e_hat, 1e-3, 1-1e-3)
psi = (m1_hat - m0_hat) + D*(Y - m1_hat)/e - (1-D)*(Y - m0_hat)/(1-e)
theta = psi.mean()
se = psi.std(ddof=1)/np.sqrt(n)
print(theta, theta - 1.96*se, theta + 1.96*se)
```

> [!example] R: Cross-fitting for PLR (partialling-out)

```r
library(caret)
set.seed(42)
K <- 5
folds <- createFolds(df$Y, k = K, list = TRUE)

g_hat <- rep(NA, nrow(df)); m_hat <- rep(NA, nrow(df))
for (idx in folds) {
  train <- setdiff(seq_len(nrow(df)), idx)
  # g(X) ~ E[Y|X]
  gfit <- ranger::ranger(Y ~ X1 + X2 + X3, data = df[train,], num.trees = 500)
  g_hat[idx] <- predict(gfit, df[idx,])$predictions
  # m(X) ~ E[D|X]
  mfit <- glm(D ~ X1 + X2 + X3, data = df[train,], family = binomial())
  m_hat[idx] <- predict(mfit, df[idx,], type = "response")
}
Ytil <- df$Y - g_hat
Dtil <- df$D - m_hat
coef <- sum(Dtil*Ytil)/sum(Dtil^2)
# OLS on residuals for SEs
fit <- lm(Ytil ~ 0 + Dtil)
summary(fit)  # coef(Dtil) is PLR estimate with robust SEs if desired
```

> [!example] Python: Group K-fold (cluster-aware)

```python
from sklearn.model_selection import GroupKFold
groups = df['cluster_id'].to_numpy()
gkf = GroupKFold(n_splits=5)
for train, test in gkf.split(X, D, groups):
    # fit nuisances on train; predict on test; prevents cross-cluster leakage
    pass
```

> [!example] Time-aware cross-fitting (blocked)

```python
# Sort by time; split into contiguous folds so training is strictly before testing
# Use custom indices for rolling-origin evaluation
```

---

## Relation to other methods

- [[double machine learning]]: cross-fitting is a key component for orthogonal scores (ATE/PLR/PLIV/IRM).
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] / [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]: cross-fitting reduces bias in DR/TMLE when using ML nuisances.
- [[uplift]] / [[policy learning]] / [[off-policy evaluation]]: cross-fitting nuisances and scores helps prevent optimistic bias in model selection/evaluation.
- Not needed for simple parametric models with low flexibility, but harmless and often recommended when using ML.

---

## Diagnostics

> [!check]
> - [ ] Out-of-fold metrics: AUC for propensities, R² for outcome models  
> - [ ] Stability across K, seeds, and learners; report ranges  
> - [ ] Overlap diagnostics; ESS of weights if IPW is used  
> - [ ] Placebo checks when applicable (pre-period leads)  
> - [ ] Compare with non-cross-fitted estimates to gauge overfitting bias (should be close if models are simple)

---

## Reporting essentials

- K (number of folds), fold construction (random/stratified/blocked/grouped)
- Learners and hyperparameter tuning (nested CV within training folds)
- Exact nuisances cross-fitted (which functions were out-of-fold)
- Estimator used (AIPW/PLR/PLIV/CATE/POLICY DR OPE) and influence-function SEs
- Overlap diagnostics and any trimming/clipping
- Sensitivity to K, learners, seeds, and fold definitions (time/cluster-aware)

---

## Common pitfalls

> [!warning]
> - Hyperparameter tuning on full data (leakage) instead of within training folds  
> - Using cross-fit for some nuisances but not all used in the score  
> - Ignoring clustered/time structure in fold assignment  
> - Tiny folds with high-variance learners → unstable predictions and scores  
> - Applying cross-fitting but then reusing in-sample predictions elsewhere (secondary leakage)

---

## Related notes

- [[double machine learning]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[uplift]] · [[policy learning]] · [[off-policy evaluation]]
- [[Unconfoundedness]] · [[Overlap]] · [[leakage]] · [[bad controls]]
- [[clustered standard errors]] · [[few-cluster corrections]]

---