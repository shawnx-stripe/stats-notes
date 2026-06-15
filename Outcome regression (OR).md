---
title: Outcome regression (OR)
aliases:
  - Outcome modeling
  - Outcome regression estimator
  - G-formula (plug-in)
tags:
  - causal-inference
  - estimation
  - g-formula
  - regression
  - semiparametric
updated: 2025-09-27
---

# Outcome regression (OR)

> [!summary] Quick definition
> Estimate causal effects by modeling the conditional outcome given treatment and covariates, then averaging predicted potential outcomes over the target population. Also called g-computation or the g-formula plug-in. Consistent under [[Unconfoundedness]] and [[Overlap]] if the outcome models are correctly specified.

## Setup and notation

- Binary treatment W ∈ {0,1}, covariates X, outcome Y.
- Define outcome models (potential outcome regressions):
  - m₁(x) = E\[Y | W=1, X=x]
  - m₀(x) = E\[Y | W=0, X=x]
- Predict potential outcomes:
  - Ŷ₁(x) = m̂₁(x), Ŷ₀(x) = m̂₀(x)
- Average over a target sample to get effects (see estimands below).

Related: [[propensity score]], [[Inverse Probability Weighting (IPW)|IPW]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]]

## Identification and assumptions

- Ignorability ([[Unconfoundedness]]): (Y(1), Y(0)) ⟂ W | X
- Positivity ([[Overlap]]): 0 < P(W=1 | X) < 1 almost surely
- Correct specification of both outcome models m₁(x), m₀(x) (if using parametric OR)
- SUTVA/[[No spillovers]]: well-defined treatments and no interference

Under these, the g-formula identifies:
$$
\text{ATE} = \mathbb{E}\big[m_1(X) - m_0(X)\big], \quad
\text{ATT} = \mathbb{E}\big[Y - m_0(X) \mid W=1\big], \quad
\text{ATC} = \mathbb{E}\big[m_1(X) - Y \mid W=0\big]
$$

Related: [[g-formula]] (a.k.a. g-computation)

## Estimands and plug-in OR estimators

- ATE (population or sample ATE):
$$
\widehat{\text{ATE}}_{\text{OR}} = \frac{1}{n}\sum_{i=1}^n \Big(\hat{m}_1(X_i) - \hat{m}_0(X_i)\Big)
$$

- ATT (on treated):
$$
\widehat{\text{ATT}}_{\text{OR}} = \frac{1}{n_1}\sum_{i: W_i=1} \Big(Y_i - \hat{m}_0(X_i)\Big)
$$

- ATC (on controls):
$$
\widehat{\text{ATC}}_{\text{OR}} = \frac{1}{n_0}\sum_{i: W_i=0} \Big(\hat{m}_1(X_i) - Y_i\Big)
$$

- Dose–response (continuous treatment A):
  - Fit m(a,x) = E\[Y | A=a, X=x], then μ(a) = E\[m(a,X)] by averaging over X.

Target population note:
- Replace the averaging set with any target sample to estimate transported effects (report target explicitly).

## Modeling choices

- Separate models by arm: fit m̂₁ on treated data, m̂₀ on controls (“T-learner” flavor).
- One-joint model with interaction: E\[Y | W,X] = g(X) + W·τ(X) (yields m̂₁, m̂₀ as ĝ ± τ̂).
- Learners:
  - Parametric: linear/GLM, interactions, splines
  - Nonparametric/ML: trees, [[random forests]], [[kernel regression]], boosting, nets
- Good practice:
  - Use flexible models with regularization
  - Tune by cross-validation within arm
  - Avoid leakage/post-treatment covariates (see [[bad controls]])

## Inference and uncertainty

- Parametric models: model-based or sandwich SEs for plug-in contrasts.
- ML-based OR: naive plug-in CIs often anti-conservative; prefer:
  - Nonparametric bootstrap (respecting clustering/blocks if needed)
  - Influence-function-based methods via [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]/[[double machine learning]] for valid asymptotics with ML
- Always report uncertainty and diagnostics (fit, overlap).

Related: [[clustered standard errors]], [[bootstrap]]

## Diagnostics and validation

- Fit quality by arm: R²/Deviance, calibration (observed vs predicted), residual checks.
- Overlap: propensity score diagnostics ([[propensity score]], [[Overlap]]); highlight regions of extrapolation.
- Sensitivity to learner class and tuning; compare multiple flexible models.
- Stability: out-of-fold predictions; cross-fitting to mitigate overfitting bias in predictions.
- Subgroup performance: ensure m̂₀ is adequate on treated X-support for ATT, and m̂₁ adequate on control X-support for ATC.

