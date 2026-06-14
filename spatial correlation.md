---
title: Spatial correlation
aliases: [spatial correlation, Spatial correlation, spatial dependence]
tags: [econometrics]
updated: 2026-03-05
---

# Spatial correlation

> [!summary]
> Correlation of errors or outcomes across spatial units (e.g., neighboring counties). Invalidates standard inference; requires spatial HAC ([[Conley standard errors]]) or spatial econometric models (SAR, SEM).

## Spatial autocorrelation

Errors satisfy:

$$
\mathbb{E}[\varepsilon_i \varepsilon_j] = \sigma^2 w_{ij}
$$

where $w_{ij}$ decays with distance (e.g., $w_{ij} = \exp(-d_{ij}/\delta)$ or inverse distance). Violations of i.i.d. assumption are common in geospatial data.

## Solutions

| Method | Description | Use case |
|--------|-------------|----------|
| [[Conley standard errors]] | HAC with distance-based kernel | Unknown spatial structure |
| Spatial clustering | Cluster by region | Discrete spatial groups |
| SAR model | Spatial autoregressive lag: $Y = \rho W Y + X\beta + \varepsilon$ | Spillovers in outcome |
| SEM model | Spatial error model: $\varepsilon = \lambda W \varepsilon + u$ | Correlated shocks |

> [!warning] Common mistake
> Standard clustered standard errors assume independence *between* clusters but do not account for within-cluster spatial correlation patterns. If units within a cluster are spatially distributed, use Conley or multi-way clustering.

## Minimal code

```r
library(plm)
# Conley SEs with distance cutoff of 500km
conley_se <- vcovSCC(model, maxdist = 500, type = "HC0")
```

## Related notes

- [[Conley standard errors]]
- [[clustered standard errors]]
- [[Moulton problem]]
