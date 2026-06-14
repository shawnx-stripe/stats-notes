---
title: Montiel Olea–Pflueger F
aliases: [Montiel Olea-Pflueger F, Montiel Olea–Pflueger, MOP F-statistic, effective F-statistic]
tags: [econometrics, iv, weak-instruments, diagnostics]
updated: 2026-03-05
---

# Montiel Olea–Pflueger F

> [!summary]
> Effective F-statistic for testing instrument strength that is robust to heteroskedasticity, serial correlation, and clustering. Preferred over Cragg–Donald in non-i.i.d. settings; compared to critical values from Montiel Olea & Pflueger (2013).

## Formula

$$
F_{\text{eff}} = \frac{\hat{\pi}' \hat{\Sigma}^{-1} \hat{\pi}}{k}
$$

where $\hat{\pi}$ is the vector of first-stage coefficients on the $k$ instruments, and $\hat{\Sigma}$ is the robust variance–covariance matrix of those coefficients (allowing for clustering, HAC, etc.).

## Decision rule

Compare $F_{\text{eff}}$ to the Montiel Olea & Pflueger (2013) critical values for the desired maximum bias or size distortion. Thresholds vary by:
- Number of instruments $k$
- Tolerance level (e.g., 10% or 20% max relative bias)
- Single vs. multiple endogenous regressors

> [!warning]
> The "rule-of-thumb" $F > 10$ is derived for i.i.d. errors. With clustering or serial correlation, use MOP critical values instead.

## Stata snippet

```stata
* ivreg2 with clustering and MOP effective F
ivreg2 y x1 (x_endog = z1 z2), cluster(cluster_id) ffirst
* Reports effective F (robust to clustering) and compares to MOP critical values
```

## Related notes

- [[weak instruments]]
- [[Kleibergen–Paap]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[relevance]]
