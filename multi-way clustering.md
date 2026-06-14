---
title: Multi-way clustering
aliases: [multi-way clustering, Multi-way clustering, multiway clustering]
tags: [econometrics]
updated: 2026-03-05
---

# Multi-way clustering

> [!summary]
> Extends [[clustered standard errors]] to account for correlation along multiple dimensions (e.g., firm and time). Uses the Cameron–Gelbach–Miller inclusion-exclusion formula to combine one-way clustered variance matrices.

## Cameron–Gelbach–Miller (CGM) formula

For two clustering dimensions (e.g., firm $i$ and time $t$):
$$
\hat{V}_{\text{multi}} = \hat{V}_i + \hat{V}_t - \hat{V}_{it}
$$
where:
- $\hat{V}_i$: cluster-robust variance by firm
- $\hat{V}_t$: cluster-robust variance by time
- $\hat{V}_{it}$: cluster-robust variance by firm-time intersection

**Extension to 3+ dimensions**: Apply inclusion-exclusion principle (sum singles, subtract pairs, add triples, etc.).

> [!warning]
> Multi-way clustering is appropriate when:
> - Errors are correlated within both dimensions
> - The number of clusters in each dimension is large (G₁, G₂ > 30)
>
> Inference is anti-conservative if the number of clusters in any dimension is small.

## Minimal code snippets

```r
# R: multi-way clustering with multiwayvcov
library(multiwayvcov)
library(lmtest)

m <- lm(y ~ x + controls, data = df)
vcov_multi <- cluster.vcov(m, cluster = df[, c("firm", "time")])
coeftest(m, vcov_multi)
```

```python
# Python: multi-way clustering with linearmodels
from linearmodels.panel import PanelOLS

mod = PanelOLS.from_formula('y ~ x + controls + EntityEffects', data=df.set_index(['firm', 'time']))
res = mod.fit(cov_type='clustered', clusters=df[['firm', 'time']])
print(res)
```

```stata
* Stata: multi-way clustering with reghdfe
reghdfe y x controls, absorb(firm time) vce(cluster firm time)
```

## Related notes

- [[clustered standard errors]]
- [[Moulton problem]]
- [[few-cluster corrections]]
