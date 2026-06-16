---
title: Spillovers
aliases: [Spillovers, interference effects, externalities, cross-unit effects]
tags: [causal-inference, did, interference, spatial, networks, policy-evaluation]
updated: 2025-09-17
---

# Spillovers

> [!summary] Quick definition
> Spillovers occur when one unit’s treatment affects other units’ outcomes. This violates the [[No spillovers]] (no-interference) part of [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and can bias designs like [[Difference-in-Differences (DiD)]], RD near borders, and IV with assignment externalities. See also: [[interference]].

- Threat: untreated “controls” are partially treated via exposure channels, breaking the [[parallel trends assumption]] and attenuating or exaggerating estimated effects.

## Types and channels

- Geographic: proximity to treated regions (border effects, commuting zones)
- Market: price, wage, demand, or competition effects
- Networks: peers, suppliers/customers, social media diffusion
- Policy displacement or migration
- Information/anticipation externalities (media, announcements)

> [!note] Direction of bias
> - Positive spillovers to controls typically attenuate effects toward zero.
> - Negative spillovers to controls can inflate effects.

## Minimal formalism (exposure mapping)

- Exposure to others’ treatment:
$$
E_i = \sum_j w_{ij} D_j
$$
with weights $w_{ij}$ encoding proximity, network ties, or market overlap.

- Potential outcomes depend on own treatment and exposure:
$$
Y_i = Y_i(d_i, e_i)
$$

- Direct and spillover effects (Hudgens–Halloran style):
$$
DE(e) = \mathbb{E}[Y_i(1,e) - Y_i(0,e)], \quad
IE(e_1,e_0) = \mathbb{E}[Y_i(0,e_1) - Y_i(0,e_0)]
$$

## Diagnosing spillovers

> [!check] Useful (but not decisive) checks
> - Distance gradients: effects for “near” vs. “far” controls; interact [[event study]] with proximity bins.
> - Border/boundary checks: discontinuities at administrative borders (see [[boundary discontinuity]]).
> - Placebos on outcomes/channels that should not be affected.
> - Residual spatial dependence (e.g., [[Moran’s I]]) on DiD residuals.
> - Sensitivity to excluding likely-exposed controls (spatial “donut” buffers), donor-pool pruning in [[Synthetic Control]].
> - For staggered rollouts, compare near/far controls over time; use [[Callaway–Sant’Anna estimator]] or [[Sun–Abraham estimator]] with exposure-aware comparisons.

## Design and modeling strategies

### 1) Avoidance by design
- Exclude controls within buffers around treated units (donut).
- Use controls in separate markets or non-adjacent geographies.
- Randomize at cluster level with large separation between clusters.
- Short analysis windows to limit diffusion.

### 2) Partial interference
- Assume interference only within clusters, none across clusters. Analyze at cluster level; use cluster-by-time effects and cluster-robust inference. See [[partial interference]].

### 3) Randomized saturation designs
- Randomize the share treated within clusters to identify direct and indirect effects; vary saturation across clusters. See [[randomized saturation design]].

### 4) Exposure modeling
- Include exposure alongside own treatment:
$$
Y_{it} = \alpha_i + \gamma_t + \beta (D_{it}\cdot Post_t) + \eta (E_{it}\cdot Post_t) + X_{it}'\theta + \varepsilon_{it}
$$
- Define $w_{ij}$ via distance decay, contiguity, or networks; report robustness to alternative $w$.

### 5) Robust comparisons
- [[Triple Differences (DDD)|DDD]] to difference out dimensions less affected by spillovers.
- Border-focused designs ([[boundary discontinuity]]) when treatment is assigned by geography.

> [!warning] Inference vs. bias
> [[clustered standard errors]] or [[Conley standard errors]] handle correlated errors but do not remove spillover bias. The design or model must address exposure.

## Spillovers in common designs

- DiD: Prefer control groups plausibly unexposed; run exposure-aware [[event study]] (near/far bins). For [[staggered adoption]], use CS/SA estimators and check proximity heterogeneity.
- RD at borders: Consider spatial RD with appropriate clustering/HAC and donut RD excluding right at the border.
- IV/Encouragement: Exclusion can fail if the offer Z shifts Y directly via spillovers; discuss and test reduced-form externalities.

## Minimal code sketches

> [!example] R: spatial buffer (donut) and exposure

```r
# Spatial buffer around treated units (points), using sf
library(sf); library(dplyr)
g <- st_as_sf(df, coords = c("lon","lat"), crs = 4326) |> st_transform(3857)
buf <- g |> filter(D == 1) |> st_buffer(20000) |> st_union()  # 20 km buffer
df$near_treated <- as.integer(st_intersects(g, buf, sparse = FALSE))

# Exclude likely-exposed controls
df_clean <- df |> filter(!(D == 0 & near_treated == 1))

# Simple exposure via k-NN treated share (sketch)
library(FNN)
coords <- as.matrix(df[,c("lon","lat")])
nn <- get.knn(coords, k = 5)$nn.index
df$E <- rowMeans(apply(nn, 2, function(idx) df$D[idx]))
```

> [!example] Python: network exposure

```python
import numpy as np
# A: row-normalized adjacency; D: treatment indicator
A = adjacency / (adjacency.sum(axis=1, keepdims=True) + 1e-12)
E = A @ df['D'].to_numpy()
df['E'] = E
# Use D*Post and E*Post in a FE regression (e.g., linearmodels PanelOLS)
```

> [!example] Stata: near/far bins for event-study heterogeneity (sketch)

```stata
* Define near/far by distance threshold dist_km
gen near = dist_km <= 20
eventstudyinteract Y G time, cohort(G) absorb(id time) vce(cluster id) by(near)
* Compare event-time paths for near vs far controls
```

## Copy-ready formulas

- Exposure mapping:
$$
E_i = \sum_j w_{ij} D_j
$$

- Direct and indirect effects:
$$
DE(e) = \mathbb{E}[Y_i(1,e) - Y_i(0,e)], \quad
IE(e_1,e_0) = \mathbb{E}[Y_i(0,e_1) - Y_i(0,e_0)]
$$

- Exposure-augmented DiD:
$$
Y_{it} = \alpha_i + \gamma_t + \beta (D_{it}\cdot Post_t) + \eta (E_{it}\cdot Post_t) + X_{it}'\theta + \varepsilon_{it}
$$

## Reporting essentials

- Define treatment, exposure (weights $w_{ij}$), and suspected channels.
- Show proximity analyses (near/far), exposure gradients, and buffer robustness.
- Document comparison groups and any excluded areas/clusters.
- Report clustering level; consider spatial HAC (e.g., [[Conley standard errors]]) and [[few-cluster corrections]] when clusters are few.

## Common pitfalls

> [!warning] Avoid these
> - Assuming [[No spillovers]] without proximity checks.
> - Keeping clearly exposed controls; DiD estimates often attenuate.
> - Treating clustered SEs as a fix for spillover bias.
> - Using a single arbitrary $w_{ij}$ without robustness to alternative exposure definitions.

---

## Related notes
- [[No spillovers]]
- [[interference]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[parallel trends assumption]]
- [[Anticipatory effects]]
- [[Triple Differences (DDD)|DDD]]
- [[boundary discontinuity]]
- [[Synthetic Control]]
- [[staggered adoption]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[exposure mapping]]
- [[partial interference]]
- [[randomized saturation design]]
- [[Moran’s I]]
- [[Conley standard errors]]
- [[clustered standard errors]]
- [[few-cluster corrections]]