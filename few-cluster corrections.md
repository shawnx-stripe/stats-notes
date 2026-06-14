---
title: Few-Cluster Corrections
aliases: [small-sample clustering, small G corrections, CR2, CR3, CR2 and CR3 corrections]
tags: [econometrics, inference, variance-estimation, clustering, did, panels]
updated: 2025-09-17
---

# Few-Cluster Corrections

> [!summary] Quick definition
> Methods that adjust inference when the number of clusters G is small, making vanilla [[clustered standard errors]] unreliable. Common tools include small-sample adjusted cluster-robust variances (CR2/CR3), [[wild cluster bootstrap]], and design-based [[randomization inference]].

- Why: Standard cluster-robust SEs rely on asymptotics in G. With few clusters, t-tests become too liberal and p-values too small.

## When do you need them?

- G < 50: start to worry; G < 30: strongly recommended; G < 10: use bootstrap or design-based inference.
- Very few treated clusters (e.g., ≤ 10 treated states) even if total G is moderate.
- Highly unbalanced cluster sizes or high cluster leverage (many covariates relative to G).
- Serial correlation and policy assignment at the cluster level in [[Difference-in-Differences (DiD)]] and [[two-way fixed effects]].

> [!warning] Classic caution
> See [[Bertrand–Duflo–Mullainathan (2004)]] for the dangers of serial correlation in DiD with inadequate clustering.

## Main approaches

### 1) Small-sample adjusted CRVEs (CR2/CR3)

- Idea: Modify the sandwich variance and degrees of freedom to account for small G.
- CR2 (a.k.a. Bell–McCaffrey/Satterthwaite-type) and CR3 (HC3 analog) tend to yield better Type I error with few clusters and unbalanced designs.
- Use Satterthwaite d.f. for tests:
  - Conceptually, replace large-sample t with t(df_eff), where df_eff is computed from cluster-level influence contributions.
- Pros: Simple, fast, works with most linear models.
- Cons: Still asymptotic; accuracy can degrade when G is very small (single digits).

See also: [[Bell–McCaffrey]], [[Satterthwaite correction]], clubSandwich.

### 2) Wild cluster bootstrap (WCB)

- Algorithm: Recompute the test statistic many times after multiplying cluster-level residuals by random weights (e.g., Rademacher ±1, or Webb’s six-point).
- Returns bootstrap p-values for H0: β = β0.
- Pros: Works well with few and unbalanced clusters; handles heteroskedasticity and within-cluster correlation.
- Cons: Computational; requires careful implementation (restricted vs. unrestricted bootstrap, choice of weights).
- Variants: Rademacher is standard; Webb weights useful with few time periods per cluster.

See: [[wild cluster bootstrap]], [[Rademacher weights]], [[Webb weights]].

### 3) Design-based randomization inference

- If you know/assume the assignment mechanism (e.g., policy randomized across clusters), compute the distribution of the statistic under reassignments consistent with the design.
- Pros: Exact under the design; robust with very few clusters.
- Cons: Requires a credible assignment model; often tests sharp nulls.
- Useful complements: [[randomization inference|permutation test]]s over clusters or placebo policy dates.

See: [[randomization inference]].

### 4) Ibragimov–Müller t-test (cluster means)

- Collapse data to cluster-level estimates, run OLS across clusters, and use a t-test with df = G − 1 (or G − k).
- Very conservative but simple and robust.
- Works best when the estimand can be computed per cluster (e.g., cluster-level DiD contrasts).

See: [[Ibragimov–Müller]].

## Choosing among methods

- G ≥ 30 and balanced: CR2 often adequate; report number of clusters.
- 10 ≤ G < 30 or very unbalanced: prefer WCB; report CR2 as robustness.
- G < 10 or very few treated clusters: WCB and/or randomization inference; IM test as a conservative check.
- Always report the number of clusters and number of treated clusters.

## Practical guidance

> [!check] Checklist
> - [ ] State cluster level and counts (total and treated).
> - [ ] Use CR2/CR3 or WCB when G < 30, and almost surely when G < 10.
> - [ ] If assignment is known, add design-based randomization inference.
> - [ ] Show robustness across methods (CR2, WCB, IM).
> - [ ] Beware of multiway clustering with small G in any dimension; consider dimension reduction or WCB variants.

