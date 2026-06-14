---
title: Independent Hypothesis Weighting (IHW)
aliases: [IHW, independent hypothesis weighting]
tags: [multiple-testing, inference, experimentation]
updated: 2026-04-02
---

# Independent Hypothesis Weighting (IHW)

> [!summary] Quick definition
> IHW improves power in multiple testing by assigning data-driven weights to hypotheses using an external covariate that is informative about power but independent of the null p-value.

## Core idea

- Partition hypotheses by a covariate such as baseline variance, count, or exposure.
- Learn weights on held-out folds.
- Apply weighted FDR control so more informative hypotheses get more testing budget.

## Minimal code snippets

```r
library(IHW)
res <- ihw(df$pvalue, df$covariate, alpha = 0.10)
adj_pvalues(res)
```

## Related notes

- [[False Discovery Rate (FDR)]] · [[Hierarchical False Discovery Rate (FDR)|hierarchical FDR]] · [[multiple testing control]]
