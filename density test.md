---
title: density test
aliases:
  - Density test
  - running variable density test
tags:
  - rdd
  - diagnostics
  - identification
  - econometrics
updated: 2026-03-05
---

# density test

> [!summary] Quick definition
> A density test checks for manipulation of the [[running variable]] at the cutoff in [[Regression Discontinuity Design (RDD)|RDD]]. If agents can precisely sort across the threshold, the density of the running variable will show a discontinuity at $c$, invalidating the RD design. The [[McCrary test]] (2008) and the Cattaneo-Jansson-Ma (2020) test are the standard approaches.

## Overview

The density test is a fundamental **diagnostic check** for [[Regression Discontinuity Design (RDD)|RDD]]. It tests the null hypothesis that the density of the [[running variable]] $X$ is continuous at the cutoff $c$:

$$
H_0: f(c^-) = f(c^+)
$$

If this hypothesis is rejected, it suggests **precise manipulation**—agents can sort themselves across the threshold, which violates the identifying assumption that assignment is "as-good-as-random" near $c$.

## Purpose: Testing for Manipulation

RDD relies on the assumption that units just below and just above the cutoff $c$ are comparable, differing only in treatment status. This requires:

> [!check] RDD continuity assumption (for density)
> The density of the running variable $X$ must be continuous at $c$:
> $$
> \lim_{x \uparrow c} f(x) = \lim_{x \downarrow c} f(x)
> $$

**Why does a density discontinuity threaten RDD?**

If $f(c^-) \neq f(c^+)$, it implies:
1. **Self-selection**: Units near $c$ are not randomly assigned; they've sorted themselves to one side
2. **Differential composition**: Observable and unobservable characteristics may differ discontinuously at $c$
3. **Invalid counterfactual**: Units just above $c$ are no longer a valid comparison group for units just below

**Examples of manipulation**:
- Students retaking tests to cross a scholarship threshold
- Firms adjusting reported revenue to avoid tax bracket changes
- Individuals misreporting age/income to qualify for programs
- Politicians manipulating vote counts near 50% threshold

> [!warning] No discontinuity doesn't guarantee no manipulation
> A continuous density is **necessary but not sufficient**. Manipulation may be:
> - **Imperfect** (noisy sorting), leaving density smooth but composition still biased
> - **Too weak** to detect with available sample size
> - Always supplement with [[covariate balance test|covariate balance checks]]

## McCrary (2008) vs Cattaneo-Jansson-Ma (2020)

Two main approaches exist for density testing in RDD:

### McCrary (2008) Test

The original and widely-used method:

**Procedure**:
1. Bin the running variable into histogram bins
2. Fit [[local linear regression]] to log-counts on each side of $c$
3. Test for discontinuity in log-density: $\theta = \log f(c^+) - \log f(c^-)$

**Strengths**:
- Intuitive and easy to visualize
- Fast computation
- Well-established in applied work

**Limitations**:
- Ad-hoc binning step introduces tuning parameter
- Inference can be sensitive to bin width choice
- Less robust with discrete running variables
- Conservative (low power) in small samples

See [[McCrary test]] for detailed implementation.

### Cattaneo-Jansson-Ma (CJM, 2020) Test

Modern refinement with improved statistical properties:

**Procedure**:
1. Estimate density directly using [[local polynomial regression]] (no binning)
2. Use MSE-optimal [[bandwidth selection]] with robust bias correction
3. Construct test statistic with undersmoothing or bias correction
4. Provide both frequentist and manipulation-robust inference

**Strengths**:
- No binning—uses raw data directly
- MSE-optimal bandwidth selection reduces researcher discretion
- Better power in finite samples
- Handles discrete running variables naturally
- Provides both point estimates and inference

**Limitations**:
- Slightly more complex implementation
- Newer method (less established in applied work)

**CJM is now the recommended approach** for new research (as of 2020+).

## Implementation

### R (rddensity)

The `rddensity` package implements the CJM test:

```r
library(rddensity)

# Run CJM density test
density_test <- rddensity(
  X = data$running_var,
  c = 0,                    # cutoff
  p = 2,                    # polynomial order (default: 2)
  kernel = "triangular",    # kernel function
  bwselect = "mse-dpi"      # MSE-optimal bandwidth
)

# Print results
summary(density_test)

# Key output:
# - Test statistic (T)
# - P-value (robust, asymptotic)
# - Bandwidth used (h_l, h_r)
# - Effective sample size (N_l, N_r)

# Plot density with confidence intervals
rdplotdensity(
  rdd = density_test,
  X = data$running_var,
  type = "both"  # show density + test statistic
)
```

**Output interpretation**:
- `p-value > 0.05`: Cannot reject continuity; no evidence of manipulation
- `p-value < 0.05`: Reject continuity; density jumps at cutoff (manipulation likely)
- `T_q`: Robust test statistic (normal distribution under $H_0$)

### R (DCdensity, legacy McCrary)

```r
# Original McCrary test
library(rdd)

mccrary_result <- DCdensity(
  runvar = data$running_var,
  cutpoint = 0,
  bin = NULL,    # auto bin width
  bw = NULL,     # auto bandwidth
  plot = TRUE,
  ext.out = TRUE
)

# Extract results
theta <- mccrary_result$theta  # log-density jump
se <- mccrary_result$se        # standard error
z <- mccrary_result$z          # z-statistic
p <- mccrary_result$p          # p-value
```

