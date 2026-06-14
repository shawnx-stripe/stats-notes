---
title: AIC
aliases: [AIC, Akaike information criterion]
tags: [econometrics, model-selection, estimation]
updated: 2026-03-05
---

# AIC

> [!summary]
> Akaike Information Criterion: $\text{AIC} = -2\ln L + 2k$. Trades off goodness of fit against model complexity. Asymptotically equivalent to leave-one-out cross-validation. Efficient but not consistent for model selection.

## When to use

Use AIC when prediction accuracy matters more than finding the "true" model. AIC tends to select larger models than [[BIC]], which can improve out-of-sample fit but may include spurious predictors. For small samples, use the corrected version:

$$\text{AIC}_c = \text{AIC} + \frac{2k(k+1)}{n-k-1}$$

The model with the *lowest* AIC is preferred, but differences $\Delta\text{AIC} < 2$ indicate negligible evidence against the higher-AIC model.

## Python

```python
from statsmodels.api import OLS
model = OLS(y, X).fit()
print(f"AIC: {model.aic:.1f}, BIC: {model.bic:.1f}")
```

## Related notes

- [[BIC]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
- [[cross-validation]]
- [[Model Estimation (MOC)]]
