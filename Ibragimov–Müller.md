---
title: Ibragimov–Müller
aliases: [Ibragimov-Müller, Ibragimov–Müller test, IM test]
tags: [econometrics, inference, few-cluster]
updated: 2026-03-05
---

# Ibragimov–Müller

> [!summary]
> Inference method for settings with few clusters: estimates the parameter separately within each cluster, then uses a $t$-test on the cluster-specific estimates. Valid under heterogeneous treatment effects and asymmetric cluster sizes.

## Procedure

1. Estimate $\hat{\theta}_g$ separately for each cluster $g = 1, \ldots, G$
2. Compute cluster-level mean: $\bar{\theta} = \frac{1}{G} \sum_{g=1}^G \hat{\theta}_g$
3. Compute cluster-level standard error: $\text{SE} = \sqrt{\frac{1}{G(G-1)} \sum_{g=1}^G (\hat{\theta}_g - \bar{\theta})^2}$
4. Test using $t$-distribution with $G-1$ degrees of freedom

> [!check] Advantages
> - Valid with as few as 5-10 clusters (conventional clustered SEs fail)
> - Robust to heterogeneous treatment effects across clusters
> - Does not require balanced cluster sizes
> - Exact finite-sample validity under normality; robust under many departures

> [!warning]
> - Requires enough variation within each cluster to estimate $\hat{\theta}_g$
> - Power loss compared to pooled estimation when clusters are homogeneous

## Code

```r
# R: Ibragimov-Müller inference
cluster_estimates <- tapply(1:nrow(df), df$cluster, function(idx) {
  coef(lm(y ~ x, data = df[idx, ]))["x"]
})
t_stat <- mean(cluster_estimates) / (sd(cluster_estimates) / sqrt(length(cluster_estimates)))
p_value <- 2 * pt(-abs(t_stat), df = length(cluster_estimates) - 1)
```

## Related notes

- [[few-cluster corrections]]
- [[clustered standard errors]]
- [[wild cluster bootstrap]]
