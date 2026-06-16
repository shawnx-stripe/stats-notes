---
title: Regression Discontinuity Design (RDD)
aliases:
- RD design
- RD
- RDD
- regression discontinuity
- regression discontinuity design
- sharp RD
tags:
- econometrics
- causal-inference
- identification
- local-methods
- rdd
updated: 2025-09-17
---

# Regression Discontinuity Design (RDD)

> [!summary] Quick definition
> RDD identifies causal effects by comparing observations just on either side of a cutoff $c$ of a [[running variable]]. Under continuity assumptions and no precise manipulation of the running variable, a discontinuous jump in outcomes at the cutoff is attributed to treatment.

- Two main flavors:
  - Sharp RD: treatment is perfectly determined by crossing the [[cutoff]].
  - Fuzzy RD: treatment probability jumps at the cutoff (imperfect compliance) → identify [[Local Average Treatment Effect (LATE)|LATE]] via a local [[Wald estimator]] (local IV).

## Setup and estimands

- Running variable: $X$; cutoff: $c$; outcome: $Y$; treatment: $D$.

### Sharp RD (SRD) estimand
- Copy-ready:
$$
\tau^{SRD} = \lim_{x \downarrow c} \mathbb{E}[Y \mid X=x] - \lim_{x \uparrow c} \mathbb{E}[Y \mid X=x]
$$

### Fuzzy RD (FRD) estimand (local Wald)
- Copy-ready:
$$
\tau^{FRD} = \frac{\lim_{x \downarrow c} \mathbb{E}[Y \mid X=x] - \lim_{x \uparrow c} \mathbb{E}[Y \mid X=x]}{\lim_{x \downarrow c} \mathbb{E}[D \mid X=x] - \lim_{x \uparrow c} \mathbb{E}[D \mid X=x]}
$$
- Interpreted as a local [[Local Average Treatment Effect (LATE)|Local Average Treatment Effect (LATE)]] for compliers near the cutoff.

## Identification assumptions

- Continuity of untreated potential outcomes at the cutoff:
$$
\lim_{x \downarrow c} \mathbb{E}[Y(0) \mid X=x] = \lim_{x \uparrow c} \mathbb{E}[Y(0) \mid X=x]
$$
- No precise manipulation/sorting of $X$ around $c$ (no bunching right above or below due to strategic behavior).
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]/[[No spillovers]] in the neighborhood of $c$.
- For FRD: instrument relevance (treatment probability jumps) and local [[exclusion restriction]] of $X \ge c$ on $Y$ operating only through $D$.

> [!tip] Local nature
> RD identifies effects for units near $c$ (local external validity). Report the bandwidth used and discuss generalization beyond the margin.

## Estimation (modern best practices)

- Use local polynomial regression (typically local linear) with a triangular kernel and [[MSE-optimal bandwidth]] selection.
- Apply robust bias-corrected (RBC) inference (e.g., [[Calonico-Cattaneo-Titiunik|Calonico–Cattaneo–Titiunik (CCT)]]).
- Avoid global high-order polynomials in $X$.

> [!equation] Local linear form (concept)
> Fit separate local polynomials on each side within bandwidth $h$:
> $$
> Y = \alpha_\pm + \tau \cdot \mathbf{1}\{X \ge c\} + \beta_\pm (X-c) + \text{higher-order local terms} + \varepsilon
> $$
> with kernel weights $K\!\left(\frac{X-c}{h}\right)$.

## Diagnostics and falsification

> [!check] What to examine
> - [[manipulation test]] of the running variable density at $c$ (e.g., [[McCrary test|McCrary density test]] / [[rddensity]]).
> - [[covariate balance]]: check continuity of predetermined covariates at $c$.
> - RD plot (a.k.a. “bin-scatter”): binned means vs. $X$ with local fits on each side.
> - Placebo cutoffs and “donut” RD (exclude observations very close to $c$) to probe robustness.
> - Sensitivity to bandwidth choice and polynomial order; report both MSE-optimal and smaller/larger $h$.

> [!warning] Common pitfalls
> - Using high-order global polynomials in $X$.
> - Ignoring bunching/manipulation near $c$.
> - Not reporting bandwidths, kernels, or RBC vs. conventional SEs.
> - Discrete running variables: standard RD theory weakens; use adapted methods or [[local randomization]] approach with narrow windows.

## Design variants and extensions

- [[fuzzy RDD]] (non-binary or imperfect compliance at the cutoff).
- [[Regression Kink Design (RKD)]]: identify effects from a kink in the slope (derivative) of treatment at $c$.
- Multi-cutoff RD: multiple thresholds; can pool or estimate cutoff-specific effects.
- Geographic/boundary RD (a.k.a. [[boundary discontinuity]] / spatial RD): running variable is distance to a border; account for spatial correlation (e.g., [[Conley standard errors]]).
- Difference-in-discontinuities: combine RD with time variation (pre/post) to difference out confounders.
- [[local randomization]] perspective: treat a small window around $c$ as quasi-random assignment and use randomized-experiment tools.

