---
title: Fuzzy RDD
aliases:
  - Fuzzy regression discontinuity
  - Fuzzy RD
  - Fuzzy discontinuity design
  - Probabilistic RDD
tags:
  - causal-inference
  - econometrics
  - quasi-experimental
  - regression-discontinuity
  - instrumental-variables
updated: 2025-09-26
---

# Fuzzy RDD

> [!summary] Quick definition
> A [[Regression Discontinuity Design (RDD)|regression discontinuity design]] where the probability of treatment jumps discontinuously at a threshold but not from 0 to 1. The discontinuity in treatment probability serves as an [[Instrumental Variables (IV)|instrumental variable]] to identify a [[Local Average Treatment Effect (LATE)|LATE]] (Local Average Treatment Effect) for units induced to change treatment status by crossing the threshold.

## Core setup and notation

- Running variable (forcing variable): X
- Threshold/cutoff: c
- Treatment indicator: D ∈ {0,1}
- Outcome: Y
- Treatment probability: P(D=1|X=x) = E\[D|X=x\]

### Key distinction from sharp RDD

| Design | Treatment probability at cutoff | Identification |
|--------|----------------------------------|----------------|
| [[sharp RDD|Sharp RDD]] | Jumps from 0 to 1 | ATE at cutoff |
| Fuzzy RDD | Jumps from p₀ to p₁ (0 < p₁-p₀ < 1) | LATE at cutoff |

The discontinuity:
$$
\tau_D = \lim_{x \downarrow c} \mathbb{E}\[D \mid X=x\] - \lim_{x \uparrow c} \mathbb{E}\[D \mid X=x\] \neq 0
$$

## Identification

### As instrumental variables

The fuzzy RDD is equivalent to an IV estimator where Z = 𝟙{X ≥ c} is the instrument:

$$
\text{Fuzzy RDD} = \frac{\lim_{x \downarrow c} \mathbb{E}\[Y \mid X=x\] - \lim_{x \uparrow c} \mathbb{E}\[Y \mid X=x\]}{\lim_{x \downarrow c} \mathbb{E}\[D \mid X=x\] - \lim_{x \uparrow c} \mathbb{E}\[D \mid X=x\]} = \frac{\tau_Y}{\tau_D}
$$

This is a [[Wald estimator]] using the threshold as instrument.

### LATE interpretation

Under standard assumptions, fuzzy RDD identifies:
$$
\tau_{\text{FRDD}} = \mathbb{E}\[Y_1 - Y_0 \mid \text{unit is a complier at } X=c\]
$$

Compliers: units induced to take treatment by crossing the threshold.

### Key assumptions

