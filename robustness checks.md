---
title: robustness checks
aliases: [robustness check, sensitivity checks]
tags: [diagnostics, causal-inference]
updated: 2026-06-16
---

# robustness checks

> [!summary] Quick definition
> Robustness checks examine whether conclusions persist under defensible alternative specifications, samples, or assumptions.

## When it matters

Robustness checks should target the design's main threats rather than enumerate arbitrary variants. They are most useful when each check maps to a concrete concern: functional form, bandwidth choice, sample definition, clustering level, placebo timing, or a specific identification assumption.

Pre-specify key checks when possible and report failures transparently. A robustness table should not become a specification search; it should show whether the main conclusion survives defensible alternatives that a skeptical reader would ask for before seeing the result.

## Examples

- Alternative bandwidths or donut windows in RDD.
- Alternative clustering levels or few-cluster corrections in panel designs.
- Placebo outcomes, placebo dates, or pre-trend checks in DiD.
- Weight trimming, covariate sets, or overlap restrictions in observational studies.

## Related notes

- [[placebo test]]
- [[Robust Methods (MOC)]]
- [[falsification tests]]
- [[Rosenbaum sensitivity]]
