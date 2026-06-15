---
title: Bootstrap
aliases:
  - Bootstrapping
  - Bootstrap sampling
  - Bootstrap resampling
  - Efron bootstrap
  - Nonparametric bootstrap
  - Bootstrap
tags:
  - statistics
  - resampling
  - inference
  - uncertainty-quantification
  - computational-statistics
updated: 2025-09-26
---

# Bootstrap

> [!summary] Quick definition
> A resampling method that estimates the sampling distribution of a statistic by repeatedly sampling with replacement from the observed data. Enables inference (confidence intervals, standard errors, bias) for complex estimators without parametric assumptions or analytical derivations.

## Core idea and procedure

### Basic bootstrap algorithm
1. Start with sample data: X = {x₁, x₂, ..., xₙ}
2. For b = 1 to B:
   - Draw n observations with replacement from X → X*ᵦ
   - Compute statistic of interest: θ̂*ᵦ = T(X*ᵦ)
3. Use empirical distribution of {θ̂*₁, ..., θ̂*ᵦ} to approximate sampling distribution of θ̂

### Key insight
The bootstrap principle (Efron, 1979):
$$
F_n \text{ is to } F \quad \text{as} \quad F_n^* \text{ is to } F_n
$$
- F: true population distribution (unknown)
- Fₙ: empirical distribution (known)
- Fₙ*: bootstrap distribution (computable)

The relationship between sample and population mirrors the relationship between bootstrap sample and original sample.

## What bootstrap estimates

### Standard error
$$
\widehat{\text{SE}}_{\text{boot}}(\hat{\theta}) = \sqrt{\frac{1}{B-1} \sum_{b=1}^B (\hat{\theta}_b^* - \bar{\theta}^*)^2}
$$
where $\bar{\theta}^* = \frac{1}{B}\sum_{b=1}^B \hat{\theta}_b^*$

### Bias
$$
\widehat{\text{Bias}}_{\text{boot}}(\hat{\theta}) = \bar{\theta}^* - \hat{\theta}
$$

### Confidence intervals
Multiple methods with different properties:

| Method | Formula | Properties |
|--------|---------|------------|
| **Percentile** | $[\hat{\theta}^*_{\alpha/2}, \hat{\theta}^*_{1-\alpha/2}]$ | Simple, transformation-respecting, can be biased |
| **Basic** | $[2\hat{\theta} - \hat{\theta}^*_{1-\alpha/2}, 2\hat{\theta} - \hat{\theta}^*_{\alpha/2}]$ | Symmetric around θ̂ |
| **Normal** | $\hat{\theta} \pm z_{1-\alpha/2} \cdot \widehat{\text{SE}}_{\text{boot}}$ | Assumes normality |
| **BCa** | Bias-corrected and accelerated | Better coverage, computationally intensive |
| **Studentized** | Using bootstrap-t pivotal quantity | Asymptotically superior, requires nested bootstrap |

## Types of bootstrap

### 1. Nonparametric bootstrap (standard)
- Sample with replacement from data
- No distributional assumptions
- Most common implementation

### 2. Parametric bootstrap
- Fit parametric model F̂(θ̂) to data
- Generate bootstrap samples from F̂
- More efficient if model is correct

### 3. Smoothed bootstrap
- Add small noise to resampled values
- Helps with discrete data or ties
- Kernel density estimation connection

### 4. Block bootstrap (for dependent data)
- Resample blocks of consecutive observations
- Preserves temporal/spatial dependence
- Variants: moving block, circular block, stationary block

### 5. Wild bootstrap (for heteroskedasticity)
- Resample residuals with random weights
- Preserves heteroskedasticity pattern
- Common in regression settings

### 6. Bayesian bootstrap
- Assign random weights from Dirichlet distribution
- Continuous analogue of bootstrap
- Connection to [[Bayesian econometrics|Bayesian inference]]

## When bootstrap works (and doesn't)

### Works well for:
- Smooth statistics (means, variances, regression coefficients)
- Statistics with continuous sampling distributions
- Moderate to large sample sizes
- [[pivotal quantities|Pivotal quantities]]

