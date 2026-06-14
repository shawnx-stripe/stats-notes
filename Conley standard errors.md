---
title: Conley standard errors
aliases: [Conley SEs, spatial HAC, spatially correlated errors, Conley (1999, 2008)]
tags: [econometrics, inference, standard-errors, spatial, panel, hac, clustering, did, geo]
updated: 2025-09-17
---

# Conley standard errors

> [!summary] Quick definition
> Conley standard errors are heteroskedasticity- and autocorrelation-consistent (HAC) covariances that allow regression errors to be spatially correlated across nearby observations (and optionally temporally correlated in panels). They downweight correlations as distance (and time lag) increase, providing valid inference under spatial dependence.

- Use when residuals are plausibly correlated across space (nearby units/markets/geos) and standard or cluster-robust SEs are not appropriate.
- Typical in [[geo experiment]]s, regional panels, spatial policy shocks, and settings with spillovers or common local shocks.

---

## When to use

- Cross-sections with spatially clustered shocks: nearby units share environment/markets.
- Panels where errors are correlated within nearby units and over short time lags.
- Alternatives:
  - [[clustered standard errors]]: good for discrete clusters (state, firm) with independence across clusters.
  - Conley: good for continuous spatial decay (no clear hard cluster boundaries).
  - [[Driscoll–Kraay]]: panel robust to general cross-sectional dependence (time-series HAC across entities), but not explicitly distance-weighted.
  - [[Conley standard errors]] can be combined with time HAC (spatial+temporal).

---

## How it works (sandwich form)

Let y = Xβ + u, with residuals û. The Conley (spatial HAC) estimator replaces the meat of the sandwich with a kernel-weighted sum over pairs (i,j):

