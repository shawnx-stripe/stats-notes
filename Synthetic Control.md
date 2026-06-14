---
title: Synthetic Control
aliases: [SCM, synthetic control method, synthetic controls]
tags: [causal-inference, comparative-case, policy-evaluation, panels, weighting, r, stata]
updated: 2025-09-17
---

# Synthetic Control

> [!summary] Quick definition
> Synthetic Control constructs a weighted average of untreated (“donor”) units to approximate the treated unit’s pre-treatment trajectory. The post-treatment difference between the treated unit and its synthetic counterpart estimates the treatment effect for that unit (or cohort).

- Strength: data-driven control tailored to match pre-treatment outcomes and predictors without imposing linear parallel trends as in [[Difference-in-Differences (DiD)]].
- Typical outputs: a “path plot” and a “gap plot” (treated minus synthetic). Inference is usually based on placebo/permutation tests.

## Setup and estimator

- One treated unit (or a treated cohort); donor pool of comparable untreated units.
- Choose predictors (often include several pre-treatment outcomes and key covariates).
- Find nonnegative weights that sum to 1 over donors to best match pre-treatment predictors/outcomes.

### Optimization (copy-ready)
- Let X1 be predictors for the treated unit, X0 for donor units; choose V (predictor weights, positive semidefinite).
- Solve for donor weights W (nonnegative, sum to 1):
$$
\min_{W} \ (X_1 - X_0 W)^\top V (X_1 - X_0 W)
\quad \text{s.t.} \quad W_j \ge 0,\ \sum_j W_j = 1.
$$

- Estimated effect at time t (post):
$$
\hat\tau_t = Y_{1t} - \sum_j W_j Y_{jt}.
$$

> [!tip] Predictors
> Pre-treatment outcomes at multiple lags are powerful predictors; add time-invariant covariates and pre-period averages as needed.

## Identification assumptions

- A convex combination of donors can approximately reproduce the treated unit’s counterfactual path in the pre-period.
- No structural break in the relationship between predictors and outcomes at treatment absent the intervention.
- [[No spillovers]]/[[interference]]: donors are not affected by the treatment.
- Correct timing (handle [[Anticipatory effects]] if present).
- Stable measurement and [[composition]].

> [!note] Relation to DiD
> - DiD assumes [[parallel trends assumption]] (often global and linear in time); SCM relaxes this by matching the entire pre-period path.
> - When pre-fit is poor, SCM is weak; when pre-fit is good, SCM can be compelling even with complex trends.

## Diagnostics and inference

> [!check] What to report
> - Pre-treatment fit: RMSPE (root mean squared prediction error) and balance tables.
> - Donor weights: distribution and any single-unit dominance.
> - Gap plot: $\hat\tau_t$ over time with pre/post vertical line.
> - Placebo tests:
>   - In-space: reassign “treatment” to each donor, recompute gaps; compare treated gap to placebo distribution (optionally scaled by pre-RMSPE).
>   - In-time: shift placebo intervention dates in the treated unit’s pre-period.
> - Sensitivity:
>   - Leave-one-(or few)-out donors; alternative predictor sets; donor pool restrictions.
>   - Robustness to excluding near-border donors if spillovers are possible (spatial “donuts”).

> [!warning] Common pitfalls
> - Poor pre-period fit (large RMSPE) yet strong causal claims.
> - Donor contamination (units exposed via spillovers included in the donor pool).
> - Post-treatment variables among predictors (see [[bad controls]]).
> - Small donor pools or heavy reliance on one donor.

## Practical workflow

> [!check] Steps
> - [ ] Define treated unit, treatment date, and donor pool; justify comparability.
> - [ ] Choose predictors (multiple pre-period outcomes, key covariates).
> - [ ] Fit SCM and check pre-fit (RMSPE, balance).
> - [ ] Plot paths and gaps; compute post/pre RMSPE ratio.
> - [ ] Run placebo tests (in-space and/or in-time) with the same donor restrictions and predictors.
> - [ ] Sensitivity: alternative donors/predictors; leave-one-out.
> - [ ] Document design choices and provide reproducible code.

## Minimal code snippets

> [!example] R: Classic Synth

```r
# install.packages("Synth")
library(Synth)

# Example columns: id (unit), time (year), Y (outcome), treat (1 if treated unit, else 0)
# Define treated and donor units
treated_id <- 1
donors <- setdiff(unique(df$id), treated_id)
pre_period  <- 1990:2004
post_period <- 2005:2010

dat <- dataprep(
  foo = df,
  predictors = c("X1","X2"),
  predictors.op = "mean",
  dependent = "Y",
  unit.variable = "id",
  time.variable = "time",
  treatment.identifier = treated_id,
  controls.identifier = donors,
  time.predictors.prior = pre_period,
  special.predictors = list(
    list("Y", 1995, "mean"),
    list("Y", 2000, "mean"),
    list("Y", 2004, "mean")
  ),
  time.optimize.ssr = pre_period,
  time.plot = c(pre_period, post_period)
)

sout <- synth(dataprep.obj = dat)

# Balance table and weights
synth.tab(dataprep.obj = dat, synth.obj = sout)
w <- sout$solution.w  # donor weights

# Plots
path.plot(dataprep.obj = dat, synth.obj = sout)  # treated vs synthetic
gaps.plot(dataprep.obj = dat, synth.obj = sout)  # gap over time
```

