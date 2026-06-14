---
title: Cutoff
aliases: [cutoff, threshold, assignment cutoff, treatment cutoff]
tags: [causal-inference, rdd, design]
updated: 2026-04-02
---

# Cutoff

> [!summary] Quick definition
> A cutoff is the threshold on a running or score variable that changes treatment assignment, eligibility, or treatment probability in threshold-based designs such as [[Regression Discontinuity Design (RDD)|RDD]].

## Why it matters

- Defines the local comparison in RD.
- Determines which observations are just above vs. just below treatment assignment.
- Can also define eligibility rules in policy or program settings.

## Minimal code snippets

```r
c0 <- 0
df$above_cutoff <- as.integer(df$running_var >= c0)
```

## Related notes

- [[running variable]] · [[Regression Discontinuity Design (RDD)]] · [[sharp RDD]] · [[fuzzy RDD]]
