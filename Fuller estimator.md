---
title: Fuller Estimator
aliases: [Fuller estimator, Fuller k-class, Fuller modification]
tags: [econometrics, iv, weak-instruments, estimation]
updated: 2026-03-05
---

# Fuller Estimator

> [!summary]
> Modified LIML estimator that subtracts a small constant (typically 1 or 4) from the LIML k-statistic, yielding finite moments and better small-sample properties under [[weak instruments]].

## Formula

The Fuller(α) estimator modifies the [[Limited Information Maximum Likelihood (LIML)|LIML]] k-statistic:

$$
\hat{\beta}_{\text{Fuller}} = \hat{\beta}_{\text{2SLS}} + \left(\hat{k}_{\text{LIML}} - \alpha \right) \left(\hat{\beta}_{\text{LIML}} - \hat{\beta}_{\text{2SLS}}\right)
$$

where $\hat{k}_{\text{LIML}}$ is the smallest eigenvalue from LIML, and $\alpha \in \{1, 4\}$ (Fuller recommends $\alpha=1$ for moderate sample sizes).

## When to Use

- **Weak instruments**: Fuller dominates 2SLS in bias when instruments are weak
- **Small samples**: Fuller(1) provides finite moments while LIML does not
- **Many instruments**: Offers better properties than 2SLS with large instrument counts
- Particularly useful when first-stage F-statistic is below 10 but you need point estimates (not just bounds)

## Code

```r
# R: ivreg with Fuller(1)
library(ivreg)
mod <- ivreg(y ~ x | z1 + z2 + z3, method = "fuller", fuller = 1)
```

## Related notes

- [[Limited Information Maximum Likelihood (LIML)|LIML]]
- [[Two-Stage Least Squares (2SLS)|2SLS]]
- [[weak instruments]]
- [[Instrumental Variables (IV)]]
- [[k-class estimator]]
