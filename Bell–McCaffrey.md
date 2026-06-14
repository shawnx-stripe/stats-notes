---
title: Bell–McCaffrey
aliases: [Bell-McCaffrey, Bell–McCaffrey correction, BM correction]
tags: [econometrics, inference, few-cluster, standard-errors]
updated: 2026-03-05
---

# Bell–McCaffrey

> [!summary]
> Bias-reduced cluster-robust variance estimator (CR2) with Satterthwaite-based degrees of freedom. Provides better finite-sample inference with few clusters than conventional cluster-robust SEs.

## When to use

Standard cluster-robust SEs (CR0, CR1) suffer from severe downward bias with $G < 30$ clusters, leading to over-rejection. Bell–McCaffrey CR2 adjusts for leverage heterogeneity across clusters and pairs with Satterthwaite df correction, maintaining correct size even with $G \approx 10$. Essential for state-level policy analysis, multi-site RCTs, or any setting with few treatment/control groups.

## R

```r
library(clubSandwich)
model <- lm(y ~ treat + x, data = df)
vcov_cr2 <- vcovCR(model, cluster = df$state, type = "CR2")
coef_test(model, vcov = vcov_cr2, test = "Satterthwaite")
```

> [!tip]
> CR2 dominates CR0/CR1 in finite samples but requires working model for residuals. For $G < 10$, consider [[wild cluster bootstrap]] as well.

## Related notes

- [[few-cluster corrections]]
- [[clustered standard errors]]
- [[Satterthwaite correction]]
- [[wild cluster bootstrap]]
