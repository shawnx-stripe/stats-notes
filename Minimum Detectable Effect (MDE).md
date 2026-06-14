---
title: Minimum Detectable Effect (MDE)
aliases: [MDE, minimally detectable effect, detectable effect size, minimum detectable effect]
tags: [experimentation, design, power, sample-size, ab-testing, ancova, cluster, did, ratios]
updated: 2025-09-17
---

# Minimum Detectable Effect (MDE)

> [!summary] Quick definition
> MDE is the smallest true effect that a study can detect with chosen significance (α) and power (1−β), given variance and design. Equivalently, for fixed N and design, it is the effect size that yields the target power.

- Typical inputs: α, power 1−β, sample sizes (and allocation), variance/SD, design features (blocking/[[stratification]], covariate adjustment (R²), clustering/ICC, serial correlation).
- Outputs: MDE on the chosen scale (absolute, relative, log).

---

## Core formulas (balanced two-arm)

> [!equation] Difference in means (equal variance, equal n per arm)
> $$
> \text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{2}{n}}
> $$

> [!equation] Unequal allocation (ratio k = n_1/n_0)
> $$
> \text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{1}{n_1}+\frac{1}{n_0}}
> $$

> [!equation] Proportions (two-sample; approximate)
> $$
> \text{MDE} \approx z_{1-\alpha/2}\sqrt{2\bar p(1-\bar p)\left(\frac{1}{n_1}+\frac{1}{n_0}\right)}
> \;+\; z_{1-\beta}\sqrt{\frac{p_1(1-p_1)}{n_1}+\frac{p_0(1-p_0)}{n_0}}
> $$
> with $\bar p=(p_1+p_0)/2$ (use a design-stage guess for p’s).

> [!equation] Ratios/percent changes via delta method
> For ratio metric $R=Y/X$ with means $(\mu_Y,\mu_X)$:
> $$
> \Var(R) \approx \frac{1}{\mu_X^2}\Var(Y)-\frac{2\mu_Y}{\mu_X^3}\Cov(Y,X)+\frac{\mu_Y^2}{\mu_X^4}\Var(X)
> $$
> Plug $\sqrt{\Var(R)}$ for σ above to get MDE on ratio scale.

> [!equation] Log-scale outcomes (percent effects)
> If outcome is log-transformed with SD $\sigma_{\log}$, then
> $$
> \text{MDE}_{\log} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma_{\log}\,\sqrt{\frac{2}{n}}
> $$
> Percent MDE ≈ $\exp(\text{MDE}_{\log})-1$.

---

## Design adjustments (precision up or down)

> [!tip] Adjust the effective variance before computing MDE.

- Covariate adjustment (ANCOVA / [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]])
  - Replace $\sigma^2$ by $\sigma^2(1-R^2)$ where $R^2$ is the variance explained by baseline covariates/pre-period outcome.
- Blocking / [[stratification]]
  - Replace $\sigma^2$ by $\sigma^2(1-R_b^2)$, where $R_b^2$ is variance explained by blocks.
- Cluster randomized designs (CRTs)
  - Inflate variance by design effect (DE):
  $$
  DE \approx 1 + (m-1)\rho \quad (\text{ICC } \rho; \text{avg cluster size } m),
  $$
  and with unequal cluster sizes (CV of size):
  $$
  DE \approx 1 + (m̄-1)\rho\,(1+CV^2).
  $$
  - Use $\sigma_{\text{eff}}=\sigma\sqrt{DE}$ or $n_{\text{eff}}=n/DE$ in MDE.
- Serial correlation (switchback/time-sliced)
  - Effective observations $N_{\text{eff}}\approx N\cdot \frac{1-\rho}{1+\rho}$ (AR(1) heuristic). Use $N_{\text{eff}}$ in MDE.
- Multiple testing / sequential looks
  - Effective α smaller under Bonferroni/Holm or α-spending → larger z-terms → larger MDE.

---

## Difference-in-Differences (DiD) MDE (heuristics)

- With unit FE and T periods (T_pre pre, T_post post), per-arm sample ≈ n units:
  - Variance of DiD estimator shrinks with more periods and stronger unit autocorrelation (ρ_Y) due to differencing:
  $$
  \text{MDE}_{DiD} \propto (z\text{’s}) \times \sigma_Y \times \sqrt{\frac{1-\rho_Y}{n\cdot T_{\text{eff}}}}
  $$
- In practice, simulate using historical variance structure and planned clustering (cluster-robust SEs often dominate). See [[Difference-in-Differences (DiD)]] and [[power analysis]].

---

## AB testing specifics

- ITT vs triggered population
  - Define which estimand MDE targets; triggered designs use exposed users, which changes variance and n.
- Variance reduction
  - [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] with robust pre-exposure baselines materially lowers MDE via $(1-R^2)$.
- Duration and cycles
  - Ensure run covers day-of-week/seasonality; otherwise variance estimates and MDE can be off (see [[seasonality]]).
