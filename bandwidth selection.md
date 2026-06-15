---
title: bandwidth selection
aliases:
  - Bandwidth selection
  - bandwidth choice
  - optimal bandwidth
tags:
  - nonparametric
  - rdd
  - smoothing
  - econometrics
updated: 2026-03-04
---

# bandwidth selection

> [!summary] Quick definition
> Bandwidth selection determines the window width $h$ around a point of interest (e.g., the cutoff in [[Regression Discontinuity Design (RDD)|RDD]]) for local estimation. Too small a bandwidth increases variance; too large introduces bias. MSE-optimal and coverage-error-optimal methods (e.g., Imbens-Kalyanaraman, Calonico-Cattaneo-Titiunik) automate this bias-variance trade-off.

---

## The bandwidth-variance tradeoff

In [[local linear regression]] or [[local polynomial regression]] at running variable value $x_0$:
$$
\hat\tau(x_0) = \arg\min_{\alpha, \beta} \sum_{i} K\left(\frac{X_i - x_0}{h}\right) (Y_i - \alpha - \beta(X_i - x_0))^2,
$$
where $K(\cdot)$ is a kernel (e.g., triangular, Epanechnikov) and $h > 0$ is the bandwidth.

**Bias-variance tradeoff**:
- **Small $h$**: few observations → high variance, low bias (wigglier estimate)
- **Large $h$**: many observations → low variance, high bias (oversmoothing)

**Mean Squared Error (MSE)**:
$$
\text{MSE}(h) = \text{Bias}^2(h) + \text{Variance}(h).
$$

Optimal $h$ minimizes MSE (or coverage error for inference).

---

## RDD context

In [[Regression Discontinuity Design (RDD)|RDD]], the treatment effect at cutoff $c$ is:
$$
\tau = \lim_{x \downarrow c} \mathbb{E}[Y \mid X=x] - \lim_{x \uparrow c} \mathbb{E}[Y \mid X=x].
$$

Estimate via [[local linear regression]] on either side of $c$ using observations within $[c-h, c+h]$.

**Key challenge**: choosing $h$ to balance:
- Bias from functional form misspecification (curvature in $\mathbb{E}[Y \mid X]$)
- Variance from limited sample size near $c$

---

## MSE-optimal bandwidth

**Imbens–Kalyanaraman (IK) bandwidth** (2012):

Minimizes asymptotic MSE of $\hat\tau$. Formula (simplified):
$$
h_{IK} = C \cdot N^{-1/5},
$$
where $C$ depends on:
- Variance of $Y$ (pooled or separate for treatment/control)
- Second derivative of conditional mean (curvature; estimated via pilot regressions)
- Kernel choice (triangular is default)

**Implementation**: plug in pilot estimates of variance and curvature.

**Pros**: theoretically justified for point estimation.

**Cons**:
- Optimizes MSE, not coverage of confidence intervals
- Can yield CIs with poor coverage (under-cover) in small samples

---

## Coverage Error Rate (CER) optimal bandwidth

**Calonico–Cattaneo–Titiunik (CCT) bandwidth** (2014, 2020):

Minimizes coverage error of confidence intervals (accounts for bias in inference).

**Key innovation**: robust bias correction and variance adjustment.

**CCT procedure**:
1. Use MSE-optimal $h$ for point estimate
2. Use larger bandwidth $b > h$ to estimate bias
3. Bias-corrected CI:
$$
\hat\tau - \hat{B}(h,b) \pm t_{\alpha/2} \cdot \widehat{\mathrm{SE}}(\hat\tau),
$$
where $\hat{B}$ is estimated bias using bandwidth $b$.

**Result**: CER-optimal $h$ is typically **smaller** than MSE-optimal (to reduce bias impact on coverage).

**Robust CI**: uses heteroskedasticity-robust SE and bias correction; yields valid coverage even with misspecification.

**Implementation**: `rdrobust` package (R/Stata) computes CCT bandwidth and robust CI by default.

---

## Practical bandwidth choices

| Method | Description | Use case |
|--------|-------------|----------|
| **IK** | MSE-optimal (Imbens-Kalyanaraman) | Point estimation; older standard |
| **CCT** | CER-optimal (Calonico-Cattaneo-Titiunik) | Inference; robust CIs; current standard |
| **ad-hoc** | $h = k \cdot \hat\sigma_X$ (e.g., $k \in [0.5, 2]$) | Quick sensitivity; not theoretically justified |
| **Cross-validation** | Minimize CV error | Rare in RDD (not tailored to discontinuity) |

> [!tip] Default recommendation
> Use **CCT bandwidth with robust bias-corrected CI** via `rdrobust`. It is now the standard in applied work.

---

## Sensitivity to bandwidth choice

**Why sensitivity matters**:
- Bandwidth choice is researcher discretion (though automated)
- Different bandwidths → different treatment effects
- Specification search / p-hacking risk

**Best practice**: report results for multiple bandwidths:
1. **Main result**: CCT optimal $h$
2. **Sensitivity**: $0.5h$, $h$, $1.5h$, $2h$
3. **Visual**: plot $\hat\tau(h)$ and CI as function of $h$ (rdrobust does this automatically)

**Interpretation**:
- If $\hat\tau$ stable across $h$: evidence of robustness
- If $\hat\tau$ varies widely: suggests sensitivity to functional form or local violations (e.g., sorting near cutoff)

---

## Bandwidth for other RDD tasks

