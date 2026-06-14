---
title: G-Formula
aliases: [g-formula, g-computation, standardization, parametric g-formula]
tags: [causal-inference, estimation]
updated: 2026-03-05
---

# G-Formula

> [!summary]
> Identification and estimation method that standardizes (integrates) an outcome model over the covariate distribution. Also called g-computation or standardization. One component of [[Doubly Robust estimators]]; requires correct outcome model specification.

## Formula and estimation

Under [[Unconfoundedness]], the ATE is:
$$
\tau = \mathbb{E}[\mathbb{E}[Y \mid D=1, X] - \mathbb{E}[Y \mid D=0, X]]
$$

**G-formula** replaces conditional expectations with fitted models:
$$
\hat{\tau} = \frac{1}{n} \sum_{i=1}^n \left[\hat{\mu}(1, X_i) - \hat{\mu}(0, X_i)\right]
$$
where $\hat{\mu}(d, x)$ is the fitted outcome model.

> [!tip]
> The g-formula is equivalent to outcome regression [[Outcome regression (OR)|OR]] but emphasizes the standardization step. It generalizes to longitudinal settings with time-varying confounding (g-formula algorithm or sequential regression).

## Minimal code snippets

```python
# Python: g-formula for ATE
from sklearn.ensemble import RandomForestRegressor

# Fit outcome model
mu = RandomForestRegressor().fit(df[['X', 'D']], df['Y'])

# Predict under both treatment assignments
df_1 = df.copy(); df_1['D'] = 1
df_0 = df.copy(); df_0['D'] = 0
tau_hat = (mu.predict(df_1[['X', 'D']]) - mu.predict(df_0[['X', 'D']])).mean()
print(f"ATE: {tau_hat:.3f}")
```

```r
# R: g-formula with gam
library(mgcv)
m <- gam(Y ~ s(X1) + s(X2) + D, data = df)
df$mu1 <- predict(m, newdata = transform(df, D = 1))
df$mu0 <- predict(m, newdata = transform(df, D = 0))
ate <- mean(df$mu1 - df$mu0)
cat("ATE:", ate, "\n")
```

## Related notes

- [[Outcome regression (OR)]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Doubly Robust estimators]]
- [[potential outcomes]]
