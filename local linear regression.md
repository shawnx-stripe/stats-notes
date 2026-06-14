---
title: local linear regression
aliases:
  - Local linear regression
  - Local linear
  - local linear estimator
  - local linear fit
tags:
  - nonparametric
  - smoothing
  - rdd
  - econometrics
updated: 2026-03-05
---

# local linear regression

> [!summary] Quick definition
> Local linear regression fits weighted least squares with a linear polynomial within a kernel window around each evaluation point. In [[Regression Discontinuity Design (RDD)|RDD]], it is the standard estimator at the cutoff because it has better boundary bias properties than local constant (Nadaraya-Watson) estimation. Combined with MSE-optimal [[bandwidth selection]], it forms the basis of modern RD estimation (Calonico, Cattaneo & Titiunik).

## Overview

Local linear regression is a **nonparametric smoothing method** that fits a linear function within a neighborhood of each point. It is the workhorse estimator for [[Regression Discontinuity Design (RDD)|RDD]] and other settings where global parametric models are inappropriate.

The key idea: to estimate $m(x_0) = E[Y|X=x_0]$ at a target point $x_0$, fit a weighted linear regression using only observations near $x_0$, with weights determined by a kernel function. This provides:

1. **Local flexibility**: Adapts to local curvature without imposing global structure
2. **Boundary correction**: Automatically adjusts bias at boundaries (critical for RDD)
3. **Interpretability**: Each estimate comes from a simple weighted regression

## Weighted Least Squares Formulation

To estimate $m(x_0)$ at a point $x_0$, solve:

$$
\min_{\alpha, \beta} \sum_{i=1}^n K\left(\frac{X_i - x_0}{h}\right) \left[ Y_i - \alpha - \beta(X_i - x_0) \right]^2
$$

where:
- $K(\cdot)$ is a **kernel function** (e.g., triangular, Epanechnikov)
- $h > 0$ is the **[[bandwidth selection|bandwidth]]** (window size)
- Observations far from $x_0$ receive lower weight $K\left(\frac{X_i - x_0}{h}\right)$

The **local linear estimate** is:

$$
\hat{m}(x_0) = \hat{\alpha}(x_0)
$$

That is, we use the **intercept** $\hat{\alpha}$ from the local regression, not $\hat{\alpha} + \hat{\beta} \cdot 0$.

> [!note] Why local **linear** and not local constant?
> Local constant (Nadaraya-Watson) would minimize:
> $$
> \min_{\alpha} \sum_{i=1}^n K\left(\frac{X_i - x_0}{h}\right) \left[ Y_i - \alpha \right]^2
> $$
> This gives $\hat{m}(x_0) = \sum_i w_i Y_i$ with kernel weights $w_i$.
>
> **Problem**: At boundary points (like cutoff $c$ in RDD), the kernel is asymmetric, inducing **boundary bias** of order $O(h)$. Local linear regression reduces this bias to $O(h^2)$ by fitting a slope that corrects for asymmetry.

## Kernel Choice

Common kernel functions $K(u)$ used in local linear regression:

| Kernel | Formula | Support | Properties |
|--------|---------|---------|-----------|
| **Uniform** | $K(u) = \frac{1}{2} \mathbb{1}[\lvert u \rvert \leq 1]$ | $[-1,1]$ | Simple; discontinuous |
| **Triangular** | $K(u) = (1 - \lvert u \rvert) \mathbb{1}[\lvert u \rvert \leq 1]$ | $[-1,1]$ | **Default for RDD** (Cattaneo et al.) |
| **Epanechnikov** | $K(u) = \frac{3}{4}(1 - u^2) \mathbb{1}[\lvert u \rvert \leq 1]$ | $[-1,1]$ | MSE-optimal for interior |
| **Gaussian** | $K(u) = \frac{1}{\sqrt{2\pi}} e^{-u^2/2}$ | $\mathbb{R}$ | Smooth; infinite support |

**Practical guidance**:
- **Triangular kernel** is standard in RDD because it has optimal MSE properties at boundary points
- Kernel choice typically has **small impact** relative to bandwidth choice
- All kernels give similar results if bandwidth is chosen appropriately

## Boundary Bias Advantage

Why local linear regression is preferred for RDD:

At an interior point $x_0$, both local constant and local linear have bias of order $O(h^2)$. But at a **boundary point** (like cutoff $c$ in sharp RDD):

| Estimator | Boundary Bias | Interior Bias |
|-----------|--------------|--------------|
| **Local constant** (Nadaraya-Watson) | $O(h)$ | $O(h^2)$ |
| **Local linear** | $O(h^2)$ | $O(h^2)$ |

The local linear estimator achieves this by effectively **reweighting** observations to account for asymmetry near the boundary. The slope parameter $\beta$ absorbs first-order bias, leaving only second-order terms.

