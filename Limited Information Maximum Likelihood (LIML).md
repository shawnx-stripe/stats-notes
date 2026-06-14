---
title: Limited Information Maximum Likelihood (LIML)
aliases:
  - Limited Information Maximum Likelihood
  - k-class estimator (LIML)
  - LIML
  - limited information maximum likelihood
tags:
  - econometrics
  - iv
  - estimation
updated: 2026-03-03
---

# Limited Information Maximum Likelihood (LIML)

> [!summary] Quick definition
> Limited Information Maximum Likelihood (LIML) is a k-class [[Instrumental Variables (IV)]] estimator that is less biased than [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] when instruments are many or weak. It sets k equal to the smallest eigenvalue of a particular matrix ratio, which makes it approximately median-unbiased even when 2SLS is severely biased toward OLS.

---

## k-class framework

All k-class estimators take the form:

$$
\hat\beta_k = \big(X'(I - k M_Z)X\big)^{-1}\, X'(I - k M_Z) y
$$

where $M_Z = I - P_Z$ is the residual-maker from the instrument projection. Special cases:
- $k=0$: OLS
- $k=1$: 2SLS
- $k=\hat\lambda_{\min}$: LIML

where $\hat\lambda_{\min}$ is the smallest eigenvalue of $(W'M_{X_1}W)^{-1}(W'M_{[X_1,Z]}W)$, with $W = [Y, X_2]$.

---

## Why LIML over 2SLS

| Property | 2SLS | LIML |
|----------|------|------|
| Finite-sample bias | Can be large with many/weak IVs | Approximately median-unbiased |
| Asymptotic distribution | Same | Same (first-order equivalent) |
| Many instruments | Bias → OLS | Robust |
| Sensitivity to outliers | Less sensitive | Slightly more sensitive (fatter tails) |

> [!tip] When to prefer LIML
> - Many instruments relative to sample size
> - [[weak instruments]] concern (first-stage F marginal)
> - Over-identified models where you want robustness to instrument proliferation

> [!warning] Downside
> LIML confidence intervals can be wider and the estimator has no moments (heavier tails than 2SLS), so point estimates may be less stable in small samples.

---

## Minimal code snippets

> [!example] R

```r
library(AER)
fit <- ivreg(y ~ x1 + x2 | x1 + z1 + z2 + z3, data = df, method = "LIML")
summary(fit, diagnostics = TRUE)
```

> [!example] Stata

```stata
ivregress liml y (x2 = z1 z2 z3) x1, vce(robust)
estat firststage
```

> [!example] Python

```python
from linearmodels.iv import IVLIML
mod = IVLIML.from_formula('y ~ 1 + x1 + [x2 ~ z1 + z2 + z3]', data=df)
res = mod.fit(cov_type='robust')
print(res.summary)
```

---

## Related notes

- [[Instrumental Variables (IV)]] · [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[weak instruments]]
- [[Anderson–Rubin]] · [[exclusion restriction]] · [[relevance]]
- [[Causal Inference (MOC)]] · [[Econometrics (MOC)]]
