---
title: de Chaisemartin–D’Haultfœuille
aliases: [de Chaisemartin–D’Haultfœuille, de Chaisemartin-D'Haultfoeuille, DID_M, DID_M estimator]
tags: [did, causal-inference, staggered-adoption]
updated: 2026-04-02
---

# de Chaisemartin–D’Haultfœuille

> [!summary] Quick definition
> de Chaisemartin and D’Haultfœuille developed Difference-in-Differences estimators for staggered adoption settings that remain interpretable under treatment-effect heterogeneity and avoid some of the weighting pathologies of naive TWFE.

## What this note usually refers to

- The `DID_M` family of estimators.
- Two-by-two comparisons that aggregate only valid switcher vs. non-switcher contrasts.
- Decompositions that clarify where TWFE weights can become problematic.

## When it matters

- Treatment timing varies across groups.
- Effects are dynamic or heterogeneous across cohorts.
- You want a robust alternative or complement to naive TWFE summaries.

## Related notes

- [[Difference-in-Differences (DiD)]]
- [[staggered adoption]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]

