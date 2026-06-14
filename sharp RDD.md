---
title: Sharp RDD
aliases: [sharp RDD, Sharp RDD, sharp regression discontinuity]
tags: [causal-inference]
updated: 2026-03-05
---

# Sharp RDD

> [!summary]
> A [[Regression Discontinuity Design (RDD)]] where treatment is deterministically assigned by crossing a cutoff of the running variable. Estimates the local average treatment effect at the cutoff under continuity assumptions.

## Design

Treatment assignment:

$$
D_i = \mathbb{1}\{R_i \geq c\}
$$

where $R_i$ is the running variable and $c$ is the cutoff. Treatment probability jumps from 0 to 1 at $c$.

## Identification

Under continuity of $\mathbb{E}[Y(d) \mid R = r]$ at $r = c$:

$$
\tau_{\text{RD}} = \lim_{r \downarrow c} \mathbb{E}[Y \mid R = r] - \lim_{r \uparrow c} \mathbb{E}[Y \mid R = r]
$$

This is the local ATE at the cutoff. Interpretation: effect for units with $R_i \approx c$.

> [!check] Contrast with fuzzy RDD
> In [[fuzzy RDD]], treatment probability changes discontinuously at $c$ but not from 0 to 1. Sharp RDD is a special case where compliance is perfect. Fuzzy RDD requires IV-like assumptions and estimates LATE for compliers at the cutoff.

## Minimal code

```r
library(rdrobust)
out <- rdrobust(y = outcome, x = running_var, c = 0)
summary(out)
```

## Related notes

- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy RDD]]