### Stata (rddensity)

```stata
* CJM test
rddensity running_var, c(0)

* With plot
rddensity running_var, c(0) plot plot_range(-10 10)

* Store results
ereturn list
local pval = e(pval_asy_r)
local h_left = e(h_l)
local h_right = e(h_r)

* Custom bandwidth
rddensity running_var, c(0) h(2 2)
```

### Python (rdrobust via rpy2)

```python
import pandas as pd
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

pandas2ri.activate()
rddensity = importr('rddensity')

# Run test
result = rddensity.rddensity(X=data['running_var'], c=0)

# Extract p-value
summary_res = rddensity.summary_rddensity(result)
# Parse from summary output
```

**Note**: Python support is limited; use R via `rpy2` or implement manually using kernel density estimation.

## Interpretation

### Visual Inspection

Always plot the density:

```r
# R: Histogram with local polynomial overlay
library(ggplot2)

ggplot(data, aes(x = running_var)) +
  geom_histogram(aes(y = ..density..), bins = 50, alpha = 0.5) +
  geom_vline(xintercept = 0, color = "red", linetype = "dashed") +
  labs(title = "Density of Running Variable", x = "Running Variable", y = "Density")
```

**What to look for**:
- Smooth density across $c$ (good)
- Visible jump or drop at $c$ (concerning)
- Spikes in histogram near $c$ (manipulation)
- Heaping at round numbers (measurement error, often benign)

### Formal Test Results

| Test Result | Interpretation | Next Steps |
|------------|----------------|-----------|
| $p > 0.10$ | No evidence of manipulation | Proceed with RDD; report test in robustness checks |
| $0.05 < p < 0.10$ | Weak evidence of discontinuity | Investigate further; consider [[covariate balance test|covariate balance]], [[donut RDD|donut hole]] |
| $p < 0.05$ | Significant discontinuity detected | **Red flag**: manipulation likely; RDD may be invalid |

> [!tip] When density test fails
> 1. **Investigate the mechanism**: Is manipulation plausible in this setting?
> 2. **Check covariates**: Are baseline characteristics balanced at $c$?
> 3. **Donut RDD**: Exclude observations very close to $c$ (within $\pm \epsilon$)
> 4. **Placebo cutoffs**: Test for density jumps at other values of $X$ (should find none)
> 5. **Report transparently**: Acknowledge the issue and discuss threats to validity

## Relation to RDD Validity

The density test is one of several validity checks for RDD:

| Check | Tests for | Interpretation if failed |
|-------|----------|------------------------|
| **Density test** | Precise manipulation | Self-selection at threshold |
| **[[covariate balance test|Covariate balance]]** | Smooth baseline characteristics | Composition effects; non-random assignment |
| **[[placebo test|Placebo test]]** | Pre-treatment outcomes smooth | Spurious discontinuity unrelated to treatment |
| **Bandwidth sensitivity** | Robustness to $h$ choice | Fragile estimates; local confounding |

A valid RDD design should:
- **Pass** density test (continuous $f(x)$ at $c$)
- **Pass** covariate balance (smooth $E[Z|X]$ at $c$ for baseline covariates $Z$)
- Show treatment effect discontinuity **only** for relevant outcomes

## Common Pitfalls

1. **Ignoring discreteness**: With discrete $X$ (e.g., test scores), raw histograms may look "lumpy" even without manipulation. Use CJM test with appropriate options or adjust bin width.

2. **Confusing discontinuity types**:
   - **Mass point at $c$**: Partial treatment (fuzzy RDD), not necessarily manipulation
   - **Discontinuous jump**: Precise manipulation (sharp RDD is threatened)

3. **Over-interpreting visual inspection**: Histograms can be misleading due to bin choices. Always run formal test.

4. **Not reporting**: Failing to conduct or report density tests is a red flag in referee reports. Always include.

5. **Using as only validity check**: Density test alone is insufficient. Combine with covariate balance and placebo tests.

> [!example] Classic application
> **Lee (2008)**: U.S. House elections. Density test shows **no discontinuity** at 50% vote share, supporting validity of RD design comparing narrow winners vs losers. This is now a standard validity check in electoral RDD studies.

## Minimal Code Snippets (Complete Workflow)

### R (recommended)

```r
library(rddensity)
library(ggplot2)

# 1. Visual inspection
ggplot(data, aes(x = running_var)) +
  geom_histogram(bins = 50, alpha = 0.6) +
  geom_vline(xintercept = 0, color = "red") +
  labs(title = "Density Check: Running Variable")

# 2. Formal test (CJM)
test <- rddensity(data$running_var, c = 0)
summary(test)

# 3. Plot with inference
rdplotdensity(test, data$running_var)

# 4. Report
cat(sprintf("Density test: T = %.3f, p = %.3f\n",
            test$test$t_jk, test$test$p_jk))
```

### Stata (workflow)

```stata
* Visual check
histogram running_var, width(0.5) xline(0, lcolor(red))

* Formal test
rddensity running_var, c(0)

* Store p-value
local pval = e(pval_asy_r)
di "Density test p-value: `pval'"

* Plot
rddensity running_var, c(0) plot
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[McCrary test]]
- [[running variable]]
- [[bandwidth selection]]
- [[covariate balance test]]
- [[placebo test]]
- [[donut RDD]]
- [[local polynomial regression]]
- [[local linear regression]]
