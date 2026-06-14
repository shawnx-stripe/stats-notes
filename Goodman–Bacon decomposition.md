---
title: Goodman–Bacon decomposition
aliases:
- Bacon decomposition
- Goodman-Bacon
- Goodman-Bacon decomposition
tags:
- causal-inference
- did
- diagnostics
updated: 2026-03-03
---

# Goodman–Bacon decomposition

> [!summary] Quick definition
> Shows that the [[two-way fixed effects]] (TWFE) DiD estimator with staggered treatment is a weighted average of all possible 2×2 DiD estimates comparing each pair of timing groups. Some weights can be negative when already-treated units serve as controls, leading to bias when treatment effects are heterogeneous across cohorts or over time.

---

## Core result

The TWFE coefficient $\hat\beta^{TWFE}$ can be written as:

$$
\hat\beta^{TWFE} = \sum_{k} w_k \, \hat\beta_k^{2\times2}
$$

where each $\hat\beta_k^{2\times2}$ is a canonical two-group, two-period DiD estimate and $w_k$ are data-determined weights that sum to 1 but can be **negative**.

Three types of 2×2 comparisons arise:
1. **Earlier vs. later treated** (earlier as treated, later as control) — clean
2. **Later vs. earlier treated** (later as treated, earlier as control) — problematic: uses already-treated units as "controls," and weights can be negative if effects evolve over time
3. **Treated vs. never-treated** — clean

> [!warning] When it breaks
> Negative weights on some $\hat\beta_k^{2\times2}$ mean $\hat\beta^{TWFE}$ can have the wrong sign even if every cohort-specific effect is positive. This is the core problem with TWFE under [[staggered adoption]] and [[treatment effect heterogeneity]].

---

## How to use it

The decomposition is a **diagnostic**, not an estimator. Use it to:

1. Visualize which 2×2 comparisons drive your TWFE estimate
2. Check for negative weights
3. Assess whether problematic comparisons (already-treated as controls) dominate

If the decomposition reveals problematic weights, switch to a robust estimator: [[Callaway–Sant'Anna estimator]], [[Sun–Abraham estimator]], or [[Borusyak–Jaravel–Spiess (imputation)]].

---

## Minimal code snippets

> [!example] R

```r
# install.packages("bacondecomp")
library(bacondecomp)

# df must have: unit id, time, outcome, treatment indicator (0/1)
dec <- bacon(Y ~ D, data = df, id_var = "id", time_var = "time")
print(dec)         # shows each 2x2 comparison, weight, estimate
plot(dec)          # scatter: weight vs estimate by comparison type
```

> [!example] Stata

```stata
* ssc install bacondecomp
bacondecomp Y D, ddetail
```

---

## Related notes

- [[Difference-in-Differences (DiD)]] · [[two-way fixed effects]] · [[staggered adoption]]
- [[treatment effect heterogeneity]] · [[Callaway–Sant'Anna estimator]] · [[Sun–Abraham estimator]]
- [[Causal Inference (MOC)]]
