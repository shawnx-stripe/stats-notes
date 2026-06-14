---
title: DSGE
aliases: [DSGE, dynamic stochastic general equilibrium]
tags: [econometrics, structural-models, macroeconomics, time-series]
updated: 2026-03-05
---

# DSGE

> [!summary]
> Dynamic Stochastic General Equilibrium models: micro-founded macro models with optimizing agents, market clearing, and stochastic shocks. Estimated via Bayesian methods (MCMC) or GMM/indirect inference.

## Key features

DSGE models derive macro dynamics from individual optimization (households, firms) subject to resource constraints and stochastic technology/preference shocks. Core components: Euler equations (inter-temporal optimization), production functions, market clearing, and law of motion for state variables. Linearized around steady state, yielding state-space form suitable for [[Kalman filter]] estimation. Priors encode economic theory; posterior inference via [[Markov Chain Monte Carlo (MCMC)|MCMC]].

## Software

```r
library(dynare)  # interfaces with Dynare for DSGE estimation
```

> [!note]
> DSGE estimation requires strong priors and identification assumptions. Critiqued for poor out-of-sample forecasting during crises (2008). VAR models often perform better for prediction.

## Related notes

- [[Structural models]]
- [[Bayesian econometrics]]
- [[Markov Chain Monte Carlo (MCMC)|MCMC]]
- [[Kalman filter]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
