---
title: Split-Plot Design
aliases: [split-plot, split-plot design, split-plot experiment]
tags: [experimentation, design, factorial]
updated: 2026-03-05
---

# Split-Plot Design

> [!summary]
> Experimental design where one factor is applied at the whole-plot (group) level and another at the subplot (unit) level. Common when some factors are harder to randomize; requires appropriate error terms for each stratum.

## Structure

Model:

$$
Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \gamma_k + \varepsilon_{ijk}
$$

- $\alpha_i$: whole-plot treatment (e.g., irrigation level)
- $\beta_j$: subplot treatment (e.g., fertilizer type)
- $\gamma_k$: whole-plot error (random effect for plot)
- $\varepsilon_{ijk}$: subplot error

## Key insight

Two error terms lead to different standard errors:
- Whole-plot effects tested against whole-plot error (less precise)
- Subplot effects and interactions tested against subplot error (more precise)

Ignoring the hierarchical structure inflates Type I error for whole-plot factors.

> [!example] Web experiments
> - Whole-plot: Server-side configuration (applied to all users on a server)
> - Subplot: UI variant (randomized per user within server)
> - Must account for clustering within servers

## Minimal code

```r
library(lme4)
model <- lmer(yield ~ irrigation * fertilizer + (1|plot), data = agr)
summary(model)
```

## Related notes

- [[factorial design]]
- [[stratification]]
- [[Experimental Design (MOC)]]
