---
title: Stable Unit Treatment Value Assumption (SUTVA)
aliases: [SUTVA, stable unit treatment value assumption, no-interference and consistency, stable unit treatment value]
tags: [causal-inference, assumptions, identification, interference, design]
updated: 2025-09-17
---

# Stable Unit Treatment Value Assumption (SUTVA)

> [!summary] Quick definition
> SUTVA has two parts:
> 1) No interference: one unit’s outcome does not depend on other units’ treatments (see [[No spillovers]] / [[interference]]).
> 2) Consistency / no hidden versions of treatment: each treatment level is well-defined and unique; observed outcomes equal the corresponding potential outcomes.

SUTVA underpins standard causal estimands and many designs (RCTs, [[Difference-in-Differences (DiD)]], [[Instrumental Variables (IV)]], [[Regression Discontinuity Design (RDD)]]).

## Formal statements

### 1) Consistency (no hidden versions)
- If unit i receives treatment $D_i = d$, then the observed outcome equals the potential outcome under d:
$$
Y_i = Y_i(d) \quad \text{whenever } D_i = d
$$
- Implies “treatment” is well-defined; there aren’t multiple indistinguishable versions of d with different effects.

### 2) No interference (no spillovers)
- Unit i’s potential outcomes depend only on i’s own treatment, not on others’ assignments:
$$
Y_i(d_i,\mathbf{d}_{-i}) = Y_i(d_i,\mathbf{d}'_{-i}) \quad \forall\, \mathbf{d}_{-i}, \mathbf{d}'_{-i}
$$
- Equivalently, write $Y_i(d)$ as $Y_i(d_i)$.
- See also: [[No spillovers]], [[spillovers]], [[interference]].

## Why SUTVA matters

- Consistency ensures observed outcomes map to a single, well-defined potential outcome.
- No interference allows defining unit-level causal effects without specifying others’ treatments.
- Violations bias standard estimators (e.g., [[DiD estimator]], 2SLS, RDD) or change the estimand (exposure-dependent effects).

## Common violations

- Hidden versions/ill-defined treatment:
  - Implementation heterogeneity (different “quality” or intensity under the same label)
  - Bundled co-interventions; treatment definition varies across sites/time
  - Misclassification of treatment timing/status (measurement error)

- Interference/spillovers:
  - Spatial or network spillovers (neighbors, markets, peers)
  - Information/announcement externalities (anticipation)
  - General equilibrium effects (prices, wages) crossing unit boundaries
  - Displacement or migration responses

- Noncompliance/contamination:
  - Assigned controls receive treatment; treated units do not comply (affects interpretation; see [[noncompliance]], [[Intent-to-Treat (ITT)]])

## Diagnosing and mitigating violations

> [!check] Diagnostics (indicative, not proofs)
> - Consistency/version checks:
>   - Document treatment protocol; verify fidelity and timing (audit logs, dosage records)
>   - Placebos on components that should not change
> - Interference/spillovers:
>   - Near vs. far comparisons; exposure gradients; [[event study]] by proximity
>   - Border discontinuities; residual spatial correlation (e.g., [[Moran’s I]])
>   - Placebo outcomes and dates

> [!tip] Design solutions
> - Consistency:
>   - Standardize and document treatment; exclude or stratify heterogeneous versions
>   - Model multi-valued/intensity treatments explicitly (dose–response)
> - Interference:
>   - Cluster-level assignment; spatial buffers (“donuts”)
>   - Assume [[partial interference]] and analyze at cluster level
>   - Model exposure: $E_i = \sum_j w_{ij} D_j$ (see [[exposure mapping]])
>   - Use [[randomized saturation design]]s to identify direct and spillover effects

> [!warning] Inference vs. bias
> Adjusting standard errors (e.g., [[clustered standard errors]], [[Conley standard errors]]) handles correlation, not spillover bias. Address interference/versions by design or modeling.

## SUTVA in common designs

- RCTs/encouragement:
  - Threats: cross-group contamination; differential implementation across sites
  - Tools: ITT analysis, site fixed effects, fidelity checks; for spillovers, saturation designs

- DiD:
  - Threats: policy info diffuses to controls; compositional shifts
  - Tools: buffer zones, exposure-augmented DiD, [[Triple Differences (DDD)|DDD]]/[[triple differences]], robust [[event study]] leads for anticipation

- RDD:
  - Threats: manipulation (not a SUTVA issue per se), cross-unit spillovers around the cutoff, heterogeneous “treatment” at threshold
  - Tools: donut RD, density/balance tests, local protocol documentation

- IV/LATE:
  - Threats: instrument changes outcomes directly (violates [[exclusion restriction]]) or affects others (interference)
  - Tools: discuss channels, placebos, reduced-form checks, local designs

## Minimal exposure-mapping sketch

```r
# R: build exposure as treated-neighbor share (k-NN example)
library(FNN)
coords <- as.matrix(df[, c("lon","lat")])
nn <- get.knn(coords, k = 5)$nn.index
df$E <- rowMeans(apply(nn, 2, function(idx) df$D[idx]))
# Use D*Post and E*Post in FE regression to separate direct vs. spillover effects
```

```python
# Python: network-based exposure
import numpy as np
A = adjacency / (adjacency.sum(axis=1, keepdims=True) + 1e-12)  # row-normalized
df["E"] = A @ df["D"].to_numpy()
# Include D*Post and E*Post in a panel FE model
```

## Copy-ready definitions

- Consistency:
$$
Y_i = Y_i(d) \ \text{when } D_i=d
$$

- No interference:
$$
Y_i(d_i,\mathbf{d}_{-i}) = Y_i(d_i,\mathbf{d}'_{-i})
$$

- Exposure mapping (interference-aware):
$$
E_i = \sum_j w_{ij} D_j,\quad Y_i = f(d_i, E_i, X_i) + \varepsilon_i
$$

## Reporting essentials

- Define treatment precisely (timing, intensity, components) and document implementation fidelity.
- Justify no-interference or describe exposure modeling/buffers.
- Show proximity/exposure diagnostics and robustness (alternative $w_{ij}$, buffer sizes).
- Clarify estimand if interference or versions are modeled (direct vs. indirect effects; dose–response).

## Common pitfalls

> [!warning] Avoid these
> - Treating heterogeneous versions as the same treatment without modeling them.
> - Ignoring obvious spillovers (e.g., adjacent markets) when defining controls.
> - Using SE fixes as substitutes for design fixes.
> - Post-treatment conditioning to “correct” versions/exposure (creates [[bad controls]]).

---

Related notes to create:
- [[No spillovers]]
- [[interference]]
- [[spillovers]]
- [[exposure mapping]]
- [[partial interference]]
- [[randomized saturation design]]
- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[Anticipatory effects]]
- [[composition]]
- [[clustered standard errors]]
- [[Conley standard errors]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Regression Discontinuity Design (RDD)]]
- [[Triple Differences (DDD)|DDD]]
- [[triple differences]]
- [[bad controls]]