1. **Continuity of potential outcomes**: E\[Y₀|X=x\] and E\[Y₁|X=x\] continuous at c
2. **Discontinuity in treatment**: τ_D ≠ 0 (first stage)
3. **Monotonicity**: No defiers (crossing threshold doesn't decrease treatment probability)
4. **Excludability**: Threshold affects Y only through D
5. **No manipulation**: Units cannot precisely control X around c

> [!check] Validity checklist
> - [ ] Test for discontinuity in treatment probability (first stage)
> - [ ] Check continuity of baseline covariates
> - [ ] Examine density of running variable (McCrary test)
> - [ ] Test for manipulation/bunching at threshold
> - [ ] Verify monotonicity (treatment increases at cutoff)
> - [ ] Assess bandwidth sensitivity

## Estimation approaches

### 1. Local linear regression (preferred)

Two-stage least squares within bandwidth h:

**First stage** (treatment equation):
$$
D_i = \alpha_0 + \alpha_1 Z_i + \beta_0 (X_i - c) + \beta_1 Z_i(X_i - c) + \nu_i
$$

**Second stage** (outcome equation):
$$
Y_i = \gamma_0 + \tau \hat{D}_i + \delta_0 (X_i - c) + \delta_1 Z_i(X_i - c) + \varepsilon_i
$$

where Z_i = 𝟙{X_i ≥ c} and estimation uses |X_i - c| ≤ h.

### 2. Local polynomial regression

Extend to higher-order polynomials:
- Bias reduction at boundary
- Increased variance
- Typically use p = 1 (local linear) or p = 2 (local quadratic)

### 3. Bias-corrected robust inference

Modern approach (Calonico, Cattaneo, Titiunik):
- Bias correction for boundary effects
- Robust standard errors
- Different bandwidths for point estimate and inference

## Bandwidth selection

### Mean Squared Error (MSE) optimal
$$
h_{\text{MSE}} = \arg\min_h \text{MSE}(\hat{\tau}(h))
$$

### Coverage Error Rate (CER) optimal
For confidence intervals:
$$
h_{\text{CER}} = \arg\min_h |\text{Coverage}_{1-\alpha}(h) - (1-\alpha)|
$$

### Practical approaches
- **Imbens-Kalyanaraman (IK)**: Plug-in bandwidth selector
- **Calonico-Cattaneo-Titiunik (CCT)**: MSE-optimal with regularization
- **Cross-validation**: Leave-one-out CV near cutoff
- **Multiple bandwidths**: Report results across range

> [!tip] Bandwidth trade-offs
> - Smaller h → Less bias, more variance, fewer observations
> - Larger h → More bias, less variance, stronger first stage
> - Rule of thumb: Start with MSE-optimal, check h/2 and 2h

## Graphical analysis

Essential plots for fuzzy RDD:

1. **First stage**: Treatment probability vs running variable
2. **Reduced form**: Outcome vs running variable  
3. **Binned scatter plots**: Local averages to show discontinuities
4. **Density test**: Histogram/density of running variable

## Common applications

### Education
- **Financial aid**: Income/asset thresholds for aid eligibility
- **School admission**: Test score cutoffs with imperfect compliance
- **Class size**: Enrollment thresholds trigger class additions

### Healthcare
- **Medicare eligibility**: Age 65 threshold with voluntary enrollment
- **Treatment guidelines**: Clinical thresholds with physician discretion
- **Insurance subsidies**: Income thresholds for subsidy amounts

### Criminal justice
- **Sentencing guidelines**: Score thresholds as recommendations
- **Pretrial release**: Risk score thresholds influence but don't determine release

### Elections
- **Incumbency advantage**: Vote share thresholds for winning
- **Campaign finance**: Vote thresholds trigger matching funds

## Diagnostics and robustness

### Covariate balance
Test for discontinuities in predetermined variables:
$$
\tau_W = \lim_{x \downarrow c} \mathbb{E}[W \mid X=x] - \lim_{x \uparrow c} \mathbb{E}[W \mid X=x] \approx 0
$$

### Placebo cutoffs
Test for discontinuities away from true cutoff:
- Use c' = c ± δ where no discontinuity expected
- Should find no effect

### Donut RDD
Exclude observations immediately around cutoff:
- Tests robustness to manipulation
- Remove |X - c| < ε for small ε

### Density test (McCrary)
Test for manipulation of running variable:
$$
\theta = \ln f^+(c) - \ln f^-(c)
$$
where f⁺(c) and f⁻(c) are densities just above/below cutoff.

## Fuzzy vs Sharp RDD

| Aspect | Sharp RDD | Fuzzy RDD |
|--------|-----------|-----------|
| **Compliance** | Perfect | Imperfect |
| **Estimand** | ATE at cutoff | LATE at cutoff |
| **Identification** | Discontinuity in Y | Ratio of discontinuities |
| **Power** | Higher | Lower (weak first stage) |
| **External validity** | All units at cutoff | Compliers at cutoff |
| **Estimation** | Single equation | Two equations/IV |

## Extensions

### Multiple cutoffs
With cutoffs c₁, c₂, ..., c_K:
- Pool discontinuities with appropriate weights
- Test heterogeneity across cutoffs
- Increase power by combining

### Fuzzy kink design
When treatment intensity (not probability) has kink:
$$
\tau_{\text{FKD}} = \frac{\lim_{x \downarrow c} \frac{\partial \mathbb{E}[Y|X=x]}{\partial x} - \lim_{x \uparrow c} \frac{\partial \mathbb{E}[Y|X=x]}{\partial x}}{\lim_{x \downarrow c} \frac{\partial \mathbb{E}[D|X=x]}{\partial x} - \lim_{x \uparrow c} \frac{\partial \mathbb{E}[D|X=x]}{\partial x}}
$$

### Geographic RDD
Spatial boundaries as discontinuities:
- Distance to border as running variable
- Account for spatial correlation

## Common pitfalls

> [!warning] Things to avoid
> - **Weak first stage**: Small jump in treatment → imprecise estimates
> - **Bandwidth shopping**: Selecting h based on significance
> - **Ignoring clustering**: When running variable is discrete or grouped
> - **Extrapolation**: Effects only identified at cutoff
> - **Multiple testing**: Testing many outcomes without adjustment

## Copy-ready formulas

- Fuzzy RDD estimator:
$$
\hat{\tau}_{\text{FRDD}} = \frac{\hat{\tau}_Y}{\hat{\tau}_D} = \frac{\lim_{x \downarrow c} \hat{\mathbb{E}}[Y|X=x] - \lim_{x \uparrow c} \hat{\mathbb{E}}[Y|X=x]}{\lim_{x \downarrow c} \hat{\mathbb{E}}[D|X=x] - \lim_{x \uparrow c} \hat{\mathbb{E}}[D|X=x]}
$$

- Local linear specification:
$$
\{Y_i, D_i\} = \alpha + \tau Z_i + \beta_1(X_i-c) + \beta_2 Z_i(X_i-c) + \varepsilon_i, \quad |X_i-c| \leq h
$$

- MSE-optimal bandwidth (simplified):
$$
h_{\text{MSE}} \propto \left(\frac{\sigma^2(c)}{f(c) \cdot B^2(c)}\right)^{1/5} n^{-1/5}
$$

## Minimal code snippets

```r
# R: Using rdrobust package
library(rdrobust)

# Fuzzy RDD estimation
fuzzy_rdd <- rdrobust(
  y = data$outcome,
  x = data$running_var,
  c = cutoff,
  fuzzy = data$treatment,  # Key difference from sharp
  covs = data[, c("cov1", "cov2")],  # Optional
  kernel = "triangular",
  bwselect = "mserd"  # MSE-optimal bandwidth
)

summary(fuzzy_rdd)
rdplot(y = data$outcome, x = data$running_var, c = cutoff)

# First stage check
first_stage <- rdrobust(
  y = data$treatment,
  x = data$running_var,
  c = cutoff
)
summary(first_stage)

# Manipulation test
library(rddensity)
density_test <- rddensity(data$running_var, c = cutoff)
summary(density_test)
```

```python
# Python: Use rdrobust via rpy2, or linearmodels IV2SLS within bandwidth
from linearmodels.iv import IV2SLS
import numpy as np

# Subset to bandwidth around cutoff
bw_mask = np.abs(df['running_var'] - cutoff) <= h
dh = df[bw_mask].copy()
dh['Z'] = (dh['running_var'] >= cutoff).astype(int)
dh['X_c'] = dh['running_var'] - cutoff

# Fuzzy RDD as 2SLS: Z instruments for treatment
res = IV2SLS.from_formula('outcome ~ 1 + X_c + [treatment ~ Z]', data=dh).fit(cov_type='robust')
print(res.summary)
```

```stata
* Stata: Fuzzy RDD using rdrobust
ssc install rdrobust

* Basic fuzzy RDD
rdrobust outcome running_var, c(0) fuzzy(treatment) bwselect(mserd)

* With covariates
rdrobust outcome running_var, c(0) fuzzy(treatment) ///
    covs(covariate1 covariate2) vce(cluster cluster_var)

* Plot the discontinuity
rdplot outcome running_var, c(0) graph_options(title("Fuzzy RDD"))

* First stage visualization
rdplot treatment running_var, c(0) graph_options(title("First Stage"))

* Manipulation testing
rddensity running_var, c(0)
```

---

---

Related notes to create:
- [[Regression Discontinuity Design (RDD)|regression discontinuity design]]
- [[sharp RDD]]
- [[Instrumental Variables (IV)|instrumental variables]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Wald estimator]]
- [[potential outcomes]]
- [[compliers]]
- [[defiers]]
- [[McCrary test]]
- [[bandwidth selection]]
- [[local linear regression]]
- [[local polynomial regression]]
- [[Calonico-Cattaneo-Titiunik]]
- [[Imbens-Kalyanaraman]]
- [[Regression Discontinuity Design (RDD)|donut RDD]]
- [[Regression Kink Design (RKD)|fuzzy kink design]]
- [[boundary discontinuity|geographic RDD]]
- [[rdrobust]]
- [[manipulation test]]
- [[density test]]
- [[first stage]]
- [[reduced form]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[weak instruments]]