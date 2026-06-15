---
title: Rubin's rules
aliases: [Rubin’s rules, Rubin rules, multiple imputation pooling]
tags: [missing-data, imputation, inference]
updated: 2026-06-16
---

# Rubin's rules

> [!summary] Quick definition
> Rubin's rules combine estimates and uncertainty across multiple imputed datasets.

## When it matters

After fitting the same model on each imputed dataset, pool the point estimates by averaging and combine within-imputation and between-imputation variance. This preserves uncertainty from missing-data imputation under the maintained imputation assumptions.

## Related notes

- [[multiple imputation]]
- [[Missing Data and Selection (MOC)]]
- [[MAR]]
