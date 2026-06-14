---
title: Satterthwaite Correction
aliases: [Satterthwaite correction, Satterthwaite degrees of freedom, Welch-Satterthwaite]
tags: [econometrics, inference]
updated: 2026-03-05
---

# Satterthwaite Correction

> [!summary]
> Approximation of the degrees of freedom for a linear combination of variance estimates with unequal variances. Used in the [[Bell–McCaffrey]] CR2 correction for few-cluster inference and in Welch's $t$-test.

## Formula

For a statistic $\hat{\theta}$ with variance $\hat{V} = \sum_{g=1}^G \hat{V}_g$, the Satterthwaite degrees of freedom are:

$$
\nu = \frac{\left(\sum_{g=1}^G \hat{V}_g\right)^2}{\sum_{g=1}^G \frac{\hat{V}_g^2}{\nu_g}}
$$

where $\nu_g$ are the degrees of freedom associated with each variance component. The t-statistic $t = \hat{\theta}/\sqrt{\hat{V}}$ is then compared to $t_{\nu}$ instead of $t_{G-1}$.

## When to use

- Few clusters ($G < 30$): standard $t_{G-1}$ is too conservative; Satterthwaite df improve power
- Unequal cluster sizes: clusters contribute unequally to the variance; Satterthwaite adjusts for this
- Combined with [[Bell–McCaffrey]] CR2 variance estimator for refined inference

> [!tip]
> Satterthwaite correction is automatic in `fixest::feols(..., vcov = "CR2")` and in R's `clubSandwich::coef_test()`.

## R snippet

```r
library(clubSandwich)
library(fixest)
model <- feols(y ~ x, data = data, cluster = ~cluster_id)
# CR2 + Satterthwaite df
coef_test(model, vcov = "CR2", test = "Satterthwaite")
```

## Related notes

- [[Bell–McCaffrey]]
- [[few-cluster corrections]]
- [[Standard Errors and Inference (MOC)]]
