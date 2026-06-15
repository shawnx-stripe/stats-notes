---
title: Interference
aliases:
- no-independence
- SUTVA violation
- network effects
- peer effects
- network interference
- Interference
tags:
- causal-inference
- assumptions
- networks
- spatial
- design
- did
updated: 2025-09-17
---

# Interference

> [!summary] Quick definition
> Interference occurs when one unit’s treatment affects another unit’s outcome. This violates the “no-interference” part of [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and complicates identification in designs like [[Difference-in-Differences (DiD)]]. See also: [[No spillovers]].

- Consequence: standard estimators that assume independent, unit-level treatment effects (e.g., classic [[DiD estimator]]) can be biased if controls are affected by treated units.

## Formal setup

- Let $D = (D_1,\dots,D_N)$ be treatment assignments. Under interference, unit i’s potential outcomes depend on others’ treatments:
$$
Y_i = Y_i(D_i, \mathbf{D}_{-i})
$$
- Without interference (i.e., [[No spillovers]]), we would have $Y_i(D) = Y_i(D_i)$.

### Exposure mapping
- A common way to model interference is to compress others’ assignments into an exposure measure:
$$
E_i = \sum_j w_{ij} D_j
$$
- Potential outcomes become $Y_i(d_i, e_i)$, where $e_i$ is i’s exposure (e.g., neighbors treated, market overlap, distance-weighted share). See [[exposure mapping]].

## Types and sources

- Geographic/spatial spillovers (neighboring regions, border effects)
- Network interference (friends, co-workers, firms in a supply chain)
- Market-equilibrium effects (price, wages, demand displacement)
- Information diffusion and media reach
- Policy-induced displacement or migration

## Estimands under interference

> [!note] Hudgens–Halloran style effects (clustered or exposure-based)
- Direct effect at exposure level $e$:
$$
DE(e) = \mathbb{E}[Y_i(1,e) - Y_i(0,e)]
$$
- Spillover/indirect effect comparing exposures $e_1$ vs. $e_0$ for untreated:
$$
IE(e_1,e_0) = \mathbb{E}[Y_i(0,e_1) - Y_i(0,e_0)]
$$
- Total effect between (1, $e_1$) and (0, $e_0$):
$$
TE(e_1,e_0) = \mathbb{E}[Y_i(1,e_1) - Y_i(0,e_0)]
$$
- Overall (policy) effect: average change when moving the entire population from one assignment regime to another (e.g., saturation $p_0 \to p_1$).

## Design strategies

### 1) Avoid or reduce interference
- Cluster-level assignment (schools, villages, firms) with buffers between clusters.
- Spatial “donut” exclusions around treated units for controls.
- Short analysis windows to limit diffusion.

### 2) Partial interference
- Assume interference only within clusters, not across clusters. Analyze at cluster level; use cluster-by-time effects and cluster-robust inference. See [[partial interference]].

### 3) Randomized saturation / two-stage designs
- Randomize clusters to different treatment probabilities; within clusters, randomize units. Enables identification of direct and indirect effects by varying exposure. See [[randomized saturation design]] and two-stage randomization.

### 4) Graph-aware assignment
- Graph cluster randomization or re-randomization to minimize edge cuts between treated and control. Useful for social-network settings.

## Estimation and modeling

- Exposure mapping + regression/DiD:
  - Include $D_i \times Post_t$ and $E_i \times Post_t$ in a panel with fixed effects to separate direct and exposure effects.
- Inverse probability weighting for exposure categories:
  - Use Horvitz–Thompson/Hájek estimators for effects defined by $(d_i,e_i)$; weights depend on assignment mechanism.
- Randomization inference:
  - Use permutation tests consistent with the actual assignment and interference structure (e.g., exposure-restricted permutations).
- Spatial/network models:
  - SAR/SEM models or network autoregressive outcomes; be cautious about causal interpretation and identification.
- Bounding/sensitivity:
  - Conduct sensitivity analyses to plausible ranges of exposure effects.

> [!warning] Clustering SEs alone does not fix bias
> Clustering addresses correlation in errors, not bias from contaminated controls. Address interference in design or model the exposure.

## Diagnostics and falsification

> [!check] Useful checks (not proofs)
> - Distance gradients: outcomes for controls vary with proximity to treatment?
> - Border checks: discontinuities at administrative boundaries?
> - Event studies by exposure bins (near/far; high/low network centrality).
> - Placebos on outcomes/channels that should not be affected.
> - Sensitivity to excluding likely-exposed controls (spatial buffers, donor-pool pruning).
> - Residual spatial/network correlation (e.g., [[Moran’s I]]).

## Interference and DiD

- Threat: controls are indirectly treated, breaking [[parallel trends assumption]].
- Remedies:
  - Redefine treatment to include exposure (high vs. low exposure groups).
  - Use [[Triple Differences (DDD)|DDD]]/[[triple differences]] to difference out an additional dimension less affected by spillovers.
  - Consider [[Synthetic Control]] or boundary-discontinuity designs for treated aggregates.

## Reporting essentials

- Define treatment, exposure, and interference channels.
- Justify interference assumptions (none, partial, modeled).
- Describe cluster structure, buffers, and network/weight matrices $w_{ij}$.
- Show robustness: alternative exposure definitions, buffer sizes, and placebo checks.
- Document assignment mechanism for valid inference (especially with randomization).

## Minimal code sketches

> [!example] Build a network exposure (Python)

```python
import numpy as np
# A: adjacency (0/1), row-normalized
A = adjacency_matrix / adjacency_matrix.sum(axis=1, keepdims=True)
D = df["D"].to_numpy()
df["E"] = (A @ D)  # neighbor-treated share
# Panel DiD with own and exposure effects (pseudocode)
# Y_it ~ EntityEffects + TimeEffects + D_it*Post_t + E_i*Post_t + ...
```

> [!example] Distance-based exposure (R)

```r
# distances: matrix of great-circle distances in km
W <- 1 / (1 + distances)     # simple decay; set diag to 0
diag(W) <- 0
W <- W / rowSums(W)          # row-normalize
df$E <- as.numeric(W %*% df$D)
# Use E*Post alongside D*Post in FE regression
# feols(Y ~ D:Post + E:Post | id + time, cluster=~id, data=df)
```

## Copy-ready formulas

- General interference:
$$
Y_i = Y_i(D_i, \mathbf{D}_{-i})
$$

- Exposure mapping:
$$
E_i = \sum_j w_{ij} D_j, \quad Y_i = f(D_i, E_i, X_i) + \varepsilon_i
$$

- Direct/spillover effects:
$$
DE(e) = \mathbb{E}[Y_i(1,e) - Y_i(0,e)], \quad
IE(e_1,e_0) = \mathbb{E}[Y_i(0,e_1) - Y_i(0,e_0)]
$$

---

## Related notes
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[spillovers]]
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[parallel trends assumption]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]
- [[Synthetic Control]]
- [[partial interference]]
- [[randomized saturation design]]
- [[exposure mapping]]
- [[boundary discontinuity]]
- [[Moran’s I]]
- [[clustering]]
