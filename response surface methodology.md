---
title: Response Surface Methodology
aliases: [response surface methodology, RSM, response surface]
tags: [experimentation, design, optimization]
updated: 2026-03-05
---

# Response Surface Methodology

> [!summary]
> Sequential experimentation strategy using fitted polynomial surfaces to find optimal factor settings. Combines factorial/fractional designs with steepest-ascent search and central composite designs for curvature estimation.

## Typical sequence

1. **Screening**: Fractional factorial to identify active factors
2. **First-order model**: $Y = \beta_0 + \sum_j \beta_j X_j + \varepsilon$ using $2^k$ or fractional designs
3. **Steepest ascent/descent**: Move along gradient until curvature detected
4. **Second-order model**: $Y = \beta_0 + \sum_j \beta_j X_j + \sum_j \beta_{jj} X_j^2 + \sum_{j<k} \beta_{jk} X_j X_k + \varepsilon$ using central composite or Box-Behnken designs
5. **Optimization**: Find maximum via canonical analysis

## Minimal example (R)

```r
library(rsm)

# Central composite design
ccd_design <- ccd(~ x1 + x2, n0 = 4)
response <- run_experiment(ccd_design)

# Fit second-order model
model <- rsm(response ~ SO(x1, x2), data = ccd_design)
summary(model)
ridge <- steepest(model, dist = 0.5)
```

> [!tip] When to use
> RSM is ideal for continuous process optimization (e.g., chemical yields, manufacturing parameters) where you can sequentially adjust settings. Less common in A/B testing but useful in bandit-like settings with continuous actions.

## Related notes

- [[factorial design]]
- [[Experimental Design (MOC)]]
