---
title: Local Projections (Jordà)
aliases: [Local projections, local projections, Jordà local projections, LP-IRF]
tags: [econometrics, time-series, causal-inference]
updated: 2026-03-05
---

# Local Projections (Jordà)

> [!summary]
> Method for estimating impulse response functions by running separate regressions at each horizon $h$. More robust to misspecification than VAR-based IRFs; easily accommodates nonlinearities, state dependence, and [[Newey–West]] inference.

## Estimation

For each horizon $h = 0, 1, 2, \ldots, H$, run:

$$
y_{t+h} = \alpha^h + \beta^h D_t + \sum_{j=1}^p \gamma_j^h y_{t-j} + \sum_{j=1}^p \delta_j^h x_{t-j} + \varepsilon_{t+h}
$$

The sequence $\{\beta^h\}_{h=0}^H$ traces out the impulse response function of $y$ to shock $D_t$.

Use [[Newey–West]] or [[Driscoll–Kraay]] standard errors to account for serial correlation in $\varepsilon_{t+h}$.

> [!check] Advantages over VAR
> - **Robustness**: Does not impose restrictions from distant horizons on near-term dynamics
> - **Flexibility**: Easy to add interactions, nonlinearities, or state-dependent effects
> - **Direct inference**: Each horizon estimated separately; no impulse response error accumulation

> [!warning]
> - Less efficient than VAR when VAR is correctly specified
> - Overlapping forecast errors require robust standard errors

## Code

```python
import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.iolib.summary2 import summary_col

irfs = []
for h in range(max_horizon + 1):
    df[f'y_lead_{h}'] = df['y'].shift(-h)
    model = OLS.from_formula(f'y_lead_{h} ~ treatment + L1.y + L2.y', data=df)
    result = model.fit(cov_type='HAC', cov_kwds={'maxlags': h})
    irfs.append(result.params['treatment'])
```

## Related notes

- [[VAR]]
- [[Newey–West]]
- [[Time Series (MOC)]]
- [[event study]]
