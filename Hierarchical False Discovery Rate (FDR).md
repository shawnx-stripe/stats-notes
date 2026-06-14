---
title: Hierarchical False Discovery Rate (FDR)
aliases: [hierarchical FDR, hierarchical false discovery rate, tree-structured FDR]
tags: [multiple-testing, inference, experimentation]
updated: 2026-04-02
---

# Hierarchical False Discovery Rate (FDR)

> [!summary] Quick definition
> Hierarchical FDR controls false discoveries when hypotheses are organized into nested families. Typical workflows test broad parent families first, then drill into children only when higher-level evidence clears a pre-specified threshold.

## Why it matters

- Reduces multiplicity burden when hypotheses come in natural trees or groups.
- Matches reporting structures such as feature families, metric bundles, or ontology-based analyses.
- Avoids spending power on deep nodes when top-level families show no signal.

## Minimal code snippets

```r
# Simple top-down workflow: test parents first, then children only for rejected parents
parent_q <- p.adjust(parent_p, method = "BH")
child_q <- lapply(child_p[parent_q <= 0.10], p.adjust, method = "BH")
```

## Related notes

- [[False Discovery Rate (FDR)]] · [[multiple testing control]] · [[Independent Hypothesis Weighting (IHW)|IHW]]
