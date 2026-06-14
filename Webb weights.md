---
title: Webb Weights
aliases: [Webb weights, six-point distribution, Webb (2023)]
tags: [econometrics, inference, bootstrap, few-cluster]
updated: 2026-03-05
---

# Webb Weights

> [!summary]
> Six-point weight distribution for the [[wild cluster bootstrap]], designed for settings with very few clusters (e.g., $G \leq 12$). Provides better size control than [[Rademacher weights]] when the number of clusters is extremely small.

## Weight distribution

Webb (2023) six-point distribution:

$$
\omega \in \left\{-\sqrt{\frac{3+\sqrt{5}}{2}}, -\sqrt{\frac{3-\sqrt{5}}{2}}, -1, 1, \sqrt{\frac{3-\sqrt{5}}{2}}, \sqrt{\frac{3+\sqrt{5}}{2}}\right\}
$$

Each value has probability $1/6$. This distribution matches the first six moments of a standard normal and provides better finite-sample performance than two-point Rademacher weights.

## When to use

- Very few clusters: $G \leq 12$ (rule of thumb)
- [[Rademacher weights]] (two-point) have poor size control
- Combined with [[wild cluster bootstrap]] and [[Bell–McCaffrey]] CR2 variance

> [!warning]
> With $G < 6$, even Webb weights struggle. Consider aggregation, randomization inference, or permutation tests instead.

## R snippet

```r
library(fwildclusterboot)
# Wild cluster bootstrap with Webb weights
boottest(model, clustid = "cluster_id", B = 9999, type = "webb")
# type = "rademacher" for two-point, "webb" for six-point
```

## Related notes

- [[wild cluster bootstrap]]
- [[Rademacher weights]]
- [[few-cluster corrections]]
