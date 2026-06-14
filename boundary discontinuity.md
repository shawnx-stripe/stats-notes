---
title: boundary discontinuity
aliases:
  - geographic RDD
  - border discontinuity
tags:
  - causal-inference
  - rdd
  - spatial
updated: 2026-03-03
---

# boundary discontinuity

> [!summary] Quick definition
> A spatial variant of [[Regression Discontinuity Design (RDD)]] that exploits geographic or administrative boundaries. Units on opposite sides of a border face different policies but share similar observable and unobservable characteristics (if the border is arbitrary relative to outcomes). Causal effects are identified by comparing outcomes of units near the boundary.

---

## Design logic

- An administrative boundary (state line, school district border, zoning edge) creates a discontinuity in policy exposure.
- Units very close to the border are similar on unobservables (geographic, economic, demographic), differing mainly in which side of the boundary they fall on.
- The running variable is typically **distance to the boundary** (signed: positive on one side, negative on the other).

$$
\tau_{\text{BRD}} = \lim_{d \to 0^+} \mathbb{E}[Y_i \mid d_i = d] - \lim_{d \to 0^-} \mathbb{E}[Y_i \mid d_i = d]
$$

where $d_i$ is signed distance from unit $i$ to the boundary.

---

## Key assumptions

- **Continuity** of potential outcomes at the boundary (no sorting or precise manipulation)
- **Local similarity**: units near the border are comparable in unobservables
- No [[spillovers]] across the boundary (or model them explicitly)

> [!warning] Threats
> - Self-selection near borders (e.g., families moving to better school districts)
> - Boundary-specific effects (borders may coincide with geographic features like rivers)
> - Spatial correlation in outcomes — use [[Conley standard errors]] or cluster by border segment

---

## Practical considerations

- Define distance to boundary carefully (Euclidean, road distance, nearest-boundary-point)
- Include boundary-segment fixed effects if multiple borders exist (to compare only within the same border)
- Bandwidth selection follows standard RDD practice (e.g., CCT optimal bandwidth)
- Check for density discontinuities (McCrary-style test on distance) to detect sorting
- Balance checks on pre-treatment covariates at the boundary

---

## Minimal code snippets

> [!example] R

```r
library(rdrobust)

# d: signed distance to boundary; Y: outcome
# Boundary-segment FE via residualization or subsetting
rd <- rdrobust(y = df$Y, x = df$distance, covs = df[, c("segment_fe")])
summary(rd)
rdplot(y = df$Y, x = df$distance)
```

---

## Related notes

- [[Regression Discontinuity Design (RDD)]] · [[fuzzy RDD]]
- [[Conley standard errors]] · [[spillovers]]
- [[Causal Inference (MOC)]]
