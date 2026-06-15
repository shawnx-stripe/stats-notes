---
title: Spillovers and Interference (MOC)
aliases:
  - Interference methods
  - Spillover effects
  - SUTVA violations
tags:
  - MOC
  - spillovers
  - interference
  - network-effects
  - causal-inference
  - experimental-design
updated: 2025-09-26
---

# Spillovers and Interference (MOC)

> [!summary] Overview
> Methods to design, identify, estimate, and validate causal effects when one unit’s treatment can affect other units’ outcomes, violating [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]. This MOC organizes concepts, designs, estimation strategies, and diagnostics for handling [[interference]] and [[spillovers]] in experiments and observational studies.

## Core concepts

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] components:
  - No hidden versions of treatment
  - [[No spillovers]] / no interference across units
- With interference:
  - Outcomes depend on own treatment and others’ treatment:
    - Potential outcomes: Y_i = Y_i(D_i, D_{-i})
  - Exposure mapping: summarize neighbors’ treatments:
    - Y_i = Y_i(D_i, g_i(D_{-i})) where g_i is an exposure function (e.g., share treated among neighbors)
- Key effects:
  - Direct effect: own treatment, holding exposure fixed
  - Indirect (spillover) effect: change in exposure, holding own treatment fixed
  - Total and overall effects combine both

Related notes: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[No spillovers]], [[interference]]

## Taxonomy of spillovers

- By mechanism:
  - Informational (learning, persuasion), resource/market (congestion, GE), physical (disease, pollution), social/peer
- By structure:
  - Clustered (groups/households), networked (graphs), spatial/geographic (distance-based), hierarchical (multi-level)
- By sign/strategic interaction:
  - Positive externalities, negative externalities, strategic complements/substitutes

Related notes: [[geo experiment]], [[randomized saturation design]], [[switchback experiment]]

## Identification strategies under interference

- Partial interference (interference within, not across, clusters)
  - Validates cluster-level exposure contrasts
- Exposure mapping approach
  - Specify g_i; identify contrasts like τ(1, g) − τ(0, g) and τ(d, g′) − τ(d, g)
- Encouragement and two-stage randomization
  - Randomize clusters’ saturation then individual treatments within clusters
- Spatial identification
  - Distance-based exposure; buffer (“donut”) zones to isolate spillovers
- IV approaches for peer exposure
  - Use randomized saturation or distant neighbors as instruments for own exposure (requires strong [[exclusion restriction]])
- Designs to detect/quantify spillovers:
  - Ring/buffer designs, stepped-wedge, alternating [[switchback experiment]]

Related notes: [[Instrumental Variables (IV)|Instrumental Variables (IV)]], [[exclusion restriction]], [[Regression Discontinuity Design (RDD)|Regression Discontinuity Design (RDD)]]

## Experimental design patterns

- [[randomized saturation design]] (partial population)
  - Randomize cluster-level treatment density; enables exposure-response estimation
- Two-stage randomization
  - Stage 1: clusters to saturation; Stage 2: individuals to treatment
- [[switchback experiment]]
  - Rotate treatment across time/space to separate direct from temporal/spatial spillovers
- [[geo experiment]]
  - Geographic clustering, minimum separation, and buffer zones for interference control
- Cluster re-randomization
  - Balance exposure distributions and connectivity features (degree, cross-cluster ties)

Related notes: [[randomized controlled trial (RCT)]], [[clustering]]

## Estimation strategies

- Exposure-response modeling
  - Regress outcomes on own treatment, exposure g_i, and interactions; interpret contrasts at specified g
- Group-saturated models
  - Estimate effects by exposure bins (e.g., quantiles of neighbor treated share)
- Cluster-level estimands
  - Cluster-average effects and spillovers via within-cluster variation
- Network models
  - Linear-in-means and spatial autoregressive forms (requires careful identification to avoid [[reflection problem]])
- Design-based estimators
  - Horvitz–Thompson/Hájek weighting under known assignment with exposure mappings
- Heterogeneous spillovers
  - Allow effects to vary by baseline traits or network position (degree/centrality)

Related notes: [[kernel regression]], [[local linear regression]], [[randomization inference]], [[Conley standard errors]]

## Inference and standard errors

- Cluster-robust SEs at the interference unit (e.g., cluster, geography)
  - See [[clustered standard errors]], [[wild cluster bootstrap]] for few clusters
