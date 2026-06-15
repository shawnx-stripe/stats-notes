---
title: McCrary Test
aliases:
  - McCrary density test
  - McCrary manipulation test
tags:
  - rdd
  - diagnostics
  - identification
  - econometrics
updated: 2026-03-05
---

# McCrary Test

> [!summary] Quick definition
> The McCrary (2008) test checks for a discontinuity in the density of the [[running variable]] at the cutoff in [[Regression Discontinuity Design (RDD)|RDD]]. It bins the running variable, constructs a histogram, then fits [[local linear regression]] on each side of the cutoff to the bin counts. A significant log-density jump suggests manipulation, threatening the validity of the RD design. The newer Cattaneo-Jansson-Ma (2020) test provides a refined alternative; see [[density test]].

## Overview

The McCrary (2008) test is a diagnostic for manipulation in [[Regression Discontinuity Design (RDD)|RDD]]. The core idea: if agents can **precisely manipulate** their position relative to the cutoff $c$, the density of the [[running variable]] $X$ will exhibit a discontinuity at $c$. This violates the identifying assumption of RDD and threatens causal inference.

The test estimates the density function $f(x)$ on both sides of the cutoff using [[local linear regression]] and tests whether:

$$
\lim_{x \uparrow c} f(x) \neq \lim_{x \downarrow c} f(x)
$$

A significant discontinuity in density suggests agents are sorting across the threshold, invalidating the RD design.

## Null Hypothesis

> [!check] McCrary test null hypothesis
> $$H_0: \lim_{x \uparrow c} f(x) = \lim_{x \downarrow c} f(x)$$
>
> The density of the running variable is **continuous** at the cutoff. Equivalently, in log-density:
> $$H_0: \log f(c^+) - \log f(c^-) = 0$$

Rejection of $H_0$ indicates a **discontinuous density**, suggesting manipulation.

## Estimation Procedure

McCrary's procedure:

1. **Bin the data**: Partition the running variable $X$ into bins of width $b$
   - Let $n_j$ be the count in bin $j$
   - Compute midpoint $x_j$ for each bin

2. **Smooth the counts**: Estimate density separately on each side of $c$ using [[local linear regression]] on log-counts:
   $$
   \log(\hat{n}_j) = \alpha + \beta (x_j - c) + \varepsilon_j
   $$
   with kernel weighting and [[bandwidth selection|bandwidth]] $h$.

3. **Estimate the discontinuity**:
   $$
   \hat{\theta} = \log \hat{f}(c^+) - \log \hat{f}(c^-)
   $$
   where $\hat{f}(c^+)$ and $\hat{f}(c^-)$ are the right and left limits from local linear fits.

4. **Construct test statistic**:
   $$
   t = \frac{\hat{\theta}}{\hat{\text{SE}}(\hat{\theta})}
   $$
   where $\hat{\text{SE}}$ accounts for estimation uncertainty in both density estimates.

5. **Test**: Under $H_0$, $t \sim N(0, 1)$ asymptotically. Reject if $|t| > 1.96$ at $\alpha = 0.05$.

## Interpretation of Results

| Result | Interpretation | Implication |
|--------|---------------|-------------|
| **No discontinuity** ($p > 0.05$) | Density is smooth at $c$ | No evidence of manipulation; RDD may be valid |
| **Positive jump** ($\theta > 0$, $p < 0.05$) | Excess density just above $c$ | Agents bunch above threshold (e.g., gaming for benefits) |
| **Negative jump** ($\theta < 0$, $p < 0.05$) | Deficit of density just above $c$ | Agents avoid crossing threshold (e.g., stigma, costs) |

> [!warning] Limitations
> - Binning choice $b$ and bandwidth $h$ can affect results (though test provides data-driven defaults)
> - Low power in small samples or with discrete running variables
> - Cannot distinguish manipulation from other discontinuities (e.g., institutional features)

## Relation to Manipulation

A discontinuous density suggests **precise manipulation**, but context matters:

- **Sharp manipulation**: Agents with $X$ slightly below $c$ can move above (or vice versa)
- **Examples**: Test scores (retaking exams), income reporting (tax avoidance), age (misreporting for program eligibility)

