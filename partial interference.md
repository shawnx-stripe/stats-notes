---
title: Partial Interference
aliases: [partial interference, stratified interference]
tags: [causal-inference, interference, design, assumptions]
updated: 2026-03-05
---

# Partial Interference

> [!summary]
> Assumption that units can be grouped into clusters such that interference occurs within but not between clusters. Weaker than [[No spillovers]] (full SUTVA) but still tractable for identification.

## Formal statement

Units partition into clusters $G_1, \ldots, G_K$. Potential outcomes satisfy:

$$
Y_i(\mathbf{D}) = Y_i(\mathbf{D}_{G_k}) \quad \text{for all } i \in G_k
$$

That is, $i$'s outcome depends only on treatment assignments within its cluster, not other clusters.

## Key insight

Partial interference permits cluster-level randomization designs and identification of direct and spillover effects within clusters. Common examples: classrooms, villages, social network components. The assumption is testable if clusters are randomized to different treatment saturation levels.

> [!check] Design implications
> Randomize clusters to varying treatment fractions (e.g., 0%, 50%, 100% treated) to separately identify direct effects and within-cluster spillovers. The number of treatment fractions should exceed the number of spillover parameters.

## Related notes

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[spillovers]]
- [[exposure mapping]]
- [[Spillovers and Interference (MOC)]]
