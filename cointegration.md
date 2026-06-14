---
title: Cointegration
aliases: [cointegration, cointegrated, cointegrating relationship]
tags: [econometrics, time-series]
updated: 2026-03-05
---

# Cointegration

> [!summary]
> Two or more non-stationary I(1) series are cointegrated if a linear combination is stationary. Implies a long-run equilibrium relationship. Tested via [[Engle–Granger]] (residual-based) or [[Johansen]] (system-based) methods.

## Definition

If $Y_t$ and $X_t$ are both I(1), they are cointegrated if there exists $\beta$ such that:

$$
Y_t - \beta X_t = \epsilon_t \sim I(0)
$$

The residual $\epsilon_t$ is stationary, meaning $Y_t$ and $X_t$ share a common stochastic trend and do not drift arbitrarily far apart.

## Economic interpretation

Cointegration implies a long-run equilibrium: deviations from $Y_t = \beta X_t$ are temporary and mean-reverting. Examples:
- Spot and futures prices
- Money supply and price level
- Consumption and income

## Testing for cointegration

| Method | Approach | Pros | Cons |
|--------|----------|------|------|
| [[Engle–Granger]] | Two-step: regress $Y$ on $X$, test residuals for unit root | Simple, single equation | Only finds one cointegrating vector; inefficient for $>2$ variables |
| [[Johansen]] | System-based VECM; tests rank of cointegrating matrix | Multiple cointegrating vectors; efficient | More complex; sensitive to lag selection |

## Python snippet

```python
from statsmodels.tsa.stattools import coint
# Engle-Granger test
score, pvalue, crit_values = coint(y, x)
print(f"Cointegration test p-value: {pvalue:.3f}")
# pvalue < 0.05 => reject null of no cointegration
```

## Related notes

- [[VECM]]
- [[Engle–Granger]]
- [[Johansen]]
- [[ADF test]]
- [[Time Series (MOC)]]
