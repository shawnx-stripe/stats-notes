---
title: local polynomial regression
aliases:
  - Local polynomial regression
  - local polynomial estimator
  - local polynomial fit
tags:
  - nonparametric
  - smoothing
  - rdd
  - econometrics
updated: 2026-03-05
---

# local polynomial regression

> [!summary] Quick definition
> Local polynomial regression fits a polynomial of degree $p$ via weighted least squares within a kernel window of [[bandwidth selection|bandwidth]] $h$ around each evaluation point. Order $p=1$ gives [[local linear regression]]; higher orders ($p=2,3$) reduce boundary bias further and are used for bias-correction in robust RD inference (Calonico, Cattaneo & Farrell). The choice of $p$ and $h$ jointly controls the bias-variance trade-off.

## Overview

Local polynomial regression is a **nonparametric smoothing technique** that generalizes [[local linear regression]] by fitting higher-degree polynomials locally. It provides flexible estimation of smooth functions $m(x) = E[Y|X=x]$ without imposing global functional form assumptions.

The estimator fits a polynomial of degree $p$ within a kernel-weighted neighborhood of each evaluation point $x_0$:

$$
\min_{\alpha_0, \alpha_1, \ldots, \alpha_p} \sum_{i=1}^n K\left(\frac{X_i - x_0}{h}\right) \left[ Y_i - \sum_{j=0}^p \alpha_j (X_i - x_0)^j \right]^2
$$

The **local polynomial estimate** at $x_0$ is:

$$
\hat{m}(x_0) = \hat{\alpha}_0(x_0)
$$

That is, the intercept of the local polynomial fit.

## Generalization of Local Linear

Local polynomial regression nests several common estimators:

| Polynomial Order $p$ | Name | Typical Use Case |
|---------------------|------|------------------|
| $p = 0$ | Local constant (Nadaraya-Watson) | Interior estimation (deprecated for RDD) |
| $p = 1$ | **[[local linear regression|Local linear]]** | **Standard for RDD estimation** |
| $p = 2$ | Local quadratic | Bias correction in robust RDD inference |
| $p = 3$ | Local cubic | Higher-order bias correction |
| $p \geq 4$ | Local higher-order | Rarely used (variance dominates) |

**Key insight**: Higher-order polynomials ($p \geq 2$) reduce bias at the cost of increased variance. The optimal choice of $p$ depends on the smoothness of $m(\cdot)$ and sample size.

## Polynomial Degree Choice: Bias-Variance Tradeoff

### Bias

For a local polynomial estimator of order $p$ estimating $m(x_0)$:

$$
\text{Bias}(\hat{m}(x_0)) \approx \frac{h^{p+1}}{(p+1)!} m^{(p+1)}(x_0) \cdot \mu_{p+1}(K)
$$

where $m^{(p+1)}$ is the $(p+1)$-th derivative of $m$ and $\mu_{p+1}(K) = \int u^{p+1} K(u) du$.

**Implication**: Bias decreases as $p$ increases (assuming $m$ is smooth), with rate $O(h^{p+1})$.

### Variance

The variance of $\hat{m}(x_0)$ is approximately:

$$
\text{Var}(\hat{m}(x_0)) \approx \frac{\sigma^2(x_0) \cdot \nu_0(K)}{n h f(x_0) \cdot [V_p]_{00}}
$$

where:
- $\nu_0(K) = \int K(u)^2 du$ (kernel variance constant)
- $[V_p]_{00}$ is the $(0,0)$ element of the variance matrix for order-$p$ polynomials
- $f(x_0)$ is the density of $X$ at $x_0$

**Implication**: Variance **increases** as $p$ increases, because fitting higher-order polynomials requires more parameters, increasing estimation uncertainty.

### Tradeoff

| Polynomial Order | Bias | Variance | MSE |
|-----------------|------|----------|-----|
| **Low $p$** (e.g., $p=1$) | Higher ($O(h^2)$) | Lower | Good for small $n$, rough $m(\cdot)$ |
| **High $p$** (e.g., $p=3$) | Lower ($O(h^4)$) | Higher | Good for large $n$, smooth $m(\cdot)$ |

