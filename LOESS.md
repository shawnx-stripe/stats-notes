---
title: LOESS
aliases: [LOESS, LOWESS, locally weighted scatterplot smoothing, local regression]
tags: [econometrics, nonparametric]
updated: 2026-03-05
---

# LOESS

> [!summary]
> Local polynomial regression method that fits weighted least-squares regressions in neighborhoods around each point. Weights decay with distance (tricube kernel). Useful for exploratory data analysis and flexible curve fitting.

## Method

At each point $x_0$, fit a weighted polynomial (typically degree 1 or 2):

$$
\hat{f}(x_0) = \arg\min_{\beta} \sum_{i=1}^n w_i(x_0) \left(y_i - \beta_0 - \beta_1 (x_i - x_0) - \cdots \right)^2
$$

**Tricube weight**: $w_i(x_0) = \left(1 - \left|\frac{x_i - x_0}{h}\right|^3\right)^3$ for $|x_i - x_0| < h$, else $0$.

Bandwidth $h$ determined by span parameter $\alpha \in (0, 1]$: use $\alpha \cdot n$ nearest neighbors.

> [!tip]
> - **Default span**: $\alpha = 0.75$ often works well
> - **Robustness**: LOESS can include iterative reweighting to downweight outliers
> - **Multivariate**: Extends to multiple predictors but suffers from curse of dimensionality

## Code

```python
from statsmodels.nonparametric.smoothers_lowess import lowess

# Fit LOESS with span = 0.3
smoothed = lowess(y, x, frac=0.3)
```

## Related notes

- [[kernel regression]]
- [[splines]]
