---
title: wild cluster bootstrap
aliases: [Wild cluster bootstrap, wild cluster bootstrap-t, WCB, wild cluster bootstrap t, boottest, wild bootstrap, wild cluster]
tags: [econometrics, inference, clustering, few-cluster, bootstrap, did, panels]
updated: 2025-09-17
---

# wild cluster bootstrap

> [!summary] Quick definition
> The wild cluster bootstrap (WCB) is a resampling method for hypothesis testing and confidence intervals in regressions with clustered errors, especially when the number of clusters is small (few G). It reweights cluster-level residuals with random weights (e.g., Rademacher or Webb) to approximate the sampling distribution of test statistics under the null, providing more reliable p-values than conventional cluster-robust SEs when G is small or unbalanced.

- Use with: [[clustered standard errors]] when cluster count is modest (e.g., G < 50; strongly recommended when G ≤ 30, and critical when G ≤ 10).
- Typical contexts: [[Difference-in-Differences (DiD)]], panel FE models, geo experiments, cluster RCTs/stepped-wedge, policy shocks with few treated clusters.

---

## Why and when to use

> [!tip] Use WCB when
> - Few clusters or few treated clusters (e.g., ≤ 30, especially ≤ 10)
> - Highly unbalanced cluster sizes
> - Inference on coefficients tied to cluster-level variation (policy at state/geo level)

> [!warning] Conventional cluster-robust SEs can substantially understate uncertainty with few clusters; WCB improves Type I error control relative to asymptotic t-tests.

See: [[few-cluster corrections]].

---

## How it works (high level)

- Fit the regression and obtain residuals under the null (restricted) or the full model (unrestricted).
- Multiply cluster-level residuals by random “wild” weights (e.g., Rademacher ±1, Webb 6-point).
- Recompute the test statistic (e.g., t or Wald) on the pseudo-sample without re-estimating fixed effects from scratch at the individual level (implementations differ).
- Repeat B times; the fraction of bootstrap statistics more extreme than the observed gives the p-value; invert tests for CIs.

Key choices
- Restricted vs unrestricted bootstrap:
  - Restricted (null-imposed) often recommended for hypothesis tests on coefficients.
- Weights:
  - Rademacher (±1 with prob 0.5) commonly used; Webb weights can perform better with very few time periods per cluster.
- Cluster dimension:
  - Choose the clustering dimension that reflects assignment/correlation; WCB is typically one-way (multiway variants exist but are less standard).

---

## Inference targets

- Single-coefficient t-tests (two-sided/one-sided)
- Linear combinations of coefficients (Wald tests)
- Confidence intervals by inverting the test (search over values until the bootstrapped test is just non-rejected)

Supports typical linear models:
- OLS with/without fixed effects (entity/time/other high-dimensional FE)
- Panel/DiD/TWFE; event-study coefficients
- Models estimated via common packages (reghdfe/fixest/linearmodels), with WCB applied to the saved objects

---

## Software

### Stata (boottest)

```stata
* Example: TWFE DiD with reghdfe
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)

* Wild cluster bootstrap-t for the interaction coefficient
* Two-sided, Rademacher weights, 9,999 reps
boottest c.Post#1.D, cluster(id) reps(9999) rademacher

* Webb weights (often useful when few periods per cluster)
boottest c.Post#1.D, cluster(id) reps(9999) webb

* One-sided test (greater)
boottest c.Post#1.D, cluster(id) reps(9999) rademacher onesided
```

- boottest supports multiple tested coefficients (joint tests), different weight distributions, and CI inversion.

### R (fwildclusterboot / wildboottest)

```r
# install.packages("fwildclusterboot")
library(fwildclusterboot)
library(fixest)

# Example: TWFE with fixest
est <- feols(Y ~ D:Post | id + time, data = df)

# Wild cluster bootstrap for the interaction
# param = "D:Post" (coefficient name as in est); cluster at id level
bt <- boottest(est, param = "D:Post", B = 9999,
               clustid = ~ id, boot_type = "wild", type = "rademacher")
bt

# Webb weights
bt_webb <- boottest(est, param = "D:Post", B = 9999,
                    clustid = ~ id, boot_type = "wild", type = "webb")
bt_webb

# Joint test (e.g., multiple event-study lags/leads)
bt_joint <- boottest(est, param = c("sunab::0", "sunab::1"), clustid = ~ id, B = 9999)
```

