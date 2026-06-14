---
title: randomization inference
aliases:
- Randomization inference
- randomization test
- permutation test
- Fisher exact test
- design-based inference
- RI
- permutation inference
- Permutation test
tags:
- experimentation
- inference
- randomization
- permutation
- cluster
- few-cluster
- design
- saturation
- switchback
- scm
updated: 2025-09-17
---

# randomization inference

> [!summary] Quick definition
> Randomization inference (RI) evaluates hypotheses by comparing the observed test statistic to its distribution under all (or many) treatment assignments consistent with the known randomization mechanism. It is exact under the design, does not rely on large-sample approximations, and is especially useful with few clusters or complex designs (blocking, clustering, saturation, switchback).

- Core idea: hold outcomes fixed; reassign treatment according to the actual randomization protocol; recompute the test statistic; obtain a design-based p-value.
- Complements: [[wild cluster bootstrap]] and asymptotic methods; often preferred when clusters are few.

---

## When to use

> [!tip] Good fit
> - Known randomization scheme (complete, stratified/blocked, matched-pairs, cluster, stepped-wedge, two-stage saturation, [[switchback experiment]])
> - Few clusters or small N, where asymptotics are unreliable
> - Need design-based p-values or confidence intervals

> [!warning] RI requires a credible, specified assignment mechanism. For observational designs (e.g., standard DiD) RI applies only if “as-if randomization” is defensible and the assignment mechanism is modeled.

---

## Setup and hypotheses

- Data: outcomes Y, covariates X (optional), observed assignment Z_obs, and the set Ω of assignments consistent with the design (e.g., all K-of-N assignments; all matched-pair flips; all cluster reassignments within blocks).
- Test statistic T(Z, Y, X): difference-in-means, regression coefficient, studentized t, rank statistic, KS, SCM gap, etc.
- Hypotheses:
  - Fisher sharp null: H0: Y_i(1) = Y_i(0) for all i (no unit-level effect).
  - Weak/Average nulls: H0: ATE = 0 (can be approximated via studentized statistics or by inverting models).

---

## Algorithm (generic)

1) Compute observed statistic: t_obs = T(Z_obs, Y, X).
2) Generate B assignments Z^(b) ∈ Ω by re-randomizing according to the actual design (respecting blocks/matched pairs/clusters/time blocks/saturation levels).
3) For each b = 1..B, compute t^(b) = T(Z^(b), Y, X).
4) Two-sided p-value:
$$
p = \frac{1 + \sum_{b=1}^B \mathbf{1}\{|t^{(b)}| \ge |t_{obs}|\}}{B + 1}.
$$
5) Confidence intervals: invert the test by finding treatment effect values that are not rejected (e.g., subtract candidate τ from treated outcomes and repeat RI).

> [!tip] Studentization
> Use studentized or regression-based statistics (e.g., t-statistics) to improve finite-sample performance under heteroskedasticity or effect heterogeneity.

---

## Designs and how to permute

