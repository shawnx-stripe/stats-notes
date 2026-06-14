---
title: Manipulation Test
aliases: [manipulation test, sorting test, bunching test]
tags: [econometrics, rdd, diagnostics]
updated: 2026-03-05
---

# Manipulation Test

> [!summary]
> Test for strategic sorting around the RDD cutoff. If units can manipulate the [[running variable]], the local randomization assumption fails. [[McCrary test]] (density discontinuity) and [[rddensity]] are standard implementations.

## Why it matters

If units manipulate $R_i$ to cross the cutoff, then $R_i \approx c$ is **not** as-good-as-random. This invalidates the RDD identifying assumption:
$$
\mathbb{E}[Y_i(0) \mid R_i = r] \text{ and } \mathbb{E}[Y_i(1) \mid R_i = r] \text{ continuous at } r = c
$$

**Test**: Look for a discontinuity in the density $f(r)$ at $c$.

> [!warning]
> Manipulation is likely when:
> - Agents have incentive to cross the cutoff (e.g., exam retaking, grant eligibility)
> - The running variable is self-reported or under agent control
> - Enforcement of the cutoff is weak

## Minimal code snippets

```r
# R: McCrary density test
library(rdd)
DCdensity(df$running_var, cutpoint = 0, plot = TRUE)

# R: modern rddensity implementation
library(rddensity)
dens <- rddensity(df$running_var, c = 0)
summary(dens)
plot(dens)
```

```python
# Python: rddensity via rdrobust
# (requires R backend via rpy2, or use rdrobust CLI)
import subprocess
subprocess.run(["rdrobust", "--density", "running_var", "--cutoff", "0"], check=True)
```

```stata
* Stata: McCrary test
DCdensity running_var, breakpoint(0) generate(Xj Yj r0 fhat se_fhat)
```

## Related notes

- [[McCrary test]]
- [[density test]]
- [[rddensity]]
- [[Regression Discontinuity Design (RDD)]]
