---
title: Exposure Mapping
aliases: [exposure mapping, exposure model, effective treatment]
tags: [causal-inference, interference, design]
updated: 2026-03-05
---

# Exposure Mapping

> [!summary]
> Function that maps a unit's own treatment assignment and neighbors' assignments into a scalar or low-dimensional exposure measure. Key building block for causal inference under [[interference]] when [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] fails.

## Definition and examples

Let $D_i$ be unit $i$'s treatment and $\mathcal{N}_i$ be its neighborhood. An exposure mapping is:
$$
E_i = f(D_i, \{D_j : j \in \mathcal{N}_i\})
$$

| Exposure | Formula | Interpretation |
|----------|---------|----------------|
| Own treatment only | $E_i = D_i$ | SUTVA (no spillovers) |
| Treated neighbors count | $E_i = \sum_{j \in \mathcal{N}_i} D_j$ | Network spillovers |
| Treated fraction | $E_i = \frac{1}{\|\mathcal{N}_i\|} \sum_{j \in \mathcal{N}_i} D_j$ | Peer effects |
| Combined | $E_i = (D_i, \bar{D}_{\mathcal{N}_i})$ | Direct + indirect effects |

> [!tip]
> A good exposure mapping should:
> 1. Be low-dimensional (for identification and power)
> 2. Capture the key mechanism of spillover
> 3. Be testable against alternative specifications

## When to use

Use exposure mappings when designing or analyzing experiments with interference (e.g., [[geo experiment]], social network experiments, marketplace experiments). The exposure model defines the causal estimand and informs randomization design.

## Related notes

- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[spillovers]]
- [[partial interference]]
- [[Spillovers and Interference (MOC)]]