- Cross-section (distance-only):
$$
\widehat{V}(\hat\beta) = (X'X)^{-1}\left(\sum_{i=1}^N\sum_{j=1}^N K\!\left(\frac{d_{ij}}{h}\right)\,x_i \hat u_i \hat u_j x_j'\right)(X'X)^{-1}
$$
- Panel with time lags (Conley (2008)):
$$
\sum_{t}\sum_{\ell=-L}^{L}\ \sum_{i}\sum_{j} K_d\!\left(\frac{d_{ij}}{h}\right)\,K_t(\ell)\,x_{it}\hat u_{it}\,\hat u_{j,t-\ell}\,x_{j,t-\ell}'
$$

- d_{ij}: great-circle or projected distance between i and j.
- h: distance bandwidth/cutoff (often a hard cutoff).
- K_d: spatial kernel (e.g., Bartlett/triangular, uniform).
- L, K_t: temporal lag window and kernel (often Bartlett with L small, e.g., 0–2).

Intuition: nearby observations contribute more to the covariance; beyond the cutoff, weight is zero.

---

## Choices you must make

- Distance metric
  - Great-circle (lat/lon on WGS84) or projected planar coordinates (e.g., UTM). Be consistent with units (km/miles).
- Spatial kernel K_d and cutoff/bandwidth h
  - Common: Bartlett (triangular) with hard cutoff (weights linearly decay to 0 at h); or uniform within h.
  - Sensitivity: vary h (e.g., 50/100/200 km) and report robustness.
- Temporal kernel and lag L (for panels)
  - Often Bartlett up to L = 1–2 periods; set L based on plausible serial correlation horizon.
- Fixed effects and controls
  - Include relevant FE (entity/time) and covariates as in your substantive model; Conley adjusts only the covariance, not the mean specification.

> [!tip] Reporting
> Always report: kernel, spatial cutoff (and units), temporal lag L (if any), coordinate system used, and robustness to alternative cutoffs.

---

## Implementation (software)

### R

- conleyreg / ConleySEs packages (user-written implementations)

```r
# Example 1: ConleySEs (returns a vcov matrix)
library(ConleySEs); library(lmtest)
mod <- lm(Y ~ X1 + X2, data = df)
# Provide unit/time ids and coordinates; choose distance cutoff (km) and time lags
Vc <- ConleySEs(reg = mod,
                unit = df$id, time = df$year,
                lat = df$lat, lon = df$lon,
                dist_cutoff = 100,    # kilometers
                lag_cutoff = 0,       # temporal lags
                kernel = "bartlett")
coeftest(mod, vcov. = Vc)

# Example 2: conleyreg (formula interface; implementation may vary by package)
# install.packages("conleyreg")  # if available
# library(conleyreg)
# out <- conleyreg(Y ~ X1 + X2, data=df, lat="lat", lon="lon",
#                  cutoff=100, kernel="bartlett", unit="id", time="year")
# summary(out)
```

- Spatial distances: geosphere::distHaversine or sf::st_distance for great-circle vs projected distances.

### Stata

- User-written conleyreg (Colella, Lalive, Lalive) or equivalents

```stata
* Install (if needed): ssc install conleyreg
conleyreg Y X1 X2, lat(lat) lon(lon) dist(100) kernel(bartlett) ///
    unit(id) time(year)

* Alternatives: some packages allow temporal lags: tlag(#)
* For FE models, include absorbed FEs in the mean equation (e.g., reghdfe), then apply Conley SEs via postestimation (package dependent).
```

### Python

- No ubiquitous built-in; options:
  - linearmodels/statsmodels for OLS, then custom Conley vcov (sketch below).
  - Third-party implementations (if available) or port from R/Stata.

```python
import numpy as np
from sklearn.metrics import pairwise_distances
import statsmodels.api as sm

def conley_vcov(X, resid, coords, cutoff_km=100.0, kernel='bartlett'):
    """
    Very simplified spatial Conley vcov (no time, great-circle approx via haversine optional).
    X: (N,K) design, resid: (N,), coords: (N,2) lat/lon in degrees
    """
    # crude planar approx (use haversine for accuracy)
    dmat = pairwise_distances(coords, metric='euclidean')  # replace with great-circle km
    W = np.where(dmat < cutoff_km, 1.0 - dmat/cutoff_km, 0.0) if kernel=='bartlett' else (dmat < cutoff_km).astype(float)
    meat = (X * resid[:,None]).T @ W @ (X * resid[:,None])
    XtX_inv = np.linalg.inv(X.T @ X)
    return XtX_inv @ meat @ XtX_inv

# Fit OLS, then replace covariance
X = sm.add_constant(df[['X1','X2']].to_numpy())
y = df['Y'].to_numpy()
res = sm.OLS(y, X).fit()
coords = df[['lat','lon']].to_numpy()
Vc = conley_vcov(X, res.resid, coords, cutoff_km=100.0, kernel='bartlett')
se_conley = np.sqrt(np.diag(Vc))
```

> [!warning] Python sketch is illustrative. Prefer tested libraries (R/Stata) or a vetted Python implementation for production.

---

## Practical guidance

> [!check] Checklist
> - [ ] Use accurate coordinates (WGS84) and great-circle distances (km/miles) or consistent projection
> - [ ] Choose kernel and cutoff based on domain knowledge (e.g., commuting/market radius)
> - [ ] If panel: set temporal lag L and include time FE; consider entity FE
> - [ ] Compare with cluster SEs at plausible geo levels as a robustness check
> - [ ] Run sensitivity to cutoffs (e.g., 50/100/200 km) and report stability
> - [ ] In small samples/few geos: prefer [[few-cluster corrections]] or SCM placebos (for single/few treated geos)

---

## Diagnostics and sensitivity

- Plot residual semivariograms/correlograms vs distance to assess spatial correlation range.
- Evaluate stability of t-stats across multiple cutoffs and kernels.
- For panels, inspect ACFs of residuals to set temporal lag L.
- Compare Conley vs cluster SEs (e.g., state-level clustering) for plausibility.

---

## Common pitfalls

> [!warning]
> - Using Euclidean distances on degrees (lat/lon) without projection → wrong distances  
> - Arbitrary cutoff with no sensitivity checks  
> - Ignoring strong time dependence in panels (set temporal lag L=0 by default)  
> - Treating Conley as a fix for misspecification (e.g., omitted spatial trends) — include appropriate FE/controls  
> - Combining with post-treatment spatial controls (see [[bad controls]])

---

## Reporting essentials

- Mean specification (FE, controls), software used, and:
  - Kernel (Bartlett/uniform), spatial cutoff h (units), and temporal lag L (if any)
  - Distance metric (great-circle/projection) and coordinate source
  - Number of observations/entities and time periods
  - Sensitivity to alternative cutoffs and comparison to cluster SEs
- Present coefficient estimates with Conley SEs (and optionally cluster SEs) side by side.

---

## Related notes

- [[clustered standard errors]] · [[clustering]] · [[few-cluster corrections]] · [[Driscoll–Kraay]]
- [[geo experiment]] · [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]
- [[spillovers]] · [[seasonality]] · [[No spillovers]] · [[interference]]