## Strengths and limitations

Advantages:
- Efficient when outcome is well modeled; can substantially reduce variance.
- Naturally extends to multi-valued/continuous treatments (dose–response).
- Straightforward to incorporate nonlinearities and interactions.

Limitations:
- Model dependence: bias if m₁ or m₀ is mis-specified.
- Extrapolation risk in poor overlap regions (untestable).
- No double robustness: unlike [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], OR needs correct outcome models.

Tip:
- Use OR for exploration/initial estimates; for primary inference with ML, prefer [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] or [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] (doubly robust/targeted).

## Connections

- OR vs [[Inverse Probability Weighting (IPW)|IPW]]: dual approaches (model outcome vs model treatment). [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] combines both (doubly robust).
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] begins with an initial OR (“Q-model”) and targets it with a fluctuation step using the clever covariate.
- [[double machine learning]] uses orthogonalization (Robinson) around OR and propensity to enable ML with valid inference.
- Missing data analogue: outcome regression under MAR for imputation; see [[Missing Data and Selection (MOC)]], [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]].

## Copy-ready formulas

- G-formula (binary W):
$$
\mathbb{E}[Y(w)] = \mathbb{E}\big[ \mathbb{E}[Y \mid W=w, X] \big], \quad w\in\{0,1\}
$$

- OR ATE:
$$
\widehat{\text{ATE}}_{\text{OR}} = \frac{1}{n}\sum_{i=1}^n \big(\hat{m}_1(X_i) - \hat{m}_0(X_i)\big)
$$

- OR ATT/ATC:
$$
\widehat{\text{ATT}}_{\text{OR}} = \frac{1}{n_1}\sum_{W_i=1} \big(Y_i - \hat{m}_0(X_i)\big), \quad
\widehat{\text{ATC}}_{\text{OR}} = \frac{1}{n_0}\sum_{W_i=0} \big(\hat{m}_1(X_i) - Y_i\big)
$$

- Dose–response:
$$
\hat{\mu}(a) = \frac{1}{n}\sum_{i=1}^n \hat{m}(a, X_i), \quad a \in \mathcal{A}
$$

## Minimal code snippets (optional)

```r
# R: OR for ATE/ATT with separate arm models
# Fit outcome models
m1 <- glm(Y ~ s(X1) + X2 + X3, data = df[df$W==1,], family = gaussian())
m0 <- glm(Y ~ s(X1) + X2 + X3, data = df[df$W==0,], family = gaussian())

# Predict for all units
m1_hat <- predict(m1, newdata = df, type = "response")
m0_hat <- predict(m0, newdata = df, type = "response")

# ATE
ATE_or <- mean(m1_hat - m0_hat)

# ATT
ATT_or <- mean(df$Y[df$W==1] - m0_hat[df$W==1])
```

```python
# Python: OR with sklearn models
from sklearn.ensemble import RandomForestRegressor

treated = df[df.W==1]; control = df[df.W==0]
X_cols = [c for c in df.columns if c not in ['Y','W']]

m1 = RandomForestRegressor(n_estimators=500, random_state=42).fit(treated[X_cols], treated['Y'])
m0 = RandomForestRegressor(n_estimators=500, random_state=42).fit(control[X_cols], control['Y'])

m1_hat = m1.predict(df[X_cols])
m0_hat = m0.predict(df[X_cols])

ATE_or = (m1_hat - m0_hat).mean()
ATT_or = (treated['Y'] - m0_hat[df.W==1]).mean()
```

## Good practice checklist

> [!check] Implementation
> - [ ] State estimand (ATE/ATT/ATC/dose–response) and target population
> - [ ] Justify [[Unconfoundedness]] and assess [[Overlap]]
> - [ ] Fit separate arm models; tune by cross-validation
> - [ ] Use out-of-fold predictions to reduce bias
> - [ ] Report fit diagnostics by arm; examine extrapolation
> - [ ] Provide uncertainty (bootstrap) and sensitivity to learners
> - [ ] Consider [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] for primary inference

---

## Related notes
- [[g-formula]]
- [[dose–response function]]
- [[calibration plot]]
- [[cross-fitting|out-of-fold prediction]]
- [[model extrapolation]]
- [[model misspecification]]
