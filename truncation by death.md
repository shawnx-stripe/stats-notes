---
title: truncation by death
aliases: [truncation-by-death, survivor average causal effect]
tags: [causal-inference, missing-data, principal-stratification]
updated: 2026-06-16
---

# truncation by death

> [!summary] Quick definition
> Truncation by death occurs when an outcome is undefined for units who do not survive or remain eligible to have it measured.

## When it matters

This is not ordinary missing data: the target estimand must define whose outcome is meaningful, often using principal strata such as always-survivors. Naive complete-case analysis can change the population being compared.

## Related notes

- [[Attrition]]
- [[principal stratification]]
- [[Missing Data and Selection (MOC)]]