## Practical guidance

> [!check] Reporting checklist
> - [ ] Define running variable, cutoff, treatment rule (sharp vs. fuzzy).
> - [ ] Show RD plot with binning choices, local fits, and confidence bands.
> - [ ] Report density test (McCrary/rddensity) and covariate continuity tests.
> - [ ] Specify kernel, polynomial order, bandwidth selector; present RBC estimates and CI.
> - [ ] Provide bandwidth and polynomial sensitivity, donut robustness, and placebo cutoffs.
> - [ ] For FRD: report first-stage jump in $D$ and LATE interpretation.

> [!tip] Choices that are often safe
> - Local linear (order 1) on each side, triangular kernel, CCT bandwidth, RBC inference.
> - Symmetric bandwidths unless strong reasons otherwise.

## Minimal code snippets

> [!example] R (rdrobust suite)

```r
# install.packages(c("rdrobust","rddensity"))
library(rdrobust); library(rddensity)

# Main RD (sharp)
rd <- rdrobust(y = df$Y, x = df$X, c = c0, p = 1, kernel = "triangular")
summary(rd)        # RBC estimate and CI
rdplot(y = df$Y, x = df$X, c = c0, binselect = "es")  # RD plot

# Density test (manipulation)
dens <- rddensity(X = df$X, c = c0)
summary(dens); rdplotdensity(dens, df$X)

# Fuzzy RD (D as treatment with imperfect compliance)
rd_fz <- rdrobust(y = df$Y, x = df$X, c = c0, fuzzy = df$D)
summary(rd_fz)     # local LATE with RBC inference
```

> [!example] Stata (rdrobust / rddensity)

```stata
* ssc install rdrobust, replace
* ssc install rddensity, replace

* Sharp RD
rdrobust Y X, c(c0) p(1) kernel(triangular)

* RD plot
rdplot Y X, c(c0)

* Density/manipulation test
rddensity X, c(c0)
rdplotdensity X, c(c0)

* Fuzzy RD (local LATE)
rdrobust Y X, c(c0) fuzzy(D)
```

> [!example] Python (manual local linear, sketch)

```python
import numpy as np
import statsmodels.api as sm

def triangular(u): 
    u = np.abs(u); return np.clip(1 - u, 0, None)

def local_linear_rd(Y, X, c, h):
    z = X - c
    w = triangular(z / h)
    left = z < 0
    right = z >= 0
    # Design: intercept + side-specific slope + treatment indicator at/above c
    D = (X >= c).astype(int)
    Z = np.column_stack([np.ones_like(X), D, z*left, z*right])
    model = sm.WLS(Y, Z, weights=w).fit(cov_type='HC1')  # not RBC; illustrative
    tau = model.params[1]
    return tau, model.bse[1]

tau, se = local_linear_rd(df['Y'].values, df['X'].values, c0, h=5.0)
print(tau, se)
# Prefer R's rdrobust for RBC inference and bandwidth selection.
```

## Copy-ready formulas

- Sharp RD:
$$
\tau^{SRD} = \lim_{x \downarrow c}\mathbb{E}[Y \mid X=x] - \lim_{x \uparrow c}\mathbb{E}[Y \mid X=x]
$$

- Fuzzy RD (local Wald):
$$
\tau^{FRD} = \frac{\Delta Y\ \text{at } c}{\Delta D\ \text{at } c}
$$

- Continuity requirement (untreated):
$$
\lim_{x \downarrow c}\mathbb{E}[Y(0) \mid X=x] = \lim_{x \uparrow c}\mathbb{E}[Y(0) \mid X=x]
$$

## When to use RDD

- Precise, known cutoff rules (scores, age thresholds, eligibility indices).
- Strong incentives to comply with the rule, but potential noncompliance around $c$ is acceptable (FRD).
- Sufficient data density around the cutoff for credible local comparisons.

---

## Related notes
- [[running variable]]
- [[cutoff]]
- [[fuzzy RDD]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Wald estimator]]
- [[local polynomial regression]]
- triangular kernel
- [[MSE-optimal bandwidth]]
- [[Calonico-Cattaneo-Titiunik|Calonico–Cattaneo–Titiunik (CCT)]]
- [[Imbens-Kalyanaraman]] (IK bandwidth)
- [[RD plot]]
- [[covariate balance]]
- [[manipulation test]]
- [[McCrary test|McCrary density test]]
- [[rddensity]]
- [[placebo test]]
- [[Regression Kink Design (RKD)]]
- [[boundary discontinuity]]
- [[spatial RD]]
- [[local randomization]]
- [[Difference-in-Discontinuities]]
- [[Conley standard errors]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