**Practical guidance**:
- Use $p=1$ ([[local linear regression]]) as the **default** for RDD and most applications
- Use $p=2$ or $p=3$ for **bias correction** in robust inference (e.g., `rdrobust` with bias-corrected CIs)
- Higher $p$ requires larger bandwidth $h$ to avoid over-fitting (variance explosion)

> [!tip] Rule of thumb
> - **For point estimation**: Use $p=1$ (local linear)
> - **For bias correction**: Use $p+1$ (e.g., $p=2$ if main estimate uses $p=1$)
> - Rarely use $p > 3$ unless $n$ is very large and $m(\cdot)$ is known to be very smooth

## $p$ vs $p+1$: Estimation vs Inference

Modern RDD practice uses **two polynomial orders**:

1. **Order $p$ for main estimate**: Provides the point estimate $\hat{\tau}$ with optimal MSE
2. **Order $p+1$ for bias correction**: Constructs bias-corrected confidence intervals with better coverage

**Example (Calonico, Cattaneo & Titiunik 2014)**:

- Main RD estimate: Local linear ($p=1$) with bandwidth $h$
- Bias estimate: Local quadratic ($p=2$) with bandwidth $b > h$
- Bias-corrected estimate: $\hat{\tau}_{\text{bc}} = \hat{\tau}_p - \widehat{\text{Bias}}_p$

This procedure ensures:
- Point estimate has low MSE (using $p=1$)
- Confidence interval has correct coverage (accounting for bias using $p=2$)

**Why not use $p=2$ directly for the main estimate?**

While $p=2$ has lower bias, it has **higher variance**, so its MSE may be worse. The two-step procedure combines the best of both: MSE-optimal point estimate ($p=1$) with valid inference (bias correction from $p=2$).

> [!check] Modern RDD inference
> The **rdrobust** package (Calonico, Cattaneo, Titiunik, et al.) implements this approach:
> - Conventional estimate: Local linear ($p=1$)
> - Robust estimate: Local linear + bias correction from local quadratic ($p=2$)
> - Bandwidth selection: MSE-optimal for main estimate, larger bandwidth for bias correction

## Mean Squared Error

For a local polynomial estimator of order $p$ with bandwidth $h$:

$$
\text{MSE}(\hat{m}(x_0)) = \text{Bias}^2(\hat{m}(x_0)) + \text{Var}(\hat{m}(x_0))
$$

$$
\approx C_1 h^{2(p+1)} + \frac{C_2}{nh}
$$

where $C_1$ depends on $m^{(p+1)}(x_0)$ and $C_2$ depends on $\sigma^2(x_0)$.

**MSE-optimal bandwidth** balances these terms:

$$
h^* = \arg\min_h \text{MSE}(\hat{m}(x_0)) \propto n^{-1/(2p+3)}
$$

which gives:

$$
\text{MSE}(\hat{m}(x_0)) = O(n^{-2(p+1)/(2p+3)})
$$

**Convergence rates**:

| Order $p$ | Optimal $h^*$ | MSE rate | Common use |
|-----------|--------------|----------|------------|
| $p=0$ | $n^{-1/3}$ | $n^{-2/3}$ | Local constant (not recommended for RDD) |
| $p=1$ | $n^{-1/5}$ | $n^{-4/5}$ | **Local linear (standard)** |
| $p=2$ | $n^{-1/7}$ | $n^{-6/7}$ | Bias correction |
| $p=3$ | $n^{-1/9}$ | $n^{-8/9}$ | Higher-order bias correction |

Higher $p$ improves convergence rate but requires larger sample sizes to achieve lower MSE in practice.

## Relation to RDD

In [[Regression Discontinuity Design (RDD)|RDD]], the treatment effect at cutoff $c$ is estimated as:

$$
\hat{\tau} = \hat{m}(c^+) - \hat{m}(c^-)
$$

