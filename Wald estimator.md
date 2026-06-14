---
title: Wald Estimator
aliases:
  - Wald estimate
  - Wald ratio
  - IV Wald estimator
tags:
  - econometrics
  - iv
  - causal-inference
  - identification
updated: 2026-03-04
---

# Wald Estimator

> [!summary] Quick definition
> The Wald estimator is the ratio of the reduced-form effect of an instrument on the outcome to the first-stage effect on treatment: $\hat{\tau}_{\text{Wald}} = \frac{\bar{Y}_1 - \bar{Y}_0}{\bar{D}_1 - \bar{D}_0}$. With a binary instrument it is the simplest IV estimator, identifying the [[Local Average Treatment Effect (LATE)|LATE]] under [[monotonicity]] and [[exclusion restriction]].

## Key formula

$$
\tau_{\text{Wald}} = \frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{E[D \mid Z=1] - E[D \mid Z=0]} = \frac{\text{ITT}_Y}{\text{ITT}_D}
$$

where $Z$ is the instrument and $D$ is treatment.

## Related notes

- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Intent-to-Treat (ITT)]]
- [[Regression Discontinuity Design (RDD)]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
