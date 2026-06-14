---
title: Policy Value
aliases: [policy value, welfare, expected policy outcome]
tags: [causal-inference, machine-learning, policy-learning]
updated: 2026-03-05
---

# Policy Value

> [!summary]
> Expected outcome under a given treatment assignment policy $\pi$: $V(\pi) = \mathbb{E}[Y(\pi(X))]$. The optimal policy maximizes policy value. Estimated via doubly robust methods; regret measures distance from optimal.

## Estimand and optimization

The optimal policy is:

$$
\pi^*(x) = \operatorname{argmax}_{d \in \{0,1\}} \mathbb{E}[Y(d) \mid X = x]
$$

with value $V^* = \mathbb{E}[Y(\pi^*(X))]$. Regret is $R(\pi) = V^* - V(\pi) \geq 0$.

## Doubly robust estimation

$$
\hat{V}(\pi) = \frac{1}{n} \sum_{i=1}^n \left[ \frac{\mathbb{1}\{D_i = \pi(X_i)\}}{e_{\pi(X_i)}(X_i)} (Y_i - \hat{\mu}_{\pi(X_i)}(X_i)) + \hat{\mu}_{\pi(X_i)}(X_i) \right]
$$

where $\hat{\mu}_d(x) = \mathbb{E}[Y \mid X=x, D=d]$ and $e_d(x) = \mathbb{P}(D=d \mid X=x)$.

> [!tip] Policy learning
> Learn $\pi$ by maximizing estimated policy value over a class of policies (e.g., decision trees). Cross-fitting and sample splitting prevent overfitting. Alternatively, estimate CATE and assign treatment where $\hat{\tau}(x) > 0$.

## Related notes

- [[treatment effect heterogeneity]]
- [[Machine Learning for Causal Inference (MOC)]]
- [[Treatment Effect Heterogeneity (MOC)]]