> [!example] R: Augmented Synthetic Control (robust to imperfect fit)

```r
# install.packages("augsynth")
library(augsynth)
# Y ~ 1 is typical; supply unit, time, and treatment indicators
as_out <- augsynth(Y ~ 1, unit = id, time = time, treatment = treat,
                   data = df, progfunc = "None", scm = TRUE)
summary(as_out)
plot(as_out)   # path and gaps
```

> [!example] R: Synthetic DiD (synthdid)

```r
# install.packages("synthdid")
library(synthdid)
Y <- synthdid::panel.matrices(df, unit = "id", time = "time", outcome = "Y", treatment = "treat")$Y
N0T0 <- synthdid::synthdid_estimate(Y)  # automatic weights for synthetic DiD
summary(N0T0); plot(N0T0)
```

> [!example] Stata: synth and placebo inference

```stata
* ssc install synth, replace
* Variables: id unit id, time year, outcome Y; treated unit 1 from 2005 on
xtset id time
synth Y X1 X2 Y(1995) Y(2000) Y(2004), trunit(1) trperiod(2005) ///
      unitnames(id) fig keep("sc_results")

* Path and gap plots are produced; review _Co_ weights in results
* Placebo (in-space): loop over donors (illustrative)
levelsof id if id != 1, local(donors)
foreach u of local donors {
    synth Y X1 X2 Y(1995) Y(2000) Y(2004), trunit(`u') trperiod(2005) ///
          unitnames(id) fig
}
```

> [!example] Python: cvxpy sketch

```python
# pip install cvxpy
import cvxpy as cp
import numpy as np

# Build X1 (p x 1) predictors of treated, X0 (p x J) predictors of donors, Y0 (T x J), Y1 (T x 1)
# Fit W: nonnegative, sums to 1
J = X0.shape[1]
W = cp.Variable(J)
V = np.eye(X0.shape[0])  # simple choice; in practice V is tuned
obj = cp.Minimize(cp.quad_form(X1 - X0 @ W, V))
constraints = [W >= 0, cp.sum(W) == 1]
prob = cp.Problem(obj, constraints).solve()
W_hat = W.value

# Post-treatment gaps
Y_synth = Y0 @ W_hat
gaps = Y1 - Y_synth
```

## Extensions and related methods

- Augmented Synthetic Control (Ben-Michael, Feller, Rothstein): combines SCM with outcome modeling for bias correction; implemented in R `augsynth`.
- Synthetic DiD (Arkhangelsky et al.): blends SCM weighting with DiD; R `synthdid`.
- Generalized Synthetic Control / Interactive Fixed Effects (Xu): R `gsynth` (not SCM per se).
- Multiple treated units:
  - Estimate unit-specific SCMs and summarize gaps; or use `microsynth` (R) for grouped/staggered adoption settings.
- Placebo-based inference refinements: RMSPE ratios, conformal inference variants (research frontier).

## When to use SCM vs. DiD

- Use SCM when:
  - One (or few) treated units and many suitable donors.
  - Rich pre-treatment period to enable close fit.
  - Trends appear non-parallel or nonlinear.

- Prefer modern DiD (e.g., [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]) when:
  - Many treated units with [[staggered adoption]].
  - You need cohort-time [[group-time average treatment effect]]s and transparent aggregation.

## Reporting essentials

- Treated unit(s), intervention date(s), donor pool definition and exclusions.
- Predictors and pre-period outcome lags used; V-tuning approach (if relevant).
- Pre-fit quality (RMSPE), balance tables, donor weights.
- Gap/path plots and placebo test results (in-space/in-time), including RMSPE-scaled statistics and p-values.
- Sensitivity (leave-one-out donors, alternative donor sets/predictors).
- Discussion of assumptions: spillovers, anticipation, measurement changes.

## Copy-ready formulas

- Weighting problem:
$$
\min_W (X_1 - X_0W)^\top V (X_1 - X_0W)
\ \ \text{s.t.} \ W_j \ge 0,\ \sum_j W_j=1
$$

- Post-period gap (effect at t):
$$
\hat\tau_t = Y_{1t} - \sum_j W_j Y_{jt}
$$

- RMSPE (pre-period fit diagnostic):
$$
\text{RMSPE} = \sqrt{\frac{1}{T_0}\sum_{t \le T_0} \left(Y_{1t} - \sum_j W_j Y_{jt}\right)^2}
$$

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[event study]]
- [[parallel trends assumption]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[group-time average treatment effect]]
- [[staggered adoption]]
- [[No spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[pre-trends]]
- [[boundary discontinuity]]
- [[Conley standard errors]]
- [[bad controls]]
- [[composition]]