### Struggles with:
- Extreme order statistics (min, max)
- Non-smooth statistics (median with ties)
- Heavy-tailed distributions (slow convergence)
- Very small samples (n < 20)
- Parameters on boundary of parameter space

> [!warning] Bootstrap failures
> The ordinary nonparametric bootstrap can be **inconsistent** or unreliable for:
> - Sample maximum/minimum
> - Number of modes
> - Degenerate or nonregular U-statistics
> - Some change-point problems

## Theoretical foundations

### Consistency
Under regularity conditions, as n → ∞ and B → ∞:
$$
\sup_x \left| P^*(\sqrt{n}(\hat{\theta}^* - \hat{\theta}) \le x) - P(\sqrt{n}(\hat{\theta} - \theta) \le x) \right| \xrightarrow{p} 0
$$

### Edgeworth expansion
Bootstrap often achieves higher-order accuracy:
- Normal approximation: O(n⁻¹/²) error
- Bootstrap: O(n⁻¹) error for many statistics
- Requires smoothness and moment conditions

### Number of replications (B)
- Standard errors: B = 50-200 often sufficient
- Confidence intervals: B = 1000-2000 recommended
- Hypothesis tests: B = 10000+ for accurate p-values
- Rule of thumb for SE: CV(SE) ≈ 1/√(2B)

## Practical implementation

> [!check] Bootstrap checklist
> - [ ] Choose appropriate bootstrap type for data structure
> - [ ] Set seed for reproducibility
> - [ ] Use B ≥ 1000 for confidence intervals
> - [ ] Check bootstrap distribution shape (plot histogram)
> - [ ] Compare different CI methods if critical
> - [ ] Consider stratification for subgroups
> - [ ] Account for survey weights if present
> - [ ] Use parallel computation for large B

## Bootstrap for specific problems

### Regression models
For model Y = Xβ + ε:

1. **Pairs bootstrap**: Resample (xᵢ, yᵢ) pairs
   - Robust to heteroskedasticity
   - Preserves predictor distribution
   
2. **Residual bootstrap**: Resample residuals
   - Assumes homoskedasticity
   - Fixes X, resamples ε̂
   
3. **Wild bootstrap**: Multiply residuals by random weights
   - Handles heteroskedasticity
   - Popular weights: Rademacher (±1), Mammen

### Time series
- **Block bootstrap**: Preserve temporal dependence
- Block length selection: l ≈ n^(1/3) (rule of thumb)
- **Sieve bootstrap**: Fit AR model, bootstrap residuals
- **Markov bootstrap**: For Markov chains

### Hierarchical/clustered data
- **Cluster bootstrap**: Resample clusters, not individuals
- **Two-stage bootstrap**: Resample at each level
- Preserves within-cluster correlation

## Advanced techniques

- **Double bootstrap**: Bootstrap the bootstrap to calibrate CI coverage; O(B²) cost.
- **m-out-of-n bootstrap**: Resample m < n observations; can be consistent when standard bootstrap fails.
- **Bag of little bootstraps (BLB)**: Divide data into subsets, subsample + bootstrap within each; scales to massive data.

## Common mistakes

> [!danger] Pitfalls to avoid
> - Using too few bootstrap replications
> - Ignoring data structure (clustering, time dependence)
> - Bootstrapping inappropriate statistics (e.g., sample max)
> - Not checking bootstrap distribution shape
> - Applying to very small samples without caution
> - Forgetting to set random seed

## Bootstrap vs other methods

| Method | Bootstrap | Jackknife | [[randomization inference|Permutation test]] | [[cross-validation|Cross-validation]] |
|--------|-----------|--------------|---------------------|---------------------|
| Purpose | General inference | Bias, variance | Hypothesis testing | Model selection |
| Resampling | With replacement | Leave-one-out | Without replacement | Without replacement |
| Sample size | Same as original | n-1 | Same as original | Training < n |
| Computational cost | O(Bn) | O(n) | O(Bn) | O(kn) |
| Assumptions | Minimal | Smoothness | Exchangeability | None |

