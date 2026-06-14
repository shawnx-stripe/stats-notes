---
title: Overidentification Test
aliases: [overidentification test, overidentifying restrictions test]
tags: [econometrics, iv, diagnostics]
updated: 2026-03-05
---

# Overidentification Test

> [!summary]
> Test of whether instruments satisfy exclusion restrictions when there are more instruments than endogenous regressors. Implemented as [[Hansen J test]] (robust) or [[Sargan test]] (homoskedastic). Rejection suggests at least one instrument is invalid.

## Test statistic

For $L$ instruments and $K$ endogenous variables ($L > K$), the test statistic is:

$$
J = n \cdot \hat{u}' Z (Z'Z)^{-1} Z' \hat{u} / \hat{\sigma}^2
$$

where $\hat{u}$ are [[Two-Stage Least Squares (2SLS)|2SLS]] residuals. Under the null that all instruments are valid, $J \xrightarrow{d} \chi^2_{L-K}$.

> [!warning] Interpretation
> The test has power only against certain violations of the exclusion restriction. Failure to reject does not prove instruments are valid—it only indicates that the overidentifying restrictions are not detectably violated. All instruments could be invalid in the same direction and the test would not reject.

## Minimal code

```python
from linearmodels.iv import IV2SLS

model = IV2SLS(y, X_exog, X_endog, Z).fit(cov_type='robust')
print(f"Hansen J: {model.j_stat.stat:.3f}, p-value: {model.j_stat.pval:.3f}")
```

## Related notes

- [[Hansen J test]]
- [[Sargan test]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
