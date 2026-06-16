---
title: balance check
aliases: [balance checks, covariate balance check]
tags: [diagnostics, causal-inference]
updated: 2026-06-16
---

# balance check

> [!summary] Quick definition
> A balance check compares pre-treatment variables across analysis groups or assignment conditions.

## When it matters

Balance checks help detect failed randomization, poor overlap, or model-dependent adjustment. They should focus on pre-treatment covariates and be interpreted with design context rather than as a mechanical pass/fail test.

In randomized experiments, large imbalances may indicate bad assignment, logging errors, or chance imbalances worth adjusting for. In observational designs, balance checks evaluate whether matching, weighting, or stratification made treated and control groups comparable on measured covariates.

## Good practice

- Prefer standardized mean differences and distributional plots over many unadjusted p-values.
- Check pre-treatment outcomes when available.
- Separate design diagnostics from outcome analysis; do not tune balance after seeing outcomes.
- Treat good balance as necessary but not sufficient for identification.

## Related notes

- [[covariate balance]]
- [[covariate balance test]]
- [[ignorability]]
- [[Love plot]]
