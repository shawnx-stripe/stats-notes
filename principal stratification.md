---
title: Principal Stratification
aliases: [principal stratification, principal strata]
tags: [causal-inference, noncompliance, missing-data]
updated: 2026-03-05
---

# Principal Stratification

> [!summary]
> Framework (Frangakis & Rubin 2002) that classifies units by joint potential treatment statuses under different assignments. Subgroups (strata) include [[compliers]], [[never-takers]], [[always-takers]], and [[defiers]]. Generalizes to truncation-by-death and mediation.

## Four principal strata

For instrument $Z$ and treatment $D$:

| Stratum | $D(0)$ | $D(1)$ | Description |
|---------|--------|--------|-------------|
| [[Compliers]] | 0 | 1 | Take treatment iff assigned |
| [[Never-takers]] | 0 | 0 | Never take treatment |
| [[Always-takers]] | 1 | 1 | Always take treatment |
| [[Defiers]] | 1 | 0 | Do opposite of assignment |

## Identification

Under [[monotonicity]] (no defiers) and random assignment of $Z$:

$$
\text{LATE} = \mathbb{E}[Y(1) - Y(0) \mid \text{complier}]
$$

Principal strata themselves are not directly observed but can be probabilistically assigned or bounded.

> [!note] Extensions
> - **Truncation-by-death**: Strata defined by survival under control/treatment
> - **Mediation**: Strata defined by mediator values $M(0), M(1)$
> - **Always useful when post-treatment variables create selection**

## Related notes

- [[compliers]]
- [[never-takers]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[noncompliance]]
- [[Attrition]]
