---
title: Within–Between Model
aliases: [within-between model, within–between model, hybrid model, Mundlak-Chamberlain device]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Within–Between Model

> [!summary]
> Panel model that separately estimates within-unit and between-unit effects by including both demeaned (within) and group-mean (between) regressors. Nests FE and RE; tests whether within and between coefficients differ.

## Model specification

$$
Y_{it} = \beta_W (X_{it} - \bar{X}_i) + \beta_B \bar{X}_i + \alpha_i + \varepsilon_{it}
$$

- $\beta_W$: within-unit effect (variation over time)
- $\beta_B$: between-unit effect (cross-sectional variation)
- If $\beta_W = \beta_B$, RE is efficient; if they differ, FE is consistent

## Minimal code

```r
library(plm)

# Within-between model
model_wb <- plm(Y ~ X + lag(X, 0:1), data = panel_data,
                model = "within", effect = "individual")

# Mundlak device: add group means to within model
panel_data$X_mean <- ave(panel_data$X, panel_data$id)
model_mundlak <- plm(Y ~ X + X_mean, data = panel_data, model = "random")
```

## Interpretation

- $\beta_W \neq \beta_B$ suggests time-invariant confounding
- Hausman test is equivalent to testing $\beta_W = \beta_B$
- Between effect may be biased by selection; within effect is robust under fixed effects

> [!check] When to use
> Use the within-between model to understand *why* FE and RE differ. If substantive interest is in both time-varying and time-invariant effects, this decomposition clarifies the source of identification.

## Related notes

- [[random effects]]
- [[two-way fixed effects]]
- [[Mundlak adjustment]]
- [[Panel Data Methods (MOC)]]
