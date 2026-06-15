---
title: bias estimation
aliases: [bootstrap bias, bias estimate]
tags: [inference, bootstrap]
updated: 2026-06-16
---

# bias estimation

> [!summary] Quick definition
> Bias estimation approximates the gap between an estimator's expected value and the target parameter.

## When it matters

Bootstrap and simulation can estimate finite-sample bias for smooth estimators, but the estimate is noisy and can be unreliable for nonsmooth or boundary problems. Bias correction should be reported separately from uncertainty.

## Related notes

- [[bootstrap]]
- [[variance estimation]]
- [[confidence intervals]]
