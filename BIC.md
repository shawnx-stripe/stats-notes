---
title: BIC
aliases: [BIC, Bayesian information criterion, Schwarz criterion, SIC]
tags: [econometrics, model-selection, estimation]
updated: 2026-03-05
---

# BIC

> [!summary]
> Bayesian Information Criterion: model selection criterion that penalizes complexity more heavily than [[AIC]]. $\text{BIC} = -2\ln L + k\ln n$. Consistent for model selection (selects true model as $n\to\infty$).

## AIC vs BIC comparison

| Criterion | Penalty | Asymptotic property | Typical use |
|-----------|---------|-------------------|-------------|
| AIC | $2k$ | Efficient (min prediction error) | Forecasting, large models |
| BIC | $k\ln n$ | Consistent (finds true model) | Hypothesis testing, parsimony |

For $n > 8$, BIC penalizes parameters more heavily than AIC, favoring smaller models. In practice, report both: AIC for prediction-focused applications, BIC for theory testing.

## R

```r
model <- lm(y ~ x1 + x2 + x3, data = df)
AIC(model); BIC(model)
```

## Related notes

- [[AIC]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
- [[Model Estimation (MOC)]]
