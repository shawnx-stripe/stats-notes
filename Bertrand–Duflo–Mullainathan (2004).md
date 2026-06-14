---
title: Bertrand–Duflo–Mullainathan (2004)
aliases: [Bertrand-Duflo-Mullainathan (2004), Bertrand Duflo Mullainathan, BDM 2004]
tags: [econometrics, inference, did, clustering, reference]
updated: 2026-03-05
---

# Bertrand–Duflo–Mullainathan (2004)

> [!summary]
> Seminal paper demonstrating that serial correlation in panel DiD settings leads to severely over-rejected standard errors. Proposed solutions include clustering at the group level, block bootstrap, and aggregation to pre/post periods.

## Key findings

Using state-level policy data, BDM showed that ignoring serial correlation inflates rejection rates from 5% to over 40%. Even robust SEs fail without clustering. The paper's Monte Carlo simulations demonstrated three reliable fixes: (1) cluster at the treatment unit level; (2) collapse to pre/post means (eliminating time-series variation); (3) parametric corrections assuming AR(1) errors. The paper catalyzed widespread adoption of clustered SEs in applied DiD research.

> [!warning]
> Clustering alone may not suffice with few treated units ($G < 20$). Consider [[wild cluster bootstrap]] or aggregation to two periods when treatment timing varies little across units.

## Related notes

- [[clustered standard errors]]
- [[Difference-in-Differences (DiD)]]
- [[few-cluster corrections]]
- [[wild cluster bootstrap]]
- [[clustering]]
