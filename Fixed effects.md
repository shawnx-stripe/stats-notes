---
title: Fixed Effects
aliases: [Fixed effects, FE estimator, entity fixed effects, unit fixed effects]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Fixed Effects

> [!summary]
> Panel estimator that controls for time-invariant unobserved heterogeneity by demeaning or first-differencing. Consistent even if individual effects correlate with regressors. Cannot estimate time-invariant coefficients.

## Model specification

$$y_{it} = \alpha_i + x_{it}'\beta + \varepsilon_{it}$$

where $\alpha_i$ is an individual-specific intercept. The within estimator applies OLS to demeaned data:

$$\tilde{y}_{it} = \tilde{x}_{it}'\beta + \tilde{\varepsilon}_{it}, \quad \tilde{y}_{it} = y_{it} - \bar{y}_i$$

This removes $\alpha_i$ without estimating $N$ parameters. Consistent if $\mathbb{E}[\varepsilon_{it} \mid x_{i1}, \ldots, x_{iT}, \alpha_i] = 0$.

## Python

```python
from linearmodels.panel import PanelOLS
model = PanelOLS.from_formula('y ~ x1 + x2 + EntityEffects', data=df)
result = model.fit(cov_type='clustered', cluster_entity=True)
```

> [!tip]
> FE is preferable to [[random effects]] when $\alpha_i$ likely correlates with regressors. Use [[Hausman test]] to test this formally. For time-invariant regressors, consider first-differences or random effects.

## Related notes

- [[two-way fixed effects]]
- [[random effects]]
- [[Hausman test]]
- [[Panel Data Methods (MOC)]]