- fwildclusterboot supports fixest, lm, and some ivreg objects; see docs for CI inversion and restricted tests.

### Python (wildboottest)

```python
# pip install wildboottest
from wildboottest.wildboottest import boottest
import statsmodels.formula.api as smf

# Fit OLS (example; for FE, include dummies or use within transforms)
res = smf.ols('Y ~ D:Post + C(id) + C(time)', data=df).fit()

# Wild cluster bootstrap test (cluster by id) for coefficient on D:Post
bt = boottest(res, param='D:Post', cluster=df['id'], B=9999, weights='rademacher', impose_null=True)
print(bt)
```

- If using linearmodels PanelOLS, extract residuals and design; package interfaces may vary—consult documentation.

---

## Practical guidance

> [!check] Best practices
> - [ ] Report total number of clusters and number of treated clusters  
> - [ ] Use restricted (null-imposed) bootstrap for hypothesis testing; report weight type (Rademacher/Webb) and reps  
> - [ ] Cluster at the assignment level; if treatment is at geo-level, do not cluster at individual level  
> - [ ] With very few clusters (≤ 10), prefer Webb weights and restricted bootstrap; complement with design-based/randomization inference when possible  
> - [ ] For event studies, test families of coefficients (joint tests) in addition to individual periods  
> - [ ] In staggered DiD with few treated cohorts, bootstrap at the cohort/cluster level accordingly

> [!warning] Pitfalls
> - Clustering at the wrong level (e.g., user instead of state when policy is state-level)  
> - Assuming WCB fixes identification issues (e.g., [[interference]]/[[No spillovers]] violations); it only addresses inference  
> - Too few reps (B) leading to noisy p-values; use 9,999+ when feasible  
> - Ignoring strong multiway dependence (e.g., entity and time); consider alternative corrections if needed

---

## Algorithm sketch (restricted WCB-t)

1) Fit the model and compute restricted residuals under H0: Rβ = r (e.g., β_j = 0).
2) For b = 1..B:
   - Draw i.i.d. cluster weights $w_g^{(b)}$ (Rademacher/Webb).
   - Form pseudo residuals $\hat u_{ig}^{(b)} = w_g^{(b)} \hat u_{ig}^{(0)}$ for observations in cluster g.
   - Create pseudo outcome $Y^{(b)} = \hat Y^{(0)} + \hat u^{(b)}$ where $\hat Y^{(0)}$ are fitted under H0.
   - Re-estimate the model and compute the test statistic $t^{(b)}$ for Rβ = r.
3) p-value = share of $|t^{(b)}| \ge |t_{obs}|$ (two-sided) or appropriate one-sided tail.
4) CI: find parameter values that are not rejected by the test (invert across grid).

---

## Diagnostics and sensitivity

- Compare WCB p-values across weight choices (Rademacher vs Webb).
- Check sensitivity to clustering choices (if multiple plausible levels).
- For very few clusters, complement with:
  - [[few-cluster corrections]] (CR2/CR3 with Satterthwaite d.f.)
  - Design-based [[randomization inference]] when assignment is known
- In geo/spatial settings, if dependence decays with distance rather than neatly clustering, consider [[Conley standard errors]] as robustness.

---

## Reporting essentials

- Model specification and clustering level
- Number of clusters (total and treated) and any blocking/stratification
- Wild bootstrap details: restricted/unrestricted, weights (Rademacher/Webb), B reps, seed
- Test results (p-values) and, if reported, CI construction method
- Sensitivity: alternative weight choices, cluster levels, and comparison with CR2/CR3 SEs
- Context: small-sample caveats; complement with randomization inference if feasible

---

## Common use cases

- DiD with few treated clusters (states/counties/schools)
- Event-study coefficients in staggered rollouts
- Cluster RCTs with small G
- Geo experiments and market-level tests
- High-leverage settings with unbalanced cluster sizes

---

## Related notes

- [[few-cluster corrections]] · [[clustered standard errors]] · [[clustering]]  
- [[Difference-in-Differences (DiD)]] · [[Sun–Abraham estimator]] · [[Callaway–Sant’Anna estimator]] · [[Triple Differences (DDD)|DDD]]  
- [[randomization inference]] · [[Conley standard errors]]

---