---
title: Indirect Inference
aliases: [indirect inference, simulation-based estimation]
tags: [econometrics, structural-models, estimation]
updated: 2026-03-05
---

# Indirect Inference

> [!summary]
> Estimation method that matches statistics from an auxiliary (reduced-form) model fitted to real data with those from data simulated by the structural model. Does not require computing the structural likelihood.

## Procedure

Let $\theta$ be structural parameters and $\beta$ be auxiliary model parameters.

1. Estimate auxiliary model on real data: $\hat{\beta}_n = \arg\min_\beta Q_n(\beta)$ (e.g., OLS coefficients)
2. For candidate $\theta$:
   - Simulate data $Y^{\text{sim}}(\theta)$ from structural model
   - Estimate auxiliary model: $\hat{\beta}_S(\theta) = \arg\min_\beta Q_S(\beta, Y^{\text{sim}}(\theta))$
3. Choose $\hat{\theta}$ to minimize distance:
$$
\hat{\theta} = \arg\min_\theta \|\hat{\beta}_n - \hat{\beta}_S(\theta)\|^2
$$

> [!tip]
> Indirect inference is useful when:
> - The structural likelihood is intractable or expensive
> - Simulating from the model is cheap
> - The auxiliary model is over-identified relative to $\theta$

## Key insight

The auxiliary model need not be correctly specified; it just needs to provide identifying moment conditions. Common choices: OLS, VAR, or even summary statistics (mean, variance, autocorrelation). Asymptotic efficiency depends on the informativeness of $\beta$ about $\theta$.

## Related notes

- [[Simulated method of moments]]
- [[Structural models]]
- [[Generalized Method of Moments (GMM)|GMM]]
- [[Model Estimation (MOC)]]
