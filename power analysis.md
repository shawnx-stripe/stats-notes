---
title: Power Analysis
aliases: [power calculation, sample size]
tags: [experimentation, design, power, sample-size, mde, cluster, ancova, sequential, ab-testing, did]
updated: 2025-09-17
---

# Power Analysis

> [!summary] Quick definition
> Power analysis determines the sample size (or runtime) required to detect a minimally important effect with a chosen significance level, or the smallest detectable effect (MDE) given a sample size. It depends on variance, effect size, allocation ratio, test type, and design features (clustering, blocking, covariates, serial/spatial correlation).

- Typical inputs: significance α (two-sided), power 1−β, effect δ, variance σ²
- Outputs: per-arm sample size n (or duration) or the MDE

---

## Core concepts

- Power and error rates
  - Significance α (Type I error), Power 1−β (Type II complement)
  - Two-sided vs. one-sided tests
- Effect size
  - Absolute (e.g., Δ in means), relative (% change), standardized (Cohen’s d = Δ/σ)
- Variance and precision levers
  - Variance σ², covariate adjustment (R²), blocking/stratification, clustering/ICC, autocorrelation
- MDE vs. N
  - MDE decreases as O(1/√N); precision gains from design features reduce the needed N

---

## Canonical formulas (balanced two-arm)

> [!equation] Difference in means (equal variance, equal n per arm)
> Required per arm:
> $$
> n = \frac{2\,(z_{1-\alpha/2}+z_{1-\beta})^2\,\sigma^2}{\delta^2}
> $$
> MDE (given n per arm):
> $$
> \text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{2}{n}}
> $$

> [!equation] Unequal allocation (ratio k = n_1/n_0)
> $$
> \text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{1}{n_1}+\frac{1}{n_0}}
> $$

> [!equation] Proportions (two-sample; approximate)
> $$
> n \approx \frac{\left[z_{1-\alpha/2}\sqrt{2\bar p(1-\bar p)} + z_{1-\beta}\sqrt{p_1(1-p_1)+p_0(1-p_0)}\right]^2}{(p_1-p_0)^2}
> $$
> with $\bar p=(p_1+p_0)/2$ for equal allocation.

---

## Precision gains from design

> [!tip] Adjust variance before plugging into formulas.

- ANCOVA / CUPED (covariate adjustment)
  - Replace σ² by σ²(1−R²), where R² is explanatory power of pre-exposure baseline
- Blocking / stratification
  - Replace σ² by σ²(1−R_b²), where R_b² is variance explained by blocks
- Cluster randomized designs (CRTs)
  - Design effect (DE) inflates variance:
  $$
  DE \approx 1 + (m-1)\rho \quad \text{(equal cluster size m, ICC } \rho)
  $$
  - With variable cluster sizes (CV of cluster size):
  $$
  DE \approx 1 + (m̄-1)\rho\,(1+CV^2)
  $$
  - Effective sample: $n_{\text{eff}} = n/DE$
- Ratio metrics (A/B)
  - Use delta method: $\Var(Y/X)\approx \frac{1}{\mu_X^2}\Var(Y)-\frac{2\mu_Y}{\mu_X^3}\Cov(X,Y)+\frac{\mu_Y^2}{\mu_X^4}\Var(X)$

---

## Time and dependence effects

- Serial autocorrelation (switchback/time-sliced designs)
  - Effective sample size (AR(1) heuristic): $N_{\text{eff}}\approx N \frac{1-\rho}{1+\rho}$; choose block lengths exceeding correlation span
- Difference-in-Differences (panel)
  - Gains from multiple periods and pre-period correlation ρ_Y:
  $$
  \text{MDE}_{DiD}\ \propto\ (z\text{’s}) \times \sqrt{\frac{\sigma^2_{Y}}{n\cdot T}}\ \times \sqrt{1-\rho_Y}
  $$
  - More pre-periods (larger T) and stronger unit-level correlation (ρ_Y) reduce variance; clustered inference often governs power (see below)
