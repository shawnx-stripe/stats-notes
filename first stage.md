---
title: First Stage
aliases: [first stage, first-stage regression, first-stage F-statistic]
tags: [econometrics, iv, diagnostics]
updated: 2026-03-05
---

# First Stage

> [!summary]
> In [[Two-Stage Least Squares (2SLS)|2SLS]], the regression of the endogenous treatment on the instrument(s) and controls. The first-stage F-statistic diagnoses instrument strength; a weak first stage (F < 10) leads to biased and size-distorted second-stage inference.

## First-stage regression and diagnostics

**Stage 1**: Regress treatment on instruments and controls:
$$
D_i = \pi_0 + Z_i'\pi_1 + X_i'\gamma + v_i
$$

**F-statistic**: Test $H_0: \pi_1 = 0$ using cluster-robust standard errors if applicable.

**Rules of thumb**:
- $F \geq 10$: acceptable (Stock–Yogo rule for single instrument)
- $F < 10$: weak instruments; 2SLS is biased toward OLS and inference is unreliable
- $F < 4$: very weak; consider [[Limited Information Maximum Likelihood (LIML)|LIML]], [[Fuller estimator]], or reporting reduced form

> [!tip]
> With multiple instruments, use the Kleibergen–Paap (robust) or Cragg–Donald (homoskedastic) F-statistic. Critical values depend on the acceptable bias and test size distortion ([[Stock–Yogo]] tables).

## Minimal code snippets

```r
# R: first-stage diagnostics with ivreg
library(ivreg)
iv <- ivreg(outcome ~ treatment + controls | instrument + controls, data = df)
summary(iv, diagnostics = TRUE)  # reports weak instrument test
```

```python
# Python: first stage with linearmodels
from linearmodels.iv import IV2SLS

iv = IV2SLS(df['outcome'], df[['controls']], df['treatment'], df['instrument']).fit()
print(iv.first_stage)  # includes F-stat
```

## Related notes

- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Instrumental Variables (IV)]]
- [[weak instruments]]
- [[relevance]]
- [[Stock–Yogo]]
