---
title: Balanced Panel
aliases: [balanced panel, balanced panel data]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Balanced Panel

> [!summary]
> Panel dataset where every unit is observed in every time period ($N \times T$ complete). Contrast with unbalanced panels where some unit-period observations are missing. Required or preferred by some estimators (e.g., certain DiD methods).

## Implications

**Advantages**:
- Simpler estimation: no need to handle missing data or adjust for varying sample composition
- Standard errors are easier to compute
- Some estimators (e.g., [[Arellano–Bond]], [[System GMM]]) assume or perform better with balance

**Disadvantages**:
- Restrictive: real data often have attrition, entry/exit
- Dropping unbalanced units can induce selection bias

## When unbalanced panels are problematic

If missingness is related to unobserved outcomes ([[MNAR]]), estimates may be biased. Use:
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] to reweight observed units
- Selection models to jointly model missingness and outcomes
- Check sensitivity to attrition assumptions

> [!tip]
> Always report whether the panel is balanced or unbalanced, and test for selective attrition if you drop incomplete units.

## Stata snippet

```stata
* Check if panel is balanced
xtset unit_id time
xtdescribe
* Reports # of balanced units and gaps
```

## Related notes

- [[Panel Data Methods (MOC)]]
- [[composition]]
- [[Attrition]]
- [[two-way fixed effects]]