**Density test (manipulation test)**:
- Check if density of running variable $X$ is continuous at $c$ (see [[density test]])
- Use McCrary (2008) or Cattaneo-Jansson-Ma (2020) bandwidth selection
- Typically use larger bandwidth than for treatment effect estimation

**Covariate balance**:
- Test if pre-treatment covariates are smooth at $c$ (placebo/falsification test)
- Use same bandwidth as main analysis or CCT-optimal for each covariate

---

## Code snippets

> [!example] R: rdrobust (CCT bandwidth)

```r
library(rdrobust)

# Default: CCT bandwidth, robust bias-corrected CI
rd <- rdrobust(y = outcome, x = running_var, c = cutoff)
summary(rd)

# Bandwidth used
rd$bws  # h (main) and b (bias estimation)

# Sensitivity to bandwidth: 0.5h, h, 1.5h
rd_half <- rdrobust(outcome, running_var, c = cutoff, h = rd$bws[1] * 0.5)
rd_1.5 <- rdrobust(outcome, running_var, c = cutoff, h = rd$bws[1] * 1.5)

# Plot estimate and CI as function of bandwidth
rdplot(outcome, running_var, c = cutoff, h = rd$bws[1])
```

> [!example] R: rdrobust with IK bandwidth

```r
# Use IK (MSE-optimal) instead of CCT
rd_ik <- rdrobust(outcome, running_var, c = cutoff, bwselect = "mserd")
summary(rd_ik)
```

> [!example] R: Manual bandwidth sensitivity table

```r
library(rdrobust)

h_seq <- c(0.5, 1, 1.5, 2) * rd$bws[1]
results <- lapply(h_seq, function(h) {
  rd_h <- rdrobust(outcome, running_var, c = cutoff, h = h)
  data.frame(
    bandwidth = h,
    estimate = rd_h$coef[1],
    se = rd_h$se[1],
    ci_lower = rd_h$ci[1,1],
    ci_upper = rd_h$ci[1,2],
    n_left = rd_h$N_h[1],
    n_right = rd_h$N_h[2]
  )
})
do.call(rbind, results)
```

> [!example] Stata: rdrobust

```stata
* CCT bandwidth with robust CI
rdrobust outcome running_var, c(cutoff)

* Display bandwidth
ereturn list  // see e(h_l) and e(h_r)

* Sensitivity: half bandwidth
rdrobust outcome running_var, c(cutoff) h(`=e(h_l)/2' `=e(h_r)/2')

* IK bandwidth
rdrobust outcome running_var, c(cutoff) bwselect(mserd)
```

> [!example] Python: rdrobust (via rpy2 or native port)

```python
# Using rpy2 to call R's rdrobust
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

rdrobust = importr('rdrobust')
rd = rdrobust.rdrobust(y=outcome, x=running_var, c=cutoff)
print(rd)

# Access bandwidth
bws = rd.rx2('bws')
```

---

## Advanced topics

**Local randomization inference**: alternative to continuity-based RDD; assumes local randomization within window. Bandwidth = window width where randomization holds. See Cattaneo-Frandsen-Titiunik (2015).

**Regression kink design (RKD)**: estimates derivative discontinuity. Use CCT-type bandwidth for kink, but different rate (slower convergence).

**Fuzzy RDD**: bandwidth selection same as sharp RDD; estimate via 2SLS with `rdrobust(..., fuzzy=...)`.

**Multiple cutoffs**: apply bandwidth selection separately at each cutoff or pool (context-dependent).

---

## Practical guidance

> [!tip] Recommended workflow
> 1. Use `rdrobust` with default (CCT) bandwidth for main result
> 2. Report robust bias-corrected CI
> 3. Show sensitivity to bandwidth: $0.5h$, $h$, $1.5h$, $2h$
> 4. Plot RD estimate and CI as function of $h$
> 5. Report $N$ within bandwidth (left and right of cutoff)
> 6. Supplement with visual plot of binned scatter and polynomial fit

> [!check] Reporting checklist
> - [ ] Bandwidth selection method (CCT/IK/manual)
> - [ ] Optimal bandwidth $h$ (and bias bandwidth $b$ if CCT)
> - [ ] Sample size within bandwidth (left and right)
> - [ ] Robust bias-corrected estimate and CI
> - [ ] Sensitivity table for multiple bandwidths
> - [ ] Plot of $\hat\tau(h)$ vs $h$

> [!warning] Common mistakes
> - Using very small $h$ (overfitting; high variance)
> - Using very large $h$ (includes observations far from cutoff; bias)
> - Reporting only one bandwidth without sensitivity
> - Ignoring robust bias correction (conventional SEs understate uncertainty)
> - Not checking for density discontinuity ([[density test]]) or covariate imbalance

---

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[local linear regression]]
- [[local polynomial regression]]
- [[density test]]
- [[McCrary test]] (McCrary density test)
- [[fuzzy RDD]]

---

## References

- Imbens & Kalyanaraman (2012), "Optimal Bandwidth Choice for the Regression Discontinuity Estimator," *Review of Economic Studies*
- Calonico, Cattaneo, & Titiunik (2014), "Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs," *Econometrica*
- Calonico, Cattaneo, & Titiunik (2020), "Optimal Bandwidth Choice for Robust Bias-Corrected Inference in Regression Discontinuity Designs," *Econometrics Journal*
- Cattaneo, Idrobo, & Titiunik (2020), *A Practical Introduction to Regression Discontinuity Designs: Foundations* (Cambridge University Press)
