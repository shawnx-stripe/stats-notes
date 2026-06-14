---
title: Multilevel models
aliases: [multilevel models, Multilevel models, hierarchical models, HLM, mixed-effects models]
tags: [econometrics]
updated: 2026-03-05
---

# Multilevel models

> [!summary]
> Regression models with random effects at multiple levels of a hierarchy (e.g., students within schools within districts). Also called hierarchical linear models (HLM) or mixed-effects models. Allow partial pooling of group-level estimates.

## Model specification

**Two-level example** (students $i$ in schools $j$):
$$
Y_{ij} = \beta_0 + \beta_1 X_{ij} + u_j + \epsilon_{ij}
$$
where:
- $u_j \sim N(0, \sigma_u^2)$ is the school random effect
- $\epsilon_{ij} \sim N(0, \sigma_\epsilon^2)$ is the individual error

**Three-level extension** (students in classrooms in schools):
$$
Y_{ijk} = \beta_0 + \beta_1 X_{ijk} + u_k + v_{jk} + \epsilon_{ijk}
$$

**Variance partition**: ICC at level $j$: $\rho_j = \sigma_u^2 / (\sigma_u^2 + \sigma_\epsilon^2)$.

> [!tip]
> Use multilevel models when:
> - Units are nested in a hierarchy
> - You want to estimate group-level effects (e.g., school quality)
> - Partial pooling (shrinkage) is desirable over no pooling (separate regressions) or complete pooling (ignore groups)

## Minimal code snippets

```r
# R: multilevel model with lme4
library(lme4)

# Two-level random intercept
m1 <- lmer(y ~ x + (1 | school), data = df)
summary(m1)

# Random intercept + random slope
m2 <- lmer(y ~ x + (1 + x | school), data = df)
summary(m2)
```

```python
# Python: multilevel model with statsmodels
import statsmodels.formula.api as smf

md = smf.mixedlm("y ~ x", df, groups=df["school"])
mdf = md.fit()
print(mdf.summary())
```

```stata
* Stata: multilevel model
mixed y x || school:, var
```

## Related notes

- [[random effects]]
- [[Fixed effects]]
- [[Moulton problem]]
- [[clustered standard errors]]
