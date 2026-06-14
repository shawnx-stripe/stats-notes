---
title: Clustering
aliases: [cluster structure, cluster choice, clustering level]
tags: [econometrics, inference, variance-estimation, did, panels, robustness]
updated: 2025-09-17
---

# Clustering

> [!summary] Quick definition
> In regression inference, “clustering” refers to how you group observations for variance estimation so that error terms may be arbitrarily correlated within each group (cluster) but are independent across clusters. Choosing the correct clustering level is crucial for valid standard errors; see [[clustered standard errors]].

- Typical clusters: units over time (serial correlation), geographic areas (states, firms, schools), time periods, markets, or assignment groups.
- Especially important in [[Difference-in-Differences (DiD)]], panels, and settings with regressors measured at higher aggregation (the [[Moulton problem]]).

## Why and when to cluster

- Serial correlation within units over time (panel data).
- Group-level shocks (e.g., state-year policies) causing correlated errors within groups.
- Treatment assigned at a cluster level (policy by state, program by school).
- Regressors vary only at a higher level than the observation (Moulton).
- Sampling designs with clustered sampling.

> [!warning] Consequence of ignoring clustering
> Biases in standard errors (often downward), leading to overstated significance; see [[Bertrand–Duflo–Mullainathan (2004)]].

## Choosing the clustering level

- General rule: cluster at the level of the most persistent and policy-relevant error correlation and at the treatment-assignment level.
- Examples:
  - State-level policy with county outcomes → cluster by state.
  - Firm-level shocks with worker outcomes → cluster by firm (and consider time if common macro shocks).
  - DiD panel of states over years → cluster by state; consider two-way (state and year) if strong cross-sectional correlation via time shocks.
- If multiple plausible dimensions matter, use multiway clustering (e.g., [[Cameron–Gelbach–Miller]]).

> [!tip] Nested structures
> If regressors vary only at a higher level (e.g., state), clustering at a lower level (e.g., county) is invalid. Cluster at the highest level at which the regressor varies.

## One-way, two-way, and multiway clustering

- One-way: allow arbitrary correlation within one dimension (e.g., unit).
- Two-way: allow correlation within two dimensions (e.g., unit and time).
- Multiway: generalization to more than two dimensions.
- Implementations typically combine single-dimension cluster-robust covariances and correct for double-counting (CGM method).

See also: [[clustered standard errors]] and [[few-cluster corrections]].

## Few clusters problem

- With a small number of clusters G, conventional cluster-robust SEs can over-reject.
- Remedies: [[few-cluster corrections]] such as CR2/CR3 (Satterthwaite d.f.) or [[wild cluster bootstrap]]; design-based [[randomization inference]] when applicable.
- Always report number of clusters and number of treated clusters in DiD.

## Clustering vs. HAC/spatial correlation

- If correlation decays with distance rather than occurring in discrete clusters, consider [[Conley standard errors]] (spatial HAC) or Driscoll–Kraay for panel cross-sectional dependence.
- HAC does not fix bias from contaminated controls or [[interference]]; it only addresses correlation in errors.

## The Moulton problem (intuition)

- When a regressor varies only at the cluster level, naive SEs (even heteroskedastic-robust) are too small due to intra-cluster correlation. Clustering at that aggregation level corrects this.

## Practical checklist

> [!check] Clustering decisions
> - [ ] Identify assignment level and dominant correlation sources.
> - [ ] Choose cluster level(s) accordingly; avoid clustering below regressor variation level.
> - [ ] Report number of clusters and, for DiD, treated-cluster counts.
> - [ ] If G < 30 (or few treated clusters), use [[few-cluster corrections]].
> - [ ] Consider two-way/multiway clustering when both unit and time (or other) dimensions induce correlation.
> - [ ] For spatial dependence, consider [[Conley standard errors]].

> [!warning] Common pitfalls
> - Clustering at too fine a level (e.g., individual) when treatment varies by state.
> - Using observation-level bootstrap instead of cluster-level bootstrap.
> - Not reporting cluster counts or changing clustering across specs without explanation.
> - Treating clustering as a fix for bias from [[spillovers]]/[[No spillovers]] violations.

## Minimal code snippets

> [!example] R

```r
# TWFE DiD with clustering (fixest)
library(fixest)
est1 <- feols(Y ~ D:Post | id + time, data = df, cluster = ~id)          # 1-way
est2 <- feols(Y ~ D:Post | id + time, data = df, cluster = ~id + time)   # 2-way

# Small-sample correction CR2 with clubSandwich
library(clubSandwich)
V_cr2 <- vcovCR(est1, type = "CR2", cluster = df$id)
clubSandwich::coef_test(est1, vcov = V_cr2, test = "Satterthwaite")

# Wild cluster bootstrap (fwildclusterboot)
library(fwildclusterboot)
boottest(est1, param = "D:Post", clustid = ~id, B = 9999,
         bootstrap_type = "wild", type = "rademacher")
```

> [!example] Stata

```stata
* One-way and two-way clustering with reghdfe
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id time)

* Wild cluster bootstrap (Roodman et al.)
* ssc install boottest
boottest c.Post#1.D, cluster(id) reps(9999) rademacher
```

> [!example] Python (linearmodels)

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + EntityEffects + TimeEffects', data=df)

# One-way clustering (by entity)
res1 = mod.fit(cov_type='clustered', cluster_entity=True)

# Two-way clustering (entity and time)
res2 = mod.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)
print(res2.summary)
```

## Reporting essentials

- Cluster level(s) used and rationale (assignment level, correlation source).
- Number of clusters (and number treated in DiD).
- Whether small-sample corrections or wild cluster bootstrap were applied.
- For multiway clustering, list all dimensions.
- If using spatial HAC/Conley, report cutoff distance and kernel choices.

## Copy-ready snippets

- Cluster-robust “sandwich” form (one-way; g indexes clusters):
$$
\widehat{\mathrm{Var}}(\hat\beta)
= (X'X)^{-1}\Big(\sum_{g=1}^{G} X_g' \hat u_g \hat u_g' X_g\Big)(X'X)^{-1}.
$$

- Heuristic for Moulton inflation (simple case):
$$
\text{Inflation} \approx 1 + (\bar n - 1)\rho,
$$
with $\bar n$ average cluster size and $\rho$ intra-cluster correlation.

---

Related notes to create:
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[wild cluster bootstrap]]
- [[Cameron–Gelbach–Miller]]
- [[Conley standard errors]]
- [[Moulton problem]]
- [[Bertrand–Duflo–Mullainathan (2004)]]
- [[Difference-in-Differences (DiD)]]
- [[two-way fixed effects]]
- [[spillovers]]
- [[No spillovers]]
- [[interference]]
