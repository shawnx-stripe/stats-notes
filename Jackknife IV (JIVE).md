---
title: Jackknife IV (JIVE)
aliases: [JIVE, Jackknife IV, jackknife instrumental variables estimator]
tags: [econometrics, iv, weak-instruments, estimation]
updated: 2026-03-05
---

# Jackknife IV (JIVE)

> [!summary]
> IV estimator that uses leave-one-out predicted values from the first stage to construct instruments, reducing the many-instruments bias of [[Two-Stage Least Squares (2SLS)|2SLS]]. Consistent even when the number of instruments grows with sample size.

## Procedure

Standard 2SLS uses fitted values $\hat{X}_i = Z_i \hat{\Pi}$ in the second stage. JIVE replaces this with leave-one-out fitted values:

$$
\hat{X}_{i}^{(-i)} = Z_i \hat{\Pi}^{(-i)}
$$

where $\hat{\Pi}^{(-i)}$ is estimated excluding observation $i$. This removes the $O(m/n)$ bias when $m$ (number of instruments) grows with $n$.

> [!check] When to Use
> - **Many instruments**: When $m/n$ is not negligible (e.g., $m > 30$ or $m/n > 0.1$)
> - **Weak instruments**: JIVE has better finite-sample properties than 2SLS in some weak-IV settings
> - **Valid instruments**: Does not address weak or invalid instruments; still requires [[relevance]] and [[exclusion restriction]]

Alternatives: [[Limited Information Maximum Likelihood (LIML)|LIML]], [[Fuller estimator]] (better for weak instruments).

## Code

```r
# R: JIVE via ivreg
library(ivreg)
mod <- ivreg(y ~ x | z1 + z2 + ..., method = "jive")
```

## Related notes

- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Fuller estimator]]
- [[weak instruments]]
- [[Instrumental Variables (IV)]]