Manipulation threatens RDD because it implies **self-selection**: units near $c$ are no longer "as-good-as-randomly" assigned to treatment. This breaks the key identifying assumption.

> [!tip] When manipulation is plausible but not detected
> Even a "passed" McCrary test doesn't guarantee no manipulation:
> - Manipulation may be **imperfect** (noisy sorting)
> - Sample size may be insufficient to detect small discontinuities
> - Always combine with other validity checks: [[covariate balance test|covariate balance]], [[placebo test|placebo tests]], [[donut RDD|donut hole estimates]]

## Minimal Code Snippets

### R (rddensity)

```r
# Modern Cattaneo-Jansson-Ma test (recommended)
library(rddensity)

# Run density test
density_test <- rddensity(X = data$running_var, c = 0)

# Print results
summary(density_test)

# Plot density
rdplotdensity(density_test, X = data$running_var)
```

### R (rdd, legacy McCrary implementation)

```r
# Original McCrary (2008) test
library(rdd)

# Run test
mccrary_test <- DCdensity(
  runvar = data$running_var,
  cutpoint = 0,
  bin = NULL,  # auto-select bin width
  bw = NULL,   # auto-select bandwidth
  plot = TRUE
)

# Extract test statistic and p-value
mccrary_test
```

### Stata (rddensity)

```stata
* Modern Cattaneo-Jansson-Ma test
rddensity running_var, c(0)

* Plot density
rddensity running_var, c(0) plot
```

### Stata (DCdensity, legacy)

```stata
* Original McCrary test (requires external command)
* Install: ssc install rddensity, replace

DCdensity running_var, breakpoint(0) generate(Xj Yj r0 fhat se_fhat)

* Plot
twoway (scatter Yj Xj if Xj < 0, msize(small)) ///
       (scatter Yj Xj if Xj >= 0, msize(small)) ///
       (line fhat Xj if Xj < 0 & r0 == 1, sort) ///
       (line fhat Xj if Xj >= 0 & r0 == 0, sort), ///
       xline(0, lcolor(red)) legend(off)
```

### Python (rdd)

```python
from rdd import rdd_density

# Run McCrary test
result = rdd_density(
    data=df,
    x='running_var',
    cutoff=0,
    bin_width=None,  # auto-select
    bandwidth=None   # auto-select
)

print(f"Log-density discontinuity: {result['theta']:.4f}")
print(f"SE: {result['se']:.4f}")
print(f"t-stat: {result['t_stat']:.4f}")
print(f"p-value: {result['p_value']:.4f}")
```

## Common Pitfalls

1. **Discrete running variables**: With heavily discrete $X$ (e.g., test scores 0-100), standard McCrary test may spuriously detect discontinuities. Use [[density test|CJM test]] with discrete adjustments or inspect raw histograms.

2. **Small sample sizes**: McCrary test requires sufficient observations near $c$. With $n < 500$ within bandwidth, power is limited.

3. **Choosing bin width**: Too wide smooths over real discontinuities; too narrow introduces noise. Use data-driven selection (e.g., Scott's rule) or sensitivity checks.

4. **Endogenous bandwidth**: Selecting $h$ to minimize $p$-value invalidates inference. Use pre-specified or data-driven $h$.

5. **Interpretation without context**: A density jump may reflect institutional features (e.g., age 65 and Medicare eligibility) rather than manipulation. Understand the **data-generating process**.

> [!example] Classic application
> **Lee, Moretti & Butler (2004)**: Electoral accountability and RDD. McCrary test shows **no discontinuity** in vote share density at 50% threshold, supporting validity of RD design comparing narrow winners vs losers.

## Relation to Other Tests

- **[[density test]]**: Generic term; McCrary is one implementation, [[density test|Cattaneo-Jansson-Ma (2020)]] is newer
- **[[covariate balance test]]**: Complements density test; checks if pre-treatment covariates are smooth at $c$
- **[[placebo test]]**: Uses outcomes that shouldn't be affected by treatment to check for spurious discontinuities

## Related notes

- [[density test]]
- [[Regression Discontinuity Design (RDD)]]
- [[running variable]]
- [[local linear regression]]
- [[bandwidth selection]]
- [[covariate balance test]]
- [[placebo test]]
- [[donut RDD]]
