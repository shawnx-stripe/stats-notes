---
title: Clustered Standard Errors
aliases: [Clustered standard errors, cluster-robust SEs, CRSE, CRVE]
tags: [econometrics, inference, did, panels, regression, variance-estimation]
updated: 2025-09-17
---

# Clustered Standard Errors

> [!summary] Quick definition
> Clustered standard errors adjust inference when regression residuals are correlated within groups (clusters), such as units over time or observations within regions/firms. They are essential in [[Difference-in-Differences (DiD)]] and panel models with serial or group-level correlation.

- Core idea: allow arbitrary correlation within clusters and independence across clusters.
- Typical clusters: unit (serial correlation), geography (state/county), firm, classroom, market, or time.

## When to use

- Treatment is assigned at a cluster level (e.g., policy by state): cluster at that level.
- Serial correlation in panels (repeated measures per unit): cluster by unit.
- Common shocks by time and cross-sectional correlation: consider two-way clustering (e.g., unit and time).
- Aggregated regressors measured at a higher level than the observation (the [[Moulton problem]]).

> [!warning] Classic result
> In DiD and panels, ignoring within-unit serial correlation severely overstates significance (see [[Bertrand–Duflo–Mullainathan (2004)]]).

## What is a cluster-robust variance?

For OLS with regressor matrix X and residuals u, the cluster-robust (CR1) “sandwich” variance is:
$$
\widehat{\mathrm{Var}}(\hat\beta)
= (X'X)^{-1}\left(\sum_{g=1}^{G} X_g' \hat u_g \hat u_g' X_g\right)(X'X)^{-1} \times \text{adj}
$$
- g indexes clusters; $X_g$ and $\hat u_g$ stack observations in cluster g.
- “adj” is a finite-sample correction (e.g., $G/(G-1)\cdot (N-1)/(N-K)$).

> [!tip] Terminology
> - CR1: basic cluster-robust (aka Liang–Zeger).
> - CR2/CR3: small-sample improved (e.g., [[Bell–McCaffrey]]/Satterthwaite adjustments). See [[few-cluster corrections]].

## Choosing the clustering level

- General rule: cluster at the level of the most persistent, policy-relevant error correlation and at the treatment assignment level.
- Examples:
  - State-level policy with county outcomes: cluster by state.
  - Firm-level shock with worker outcomes: cluster by firm (and possibly by time if macro shocks matter).
  - DiD panel by states over years: cluster by state; consider two-way clustering by state and year if cross-sectional correlation via common shocks is strong.
- If multiple plausible dimensions matter, use multiway clustering (e.g., [[Cameron–Gelbach–Miller]]).

## Few clusters problem

- CRSEs rely on asymptotics in the number of clusters G. With few clusters, t-tests can be too liberal.
- Rules of thumb:
  - G ≥ 50: usually fine.
  - 30 ≤ G < 50: some caution.
  - G < 30: prefer [[few-cluster corrections]].
  - Very few treated clusters (e.g., ≤ 10): use wild cluster bootstrap or randomization inference.

### Remedies
- Wild cluster bootstrap-t (Rademacher or Webb weights) on the test statistic.
- CR2/CR3 with Satterthwaite d.f. (clubSandwich/CR2).
- Permutation/randomization inference if assignment is known and clustered.
- [[Ibragimov–Müller]] t-tests using cluster means (very conservative, needs enough clusters).

## Two-way and multiway clustering

- Two-way: allow correlation within entities and within time (or other second dimension).
- Estimators are available for two- and multiway clustering; ensure clusters are not perfectly nested unless the software supports it.
- If one dimension clearly dominates correlation, single-way clustering at that level may suffice.

## The Moulton problem (intuition)

- If a regressor varies only at a higher level (e.g., policy at state level) but outcomes are at a lower level (individuals), naive SEs are too small.
- Inflation factor (simple case):
$$
\text{Var}(\hat\beta) \propto 1 + (\bar{n}-1)\rho
$$
where $\bar{n}$ is average cluster size and ρ is intra-cluster error correlation. Clustering addresses this.

## Practical guidance

> [!check] Checklist
> - [ ] Identify assignment level and main correlation source; set cluster(s) accordingly.
> - [ ] Report number of clusters and, in DiD, number of treated clusters.
> - [ ] If G is small, apply small-sample corrections (CR2) or wild cluster bootstrap.
> - [ ] Consider multiway clustering when both entity and time (or geography) induce correlation.
> - [ ] For spatial decay rather than discrete clusters, consider [[Conley standard errors]] (spatial HAC).

> [!warning] Common pitfalls
> - Clustering at too fine a level (e.g., individual) when treatment is at state level.
> - Treating clustering as a cure for bias from [[interference]]/[[No spillovers]] violations (it only fixes SEs, not bias).
> - Not reporting clusters count or mixing specifications with different clustering without explanation.

## Minimal code snippets

> [!example] R

```r
# TWFE DiD with clustering in fixest
library(fixest)
est <- feols(Y ~ D:Post | id + time, data = df, cluster = ~id)   # cluster by entity
etable(est)

# Two-way clustering (entity and time)
est2 <- feols(Y ~ D:Post | id + time, data = df, cluster = ~id + time)

# CR2 (small-sample) with clubSandwich
library(clubSandwich)
vc <- vcovCR(est, type = "CR2", cluster = df$id)
coef_test(est, vcov = vc, test = "Satterthwaite")

# Wild cluster bootstrap (fwildclusterboot)
# install.packages("fwildclusterboot")
library(fwildclusterboot)
boottest(est, param = "D:Post", clustid = ~id, B = 9999, bootstrap_type = "wild", type = "rademacher")
```

> [!example] Stata

```stata
* TWFE with cluster-robust SEs
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)

* Two-way clustering (entity and time)
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id time)

* Wild cluster bootstrap for a coefficient (boottest)
* ssc install boottest
boottest c.Post#1.D, cluster(id) bootcluster(id) reps(9999) rademacher
```

> [!example] Python (linearmodels)

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + EntityEffects + TimeEffects', data=df)

# Cluster by entity
res1 = mod.fit(cov_type='clustered', cluster_entity=True)

# Two-way clustering by entity and time
res2 = mod.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)

print(res2.summary)
```

## Reporting essentials

- State clearly: clustering level(s), number of clusters, and rationale (assignment level, correlation source).
- For DiD: report treated vs. control cluster counts; if few treated clusters, note bootstrap or CR2 method used.
- If multiway clustering: list all dimensions and software used.
- Provide robustness using alternative clustering choices when plausible (e.g., geography vs. entity).

## Copy-ready snippets

- Cluster-robust variance:
$$
\widehat{\mathrm{Var}}(\hat\beta)
= (X'X)^{-1}\left(\sum_{g=1}^{G} X_g' \hat u_g \hat u_g' X_g\right)(X'X)^{-1}
$$

- Moulton inflation (intuition):
$$
1 + (\bar{n}-1)\rho
$$

---

## Related notes
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[pre-trends]]
- [[event study]]
- [[few-cluster corrections]]
- [[Moulton problem]]
- [[Cameron–Gelbach–Miller]]
- [[Bertrand–Duflo–Mullainathan (2004)]]
- [[Conley standard errors]]
- [[No spillovers]]
- [[interference]]
- [[clustering]]