> [!tip] Intuition for boundary correction
> Near a boundary, the kernel window is one-sided (e.g., only observations to the left of $c$ for $\lim_{x \uparrow c}$). A local constant fit would overweight observations further from $c$, inducing bias. The local linear fit adjusts for this by tilting the line to match the local slope, centering the estimate at $c$.

## Connection to Bandwidth Selection

The **bias-variance tradeoff** is controlled by bandwidth $h$:

- **Large $h$**: More observations in window → lower variance, higher bias (over-smoothing)
- **Small $h$**: Fewer observations → higher variance, lower bias (under-smoothing)

The **MSE-optimal bandwidth** balances these:

$$
h^* = \arg\min_h \text{MSE}(\hat{m}(x_0)) = \arg\min_h \left[ \text{Bias}^2(\hat{m}(x_0)) + \text{Var}(\hat{m}(x_0)) \right]
$$

For local linear regression:
- **Bias**: $\text{Bias}(\hat{m}(x_0)) \approx \frac{h^2}{2} m''(x_0) \mu_2(K)$, where $\mu_2(K) = \int u^2 K(u) du$
- **Variance**: $\text{Var}(\hat{m}(x_0)) \approx \frac{\sigma^2(x_0)}{nh f(x_0)} \nu_0(K)$, where $\nu_0(K) = \int K(u)^2 du$

Optimal bandwidth scales as:

$$
h^* \propto n^{-1/5}
$$

for interior points (standard nonparametric rate). See [[bandwidth selection]] for data-driven procedures (e.g., cross-validation, plug-in methods, Imbens-Kalyanaraman for RDD).

## MSE Properties

The local linear estimator $\hat{m}(x_0)$ satisfies:

$$
\text{MSE}(\hat{m}(x_0)) = O(h^4) + O\left(\frac{1}{nh}\right)
$$

where:
- $O(h^4)$ is **squared bias** (assuming $m(\cdot)$ is twice differentiable)
- $O\left(\frac{1}{nh}\right)$ is **variance**

With optimal bandwidth $h^* \propto n^{-1/5}$:

$$
\text{MSE}(\hat{m}(x_0)) = O(n^{-4/5})
$$

This is the standard **nonparametric convergence rate** for local polynomial estimators with $p=1$ (local linear).

## RDD Context

In [[Regression Discontinuity Design (RDD)|RDD]], the treatment effect at the cutoff $c$ is:

$$
\tau = \lim_{x \downarrow c} E[Y|X=x] - \lim_{x \uparrow c} E[Y|X=x] = m(c^+) - m(c^-)
$$

**Local linear RDD estimator**:

1. Estimate $\hat{m}(c^-)$ using local linear regression on observations with $X < c$ (left of cutoff)
2. Estimate $\hat{m}(c^+)$ using local linear regression on observations with $X \geq c$ (right of cutoff)
3. Compute $\hat{\tau} = \hat{m}(c^+) - \hat{m}(c^-)$

This is equivalent to a **single regression** with treatment dummy and interaction:

$$
Y_i = \alpha + \tau D_i + \beta_- (X_i - c) + \beta_+ D_i (X_i - c) + \varepsilon_i
$$

with kernel weights $K_h(X_i - c)$, where $D_i = \mathbb{1}[X_i \geq c]$. Then $\hat{\tau}$ is the coefficient on $D_i$.

> [!check] Why local linear is standard for RDD
> - **Boundary bias**: RDD estimation is always at a boundary (cutoff $c$), where local linear has optimal bias properties
> - **Robustness**: Less sensitive to bandwidth choice than local constant
> - **Inference**: Standard errors and confidence intervals are well-understood (Calonico, Cattaneo & Titiunik 2014)

## Minimal Code Snippets

### R (rdrobust)

The `rdrobust` package implements MSE-optimal local linear regression for RDD:

```r
library(rdrobust)

# Local linear RDD with MSE-optimal bandwidth
rd_result <- rdrobust(
  y = data$outcome,
  x = data$running_var,
  c = 0,                  # cutoff
  p = 1,                  # local linear (order 1)
  kernel = "triangular",  # default
  bwselect = "mserd",     # MSE-optimal bandwidth
  vce = "hc1"             # heteroskedasticity-robust SE
)

summary(rd_result)

# Key outputs:
# - Conventional estimate (local linear)
# - Bias-corrected estimate (using p=2 for bias correction)
# - Robust confidence interval
# - Bandwidths: h (main), b (bias-correction)

# Plot RD with local linear fit
rdplot(
  y = data$outcome,
  x = data$running_var,
  c = 0,
  p = 1,  # local linear
  kernel = "triangular"
)
```

### R (locfit)

For general local linear regression (not specific to RDD):

```r
library(locfit)

# Fit local linear model
fit <- locfit(
  outcome ~ lp(running_var, deg = 1),  # deg=1 for local linear
  data = data,
  kern = "triang",
  alpha = 0.5  # bandwidth (as fraction of data range)
)

# Predict at specific points
predict(fit, newdata = data.frame(running_var = 0))

# Plot
plot(fit)
```

