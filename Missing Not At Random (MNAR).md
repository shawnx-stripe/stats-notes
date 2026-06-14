---
title: Missing Not At Random (MNAR)
aliases: [MNAR, Missing Not At Random, nonignorable missingness, non-ignorable missingness]
tags: [missing-data, selection-bias, identification]
updated: 2026-04-02
---

# Missing Not At Random (MNAR)

> [!summary] Quick definition
> Data are MNAR when the probability of being missing depends on the unobserved value itself, even after conditioning on observed covariates.

## Formal idea

If $R$ indicates observation,

$$
P(R = 1 \mid Y, X)
$$

depends on the missing outcome or covariate value $Y$, not only on $X$.

## Implications

- Standard complete-case analysis is generally biased.
- [[multiple imputation]] under MAR assumptions is not automatically valid.
- Identification usually requires structure, instruments, or bounds.

## Typical responses

- Sensitivity analysis or tipping-point analysis.
- Selection or pattern-mixture models.
- Bounds such as [[Lee bounds]] when the design supports them.
- Careful design and follow-up data collection to make MNAR less plausible.

## Related notes

- [[Missing Data and Selection (MOC)]]
- [[Attrition]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[Lee bounds]]

