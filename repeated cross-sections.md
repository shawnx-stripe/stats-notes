---
title: Repeated Cross-Sections
aliases: [repeated cross-sections, repeated cross-section data, pseudo-panel]
tags: [econometrics, panel-data, did]
updated: 2026-03-05
---

# Repeated Cross-Sections

> [!summary]
> Data structure where different units are sampled in each period (unlike panels where the same units are tracked). DiD can still be applied using group-level averages. Avoids attrition but cannot track individual dynamics.

## DiD with repeated cross-sections

Estimate:

$$
Y_{igt} = \alpha + \beta \text{Treat}_g + \gamma \text{Post}_t + \delta (\text{Treat}_g \times \text{Post}_t) + \varepsilon_{igt}
$$

$\delta$ identifies the ATT under parallel trends in group means, even though individuals differ across periods.

## Advantages and limitations

| Aspect | Repeated cross-sections | Panel data |
|--------|------------------------|------------|
| Attrition | Not a problem | Can bias estimates |
| Fixed effects | Only group-level | Individual-level possible |
| Dynamics | Cannot track | Can model transitions |
| Cost | Often cheaper | Expensive to track |

> [!check] When to use
> Repeated cross-sections are ideal when individual tracking is infeasible (e.g., large population surveys like CPS, DHS) and the causal question concerns group-level changes rather than individual trajectories.

## Related notes

- [[balanced panel]]
- [[Difference-in-Differences (DiD)]]
- [[composition]]
- [[Panel Data Methods (MOC)]]