### Stata (lpoly)

```stata
* Local linear regression plot
lpoly outcome running_var, ///
    degree(1) ///           /* local linear */
    kernel(triangle) ///
    bwidth(2) ///           /* bandwidth = 2 */
    noscatter ///           /* don't show points */
    at(running_var)         /* eval at observed X */

* For RDD, use rdrobust package
rdrobust outcome running_var, c(0) p(1) kernel(triangular)
```

### Stata (manual implementation)

```stata
* Generate weights for local linear at cutoff c=0
gen dist = abs(running_var - 0)
gen weight = max(0, 1 - dist/2) if dist <= 2  /* triangular kernel, h=2 */

* Demean running variable
gen x_demean = running_var - 0

* Run weighted regression
reg outcome i.treat##c.x_demean [aweight=weight] if dist <= 2

* Treatment effect is coefficient on treat
```

### Python (scipy, manual implementation)

```python
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.linear_model import LinearRegression

def local_linear(X, Y, x0, h, kernel='triangular'):
    """
    Local linear regression at point x0.

    Parameters:
    - X: running variable (n x 1)
    - Y: outcome (n x 1)
    - x0: evaluation point
    - h: bandwidth
    - kernel: 'triangular', 'epanechnikov', or 'gaussian'
    """
    # Compute distances
    u = (X - x0) / h

    # Kernel weights
    if kernel == 'triangular':
        weights = np.maximum(0, 1 - np.abs(u))
    elif kernel == 'epanechnikov':
        weights = np.maximum(0, 0.75 * (1 - u**2))
    elif kernel == 'gaussian':
        weights = np.exp(-0.5 * u**2) / np.sqrt(2 * np.pi)

    # Only use observations with positive weight
    idx = weights > 0
    X_local = X[idx] - x0  # demean
    Y_local = Y[idx]
    w_local = weights[idx]

    # Weighted least squares: Y ~ alpha + beta * (X - x0)
    model = LinearRegression()
    model.fit(
        X_local.reshape(-1, 1),
        Y_local,
        sample_weight=w_local
    )

    # Return intercept (estimate at x0)
    return model.intercept_

# Example usage
x0 = 0.0  # cutoff
h = 2.0   # bandwidth

# Estimate left and right limits
m_left = local_linear(X[X < x0], Y[X < x0], x0, h)
m_right = local_linear(X[X >= x0], Y[X >= x0], x0, h)

# RD estimate
tau_hat = m_right - m_left
print(f"RD estimate: {tau_hat:.4f}")
```

### Python (rdrobust via rpy2)

```python
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

rdrobust = importr('rdrobust')

# Run local linear RDD
result = rdrobust.rdrobust(
    y=ro.FloatVector(data['outcome']),
    x=ro.FloatVector(data['running_var']),
    c=0,
    p=1,  # local linear
    kernel='triangular'
)

# Print results
print(rdrobust.summary_rdrobust(result))
```

## Comparison with Other Estimators

| Estimator | Order | Boundary Bias | Use Case |
|-----------|-------|---------------|----------|
| **Local constant** (Nadaraya-Watson) | $p=0$ | $O(h)$ | Interior estimation; deprecated for RDD |
| **Local linear** | $p=1$ | $O(h^2)$ | **Standard for RDD**; general smoothing |
| **Local quadratic** | $p=2$ | $O(h^2)$ | Bias correction in robust RDD inference |
| **Local cubic** | $p=3$ | $O(h^2)$ | Higher-order bias correction |

See [[local polynomial regression]] for the general framework.

## Common Pitfalls

1. **Using global polynomial**: Never fit $Y = \alpha + \beta_1 X + \beta_2 X^2 + \ldots + \tau D$ globally. This imposes strong functional form assumptions. Always use local estimation.

2. **Ignoring boundary bias**: At cutoff $c$, using local constant (Nadaraya-Watson) induces $O(h)$ bias. Always use local linear (or higher order).

3. **Not reporting bandwidth**: Bandwidth $h$ is critical for replication. Always report the bandwidth used, and ideally show sensitivity to bandwidth choice.

4. **Cherry-picking bandwidth**: Selecting $h$ to maximize significance is invalid. Use data-driven methods (e.g., MSE-optimal, cross-validation) or pre-specify $h$.

5. **Over-interpreting slope coefficient**: In local linear regression, $\hat{\beta}$ is a nuisance parameter used for bias correction. The object of interest is $\hat{\alpha}$ (the intercept).

> [!example] Classic RDD application
> **Lee (2008)**: U.S. House elections. Uses local linear regression with triangular kernel and Imbens-Kalyanaraman bandwidth to estimate incumbency advantage. Shows that local linear estimates are robust to bandwidth choice, unlike global polynomial fits.

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[local polynomial regression]]
- [[bandwidth selection]]
- [[Wald estimator]]
- [[density test]]
- [[McCrary test]]
- [[covariate balance test]]
