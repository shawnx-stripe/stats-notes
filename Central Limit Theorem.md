---
title: Central Limit Theorem
aliases: [Central Limit Theorem, CLT, asymptotic normality of sample mean]
tags: [statistics, inference, asymptotics]
updated: 2026-04-02
---

# Central Limit Theorem

> [!summary] Quick definition
> The Central Limit Theorem says that properly normalized averages converge in distribution to a normal law under broad conditions, which is why z-tests, t-tests, and many large-sample confidence intervals work.

## Canonical form

For iid observations with mean $\mu$ and variance $\sigma^2 < \infty$,
$$
\sqrt{n}\,\frac{\bar X_n - \mu}{\sigma} \xrightarrow{d} \mathcal{N}(0,1).
$$

## Minimal code snippets

```r
xbar <- replicate(5000, mean(rexp(200)))
hist(xbar, breaks = 50)
```

## Related notes

- [[Law of Large Numbers]] · [[Hypothesis testing]] · [[variance estimation]] · [[Standard Errors and Inference (MOC)]]
