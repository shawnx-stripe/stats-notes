---
title: Coarsened Exact Matching (CEM)
aliases: [CEM, coarsened exact matching, coarsened exact matching (CEM)]
tags: [causal-inference, matching, design]
updated: 2026-04-02
---

# Coarsened Exact Matching (CEM)

> [!summary] Quick definition
> Coarsened Exact Matching (CEM) bins covariates into substantively meaningful categories, then matches treated and control units exactly within those coarsened strata.

## Why use it

- Improves covariate balance by construction within matched strata.
- Makes overlap problems visible because unmatched strata are dropped.
- Usually easier to explain than high-dimensional distance-based matching.

## Core workflow

1. Choose bins for continuous and categorical covariates.
2. Form strata on the coarsened covariates.
3. Keep strata containing both treated and control units.
4. Reweight retained observations and estimate the target effect.

## Minimal code snippets

```r
library(cem)
c <- cem(treatment = "D", data = df, cutpoints = list(age = c(30, 40, 50)))
df$w <- c$w
```

## Related notes

- [[matching]]
- [[covariate balance]]
- [[Overlap]]
- [[Treatment-on-the-Treated (TOT)]]

