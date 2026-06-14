---
title: M-Estimation
aliases: [M-estimation, M-estimator, maximum likelihood-type estimation]
tags: [econometrics, inference, robust-methods]
updated: 2026-03-05
---

# M-Estimation

> [!summary]
> General class of estimators defined as solutions to $\sum \psi(Y_i, \theta)=0$. Encompasses MLE, OLS, quantile regression, and Huber regression. Asymptotic theory via the sandwich formula provides robust variance estimates.

## Definition

M-estimator $\hat{\theta}$ solves:

$$
\sum_{i=1}^n \psi(Y_i, X_i, \hat{\theta}) = 0
$$

where $\psi$ is the **score function** or **estimating equation**.

## Asymptotic Distribution

Under regularity conditions:

$$
\sqrt{n}(\hat{\theta} - \theta_0) \xrightarrow{d} N(0, A^{-1} B A^{-1})
$$

where:
- $A = \mathbb{E}\left[\frac{\partial \psi}{\partial \theta}\right]$ (Jacobian)
- $B = \mathbb{E}[\psi \psi^\top]$ (outer product of scores)

**Sandwich variance**: $\widehat{\text{Var}}(\hat{\theta}) = \frac{1}{n} \hat{A}^{-1} \hat{B} \hat{A}^{-1}$

> [!tip]
> - When $\psi$ is the score of a correctly specified likelihood, $A = B$ and we recover the usual Fisher information variance
> - Sandwich formula remains valid under misspecification (robust SEs)
> - Encompasses [[Huber regression]], [[quantile regression]], [[Generalized Method of Moments (GMM)|GMM]], [[Maximum Likelihood Estimation (MLE)|MLE]]

## Related notes

- [[influence function]]
- [[Huber regression]]
- [[Robust Methods (MOC)]]
- [[Model Estimation (MOC)]]