- Geo/cluster experiments
  - Few clusters → power dominated by between-cluster variance; plan at cluster level and use [[few-cluster corrections]]; consider matched-pairs or [[Synthetic Control]]

---

## Multiple testing and sequential looks

- Multiple outcomes (families)
  - Adjust α (FWER Bonferroni/Holm) or control [[False Discovery Rate (FDR)|FDR]]; effective α increases required n
- Sequential/peeking
  - Group-sequential tests require α-spending; information fraction < 1 inflates required n vs. fixed-horizon designs

---

## A/B (AB) testing specifics

- Variance reduction: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] (ANCOVA with pre-exposure baseline), stratification by traffic segment
- Triggered vs. ITT populations: define estimand; use exposure-based baselines for CUPED
- Duration: cover day-of-week/seasonality cycles; avoid outages/holiday bias (see [[seasonality]])
- Diagnostics: [[AA test]] power; [[Sample Ratio Mismatch (SRM)|SRM]] monitors; cluster or session-level randomization implies clustered SEs

---

## Clustered and stepped-wedge trials

- Cluster randomization
  - Plan using cluster-level variance or ICC-based DE; prioritize increasing #clusters over cluster size
- Stepped-wedge (staggered rollout)
  - Power driven by cluster count and within-cluster pre/post contrast; analyze with DiD/GLMM; check spillovers

---

## Minimal code snippets

> [!example] R: Means and proportions; ANCOVA adjustment

```r
# Means (balanced; known sd)
alpha <- 0.05; power <- 0.8; sigma <- 10; delta <- 2
z1a <- qnorm(1 - alpha/2); z1b <- qnorm(power)
n_per_arm <- 2 * ( (z1a + z1b)^2 * sigma^2 ) / (delta^2)

# MDE given n
n <- 500
MDE <- (z1a + z1b) * sigma * sqrt(2 / n)

# Proportions (approx)
p0 <- 0.20; p1 <- 0.24; pbar <- (p0 + p1)/2
n_prop <- ( z1a*sqrt(2*pbar*(1-pbar)) + z1b*sqrt(p1*(1-p1) + p0*(1-p0)) )^2 / ( (p1-p0)^2 )

# ANCOVA/CUPED adjustment: use sigma_adj = sigma*sqrt(1 - R2)
R2 <- 0.5
sigma_adj <- sigma * sqrt(1 - R2)
n_per_arm_ancova <- 2 * ( (z1a + z1b)^2 * sigma_adj^2 ) / (delta^2)
```

> [!example] R: Cluster design effect and effective n

```r
m <- 50        # avg cluster size
ICC <- 0.02
DE <- 1 + (m - 1) * ICC
n_raw <- 5000
n_eff <- n_raw / DE
```

> [!example] Stata: power for means/proportions; clusters

