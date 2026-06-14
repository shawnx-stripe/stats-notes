---
title: Oster’s delta
aliases: [Oster’s delta, Oster's delta, proportional selection, Oster delta]
tags: [causal-inference, sensitivity-analysis, omitted-variable-bias]
updated: 2026-04-02
---

# Oster’s delta

> [!summary] Quick definition
> Oster’s delta is a sensitivity-analysis statistic that asks how strong selection on unobservables would need to be, relative to selection on observables, to explain away a regression effect.

## Core idea

- Compare coefficient movement and $R^2$ movement across sparse and rich specifications.
- Extrapolate how much omitted-variable selection would be needed to drive the estimate to zero or another benchmark.
- Larger required deltas suggest more robustness to omitted variables.

## Practical use

- Most common in observational regressions under selection-on-observables arguments.
- Depends on a choice of maximum attainable $R^2$.
- It is a robustness diagnostic, not a proof of causal identification.

## Related notes

- [[selection bias]]
- [[Unconfoundedness]]
- [[Rosenbaum sensitivity]]
- [[covariates]]

