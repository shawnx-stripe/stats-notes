---
title: MASE
aliases: [MASE, mean absolute scaled error]
tags: [time-series, forecasting, evaluation]
updated: 2026-03-05
---

# MASE

> [!summary]
> Mean Absolute Scaled Error: scale-free forecast accuracy metric that divides MAE by the MAE of a naive (random walk) forecast. Values < 1 indicate improvement over naive; works for intermittent and cross-series comparisons.

## Formula

$$
\text{MASE} = \frac{\text{MAE}}{\text{MAE}_{\text{naive}}} = \frac{\frac{1}{T} \sum_{t=1}^T |y_t - \hat{y}_t|}{\frac{1}{T-1} \sum_{t=2}^T |y_t - y_{t-1}|}
$$

- **Numerator**: MAE of the forecast
- **Denominator**: MAE of the naive (random walk) in-sample forecast

**Interpretation**: MASE < 1 means the model beats naive; MASE > 1 means naive is better.

> [!tip]
> - **Scale-free**: Can compare across series with different scales
> - **Intermittent series**: Works when many observations are zero (unlike percentage errors)
> - **Symmetric**: Equal penalty for over- and under-forecasting

## Code

```python
import numpy as np

def mase(y_true, y_pred, y_train):
    mae = np.mean(np.abs(y_true - y_pred))
    naive_mae = np.mean(np.abs(np.diff(y_train)))
    return mae / naive_mae

score = mase(y_test, forecast, y_train)
```

## Related notes

- [[Time Series (MOC)]]
- [[Diebold–Mariano test]]
- [[Prophet]]
