---
title: calibration plot
aliases: [calibration curve, reliability plot]
tags: [diagnostics, prediction, causal-ml]
updated: 2026-06-16
---

# calibration plot

> [!summary] Quick definition
> A calibration plot compares predicted probabilities or effects with observed frequencies or validation estimates.

## When it matters

For outcome models it checks probability calibration; for CATE models it can compare predicted effect groups to honest treatment-effect estimates. Use held-out data when possible.

## Related notes

- [[Outcome regression (OR)]]
- [[causal forests]]
- [[uplift metrics]]
