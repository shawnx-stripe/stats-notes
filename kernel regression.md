---
title: Kernel regression
aliases:
- Kernel smoothing
- Nadaraya-Watson estimator
- Local constant regression
- Nonparametric regression
- Kernel density regression
- Kernel Regression
- Kernel regression
tags:
- statistics
- nonparametric
- machine-learning
- smoothing
- regression
updated: 2025-09-26
---

# Kernel regression

> [!summary] Quick definition
> A nonparametric method that estimates the conditional expectation E[Y|X=x] by taking a weighted average of nearby observations, where weights decrease smoothly with distance from x. The kernel function determines the weight shape, and bandwidth controls the neighborhood size.

## Core idea and estimator

### Nadaraya-Watson estimator
$$
\hat{m}(x) = \frac{\sum_{i=1}^n K_h(x - X_i) Y_i}{\sum_{i=1}^n K_h(x - X_i)}
$$

where:
- K_h(u) = (1/h)K(u/h) is the scaled kernel
- K(·) is the kernel function
- h is the bandwidth (smoothing parameter)

### Intuition
- At each point x, fit a local constant (weighted mean)
- Weights determined by kernel function K and bandwidth h
- Larger h → smoother fit (more bias, less variance)
- Smaller h → wigglier fit (less bias, more variance)

## Kernel functions

| Kernel | Formula K(u) | Properties |
|--------|--------------|------------|
| **Gaussian** | $(2\pi)^{-1/2} \exp(-u^2/2)$ | Smooth, unbounded support, differentiable |
| **Epanechnikov** | $\frac{3}{4}(1-u^2) \cdot \mathbf{1}\{|u| \leq 1\}$ | Optimal MSE, compact support |
| **Uniform** | $\frac{1}{2} \cdot \mathbf{1}\{|u| \leq 1\}$ | Simple, discontinuous derivative |
| **Triangular** | $(1-|u|) \cdot \mathbf{1}\{|u| \leq 1\}$ | Linear decay, continuous |

Valid kernels: non-negative, integrate to 1, symmetric, decreasing in |u|.

## Bandwidth selection

### Cross-validation
$$
\text{CV}(h) = \frac{1}{n} \sum_{i=1}^n (Y_i - \hat{m}_{-i}(X_i))^2
$$

### Plug-in (AMSE-optimal)
$$
h_{\text{opt}} = \left(\frac{R(K)}{\mu_2^2 \cdot R(m'') \cdot n}\right)^{1/5}
$$

### Rules of thumb
- **Silverman's rule**: h = 0.9 × min(σ, IQR/1.34) × n^(-1/5)
- **Scott's rule**: h = 3.5σ × n^(-1/3)

> [!tip] Bandwidth trade-offs
> - Undersmoothing (h too small): High variance, captures noise
> - Oversmoothing (h too large): High bias, misses features
> - Optimal h balances bias² and variance

## Extensions

### Local polynomial regression
Fits local polynomials of degree p:
$$
\hat{m}(x) = \hat{\beta}_0 \text{ where } (\hat{\beta}_0, \ldots, \hat{\beta}_p) = \arg\min_\beta \sum_{i=1}^n K_h(X_i - x) \left(Y_i - \sum_{j=0}^p \beta_j(X_i-x)^j\right)^2
$$

- p = 0: Local constant (Nadaraya-Watson)
- p = 1: [[local linear regression|Local linear regression]] (reduces boundary bias)
- p = 2: Local quadratic

### Multivariate kernel regression
For d-dimensional X, use product kernel K(x) = ∏_{j=1}^d K(x_j) or spherical kernel with bandwidth matrix H. Performance degrades rapidly for d > 3–4 (curse of dimensionality).

## Statistical properties

### Bias and variance (interior point)
$$
\text{Bias}[\hat{m}(x)] \approx \frac{h^2}{2} m''(x) \int u^2 K(u) du
$$
$$
\text{Var}[\hat{m}(x)] \approx \frac{\sigma^2(x)}{nhf(x)} \int K(u)^2 du
$$

MSE-optimal bandwidth: h ∝ n^(-1/5).

### Asymptotic distribution
$$
\sqrt{nh} \left( \hat{m}(x) - m(x) - \text{Bias} \right) \xrightarrow{d} N\left(0, \frac{\sigma^2(x) \int K(u)^2 du}{f(x)}\right)
$$

### Boundary effects
Near boundaries: increased bias, slower convergence. Solutions: boundary kernels, [[local linear regression]], reflection.

## Comparison with other methods

| Method | Kernel Regression | [[splines|Splines]] | [[Local linear]] | [[LOESS]] | [[Gaussian process]] |
|--------|------------------|------------|-----------------|-----------|---------------------|
| **Flexibility** | High | Medium | High | High | Very high |
| **Boundary** | Poor | Good | Good | Good | Good |
| **Computation** | O(n²) | O(n) | O(n²) | O(n²) | O(n³) |
| **Uncertainty** | Available | Available | Available | Limited | Natural |

## Common pitfalls

> [!warning] Things to avoid
> - **Curse of dimensionality**: Performance degrades rapidly with d > 3-4
> - **Extrapolation**: Poor performance outside data range
> - **Discrete predictors**: Need special kernels or methods
> - **Heteroskedasticity**: Consider weighted kernel regression

## Copy-ready formulas

- Nadaraya-Watson:
$$
\hat{m}(x) = \frac{\sum_{i=1}^n K_h(x - X_i) Y_i}{\sum_{i=1}^n K_h(x - X_i)}
$$

- Gaussian kernel:
$$
K_h(u) = \frac{1}{h\sqrt{2\pi}} \exp\left(-\frac{u^2}{2h^2}\right)
$$

- MSE decomposition:
$$
\text{MSE}(x) = \frac{h^4}{4}[m''(x)]^2 \mu_2^2 + \frac{\sigma^2(x)R(K)}{nhf(x)}
$$

## Minimal code snippets

```python
# Python: statsmodels kernel regression
from statsmodels.nonparametric.kernel_regression import KernelReg

kr = KernelReg(Y, X, var_type='c', reg_type='lc', bw='cv_ls')
# var_type: 'c'=continuous, 'd'=discrete; reg_type: 'lc'=local constant, 'll'=local linear
Y_pred, _ = kr.fit(X_grid)
```

```r
# R: np package with CV bandwidth
library(np)
bw <- npregbw(Y ~ X, regtype = "lc", bwmethod = "cv.ls")
model <- npreg(bw)
plot(model, plot.errors.method = "asymptotic")
```

```stata
* Stata: local polynomial and kernel regression
lpoly Y X, degree(0) kernel(epanechnikov)
npregress kernel Y X, kernel(gaussian)
```

---

Related notes to create:
- [[local linear regression]]
- [[local polynomial regression]]
- [[bandwidth selection]]
- [[kernel density estimation]]
- [[LOESS]]
- [[splines]]
- [[Gaussian process]]
- [[cross-validation]]
- [[curse of dimensionality]]
- [[partial linear models]]
