---
title: Interactive Fixed Effects
aliases: [interactive fixed effects, factor model, common factors]
tags: [econometrics, panel-data]
updated: 2026-03-05
---

# Interactive Fixed Effects

> [!summary]
> Panel model where unobserved heterogeneity has a factor structure: $\alpha_{it} = \lambda_i' f_t$, allowing unit-specific loadings on common time-varying factors. Generalizes additive FE; estimated via iterative least squares or nuclear norm penalization.

## Model specification

$$
Y_{it} = X_{it}'\beta + \lambda_i' f_t + \epsilon_{it}
$$
where:
- $\lambda_i \in \mathbb{R}^r$ are unit-specific factor loadings
- $f_t \in \mathbb{R}^r$ are common time-varying factors (unobserved)
- $r$ is the number of factors (typically small)

**Additive two-way FE** is a special case: $\lambda_i = 1$ for all $i$.

> [!tip]
> Interactive FE models are useful when parallel trends fail in DiD but a factor model can capture differential trends. Estimation:
> - **Iterative LS**: Bai (2009) alternates between estimating $\lambda, f$ and $\beta$
> - **Matrix completion**: Athey et al. use nuclear norm regularization
> - **Pre-specified factors**: If $f_t$ is observed (e.g., macro indicators), estimate via interacted FE

## Minimal code snippets

```r
# R: interactive fixed effects with gsynth
library(gsynth)
out <- gsynth(Y ~ D + X, data = panel_df,
              index = c("unit", "time"),
              force = "two-way",
              r = c(0, 5),  # search over 0-5 factors
              CV = TRUE)
plot(out)
```

```python
# Python: nuclear norm minimization (simplified)
from sklearn.decomposition import TruncatedSVD

# Residualize Y on X, reshape to unit × time matrix
resid_matrix = residuals.pivot(index='unit', columns='time', values='resid')
svd = TruncatedSVD(n_components=2)  # assume 2 factors
svd.fit(resid_matrix.fillna(0))
factor_structure = svd.transform(resid_matrix.fillna(0))
```

## Related notes

- [[two-way fixed effects]]
- [[Panel Data Methods (MOC)]]
- [[Synthetic Control]]
