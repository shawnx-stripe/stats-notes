---
title: E-value
aliases: [E value, VanderWeele Ding E-value]
tags: [robust-methods, sensitivity-analysis, causal-inference]
updated: 2026-06-16
---

# E-value

> [!summary] Quick definition
> An E-value summarizes the minimum unmeasured-confounding strength needed to explain away an observed association.

## When it matters

Use an E-value when a published or observational estimate is vulnerable to unmeasured confounding and you want a scale-free robustness summary. For a risk ratio above 1, the E-value is the minimum association that an unmeasured confounder would need with both treatment and outcome, conditional on measured covariates, to move the estimate to the null.

It is a sensitivity-analysis summary, not a fix for confounding. Large E-values are more reassuring only if confounders of that strength are implausible in the domain. Small E-values mean modest unmeasured confounding could explain the result.

## Practical cautions

- Use effect measures compatible with the published E-value formula; convert odds ratios carefully when outcomes are common.
- Report the E-value for the point estimate and for the confidence-limit closest to the null.
- Interpret it alongside design quality, measured covariate balance, negative controls, and subject-matter benchmarks.

## Related notes

- [[Robust Methods (MOC)]]
- [[ignorability]]
- [[Oster’s delta]]
- [[Rosenbaum sensitivity]]