## Copy-ready formulas

- Bootstrap standard error:
$$
\widehat{\text{SE}}_{\text{boot}} = \sqrt{\frac{1}{B-1} \sum_{b=1}^B (\hat{\theta}_b^* - \bar{\theta}^*)^2}
$$

- Percentile CI:
$$
\text{CI}_{1-\alpha} = [\hat{\theta}^*_{\alpha/2}, \hat{\theta}^*_{1-\alpha/2}]
$$

- BCa CI acceleration constant:
$$ \hat{a} = \frac{\sum_{i=1}^n (\hat{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^3}{6\left[\sum_{i=1}^n (\hat{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^2\right]^{3/2}} $$

- Wild bootstrap weights (Mammen):
$$
w_i = \begin{cases}
-(\sqrt{5}-1)/2 & \text{with probability } (\sqrt{5}+1)/(2\sqrt{5}) \\
(\sqrt{5}+1)/2 & \text{with probability } (\sqrt{5}-1)/(2\sqrt{5})
\end{cases}
$$

## Minimal code snippets

```python
# Python: Basic bootstrap with scipy
from scipy import stats
import numpy as np

def bootstrap_ci(data, statistic, alpha=0.05, B=10000, method='percentile'):
    """Bootstrap confidence interval"""
    n = len(data)
    boot_stats = []
    
    for _ in range(B):
        sample = np.random.choice(data, n, replace=True)
        boot_stats.append(statistic(sample))
    
    boot_stats = np.array(boot_stats)
    
    if method == 'percentile':
        ci = np.percentile(boot_stats, [100*alpha/2, 100*(1-alpha/2)])
    elif method == 'basic':
        theta_hat = statistic(data)
        ci = [2*theta_hat - np.percentile(boot_stats, 100*(1-alpha/2)),
              2*theta_hat - np.percentile(boot_stats, 100*alpha/2)]
    elif method == 'normal':
        theta_hat = statistic(data)
        se = np.std(boot_stats)
        ci = stats.norm.interval(1-alpha, loc=theta_hat, scale=se)
    
    return ci, boot_stats

# Example: Bootstrap CI for median
data = np.random.exponential(2, 100)
ci, boot_dist = bootstrap_ci(data, np.median, B=10000)
print(f"95% Bootstrap CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

```r
# R: Using boot package
library(boot)

# Define statistic function
median_stat <- function(data, indices) {
  median(data[indices])
}

# Run bootstrap
boot_results <- boot(
  data = my_data,
  statistic = median_stat,
  R = 10000,
  parallel = "multicore",
  ncpus = 4
)

# Get confidence intervals
boot.ci(boot_results, type = c("norm", "basic", "perc", "bca"))

# For regression
reg_boot <- function(data, indices) {
  d <- data[indices, ]
  fit <- lm(y ~ x1 + x2, data = d)
  coef(fit)
}

boot_reg <- boot(mydata, reg_boot, R = 1000)
```

```python
# Python: Block bootstrap for time series (sketch)
def block_bootstrap(data, block_length, n_boot=1000):
    n = len(data)
    boot_samples = []
    for _ in range(n_boot):
        starts = np.random.randint(0, n - block_length + 1, n // block_length + 1)
        boot_samples.append(np.concatenate([data[s:s+block_length] for s in starts])[:n])
    return np.array(boot_samples)
# Rule of thumb for block length: l ≈ n^(1/3)
```

---

## Related notes
- jackknife
- [[randomization inference|permutation test]]
- [[cross-validation]]
- [[resampling methods]]
- [[confidence intervals]]
- [[standard error]]
- [[bias estimation]]
- [[BCa bootstrap]]
- [[wild cluster bootstrap|wild bootstrap]]
- [[block bootstrap]]
- [[Bayesian bootstrap]]
- [[pivotal quantities]]
- [[Bayesian econometrics|Bayesian inference]]
- regression
- [[clustered standard errors]]
- [[Time Series (MOC)|time series]]
- [[heteroskedasticity]]