- Cluster/session/geo designs
  - Use cluster DE and plan at cluster level; apply [[clustered standard errors]] and [[few-cluster corrections]].

---

## Converting between absolute and relative MDE

- Relative (% of baseline mean μ):
  $$
  \text{MDE}_{\%} = \frac{\text{MDE}_{\text{abs}}}{\mu}\times 100\%
  $$
- Given target relative effect r%, absolute MDE is $r\%\times \mu$; plug as δ in formulas.

---

## Minimal code snippets

> [!example] R: MDE for means; ANCOVA and clustering

```r
alpha <- 0.05; power <- 0.8
z1a <- qnorm(1 - alpha/2); z1b <- qnorm(power)

sigma <- 10; n_per_arm <- 1000
MDE <- (z1a + z1b) * sigma * sqrt(2 / n_per_arm)

# ANCOVA/CUPED adjustment
R2 <- 0.5
MDE_ancova <- (z1a + z1b) * sigma * sqrt( (1 - R2) * 2 / n_per_arm )

# Cluster design effect
m <- 50; ICC <- 0.02
DE <- 1 + (m - 1) * ICC
MDE_cluster <- (z1a + z1b) * sigma * sqrt( 2*DE / n_per_arm )
```

> [!example] Stata: MDE via power commands (invert for N if needed)

```stata
* Given n per arm, approximate MDE for two-sample means (balanced)
local alpha = 0.05
local power = 0.80
local sd = 10
local n = 1000
scalar z1a = invnormal(1-`alpha'/2)
scalar z1b = invnormal(`power')
scalar MDE = (z1a + z1b) * `sd' * sqrt(2/`n')
di "MDE = " %9.4f MDE
```

> [!example] Python: MDE for means with statsmodels

```python
from statsmodels.stats.power import TTestIndPower
import numpy as np

alpha=0.05; power=0.8; sigma=10; n_per_arm=1000
z_term = 1.959964 + 0.841621  # ~ z_(1-alpha/2) + z_(power)
MDE = z_term * sigma * np.sqrt(2 / n_per_arm)
print(MDE)
```

> [!example] R: Ratio metric MDE via delta method (sketch)

```r
muY <- 5; muX <- 2
varY <- 4; varX <- 0.5; covYX <- 0.2
varR <- varY/muX^2 - 2*muY*covYX/muX^3 + (muY^2)*varX/muX^4
sdR <- sqrt(varR)
MDE_ratio <- (z1a + z1b) * sdR * sqrt(2 / n_per_arm)
```

> [!example] R: Simulated DiD MDE (template; see [[power analysis]] for details)

```r
# simulate panels, estimate FE DiD with cluster SEs, sweep delta to hit 80% power
```

---

## Planning checklist

> [!check] Before you compute MDE
> - [ ] Clarify estimand (absolute vs relative; ITT vs triggered) and scale (raw/log/ratio)  
> - [ ] Use representative variance and, for ratios, covariances  
> - [ ] Account for design: covariate R², blocks/strata, clustering (ICC/DE), serial correlation  
> - [ ] Consider multiple testing/sequential looks (adjust α)  
> - [ ] Ensure runtime covers seasonality/cycles; exclude outages/blackouts  
> - [ ] If clustered/few clusters: plan using cluster-level variance and apply [[few-cluster corrections]] in analysis

---

## Reporting essentials

- Inputs: α, power, allocation, variance/SD (and R², ICC, CV of cluster sizes, serial ρ as applicable)
- Output: MDE on chosen scale (absolute and %), and implied runtime if N accrues over time
- Adjustments: covariate/blocking reductions; design effect; multiplicity/sequential inflation
- Sensitivity: MDE under high/low variance, ICC, R²; alternative allocations (e.g., 75/25 vs. 50/50)
- Assumptions: seasonality coverage; data quality/exposure logging for AB tests

---

## Common pitfalls

> [!warning]
> - Ignoring clustering/ICC → overly optimistic MDE  
> - Using historical variance not representative of the experimental population or metric definition  
> - CUPED/ANCOVA with post-treatment features (leakage) inflates apparent power  
> - Ratio/log metrics without proper delta/log variance treatment  
> - Not adjusting for sequential peeking or multiple metrics  
> - Underestimating serial correlation in switchback/geo tests

---

## Copy-ready snippets

- Means (balanced):
$$
\text{MDE} = (z_{1-\alpha/2}+z_{1-\beta})\,\sigma\,\sqrt{\frac{2}{n}}
$$

- Design effects:
$$
DE \approx 1 + (m-1)\rho, \quad
DE \approx 1 + (m̄-1)\rho\,(1+CV^2)
$$

- ANCOVA/CUPED:
$$
\sigma_{\text{adj}}^2 = \sigma^2(1-R^2)
$$

- Log to percent:
$$
\%\Delta \approx \exp(\text{MDE}_{\log}) - 1
$$

---

## Related notes

- [[power analysis]] · [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]
- [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[stratification]]
- [[clustered standard errors]] · [[few-cluster corrections]] · [[ICC]]
- [[seasonality]] · [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]