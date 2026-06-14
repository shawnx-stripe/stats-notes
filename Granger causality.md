---
title: Granger Causality
aliases: [Granger causality, Granger causality test, Granger-causes]
tags: [econometrics, time-series]
updated: 2026-03-05
---

# Granger Causality

> [!summary]
> $X$ Granger-causes $Y$ if past values of $X$ improve prediction of $Y$ beyond past values of $Y$ alone. Tested via F-test on lagged $X$ in a [[VAR]]. Measures predictive precedence, not true causation.

## Test Procedure

Compare two regressions:

**Unrestricted**: $Y_t = \alpha_0 + \sum_{i=1}^p \alpha_i Y_{t-i} + \sum_{j=1}^p \beta_j X_{t-j} + \varepsilon_t$

**Restricted**: $Y_t = \alpha_0 + \sum_{i=1}^p \alpha_i Y_{t-i} + u_t$

F-test: $H_0: \beta_1 = \cdots = \beta_p = 0$.

> [!warning]
> - Granger causality ≠ structural causality; both $X$ and $Y$ could be driven by a third variable
> - Sensitive to lag length choice (use AIC/BIC or information criteria)
> - Requires stationarity (difference variables if needed)

## Code

```python
from statsmodels.tsa.stattools import grangercausalitytests
import pandas as pd

# Test if X Granger-causes Y (maxlag=4)
data = pd.DataFrame({'Y': y, 'X': x})
results = grangercausalitytests(data[['Y', 'X']], maxlag=4, verbose=True)
```

## Related notes

- [[VAR]]
- [[Time Series (MOC)]]
- [[Local projections (Jordà)]]
