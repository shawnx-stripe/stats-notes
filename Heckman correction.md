---
title: Heckman Correction
aliases: [Heckman correction, Heckman selection model, Heckman selection, Heckman two-step, Heckit]
tags: [econometrics, missing-data, selection]
updated: 2026-03-05
---

# Heckman Correction

> [!summary]
> Two-step method correcting for sample selection bias: (1) estimate a probit selection equation; (2) include the inverse Mills ratio in the outcome equation. Requires an exclusion restriction for identification.

## Two-Step Procedure

**Step 1**: Estimate selection equation via probit:
$$
P(S_i = 1 | Z_i) = \Phi(Z_i \gamma)
$$
Compute inverse Mills ratio: $\hat{\lambda}_i = \phi(\hat{Z}_i \gamma) / \Phi(\hat{Z}_i \gamma)$.

**Step 2**: Estimate outcome equation with IMR:
$$
Y_i = X_i \beta + \rho \sigma \hat{\lambda}_i + \varepsilon_i \quad \text{for } S_i = 1
$$

Coefficient on $\hat{\lambda}_i$ tests for selection bias; if insignificant, OLS is consistent.

> [!tip]
> - **Identification**: Requires at least one variable in $Z$ excluded from $X$ (an "instrument" for selection)
> - **Normality**: Relies on joint normality of errors; misspecification leads to inconsistency
> - Alternative: [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] or [[Inverse Probability Weighting (IPW)|IPW]] under weaker assumptions

## Code

```r
# R: Heckman two-step
library(sampleSelection)
heckit_model <- heckit(selection = S ~ z1 + z2, outcome = y ~ x1 + x2, data = df)
summary(heckit_model)
```

## Related notes

- [[Missing Data and Selection (MOC)]]
- [[selection bias]]
- [[inverse Mills ratio]]
