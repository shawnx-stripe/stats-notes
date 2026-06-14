---
title: Moran’s I
aliases: [Moran's I, Moran I, global Moran's I]
tags: [econometrics, spatial, diagnostics]
updated: 2026-04-02
---

# Moran’s I

> [!summary] Quick definition
> Moran’s I is a global measure of spatial autocorrelation. It tests whether nearby units have systematically similar or dissimilar values relative to what would be expected under spatial randomness.

## Interpretation

- Positive Moran’s I: nearby units tend to look similar.
- Negative Moran’s I: nearby units tend to look dissimilar.
- Near zero: little evidence of global spatial dependence.

For outcome vector $x$ and spatial weights matrix $W$,
$$
I = \frac{n}{S_0} \cdot \frac{\sum_i \sum_j w_{ij}(x_i-\bar x)(x_j-\bar x)}{\sum_i (x_i-\bar x)^2},
\quad S_0 = \sum_i \sum_j w_{ij}.
$$

## Minimal code snippets

```r
library(spdep)
lw <- nb2listw(nb_obj, style = "W")
moran.test(df$y, lw)
```

## Related notes

- [[spatial correlation]] · [[Conley standard errors]] · [[spillovers]] · [[interference]]
