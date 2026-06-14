---
title: Kleibergen–Paap
aliases: [Kleibergen-Paap, Kleibergen–Paap rk statistic, Kleibergen-Paap rk Wald F, Kleibergen–Paap rk Wald F, KP statistic]
tags: [econometrics, iv, weak-instruments, diagnostics]
updated: 2026-03-05
---

# Kleibergen–Paap

> [!summary]
> Generalization of the Cragg–Donald statistic for testing weak instruments that is robust to heteroskedasticity, autocorrelation, and clustering. The rk Wald F-statistic is compared to [[Stock–Yogo]] critical values.

## rk Wald F-Statistic

$$
F_{\text{KP}} = \frac{n - k - L}{L} \cdot \frac{\hat{\pi}^\top Z^\top P_X Z \hat{\pi}}{\hat{\pi}^\top Z^\top M_X Z \hat{\pi}}
$$

where $P_X$ and $M_X$ are projection matrices, and variance matrices are robust to non-i.i.d. errors.

Compare to Stock–Yogo critical values (e.g., 10 for 10% maximal IV relative bias).

> [!warning]
> - **Rule of thumb**: $F_{\text{KP}} > 10$ suggests instruments are not weak (but threshold varies by context)
> - **Clustering**: KP statistic is valid with clustered errors; standard first-stage F is not
> - **Multiple endogenous regressors**: Use with caution; weak-IV diagnostics less clear-cut

## Code

```stata
* Stata: weak instrument test with clustering
ivregress 2sls y (x = z1 z2 z3), vce(cluster cluster_id)
estat firststage  // reports Kleibergen-Paap F
```

## Related notes

- [[weak instruments]]
- [[Stock–Yogo]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[relevance]]