- Completely randomized (CRD; K treated of N): sample K treated labels without replacement.
- Bernoulli (coin-flip) randomization: draw Z_i ∼ Bernoulli(p) independently.
- Blocked/stratified: permute within blocks; keep totals per block fixed.
- Matched pairs: swap labels within each pair; number of assignments is 2^(#pairs).
- Cluster randomized: permute treatment across clusters; keep cluster counts fixed; all units in cluster inherit cluster label.
- Stepped-wedge / staggered cluster: permute the calendar of which clusters switch at which times consistent with the rollout protocol (often within cohort strata).
- Two-stage [[randomized saturation design]]: permute cluster-level saturation labels; within each cluster permute individual treatment consistent with assigned saturation.
- [[switchback experiment]] (time-sliced): permute treatment labels across time blocks (and across shards/geos if applicable) respecting block design and washouts.
- Synthetic control placebos (“in-space”): treat each donor as if treated; compare treated post/pre gap to placebo distribution (RI spirit).

---

## Choice of test statistic

- Difference in means (simple, nonparametric)
- Regression coefficient (e.g., from OLS/FE model) and its t-statistic
- Rank-based or sign tests (robust to outliers)
- Event-study statistics (joint tests over selected leads/lags)
- SCM post/pre RMSPE ratio or average post gap
- Studentized statistics often recommended for weak nulls (ATE=0) approximation

> [!warning] Always compute the statistic exactly the same way under observed and permuted assignments.

---

## Sharp vs weak nulls and CIs

- Fisher sharp null (no effect on any unit) yields exact finite-sample p-values.
- Weak null (ATE=0) can be approximated with studentization or by imposing constant effects (Y_i(1)=Y_i(0)+τ) and inverting across τ to form a confidence interval (“Hodges–Lehmann”-style).
- In clusters, invert at the cluster-aggregated level (means/differences) to obtain design-based CIs.

---

## Relationship to clustered/few-cluster settings

- With few clusters, RI provides valid design-based tests by reassigning at the cluster level (or cluster-pair).
- Complement or cross-check [[wild cluster bootstrap]] results; report both when feasible.

---

## Interference and exposure

- Under partial interference (e.g., within-cluster spillovers), define exposure mapping E_i(Z) and test hypotheses about direct/indirect effects by permuting Z consistent with the saturation/exposure design (Hudgens–Halloran framework).
- For [[randomized saturation design]], test direct effects at a given saturation by permuting individual assignments within clusters at fixed saturation; test spillovers by permuting cluster saturation labels.

---

## Code examples

> [!example] R: complete randomization (difference-in-means)

```r
set.seed(1)
Y <- df$Y
Z <- df$Z            # observed assignment (0/1)
K <- sum(Z); N <- length(Z)
t_obs <- mean(Y[Z==1]) - mean(Y[Z==0])

B <- 5000
t_sim <- numeric(B)
for (b in 1:B) {
  Zb <- rep(0, N)
  Zb[sample.int(N, K, replace = FALSE)] <- 1
  t_sim[b] <- mean(Y[Zb==1]) - mean(Y[Zb==0])
}
pval <- (1 + sum(abs(t_sim) >= abs(t_obs))) / (B + 1)
c(t_obs = t_obs, p = pval)
```

> [!example] R: blocked randomization (permute within blocks)

```r
t_stat <- function(Z, Y, block) {
  # weighted diff-in-means across blocks
  sum(tapply(Y*Z, block, sum)/tapply(Z, block, sum) * (tapply(Z, block, sum)>0) -
      tapply(Y*(1-Z), block, sum)/tapply(1-Z, block, sum) * (tapply(1-Z, block, sum)>0),
      na.rm = TRUE)
}
block <- df$block
Z <- df$Z; Y <- df$Y
t_obs <- t_stat(Z, Y, block)
B <- 5000; t_sim <- numeric(B)
for (b in 1:B) {
  Zb <- unlist(tapply(Z, block, function(z) sample(z))) # permute labels within each block
  t_sim[b] <- t_stat(Zb, Y, block)
}
pval <- (1 + sum(abs(t_sim) >= abs(t_obs))) / (B + 1)
```

> [!example] R: cluster-randomized (permute at cluster level; regression t-stat)

```r
library(lmtest); library(sandwich)
cluster <- df$cluster
Zc <- aggregate(Z ~ cluster, df, mean)   # cluster assignment (0/1)
Zc$Z <- as.integer(Zc$Z > 0.5)

t_obs <- coeftest(lm(Y ~ Z, data = merge(df, Zc, by="cluster")),
                  vcov = vcovCL, cluster = ~ cluster)["Z","t value"]

B <- 5000; t_sim <- numeric(B)
for (b in 1:B) {
  Zc_perm <- Zc; Zc_perm$Z <- sample(Zc$Z)    # permute cluster labels
  t_sim[b] <- coeftest(lm(Y ~ Z, data = merge(df, Zc_perm, by="cluster")),
                       vcov = vcovCL, cluster = ~ cluster)["Z","t value"]
}
pval <- (1 + sum(abs(t_sim) >= abs(t_obs))) / (B + 1)
```

> [!example] Stata: `ritest` (cluster-level)

```stata
* Install ritest if needed: ssc install ritest
* Example: cluster-randomized, test coefficient on Z using permutation of cluster assignment
ritest Z _b[Z], cluster(cluster) reps(5000): reg Y Z X1 X2, vce(cluster cluster)
```

> [!example] Python: blocked permutation (difference-in-means)

```python
import numpy as np

def permute_blocked(Z, blocks, rng):
    Zb = Z.copy()
    for b in np.unique(blocks):
        idx = np.where(blocks == b)[0]
        Zb[idx] = rng.permutation(Z[idx])
    return Zb

rng = np.random.default_rng(1)
Y = df['Y'].to_numpy()
Z = df['Z'].to_numpy()
block = df['block'].to_numpy()

t_obs = Y[Z==1].mean() - Y[Z==0].mean()
B = 5000
t_sim = np.empty(B)
for b in range(B):
    Zb = permute_blocked(Z, block, rng)
    t_sim[b] = Y[Zb==1].mean() - Y[Zb==0].mean()
pval = (1 + np.sum(np.abs(t_sim) >= np.abs(t_obs))) / (B + 1)
```

---

## Design-specific notes

- Matched pairs: the exact test flips treatment within each pair; p-values can be computed analytically or via 2^P enumeration.
- Cluster-pair designs: flip assignment within each pair of clusters; use pair-mean differences as the statistic.
- Stepped-wedge: randomize the order of cluster switchovers; test uses permutations of cohort labels.
- Two-stage saturation: permute cluster saturation labels; within cluster, permute individual assignments consistent with saturation; test direct and spillover effects separately (see [[randomized saturation design]]).
- SCM (synthetic control): in-space “placebo” tests treat each donor as if treated—this is RI in spirit; the treated gap’s rank among placebos yields a permutation p-value.

---

## Advantages and limitations

> [!tip] Advantages
> - Exact (finite-sample) under the design; valid with few clusters  
> - Minimal modeling assumptions; aligns inference with the randomization itself  
> - Flexible statistics (including regression/studentized tests)

> [!warning] Limitations
> - Requires known assignment mechanism and no post-randomization deviations (or must be modeled)  
> - Sharp-null focus; weak-null tests need studentization or inversion  
> - Computationally intensive for large Ω (use Monte Carlo with B ≫ 1000)

---

## Diagnostics and good practice

> [!check]
> - [ ] Verify the permutation scheme matches the actual design (blocks, cluster counts, time blocks)  
> - [ ] Use studentized statistics for heteroskedasticity/weak-null robustness  
> - [ ] Use enough reps (e.g., B≥5000; larger for tail accuracy); report seed and CI of p-value if needed  
> - [ ] For few clusters, complement with [[wild cluster bootstrap]] and report both  
> - [ ] For designs with possible cross-cluster spillovers, consider [[Conley standard errors]] as robustness and widen buffers

---

## Reporting essentials

- Assignment mechanism (CRD, blocked, matched pairs, cluster, stepped-wedge, saturation, switchback)
- Test statistic definition and whether studentized/regression-based
- Number of permutations B (or exact enumeration), random seed
- Two-sided/one-sided p-values; CI construction method (if any)
- Handling of clustering/blocks/time; any deviations from planned randomization
- Sensitivity: alternative statistics, blocking definitions, and results

---

## Common pitfalls

> [!warning]
> - Permuting labels in a way that violates the design (e.g., breaking block sizes or cluster counts)  
> - Using iid residuals/statistics that ignore clustering when design is clustered  
> - Too few permutations (noisy p-values)  
> - Treating RI as a cure-all for identification issues (e.g., spillovers, noncompliance)  
> - Mixing ITT and as-treated without modeling the assignment and compliance

---

## Related notes

- [[wild cluster bootstrap]] · [[few-cluster corrections]] · [[clustered standard errors]]  
- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]] · [[randomized saturation design]] · [[switchback experiment]] · [[geo experiment]]  
- [[Synthetic Control]] (placebo inference)  
- [[sequential testing]] (distinct but complementary for online monitoring)

---