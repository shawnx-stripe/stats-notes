---
title: Hotz–Miller CCP
aliases: [Hotz-Miller CCP, Hotz–Miller, conditional choice probabilities, CCP estimator]
tags: [econometrics, structural-models]
updated: 2026-03-05
---

# Hotz–Miller CCP

> [!summary]
> Conditional Choice Probability estimator (Hotz & Miller 1993) for dynamic discrete choice models. Two-step: first estimate CCPs nonparametrically, then invert the Bellman equation to recover structural parameters without solving the full dynamic program.

## Two-Step Approach

**Step 1**: Estimate CCPs nonparametrically:
$$
\hat{p}(d | x) = \frac{\sum_{i,t} \mathbb{1}(d_{it} = d, x_{it} = x)}{\sum_{i,t} \mathbb{1}(x_{it} = x)}
$$

**Step 2**: Invert Euler equation to form moment conditions. For each choice $d$:
$$
\delta_d(x, \theta) = u_d(x, \theta) + \beta \sum_{x'} f(x' | x, d) V(x', \theta)
$$
where $V(x, \theta)$ is recovered from CCPs using the Bellman equation inversion.

## When to Use

- **Large state spaces**: Avoids nested fixed-point (NFXP) iteration in each optimization step
- **Computational speed**: Particularly fast for models with many choices or states
- **Finite-sample bias**: Can be large if CCPs are poorly estimated (requires large $n$)
- Compare with [[MPEC]] (mathematical programming with equilibrium constraints) for alternative computational approach

## Related notes

- [[Structural models]]
- [[DSGE]]
- [[MPEC]]
- [[Maximum Likelihood Estimation (MLE)|MLE]]
