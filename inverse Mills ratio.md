---
title: Inverse Mills Ratio
aliases: [inverse Mills ratio, IMR, Mills ratio]
tags: [econometrics, missing-data, selection]
updated: 2026-03-05
---

# Inverse Mills Ratio

> [!summary]
> Ratio of the standard normal PDF to CDF: $\lambda(z) = \phi(z)/\Phi(z)$. In the [[Heckman correction]], the IMR from the selection equation enters the outcome equation as a bias-correction term for sample selection.

## Formula and properties

$$
\lambda(z) = \frac{\phi(z)}{\Phi(z)}
$$
where $\phi(\cdot)$ is the standard normal PDF and $\Phi(\cdot)$ is the CDF.

**Properties**:
- $\lambda(z) > 0$ for all $z$
- $\lambda(z) \to 0$ as $z \to \infty$
- $\lambda(z) \approx -z$ for $z \to -\infty$

## Use in Heckman correction

**Selection equation** (probit):
$$
S_i^* = Z_i'\gamma + u_i, \quad S_i = \mathbb{1}\{S_i^* > 0\}
$$

**Outcome equation** (observed only if $S_i = 1$):
$$
Y_i = X_i'\beta + \epsilon_i
$$

If $(u_i, \epsilon_i)$ are jointly normal, then:
$$
\mathbb{E}[Y_i \mid S_i = 1, X_i] = X_i'\beta + \rho \sigma_\epsilon \cdot \lambda(Z_i'\gamma)
$$

The IMR $\hat{\lambda}(Z_i'\hat{\gamma})$ from the first-stage probit is included as a regressor in the second stage.

## Minimal code snippets

```python
# Python: Heckman correction with statsmodels
from scipy.stats import norm

# Stage 1: Probit for selection
from statsmodels.discrete.discrete_model import Probit
probit = Probit(df['selected'], df[['Z']]).fit()
df['imr'] = norm.pdf(probit.fittedvalues) / norm.cdf(probit.fittedvalues)

# Stage 2: OLS with IMR
from statsmodels.api import OLS, add_constant
X2 = add_constant(df.loc[df['selected'] == 1, ['X', 'imr']])
ols = OLS(df.loc[df['selected'] == 1, 'Y'], X2).fit()
```

## Related notes

- [[Heckman correction]]
- [[Missing Data and Selection (MOC)]]
- [[selection bias]]
