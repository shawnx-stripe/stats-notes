---
title: Overlap Weights
aliases: [overlap weights, tilting weights]
tags: [causal-inference, weighting]
updated: 2026-03-05
---

# Overlap Weights

> [!summary]
> Weights proportional to $e(X)(1-e(X))$ that target the population with the most overlap between treatment groups. Minimizes variance among balancing weights; most robust to extreme propensity scores. Estimates the ATO (average treatment effect on the overlap population).

## Weight formula

$$
w_i = \frac{D_i (1 - e(X_i)) + (1 - D_i) e(X_i)}{\mathbb{E}[D_i(1-e(X_i)) + (1-D_i)e(X_i)]}
$$

Equivalently:
- Treated units: $w_i \propto 1 - e(X_i)$
- Control units: $w_i \propto e(X_i)$

## Comparison with other weighting schemes

| Method | Target population | Variance | Robustness to extremes |
|--------|------------------|----------|----------------------|
| [[Inverse Probability Weighting (IPW)|IPW]] | ATE | High | Low (extreme weights) |
| [[Average Treatment Effect on the Treated (ATT)|ATT]] weights | Treated | Moderate | Moderate |
| Overlap weights | Overlap | Lowest | High (bounded weights) |
| Matching weights | ATT or ATC | Moderate | Moderate |

> [!tip] When to use
> Prefer overlap weights when positivity violations are a concern or when variance reduction is paramount. The estimand (ATO) may be less interpretable than ATE but avoids extreme-weight instability.

## Related notes

- [[Inverse Probability Weighting (IPW)|IPW]]
- [[propensity score]]
- [[Overlap]]
- [[balancing weights]]
