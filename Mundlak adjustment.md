---
title: Mundlak Adjustment
aliases: [Mundlak adjustment, Mundlak device, correlated random effects]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Mundlak Adjustment

> [!summary]
> Augments a random-effects model with group means of time-varying regressors ($\bar{X}_i$), relaxing the RE assumption. Makes RE numerically equivalent to FE for the slopes while retaining RE efficiency for between-variation.

## Model

$$
y_{it} = \alpha + \beta x_{it} + \gamma \bar{x}_i + u_i + \epsilon_{it}
$$

where $\bar{x}_i = T^{-1}\sum_t x_{it}$ is the within-unit mean. The coefficient $\beta$ is identified from within-variation (like FE), but the model can also include time-invariant regressors and estimate their coefficients via $\gamma$.

## When to use

- You want to allow correlation between unit effects $u_i$ and regressors $x_{it}$ (relaxing RE assumption)
- You also want to include time-invariant covariates (which FE drops)
- You want to test whether between and within effects differ: $H_0: \gamma = 0$

> [!tip]
> If $\gamma \approx 0$, standard RE is valid. If $\gamma \neq 0$, the Mundlak adjustment controls for endogeneity via within-transformation while retaining time-invariant covariates.

## R snippet

```r
library(plm)
# Create within-unit means
data$x_mean <- ave(data$x, data$unit_id, FUN = mean)
# Mundlak RE: include both x and x_mean
plm(y ~ x + x_mean + z_time_invariant, data = data,
    model = "random", index = c("unit_id", "time"))
```

## Related notes

- [[random effects]]
- [[two-way fixed effects]]
- [[Hausman test]]
- [[Panel Data Methods (MOC)]]
