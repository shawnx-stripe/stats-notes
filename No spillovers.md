---
title: No Spillovers
aliases: [no interference, SUTVA-no-interference, absence of spillovers]
tags: [causal-inference, assumptions, did, interference, sutva, design]
updated: 2025-09-17
---

# No Spillovers

> [!summary] Quick definition
> The assumption that one unit’s treatment does not affect other units’ outcomes. Formally, each unit’s outcome depends only on its own treatment, not on others’ treatment status. This is the “no-interference” part of [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and is often summarized as “no spillovers.”

- Why it matters: Many designs (especially [[Difference-in-Differences (DiD)]]) require that the [[control group]] is unaffected by the treatment given to the [[treated group]]. If controls are affected, estimates are biased.

## Formal statement

Let D be the vector of treatment assignments across all units. No spillovers means unit i’s potential outcome depends only on its own treatment:
- Copy-ready:
$$
Y_i(d_i, \mathbf{d}_{-i}) = Y_i(d_i, \mathbf{d}'_{-i}) \quad \text{for all } \mathbf{d}_{-i}, \mathbf{d}'_{-i}
$$
Equivalently, write $Y_i(d)$ as $Y_i(d_i)$.

> [!note] Relation to [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
> SUTVA consists of (a) no hidden variations of treatment (consistency) and (b) no interference (no spillovers). This page is about (b).

## Why violations bias DiD

- If some controls are affected by nearby treatment (e.g., business diversion, information diffusion), their outcomes change even without being treated, breaking the [[parallel trends assumption]].
- Direction of bias depends on how control outcomes move relative to treated outcomes:
  - Positive spillovers to controls attenuate effects toward zero.
  - Negative spillovers to controls exaggerate effects.

## Common sources of spillovers

- Geographic diffusion (neighbors, border regions)
- Market competition and price effects
- Networks and peer effects (schools, firms, social graphs)
- Policy displacement or migration
- General equilibrium effects (labor, housing, input markets)
- Information and media reach beyond treated units

## Diagnostics and falsification (imperfect but useful)

> [!check] What to look for
> - Compare “nearby” vs. “far” controls:
>   - Event studies by distance bins to treated areas.
>   - Interact “Post” with proximity-to-treated indicators.
> - Pre/post discontinuities at geographic or administrative borders (boundary checks).
> - Placebos on unaffected outcomes that could pick up spillovers.
> - Residual spatial correlation (e.g., [[Moran’s I]]) suggesting unmodeled spatial dependence.
> - Sensitivity to excluding likely-contaminated controls (spatial buffers, donor pool pruning in [[Synthetic Control]]).

> [!warning] Caveat
> Statistical tests rarely prove “no spillovers.” Use them to bound concerns and guide robustness designs.

## Design and modeling strategies

### 1) Avoidance by design
- Use spatial buffers (“donuts”): exclude controls within a chosen radius of treated units.
- Choose control regions in separate markets or non-adjacent geographies.
- Cluster-level assignment (RCTs or natural clusters) to reduce cross-cluster interference.
- Short analysis windows to limit diffusion.

### 2) Model exposure (exposure mapping)
- Define exposure to others’ treatment:
$$
E_i = \sum_j w_{ij} D_j
$$
where $w_{ij}$ captures proximity, network ties, or market overlap.
- Potential outcomes depend on own treatment and exposure: $Y_i(d_i, e_i)$.
- Estimate direct effect (change in $d_i$ holding $e_i$ fixed) and spillover effect (change in $e_i$ holding $d_i$ fixed).

### 3) Partial interference
- Assume interference only within clusters, not across them. Analyze at the cluster level or include cluster-by-time effects; use cluster-robust inference.
- Consider [[randomized saturation design]]s that vary treated share within clusters to identify spillovers.

### 4) Robust DiD variants
- Redefine treatment to incorporate exposure (e.g., high-exposure vs. low-exposure) and compare groups with similar exposure trends.
- Use [[Triple Differences (DDD)|DDD]]/[[triple differences]] to difference out an additional dimension less affected by spillovers.
- In border settings, consider [[boundary discontinuity]] designs.

### 5) Inference adjustments
- Cluster at exposure-relevant levels (e.g., market, region, network community).
- Spatial HAC or two-way clustering can handle correlation but do not remove spillover bias. Bias must be addressed by design/modeling.

## Reporting essentials

- Define what “treated,” “control,” and “exposed” mean in your context.
- Justify why spillovers are unlikely or how you modeled them.
- Show proximity analyses and buffer robustness.
- Document clustering and any exposure weights $w_{ij}$ used.

## Minimal code sketches

> [!example] Build a spatial buffer and drop likely-contaminated controls

```r
# R: using sf
library(sf); library(dplyr)
# polygons or points with treatment flag D and time vars
g <- st_as_sf(df, coords = c("lon","lat"), crs = 4326) |> st_transform(3857)
treated <- g |> filter(D == 1)
# 20 km buffer around treated
buf <- st_union(st_buffer(treated, dist = 20000))
df$near_treated <- as.integer(st_intersects(g, buf, sparse = FALSE))
# Exclude near controls
analysis <- df |> filter(!(D == 0 & near_treated == 1))
```

```python
# Python: geopandas
import geopandas as gpd
from shapely.ops import unary_union
df_g = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326").to_crs(3857)
treated = df_g[df_g["D"] == 1]
buf = unary_union(treated.buffer(20000))
df_g["near_treated"] = df_g.geometry.within(buf).astype(int)
analysis = df_g[~((df_g["D"]==0) & (df_g["near_treated"]==1))]
```

> [!example] Create an exposure measure and include it in DiD

```r
# R: simple k-nearest neighbors exposure using distances (sketch)
library(FNN)
coords <- as.matrix(df[,c("lon","lat")])
nn <- get.knn(coords, k = 5)$nn.index
E <- rowMeans(apply(nn, 2, function(idx) df$D[idx]))
df$E <- E
# Regression with own treatment and exposure (plus FE)
# feols(Y ~ D*Post + E*Post | id + time, data = df, cluster = ~id)
```

```python
# Python: exposure via nearest neighbors (sketch)
import numpy as np
from sklearn.neighbors import NearestNeighbors
coords = df[["lon","lat"]].to_numpy()
nbrs = NearestNeighbors(n_neighbors=5).fit(coords)
_, idx = nbrs.kneighbors(coords)
E = df["D"].to_numpy()[idx].mean(axis=1)
df["E"] = E
# Include E*Post alongside D*Post in a panel model with FE
```

## Copy-ready definitions

- No spillovers (no interference):
$$
Y_i(d_i, \mathbf{d}_{-i}) = Y_i(d_i)
$$

- Exposure mapping:
$$
E_i = \sum_j w_{ij} D_j, \quad Y_i = f(d_i, E_i, X_i) + \varepsilon_i
$$

## When is “no spillovers” plausible?

- Units are geographically or administratively isolated.
- Outcomes are local and non-rival (one unit’s treatment cannot affect others).
- Short time horizon with limited diffusion channels.
- Explicit policies preventing cross-unit effects (e.g., hard borders, non-overlapping markets).

---

Related notes to create:
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[interference]]
- [[spillovers]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[treated group]]
- [[control group]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]
- [[boundary discontinuity]]
- [[Synthetic Control]]
- [[spatial buffers]]
- [[exposure mapping]]
- [[partial interference]]
- [[randomized saturation design]]
- [[Moran’s I]]
- [[clustering]]