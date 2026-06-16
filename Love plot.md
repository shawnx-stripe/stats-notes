---
title: Love plot
aliases: [standardized mean difference plot, covariate balance plot]
tags: [matching, diagnostics, visualization]
updated: 2026-06-16
---

# Love plot

> [!summary] Quick definition
> A Love plot displays standardized covariate differences before and after adjustment.

## When it matters

It is a compact balance diagnostic for matching, weighting, or stratification. Each row is a covariate, and points show standardized mean differences before and after adjustment. Good plots make it easy to see whether adjustment improved balance globally or only for a few variables.

Large remaining standardized differences indicate model or support problems that may require trimming, revised propensity-score specification, exact matching on key covariates, or a narrower estimand. A Love plot is descriptive: it diagnoses measured covariates only and says nothing about unmeasured confounding.

## Reporting tips

- Sort covariates by post-adjustment imbalance.
- Mark common thresholds such as absolute SMD of 0.1.
- Show both pre- and post-adjustment points.
- Include variance ratios or distribution plots when mean balance hides tail imbalance.

## Related notes

- [[propensity score]]
- [[matching]]
- [[covariate balance]]
- [[balance check]]
