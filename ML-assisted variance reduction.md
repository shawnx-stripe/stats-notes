---
title: ML-assisted variance reduction
aliases: [MLRATE, ML variance reduction, machine learning variance reduction, ML-adjusted estimator, prediction-powered inference]
tags: [experimentation, ab-testing, variance-reduction, machine-learning, power, mde]
updated: 2026-06-17
---

# ML-assisted variance reduction

> [!summary] Quick definition
> ML-assisted variance reduction extends CUPED/ANCOVA by using flexible ML models (gradient boosting, neural networks) to predict outcomes from pre-treatment covariates, then adjusting the experiment analysis on the residuals. The variance reduction equals approximately $(1 - R^2_{\text{ML}})$, which can substantially exceed what a single pre-period mean achieves.

- Generalizes [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]: CUPED uses a linear baseline; ML methods use any predictor of the outcome.
- Key requirement: predictions must use only pre-treatment information (no [[leakage]]).
- Unbiasedness preserved: the treatment effect estimator remains unbiased regardless of ML model quality (the model only affects variance, not bias).

---

## Intuition

Standard CUPED adjusts with $\hat{Y} = f(X_{\text{pre}})$ where $f$ is linear. ML variance reduction replaces the linear model with a flexible predictor:

$$
Y_i^{\star} = Y_i - \hat{m}(X_i^{\text{pre}})
$$

where $\hat{m}$ is trained to predict $Y$ from pre-treatment features. The treatment effect is estimated on residuals $Y^{\star}$:

$$
\hat{\tau} = \bar{Y}^{\star}_{\text{treat}} - \bar{Y}^{\star}_{\text{control}}
$$

> [!note] Why unbiased?
> Because $\hat{m}$ depends only on pre-treatment covariates (independent of treatment assignment under randomization), subtracting predictions preserves the treatment effect in expectation. The ML model acts as a variance sponge, not a bias source.

---

## Core approach

1. **Feature engineering**: collect rich pre-treatment features (historical metrics, engagement patterns, user attributes, seasonality indicators).
2. **Train predictor**: fit $\hat{m}(X^{\text{pre}}) \approx Y$ using control data or pre-period data. Use cross-fitting to avoid overfitting bias.
3. **Residualize**: compute $Y_i^{\star} = Y_i - \hat{m}(X_i^{\text{pre}})$ for all units.
4. **Analyze**: run standard difference-in-means or regression on $Y^{\star}$ with appropriate SEs.

---

## Variance reduction factor

$$
\frac{\operatorname{Var}(\hat{\tau}_{\text{ML}})}{\operatorname{Var}(\hat{\tau}_{\text{raw}})} \approx 1 - R^2_{\text{ML}}
$$

where $R^2_{\text{ML}}$ is the out-of-sample predictive $R^2$ of the ML model for the outcome.

- Linear CUPED: $R^2 \approx 0.3\text{–}0.5$ (single pre-period mean).
- ML-assisted: $R^2 \approx 0.5\text{–}0.8$ with rich features and nonlinear models.
- Effective MDE shrinks by $\sqrt{1 - R^2}$.

---

## Cross-fitting for valid inference

To avoid overfitting bias in $\hat{m}$:

1. Split data into $K$ folds.
2. For each fold $k$, train $\hat{m}_{-k}$ on all other folds.
3. Predict $\hat{m}_{-k}(X_i)$ for units in fold $k$.
4. Use these out-of-fold predictions for residualization.

This mirrors the [[cross-fitting]] approach in [[double machine learning]].

---

## Practical workflow

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingRegressor
import statsmodels.api as sm

