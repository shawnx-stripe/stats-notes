---
title: Pivotal quantities
aliases: [pivotal quantities, Pivotal quantities, pivotal statistic]
tags: [econometrics]
updated: 2026-03-05
---

# Pivotal quantities

> [!summary]
> A quantity whose distribution does not depend on unknown parameters, enabling exact or asymptotically exact inference. Classical examples: t-statistic, F-statistic. Used in [[wild cluster bootstrap]] and [[randomization inference]] to construct tests that do not depend on nuisance parameters.

## Definition

A statistic $Q(Y, \theta)$ is pivotal if its distribution does not depend on unknown parameters:

$$
Q(Y, \theta_0) \sim F \quad \text{for a known distribution } F
$$

Examples: Student's t-statistic (under normality), F-ratio, likelihood ratio under the null.

## Why this matters

Pivotal quantities enable inference without estimating nuisance parameters. In finite-sample settings (e.g., randomization inference), the exact distribution is known by design. In bootstrap and permutation tests, pivotal statistics ensure that resampling approximates the correct null distribution even when variance is unknown.

> [!example] Randomization inference
> The test statistic $T = \hat{\tau}$ is not pivotal (its distribution depends on unknown $Y(0), Y(1)$), but the *rank* of $T$ under all permutations is pivotal—its distribution is uniform given the sharp null. This justifies permutation p-values without parametric assumptions.

## Related notes

- [[Hypothesis testing]]
- [[bootstrap]]
- [[wild cluster bootstrap]]
