---
title: Interrupted Time Series (ITS)
aliases: [Interrupted Time Series, ITS, interrupted time series design, ITS design]
tags: [causal-inference, quasi-experimental, time-series]
updated: 2026-03-05
---

# Interrupted Time Series (ITS)

> [!summary]
> Quasi-experimental design that uses a time series of outcomes before and after an intervention to estimate causal effects. Models both level and slope changes at the interruption point. Requires no simultaneous co-interventions.

## Regression Specification

$$
Y_t = \beta_0 + \beta_1 \cdot \text{Time}_t + \beta_2 \cdot \text{Post}_t + \beta_3 \cdot (\text{Time}_t \times \text{Post}_t) + \varepsilon_t
$$

- $\beta_2$: immediate level change at intervention
- $\beta_3$: change in slope (trend) post-intervention
- Requires sufficient pre- and post-intervention periods (≥12 each recommended)

> [!warning]
> **Key threats to validity**:
> - **Co-interventions**: Other events coinciding with the interruption
> - **Seasonality**: Adjust with seasonal dummies or [[seasonal differencing]]
> - **Autocorrelation**: Use [[Newey–West]] or ARIMA errors
> - **Regression to the mean**: Intervention timing based on extreme values

## Code

```python
import statsmodels.formula.api as smf

df['time'] = range(len(df))
df['post'] = (df['time'] >= intervention_time).astype(int)
df['time_post'] = df['time'] * df['post']

model = smf.ols('y ~ time + post + time_post', data=df).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
print(model.summary())
```

## Related notes

- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[quasi-experimental design]]
- [[parallel trends assumption]]
