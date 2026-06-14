---
title: Few clusters problem
aliases: [few clusters problem, Few clusters problem, few-cluster inference]
tags: [econometrics, ab-testing]
updated: 2026-03-05
---

# Few clusters problem

> [!summary]
> When the number of clusters is small (G < 30–50), cluster-robust standard errors are severely biased downward. Requires corrections such as the [[wild cluster bootstrap]], [[few-cluster corrections]], or [[randomization inference]].

## Why it matters

Cluster-robust variance estimator (CRVE):
$$
\hat{V}_{\text{CR}} = \left(\sum_{g=1}^G X_g'X_g\right)^{-1} \left(\sum_{g=1}^G X_g'u_g u_g'X_g\right) \left(\sum_{g=1}^G X_g'X_g\right)^{-1}
$$
relies on asymptotics in $G$. With small $G$, coverage falls well below nominal levels (e.g., 80% instead of 95%).

> [!warning]
> Standard cluster-robust SEs are anti-conservative (too small) when $G < 30$. Tests over-reject; confidence intervals under-cover. The problem worsens when:
> - Treatment varies at the cluster level
> - Clusters are unbalanced
> - Few treated clusters

## Solutions

| Method | When to use | Implementation |
|--------|-------------|----------------|
| [[wild cluster bootstrap]] | $G \geq 6$, gold standard | `boottest` (Stata), `fwildclusterboot` (R) |
| [[few-cluster corrections]] (CR2/CR3) | $G \geq 10$, fast approximation | `clubSandwich` (R) |
| [[randomization inference]] | Cluster randomization, exact | `ritest` (Stata), `ri2` (R) |
| Aggregate to cluster level | Always valid if $G$ small | Manual |

## Minimal code snippets

```r
# R: CR2 standard errors with clubSandwich
library(clubSandwich)
library(lmtest)
m <- lm(outcome ~ treatment + controls, data = df)
coeftest(m, vcov = vcovCR(m, cluster = df$cluster, type = "CR2"))
```

## Related notes

- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[wild cluster bootstrap]]
- [[Moulton problem]]
