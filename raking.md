---
title: raking
aliases: [iterative proportional fitting, raking weights]
tags: [weighting, surveys, causal-inference]
updated: 2026-06-16
---

# raking

> [!summary] Quick definition
> Raking adjusts weights so weighted sample margins match known population margins.

## When it matters

Raking is common in survey adjustment, post-stratification, and calibration weighting when the sample distribution differs from known population margins. It iteratively rescales weights so each marginal distribution matches targets such as age, geography, or device type.

In causal analyses, use only pre-treatment margins. Raking can improve representativeness or covariate balance, but it cannot repair missing support: if a target cell has no comparable observations, weights become unstable or extrapolative.

## Diagnostics

- Compare weighted and target margins after convergence.
- Inspect maximum weights, effective sample size, and whether a few cells dominate.
- Pre-specify caps or trimming rules when operational weights can explode.

## Related notes

- [[stratification]]
- [[entropy balancing]]
- [[balancing weights]]
- [[effective sample size]]
