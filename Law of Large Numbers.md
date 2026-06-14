---
title: Law of Large Numbers
aliases: [Law of Large Numbers, LLN, consistency of sample average]
tags: [statistics, inference, asymptotics]
updated: 2026-04-02
---

# Law of Large Numbers

> [!summary] Quick definition
> The Law of Large Numbers says that sample averages converge to their population expectation as the sample grows. It underpins consistency for many estimators.

## Canonical form

For iid observations with finite mean $\mu$,
$$
\bar X_n \xrightarrow{p} \mu.
$$

## Minimal code snippets

```r
x <- rexp(5000)
cum_mean <- cumsum(x) / seq_along(x)
plot(cum_mean, type = "l")
abline(h = mean(x), col = "red")
```

## Related notes

- [[Central Limit Theorem]] · [[Maximum Likelihood Estimation (MLE)]] · [[Hypothesis testing]] · [[Standard Errors and Inference (MOC)]]
