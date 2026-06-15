---
title: Kleibergen–Paap
aliases: [Kleibergen-Paap, Kleibergen–Paap rk statistic, Kleibergen-Paap rk Wald F, Kleibergen–Paap rk Wald F, KP statistic]
tags: [econometrics, iv, weak-instruments, diagnostics]
updated: 2026-03-05
---

# Kleibergen–Paap

> [!summary]
> Robust weak-instrument diagnostic for IV models under heteroskedasticity, autocorrelation, or clustering. The rk Wald F-statistic is often reported near Stock-Yogo references, but those critical values are homoskedastic Cragg-Donald benchmarks rather than exact KP cutoffs.

## rk Wald F-Statistic

$$
F_{\text{KP}} = \frac{n - k - L}{L} \cdot \frac{\hat{\pi}^\top Z^\top P_X Z \hat{\pi}}{\hat{\pi}^\top Z^\top M_X Z \hat{\pi}}
$$

where $P_X$ and $M_X$ are projection matrices, and variance matrices are robust to non-i.i.d. errors.

Do not treat Stock-Yogo critical values as strictly valid for robust KP statistics. They are useful homoskedastic Cragg-Donald references; for robust weak-IV diagnostics, prefer context-specific effective F guidance such as [[Montiel Olea–Pflueger F]] where available.

> [!warning]
> - **Rule of thumb**: $F_{\text{KP}} > 10$ is only a rough screen; threshold quality depends on the model and covariance structure
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
- [[Montiel Olea–Pflueger F]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[relevance]]
