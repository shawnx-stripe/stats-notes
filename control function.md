---
title: Control Function
aliases: [control function, control function approach, two-step control function]
tags: [econometrics, iv, estimation]
updated: 2026-03-05
---

# Control Function

> [!summary]
> Two-step method for handling endogeneity: first-stage residuals (capturing endogenous variation) are included as additional regressors in the second stage. More flexible than [[Two-Stage Least Squares (2SLS)|2SLS]] for nonlinear models; allows heteroskedasticity-based identification.

## Two-stage procedure

**Stage 1**: Regress the endogenous variable $D$ on instruments $Z$ and controls $X$:
$$
D_i = \pi_0 + Z_i'\pi_1 + X_i'\pi_2 + v_i
$$
Save the residuals $\hat{v}_i = D_i - \hat{D}_i$.

**Stage 2**: Include $\hat{v}_i$ as a control in the outcome equation:
$$
Y_i = \beta_0 + \beta_1 D_i + X_i'\beta_2 + \gamma \hat{v}_i + \epsilon_i
$$

Under exogeneity of $Z$, $\hat{\beta}_1$ is consistent. Standard errors must account for the generated regressor.

> [!tip]
> The control function approach extends naturally to probit, logit, and other nonlinear models where 2SLS is inconsistent. It also allows testing exogeneity via the significance of $\gamma$.

## Minimal code snippets

```r
# R: Control function with lm + ivreg for comparison
library(ivreg)
stage1 <- lm(treatment ~ instrument + controls, data = df)
df$resid <- residuals(stage1)
stage2 <- lm(outcome ~ treatment + controls + resid, data = df)

# Compare with 2SLS
iv_model <- ivreg(outcome ~ treatment + controls | instrument + controls, data = df)
```

```python
# Python: two-stage control function
from statsmodels.api import OLS, add_constant

# Stage 1
X1 = add_constant(df[['instrument', 'controls']])
stage1 = OLS(df['treatment'], X1).fit()
df['v_hat'] = stage1.resid

# Stage 2
X2 = add_constant(df[['treatment', 'controls', 'v_hat']])
stage2 = OLS(df['outcome'], X2).fit()
print(stage2.summary())
```

## Related notes

- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[Heckman correction]]
- [[exclusion restriction]]
