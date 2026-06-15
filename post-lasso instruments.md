---
title: post-lasso instruments
aliases: [post-Lasso instruments, lasso-selected instruments]
tags: [econometrics, iv, machine-learning]
updated: 2026-06-16
---

# post-lasso instruments

> [!summary] Quick definition
> Post-lasso IV uses regularization to select instruments or controls, then estimates the final IV model on the selected set.

## When it matters

It can help with many candidate instruments, but selection uncertainty and weak identification remain concerns. Use sample splitting or orthogonal methods where possible and report first-stage diagnostics after selection.

## Related notes

- [[Two-Stage Least Squares (2SLS)]]
- [[Instrumental Variables (IV)]]
- [[double machine learning]]
