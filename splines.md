---
title: Splines
aliases: [splines, Splines, basis splines, B-splines, natural splines, regression splines]
tags: [econometrics, nonparametric, machine-learning, estimation]
updated: 2026-03-05
---

# Splines

> [!summary]
> Piecewise polynomial functions joined smoothly at knot points. Used for flexible modeling of nonlinear relationships; includes B-splines, natural splines, and penalized (smoothing) splines.

## Structure

A degree-$d$ spline with knots $\{t_1, \ldots, t_K\}$ is:

$$
f(x) = \sum_{j=0}^d \beta_j x^j + \sum_{k=1}^K \gamma_k (x - t_k)_+^d
$$

where $(u)_+ = \max(0, u)$. Natural splines add boundary constraints (linear beyond outer knots). B-splines use a different basis for numerical stability.

## Minimal code

```python
from sklearn.preprocessing import SplineTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# Natural cubic spline with 5 knots
model = make_pipeline(
    SplineTransformer(n_knots=5, degree=3, extrapolation='linear'),
    LinearRegression()
)
model.fit(X.reshape(-1, 1), y)
```

> [!tip] When to use
> - Flexible nonparametric regression (alternative to kernel methods)
> - Modeling dose-response curves in experiments
> - RDD with flexible polynomial approximations
> - Knot selection: use quantiles of $X$ or cross-validation

## Comparison

- **B-splines**: Numerically stable, local support
- **Natural splines**: Linear extrapolation, better boundary behavior
- **Smoothing splines**: Penalized, auto-select effective knots

## Related notes

- [[kernel regression]]
- [[regularization]]
- [[Generalized Linear Model (GLM)|GLM]]
- [[Model Estimation (MOC)]]