def ml_variance_reduction(df, outcome_col, treatment_col, pre_features, n_folds=5):
    """ML-assisted variance reduction with cross-fitting."""
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    df = df.copy()
    df['y_pred'] = np.nan

    X_pre = df[pre_features].values
    y = df[outcome_col].values

    # Cross-fitted predictions
    for train_idx, val_idx in kf.split(X_pre):
        model = GradientBoostingRegressor(
            n_estimators=200, max_depth=5, learning_rate=0.1,
            subsample=0.8, random_state=42
        )
        model.fit(X_pre[train_idx], y[train_idx])
        df.iloc[val_idx, df.columns.get_loc('y_pred')] = model.predict(X_pre[val_idx])

    # Residualize
    df['y_residual'] = df[outcome_col] - df['y_pred']

    # Treatment effect on residuals
    treat = df[df[treatment_col] == 1]['y_residual']
    control = df[df[treatment_col] == 0]['y_residual']
    tau_hat = treat.mean() - control.mean()

    # SE (pooled)
    se = np.sqrt(treat.var() / len(treat) + control.var() / len(control))

    # Compare to raw
    raw_treat = df[df[treatment_col] == 1][outcome_col]
    raw_control = df[df[treatment_col] == 0][outcome_col]
    se_raw = np.sqrt(raw_treat.var() / len(raw_treat) + raw_control.var() / len(raw_control))

    variance_reduction = 1 - (se / se_raw) ** 2

    return {
        'tau_hat': tau_hat,
        'se': se,
        'se_raw': se_raw,
        'variance_reduction_pct': variance_reduction * 100,
        'r_squared_ml': 1 - df['y_residual'].var() / df[outcome_col].var()
    }
```

---

## Comparison with CUPED

| Method | Predictor | Typical $R^2$ | Complexity |
|--------|-----------|---------------|------------|
| Raw difference-in-means | None | 0 | Trivial |
| CUPED (scalar) | Pre-period mean | 0.3–0.5 | Low |
| CUPED (multi-covariate) | Linear combination | 0.4–0.6 | Low |
| ML-assisted | GBM/NN on rich features | 0.5–0.8 | Moderate |

> [!tip] When to use ML over CUPED
> - Many pre-treatment features with nonlinear relationships to the outcome.
> - Outcome is predictable but not well-captured by a single pre-period metric.
> - Marginal sensitivity gains matter (e.g., large experiment portfolio, expensive traffic).

---

## Industry implementations

- **Netflix (MLRATE)**: uses ML predictions to reduce variance in streaming engagement experiments.
- **LinkedIn**: extends CUPED with ML-based covariates for feed ranking experiments.
- **Airbnb**: combines with [[interleaving experiments]] for ranking model evaluation.
- **Microsoft ExP**: supports covariate adjustment with flexible models in their experimentation platform.

---

## Diagnostics

> [!check] Validation steps
> - [ ] All features in $\hat{m}$ are strictly pre-treatment (no [[leakage]])
> - [ ] Cross-fitting used (out-of-fold predictions)
> - [ ] Report out-of-sample $R^2$ and variance reduction achieved
> - [ ] Compare adjusted vs. raw estimates (point estimate should be similar; SE should shrink)
> - [ ] Check that residuals are balanced across treatment groups (SRM-like check on residuals)
> - [ ] Sensitivity to model choice (try linear, GBM, and NN; results should agree on $\hat{\tau}$)

---

## Common pitfalls

> [!warning]
> - Using post-treatment features in the ML model ([[leakage]]) — invalidates unbiasedness.
> - Not cross-fitting — overfitting inflates apparent $R^2$ and can distort SEs.
> - Confusing variance reduction with bias correction — ML adjustment does not fix confounding.
> - Over-investing in model tuning when $R^2$ gains are marginal (diminishing returns past ~0.7).
> - Applying to ratio metrics without proper delta-method adjustment.

---

## Related notes

- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]
- [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[cross-fitting]] · [[double machine learning]]
- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]

---

## References

- Deng, Xu, Kohavi, & Walker (2013). "Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data." (CUPED)
- Poyarkov et al. (2016). "Boosted Decision Tree Regression Adjustment for Variance Reduction in Online Controlled Experiments." KDD.
- Guo et al. (2021). "Machine Learning for Variance Reduction in Online Experiments." NeurIPS.