**Standard approach** (Hahn, Todd & van der Klaauw 2001; Imbens & Lemieux 2008):
- Use local linear ($p=1$) on each side of $c$
- Select bandwidth $h$ using MSE-optimal criterion (e.g., Imbens-Kalyanaraman)

**Robust inference approach** (Calonico, Cattaneo & Titiunik 2014):
- Main estimate: Local linear ($p=1$) with bandwidth $h_{\text{MSE}}$
- Bias correction: Local quadratic ($p=2$) with bandwidth $b > h$
- Construct bias-corrected CI: $\hat{\tau}_{\text{bc}} \pm 1.96 \cdot \widehat{\text{SE}}_{\text{robust}}$

**Why not use the same bandwidth for estimation and bias correction?**

The bias-correction bandwidth $b$ is chosen to estimate $\widehat{\text{Bias}}(\hat{\tau})$, not $\tau$ itself. Using $b > h$ ensures the bias estimate is consistent while keeping variance low for the main estimate.

> [!example] rdrobust output
> When you run `rdrobust(y, x, c=0, p=1)`, you get:
> - **Conventional estimate**: Local linear with $h_{\text{MSE}}$
> - **Robust estimate**: Bias-corrected using local quadratic with $b > h$
> - **Robust CI**: Accounts for bias, typically wider than conventional CI but has correct coverage

## Minimal Code Snippets

### R (rdrobust)

```r
library(rdrobust)

# Local polynomial RDD with bias-corrected inference
rd_fit <- rdrobust(
  y = data$outcome,
  x = data$running_var,
  c = 0,
  p = 1,                # order for point estimate (local linear)
  q = 2,                # order for bias correction (local quadratic)
  kernel = "triangular",
  bwselect = "mserd",   # MSE-optimal bandwidth
  vce = "hc1"           # robust SE
)

summary(rd_fit)

# Key outputs:
# - Conventional: Local linear estimate (may be biased)
# - Bias-corrected: Robust estimate with bias correction
# - Bandwidth h: for main estimate
# - Bandwidth b: for bias correction (b > h)
# - Robust CI: Use this for inference

# Change polynomial order
rd_quad <- rdrobust(y, x, c=0, p=2, q=3)  # local quadratic + cubic bias correction
```

### R (KernSmooth)

For general local polynomial regression (not RDD-specific):

```r
library(KernSmooth)

# Local polynomial fit
fit <- locpoly(
  x = data$running_var,
  y = data$outcome,
  degree = 1,           # polynomial order (0=constant, 1=linear, ...)
  kernel = "normal",
  bandwidth = 2
)

# Plot
plot(fit, type = "l", xlab = "X", ylab = "m(x)")
```

### Stata (rdrobust)

```stata
* Local polynomial RDD with robust inference
rdrobust outcome running_var, c(0) p(1) q(2) kernel(triangular) bwselect(mserd)

* Key outputs stored in e():
* e(tau_cl): conventional estimate (local linear)
* e(tau_bc): bias-corrected estimate
* e(h_l), e(h_r): MSE-optimal bandwidths (left, right)
* e(b_l), e(b_r): bias-correction bandwidths

* Display bias-corrected estimate with robust CI
di "Bias-corrected estimate: " e(tau_bc)
di "Robust 95% CI: [" e(ci_l_rb) ", " e(ci_r_rb) "]"
```

### Stata (lpoly)

For general local polynomial smoothing:

```stata
* Local polynomial plot
lpoly outcome running_var, ///
    degree(1) ///           /* polynomial order */
    kernel(epan) ///
    bwidth(2) ///
    ci ///                  /* show confidence interval */
    noscatter
```

### Python (rdrobust via rpy2)

```python
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

rdrobust = importr('rdrobust')

# Run local polynomial RDD
result = rdrobust.rdrobust(
    y=ro.FloatVector(data['outcome']),
    x=ro.FloatVector(data['running_var']),
    c=0,
    p=1,  # local linear
    q=2,  # bias correction with local quadratic
    kernel='triangular'
)

# Print summary
print(rdrobust.summary_rdrobust(result))
```

### Python (statsmodels, manual implementation)

