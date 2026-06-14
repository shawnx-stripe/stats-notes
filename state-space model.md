---
title: State-Space Model
aliases: [state-space model, state space model, state-space/Kalman filter]
tags: [econometrics, time-series]
updated: 2026-03-05
---

# State-Space Model

> [!summary]
> General framework representing a time series via latent states evolving by a transition equation and linked to observables via an observation equation. Estimated via [[Kalman filter]]. Nests ARIMA, local level/trend, and structural time series models.

## Equations

**State equation** (transition):

$$
\alpha_{t+1} = T_t \alpha_t + R_t \eta_t, \quad \eta_t \sim N(0, Q_t)
$$

**Observation equation** (measurement):

$$
Y_t = Z_t \alpha_t + \varepsilon_t, \quad \varepsilon_t \sim N(0, H_t)
$$

Latent state $\alpha_t$ evolves according to $T_t$; observables $Y_t$ are noisy measurements via $Z_t$.

## Examples

- **Local level**: $\alpha_{t+1} = \alpha_t + \eta_t$, $Y_t = \alpha_t + \varepsilon_t$ (random walk plus noise)
- **Local linear trend**: $\alpha_t = [\mu_t, \beta_t]'$, $\mu_{t+1} = \mu_t + \beta_t + \eta_t$
- **ARIMA(p,d,q)**: Rewrite in state-space form with $\alpha_t$ containing lagged values

## Minimal code

```python
from statsmodels.tsa.statespace.structural import UnobservedComponents

# Local level + seasonal model
model = UnobservedComponents(y, level='local level', seasonal=12)
results = model.fit()
print(results.summary())
```

> [!tip] When to use
> State-space models handle missing data naturally, allow time-varying parameters, and provide optimal forecasts via Kalman filtering. Ideal for structural decomposition (trend + cycle + seasonal).

## Related notes

- [[Kalman filter]]
- [[ARIMA]]
- [[ETS]]
- [[Hidden Markov Model (HMM)|HMM]]
- [[Sequential Monte Carlo (SMC)|SMC]]
- [[Time Series (MOC)]]