> [!warning] Pitfalls
> - Reporting only conventional cluster-robust SEs with G small.
> - Bootstrapping at the observation level instead of the cluster level.
> - Ignoring that few treated clusters can drive over-rejection even if total G is moderate.
> - Treating clustering fixes as a remedy for bias from [[interference]]/[[No spillovers]] violations (they don’t).

## Minimal code snippets

> [!example] R: CR2/CR3 and wild cluster bootstrap

```r
# Model (fixest example)
library(fixest)
est <- feols(Y ~ D:Post | id + time, data = df, cluster = ~state)

# CR2 with clubSandwich
library(clubSandwich)
V_cr2 <- vcovCR(est, type = "CR2", cluster = df$state)
clubSandwich::coef_test(est, vcov = V_cr2, test = "Satterthwaite")

# Wild cluster bootstrap (fwildclusterboot)
# install.packages("fwildclusterboot")
library(fwildclusterboot)
boottest(est, param = "D:Post", clustid = ~state, B = 9999,
         bootstrap_type = "wild", type = "rademacher")  # or type = "webb"
```

> [!example] Stata: CR2-like and boottest

```stata
* TWFE with cluster-robust SEs
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster state)

* Wild cluster bootstrap p-value (Roodman et al.)
* ssc install boottest
boottest c.Post#1.D, cluster(state) reps(9999) rademacher
* Option: webb weights for short panels
boottest c.Post#1.D, cluster(state) reps(9999) webb
```

> [!example] Python: linearmodels + wild cluster bootstrap (sketch)

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + EntityEffects + TimeEffects', data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)  # baseline clustered

# Wild cluster bootstrap (using wildboottest package, if installed)
# pip install wildboottest
from wildboottest.wildboottest import boottest
bt = boottest(res, param='D:Post', cluster=df.reset_index()['state'], B=9999, weights='rademacher')
print(bt)
```

> [!example] Ibragimov–Müller across clusters (R sketch)

```r
# Compute cluster-level estimates (e.g., per-state DiD contrasts) -> data.frame 'by_state'
# by_state has columns: state, beta_hat_state
im <- lm(beta_hat_state ~ 1, data = by_state)
summary(im)  # t-test with df = G - 1
```

> [!example] Randomization inference (cluster permutations; sketch in R)

```r
set.seed(123)
G <- length(unique(df$state))
B <- 5000
t_obs <- coef(est)['D:Post']

t_null <- replicate(B, {
  perm <- sample(unique(df$state))
  df_perm <- within(df, {
    state_perm <- match(state, unique(state))
    D_perm <- D[match(perm[state_perm], unique(state))]
  })
  est_b <- feols(Y ~ D_perm:Post | id + time, data = df_perm, cluster = ~state)
  coef(est_b)['D_perm:Post']
})

p_val <- mean(abs(t_null) >= abs(t_obs))
```

## Copy-ready snippets

- Satterthwaite idea (conceptual): replace large-sample t by t with effective d.f.
$$
t_{\text{CR2}} = \frac{\hat\beta - \beta_0}{\sqrt{\widehat{\mathrm{Var}}_{\text{CR2}}(\hat\beta)}},\quad
t_{\text{CR2}} \sim t(\text{df}_\text{eff})
$$

- Wild cluster bootstrap p-value:
$$
p = \Pr^\ast\big(|t^\ast| \ge |t_{\text{obs}}|\big)
$$
where t* are bootstrap statistics under random cluster weights.

## Reporting essentials

- Number of clusters (total and treated), clustering level(s), and why.
- Which correction(s) you used (CR2/CR3, WCB with weight type, randomization inference).
- Number of bootstrap repetitions; whether tests are one- or two-sided.
- Sensitivity across methods and alternative cluster definitions if plausible.

---

Related notes to create:
- [[clustered standard errors]]
- [[Difference-in-Differences (DiD)]]
- [[two-way fixed effects]]
- [[wild cluster bootstrap]]
- [[Bell–McCaffrey]]
- [[Satterthwaite correction]]
- clubSandwich
- [[Ibragimov–Müller]]
- [[randomization inference]]
- [[randomization inference|permutation test]]
- [[Rademacher weights]]
- [[Webb weights]]
- [[Bertrand–Duflo–Mullainathan (2004)]]
- [[Conley standard errors]]
- [[clustering]]
