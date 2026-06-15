---
title: MAR
aliases: [Missing At Random, MAR]
tags: [missing-data, assumptions]
updated: 2026-06-16
---

# MAR

> [!summary] Quick definition
> Missing At Random means missingness may depend on observed covariates but not on the missing value after conditioning on those covariates.

## When it matters

MAR is the identifying assumption behind many imputation, weighting, and likelihood methods. The practical question is whether the observed data include enough predictors of both missingness and outcomes.

## Related notes

- [[Missing Data and Selection (MOC)]]
- [[multiple imputation]]
- [[Inverse Probability of Censoring Weighting (IPCW)]]
