---
title: Design Effect
aliases: [design effect, DEFF, Kish design effect]
tags: [experimentation, design, clustering]
updated: 2026-03-05
---

# Design Effect

> [!summary]
> Ratio of the variance of an estimator under the actual (complex) design to the variance under simple random sampling: $\text{DEFF} = 1 + (\bar{m}-1)\cdot \text{ICC}$. Used to inflate required sample sizes for clustered/stratified experiments.

## Formula and interpretation

For cluster-randomized designs:
$$
\text{DEFF} = 1 + (\bar{m} - 1) \cdot \rho
$$
where $\bar{m}$ is the average cluster size and $\rho$ is the intraclass correlation ([[ICC]]).

**Sample size adjustment**: If a simple random sample requires $n$ units, a clustered design requires $n \times \text{DEFF}$ units for the same power.

> [!example]
> If ICC = 0.05 and average cluster size is 20, then DEFF = 1 + 19 × 0.05 = 1.95. You need nearly twice as many observations as under simple randomization.

> [!tip]
> Reduce DEFF by: (1) decreasing cluster size, (2) including cluster-level covariates to reduce ICC, or (3) stratifying randomization by cluster characteristics.

## Minimal code snippets

```r
# R: compute DEFF from ICC estimate
library(lme4)
m <- lmer(outcome ~ treatment + (1 | cluster), data = df)
icc <- as.numeric(VarCorr(m)$cluster) / (as.numeric(VarCorr(m)$cluster) + sigma(m)^2)
avg_cluster_size <- mean(table(df$cluster))
deff <- 1 + (avg_cluster_size - 1) * icc
cat("DEFF:", deff, "\n")
```

```python
# Python: compute DEFF manually
import numpy as np
icc = 0.05  # from prior study or pilot
avg_cluster_size = df.groupby('cluster').size().mean()
deff = 1 + (avg_cluster_size - 1) * icc
print(f"Design effect: {deff:.2f}")
```

## Related notes

- [[ICC]]
- [[power analysis]]
- [[Moulton problem]]
- [[clustered standard errors]]