- Spatial correlation
  - [[Conley standard errors]] when exposure decays with distance
- Design-based inference
  - [[randomization inference]] for sharp or weak nulls under known assignment
- Few clusters or coarse networks
  - [[few-cluster corrections]]; report number of clusters and effective units

Related notes: [[Standard Errors and Inference (MOC)]], [[Cameron–Gelbach–Miller]]

## Diagnostics and validation

- Pre-analysis checks
  - Define exposure mapping(s) g_i ex ante; justify mechanism and radius
  - Assess network/cluster stability and measurement quality
  - Ensure sufficient variation/support in exposure across treated/control
- Empirical diagnostics
  - Balance on pre-treatment covariates across exposure levels
  - Placebo/halo tests (effects where none expected, e.g., far-away units)
  - Donut buffers around boundaries; sensitivity to buffer width
  - Spatial autocorrelation (e.g., Moran’s I) of residuals
- Robustness
  - Alternative exposure mappings and radii
  - Alternative clustering schemes/geographies
  - Bandwidth and bin sensitivity for exposure bins

Related notes: [[placebo test]], [[bandwidth selection]], [[density test]]

## Reporting checklist

> [!check] Minimum reporting
> - [ ] Conceptual mechanism and chosen exposure mapping(s) g_i
> - [ ] Randomization or identification strategy (partial interference, 2-stage, geo)
> - [ ] Support/variation of exposure across units
> - [ ] Primary estimands (direct/indirect/total) and contrasts
> - [ ] Inference approach (cluster level, spatial SEs, design-based)
> - [ ] Sensitivity to exposure definitions and buffer sizes
> - [ ] Number of clusters/networks and effective sample size
> - [ ] Any deviations from [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and implications

## Common pitfalls

> [!warning] Avoid these
> - Assuming no interference when design suggests otherwise
> - Post hoc exposure mappings chosen to fit results
> - Using wrong clustering level for SEs
> - Ignoring cross-cluster ties under “partial interference”
> - Confounding exposure with context (e.g., dense areas differ systematically)
> - Reflection problem: attributing peers’ outcomes to peer effects without valid instruments/design

Related notes: [[bad controls]], [[reflection problem]], [[randomization inference|design-based inference]]

## When to use

- Social/network interventions (education, health behaviors, platforms)
- Policies with geographic diffusion or market equilibrium effects
- Epidemiology and diffusion (herd immunity, contagion)
- Any setting with plausible externalities across units

## Minimal formulas (copy-ready)

- Exposure mapping potential outcomes:
$$
Y_i(d, g) \quad \text{with} \quad g = g_i(D_{-i})
$$

- Direct effect at exposure g:
$$
\Delta_{\text{direct}}(g) = \mathbb{E}[Y_i(1,g)] - \mathbb{E}[Y_i(0,g)]
$$

- Spillover (on untreated) from g to g′:
$$
\Delta_{\text{spill}}^{(0)}(g \to g') = \mathbb{E}[Y_i(0,g')] - \mathbb{E}[Y_i(0,g)]
$$

- Spillover (on treated) from g to g′:
$$
\Delta_{\text{spill}}^{(1)}(g \to g') = \mathbb{E}[Y_i(1,g')] - \mathbb{E}[Y_i(1,g)]
$$

- Overall effect combining both (at specified exposure paths) is the sum of direct and spillover contrasts.

## Cross-links

- Foundational: [[Causal Inference (MOC)]], [[Experimental Design (MOC)]], [[Econometrics (MOC)]]
- Designs: [[randomized saturation design]], [[switchback experiment]], [[geo experiment]]
- Inference: [[clustered standard errors]], [[wild cluster bootstrap]], [[Conley standard errors]], [[randomization inference]]
- Related methods: [[Difference-in-Differences (DiD)]], [[fuzzy RDD]], [[Instrumental Variables (IV)|Instrumental Variables (IV)]]

---

## Related notes
- [[exposure mapping]]
- [[partial interference]]
- [[network interference]]
- [[spillover estimands]]
- [[halo test]]
- [[buffer zone design]]
- [[spatial autocorrelation]]
- [[reflection problem]]
- [[randomized saturation design|two-stage randomization]]
- [[stepped-wedge design]]