```python
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

def local_polynomial(X, Y, x0, h, p=1, kernel='triangular'):
    """
    Local polynomial regression of order p at point x0.

    Parameters:
    - X: running variable (n,)
    - Y: outcome (n,)
    - x0: evaluation point
    - h: bandwidth
    - p: polynomial order (0=constant, 1=linear, 2=quadratic, ...)
    - kernel: 'triangular', 'epanechnikov', or 'gaussian'
    """
    u = (X - x0) / h

    # Kernel weights
    if kernel == 'triangular':
        weights = np.maximum(0, 1 - np.abs(u))
    elif kernel == 'epanechnikov':
        weights = np.maximum(0, 0.75 * (1 - u**2))
    elif kernel == 'gaussian':
        weights = np.exp(-0.5 * u**2) / np.sqrt(2 * np.pi)

    # Design matrix: [1, (X-x0), (X-x0)^2, ..., (X-x0)^p]
    idx = weights > 0
    X_local = X[idx] - x0
    Y_local = Y[idx]
    w = weights[idx]

    # Construct polynomial design matrix
    D = np.column_stack([X_local**j for j in range(p+1)])

    # Weighted least squares
    W = np.diag(w)
    beta = np.linalg.solve(D.T @ W @ D, D.T @ W @ Y_local)

    # Return intercept (estimate at x0) and all coefficients
    return beta[0], beta

# Example: Local linear (p=1)
m_hat, coefs = local_polynomial(X, Y, x0=0, h=2, p=1)
print(f"Local linear estimate at x0=0: {m_hat:.4f}")

# For RDD: estimate on both sides
m_left, _ = local_polynomial(X[X < 0], Y[X < 0], x0=0, h=2, p=1)
m_right, _ = local_polynomial(X[X >= 0], Y[X >= 0], x0=0, h=2, p=1)
tau_hat = m_right - m_left
print(f"RD estimate: {tau_hat:.4f}")
```

## Practical Guidelines

1. **Default choice**: Use $p=1$ ([[local linear regression]]) for RDD point estimates
   - Best bias-variance tradeoff in most applications
   - Standard in applied work since mid-2000s

2. **Bias-corrected inference**: Use $p=1$ for estimation, $p=2$ for bias correction
   - Implemented in `rdrobust` package (R and Stata)
   - Provides valid confidence intervals with correct coverage

3. **Bandwidth selection**: Use MSE-optimal $h$ for polynomial order $p$
   - Don't reuse the same $h$ across different $p$
   - Let `rdrobust` or similar packages choose bandwidths automatically

4. **Avoid global polynomials**: Never use $Y \sim \text{poly}(X, p) + D$ without local weighting
   - Global polynomials impose strong functional form assumptions
   - Highly sensitive to degree choice, especially near boundaries

5. **Report both conventional and robust estimates**: Show that results are not sensitive to bias correction

> [!warning] Don't use high-order polynomials without justification
> - $p \geq 4$ rarely improves MSE in finite samples (variance explodes)
> - If you need $p > 2$, you likely need more data or a different model
> - Higher $p$ does NOT automatically mean "better fit"—it's a bias-variance tradeoff

## Comparison Table

| Feature | Local Linear ($p=1$) | Local Quadratic ($p=2$) | Local Cubic ($p=3$) |
|---------|---------------------|------------------------|-------------------|
| **Bias rate** | $O(h^2)$ | $O(h^3)$ | $O(h^4)$ |
| **Variance** | Low | Medium | High |
| **Typical use** | Main RDD estimate | Bias correction | Rarely used |
| **Optimal $h$** | $n^{-1/5}$ | $n^{-1/7}$ | $n^{-1/9}$ |
| **MSE rate** | $n^{-4/5}$ | $n^{-6/7}$ | $n^{-8/9}$ |
| **Recommendation** | **Default** | Bias correction only | Large $n$ only |

## Related notes

- [[local linear regression]]
- [[Regression Discontinuity Design (RDD)]]
- [[bandwidth selection]]
- [[density test]]
- [[McCrary test]]
- [[covariate balance test]]