```stata
* Two-sample means (balanced)
power twomeans 0 2, sd(10) power(0.8) alpha(0.05)

* Two-sample proportions
power twoproportions 0.20 0.24, alpha(0.05) power(0.8)

* Clustered means (approx via design effect)
local m = 50
local ICC = 0.02
local DE = 1 + (`m' - 1)*`ICC'
power twomeans 0 2, sd(10*sqrt(`DE')) power(0.8) alpha(0.05)
```

> [!example] Python: statsmodels power

```python
from statsmodels.stats.power import TTestIndPower, NormalIndPower
import numpy as np

alpha=0.05; power=0.8; sigma=10; delta=2
effect = delta / sigma
analysis = TTestIndPower()
n_per_arm = analysis.solve_power(effect_size=effect, alpha=alpha, power=power, alternative='two-sided')

# Proportions (approx, normal)
p0, p1 = 0.20, 0.24
pbar = (p0 + p1)/2
z_alpha = 1.959964; z_beta = 0.841621
n_prop = ( z_alpha*np.sqrt(2*pbar*(1-pbar)) + z_beta*np.sqrt(p1*(1-p1) + p0*(1-p0)) )**2 / ( (p1-p0)**2 )
```

> [!example] Heuristic DiD MDE (simulation template in R)

```r
# Simulate panel to approximate MDE under DiD with serial correlation and cluster SEs
library(fixest)
set.seed(1)
G <- 50  # clusters
Tt <- 8  # periods (half pre, half post)
N <- 50  # units per cluster per period
rho_u <- 0.6 # cluster-time corr proxy via random effects

sim_once <- function(delta=0){
  df <- expand.grid(g=1:G, t=1:Tt, i=1:N)
  df$post <- as.integer(df$t > Tt/2)
  # treat half the clusters
  treat_g <- sample(1:G, G/2)
  df$treat <- as.integer(df$g %in% treat_g)
  # random effects
  alpha_g <- rnorm(G, 0, 1)[df$g]
  gamma_t <- rnorm(Tt, 0, 1)[df$t]
  eps <- rnorm(nrow(df), 0, 1)
  Y0 <- alpha_g + gamma_t + eps
  df$Y <- Y0 + delta * (df$treat * df$post)
  est <- feols(Y ~ treat:post | g + t, cluster=~g, data=df)
  coef(est)["treat:post"]
}
# Loop over deltas to find hit-rate ~ power target
```

---

## Planning checklist

> [!check] Before you compute
> - [ ] Estimand and test (two-sided/one-sided)  
> - [ ] Baseline variance and metric definition (ratio/log?)  
> - [ ] Allocation ratio and constraints  
> - [ ] Design features: clustering (ICC), blocking/strata, covariate baselines (R²), autocorrelation  
> - [ ] Multiple metrics/families and sequential looks (α adjustments)  
> - [ ] Interference risks and spillovers (may reduce effective n)  
> - [ ] Seasonality/calendar coverage (runtime)  
> - [ ] Attrition/missingness assumptions (consider [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]], [[Lee bounds]])

---

## Reporting essentials

- Inputs: α, 1−β, effect scale (absolute/relative/standardized), variance/SD, allocation, design assumptions (ICC, R², blocking)
- Output: required n per arm (or duration) and/or MDE
- Adjustments: multiplicity/sequential; covariate/blocking reductions; clustering inflation
- Sensitivity: ranges for key inputs (variance, ICC, R²) and resulting n/MDE
- Operational plan: ramp schedule, monitoring (AA/SRM), stopping rules

---

## Common pitfalls

> [!warning]
> - Ignoring clustering/ICC (over-optimistic power)  
> - Under-accounting for autocorrelation or seasonality in time-sliced/geo tests  
> - CUPED/ANCOVA using post-treatment features (leakage)  
> - Using historical variance not representative of experiment context  
> - Treating pilot uplift as “true” δ without uncertainty  
> - Multiple metrics/sequential peeks without α adjustment  
> - Planning on per-session while analyzing per-user (unit mismatch)

---

## Copy-ready snippets

- Means (balanced):
$$
n = \frac{2\,(z_{1-\alpha/2}+z_{1-\beta})^2\,\sigma^2}{\delta^2},\quad
\text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{2}{n}}
$$

- Design effects:
$$
DE \approx 1 + (m-1)\rho \quad (\text{ICC } \rho),\quad
DE \approx 1 + (m̄-1)\rho(1+CV^2)
$$

- ANCOVA/CUPED:
$$
\sigma_{\text{adj}}^2 = \sigma^2(1-R^2)
$$

---

## Related notes

- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]
- [[Minimum Detectable Effect (MDE)|MDE]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[stratification]] · [[randomized controlled trial (RCT)|cluster randomization]] · [[ICC]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]]
- [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]
- [[seasonality]] · [[clustered standard errors]] · [[few-cluster corrections]]
- [[Attrition]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Lee bounds]]
