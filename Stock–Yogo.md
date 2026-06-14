---
title: Stock–Yogo
aliases: [Stock-Yogo, Stock–Yogo critical values, Stock-Yogo critical values]
tags: [econometrics, iv, weak-instruments, diagnostics]
updated: 2026-03-05
---

# Stock–Yogo

> [!summary]
> Critical values (Stock & Yogo 2005) for testing whether instruments are weak. Based on maximum bias or size distortion thresholds for 2SLS/LIML. The first-stage F-statistic is compared against these thresholds (rule-of-thumb: F > 10).

## Critical values

Stock–Yogo provide tables for two criteria:
1. **Maximal IV bias relative to OLS**: Reject weak instruments if first-stage F exceeds the critical value for desired bias threshold (e.g., 10%, 20%)
2. **Maximal Wald test size distortion**: Reject if F exceeds the critical value for desired size (e.g., 10% actual size when nominal is 5%)

Example: For 1 endogenous regressor and 2 instruments, $F > 19.93$ ensures 2SLS bias is $< 10\%$ of OLS bias.

## Comparison table

| F-statistic | Interpretation |
|-------------|----------------|
| $F < 10$ | Weak instruments; bias and size distortion likely severe |
| $10 < F < 20$ | Marginal; check Stock–Yogo tables for your case |
| $F > 20$ | Generally safe for 1 endogenous variable |

> [!warning]
> Stock–Yogo critical values assume i.i.d. errors. With clustering or heteroskedasticity, use [[Montiel Olea–Pflueger F]] or [[Kleibergen–Paap]] instead.

## Stata snippet

```stata
ivregress 2sls y x1 (x_endog = z1 z2), first
* Reports first-stage F and flags weak instruments if F < Stock-Yogo threshold
```

## Related notes

- [[weak instruments]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Kleibergen–Paap]]
- [[Instrumental Variables (IV)]]
