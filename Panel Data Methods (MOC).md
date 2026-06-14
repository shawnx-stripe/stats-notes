---
title: Panel Data Methods (MOC)
aliases:
  - Panel econometrics (MOC)
  - Longitudinal data (MOC)
  - Repeated measures (MOC)
tags:
  - MOC
  - econometrics
  - panel-data
  - causal-inference
  - fixed-effects
  - difference-in-differences
updated: 2025-09-26
---

# Panel Data Methods (MOC)

> [!summary] Start here
> Tools to analyze data observed for multiple units over time. This MOC organizes design, identification, estimation, and inference for panels: fixed effects, first differences, [[Difference-in-Differences (DiD)]], staggered adoption, event-studies, dynamic panels, and modern alternatives like [[Synthetic Control]].

Related starting points:
- Foundations: [[Econometrics (MOC)]], [[Causal Inference (MOC)]], [[Experimental Design (MOC)]], [[Identification Strategies (MOC)]]
- Heterogeneity: [[Treatment Effect Heterogeneity (MOC)]]
- Inference: [[Standard Errors and Inference (MOC)]]
- Complications: [[Missing Data and Selection (MOC)]], [[Spillovers and Interference (MOC)]]

## Why panel data

- Control for time-invariant unobservables via unit fixed effects
- Separate time shocks via time fixed effects
- Identify dynamic and lagged responses
- Enable quasi-experimental designs (DiD, event study, staggered treatments)
- Improve precision and interpretability vs. single cross-sections

## Core models and estimators

- Two-way fixed effects (TWFE):
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + X_{it}'\theta + \varepsilon_{it}
$$
  - Remove time-invariant unit confounders (α_i) and common time shocks (γ_t)
  - See: [[two-way fixed effects]]

- Within (fixed-effects) estimator:
  - Demean by unit (or unit-time absorption) and run OLS
  - Equivalent to including unit dummies
  - Related: first-difference estimator

- First differences (FD):
$$
\Delta Y_{it} = \beta\, \Delta D_{it} + \Delta X_{it}'\theta + \Delta \varepsilon_{it}
$$
  - Removes unit fixed effect when dynamics are simple; can reduce serial correlation structure

- Random effects (RE) and hybrids:
  - RE assumes uncorrelated effects with regressors; Hausman test for FE vs RE
  - Mundlak adjustment includes unit means of X to relax RE; “within–between” models
  - Related notes to create: [[random effects]], [[Hausman test]], [[Mundlak adjustment]], [[within–between model]]

- Event study (leads/lags around treatment):
  - Dynamic path of treatment effects; pre-trend diagnostics
  - See: [[event study]], [[pre-trends]]

## DiD and staggered adoption

- Canonical DiD (two groups, two periods):
$$
\text{DiD} = (\bar{Y}_T^{\text{post}}-\bar{Y}_T^{\text{pre}}) - (\bar{Y}_C^{\text{post}}-\bar{Y}_C^{\text{pre}})
$$
  - Assumption: [[parallel trends assumption]], stable [[composition]], no anticipation
  - See: [[Difference-in-Differences (DiD)]], [[DiD estimator]]

- Staggered treatment timing:
  - Classic TWFE biased with treatment effect heterogeneity across cohorts/event-time
  - Prefer estimators:
    - [[Callaway–Sant’Anna estimator]] (group-time ATTs; report [[group-time average treatment effect]])
    - [[Sun–Abraham estimator]] (interaction-weighted/event-study correction)
  - See: [[staggered adoption]], [[drdid]]

- Triple differences (DDD):
  - Add a third differencing dimension (e.g., group × time × second control)
  - See: [[Triple Differences (DDD)|DDD]]

## Identification in panels

- FE identification:
  - Requires within-unit variation in regressors of interest
  - Assumes no time-varying omitted variables correlated with treatment
- DiD identification:
  - [[parallel trends assumption]] in the untreated potential outcome
  - No differential [[spillovers]] or reweighting unless modeled
  - Assess with [[pre-trends]] and [[event study]] leads
- Anticipation and dynamic effects:
  - Check and model [[Anticipatory effects]]
  - Include lags/leads; interpret dynamics carefully
- Composition changes:
  - Track sample [[composition]] over time (entry/exit, [[Attrition]])
- Interference:
  - Potential within- or cross-cluster spillovers; see [[Spillovers and Interference (MOC)]]

## Inference and standard errors

- Cluster-robust SEs:
  - Cluster at the unit level when errors are serially correlated within units
  - With two dimensions of dependence, consider multi-way clustering (unit × time)
  - See: [[clustered standard errors]], [[Cameron–Gelbach–Miller]]
- Few clusters/time periods:
  - Use [[few-cluster corrections]] or [[wild cluster bootstrap]]
- Cross-sectional/spatial dependence:
  - Consider [[Conley standard errors]] (distance decay) or Driscoll–Kraay SEs (to create)
- Moulton issue:
  - Group-level treatments with unit outcomes → underestimated SEs if ignoring clustering
  - See: [[Moulton problem]]

## Diagnostics and robustness

- Pre-analysis checks
  - Visualize outcomes and treatment over time; check overlap by cohort
  - Balance on pre-treatment covariates across treated vs. control trajectories
  - Document missingness/[[Attrition]] and selection over time
- DiD diagnostics
  - Plot [[event study]] with CIs; test [[pre-trends]]
  - Vary time windows and control groups; placebo policy dates
  - Report cohort-specific effects ([[group-time average treatment effect]])
- Sensitivity and alternatives
  - Consider [[Synthetic Control]] when few treated or strong idiosyncratic trends
  - Hybrid DiD–SC or matrix completion when trends are complex
  - For staggered adoption, avoid naive TWFE averages; use modern estimators
- Interference checks
  - Explore spatial/network spillovers; “donut buffer” around treated units
  - See: [[Spillovers and Interference (MOC)]]

## Common pitfalls

> [!warning] Avoid these
> - Using TWFE with staggered adoption and heterogeneous effects without modern corrections
> - Clustering at the wrong level; ignoring serial correlation
> - Conditioning on post-treatment variables ([[bad controls]])
> - Ignoring anticipation or dynamic treatment exposure
> - Extrapolation from cohorts with limited overlap
> - Failing to report number of clusters and effective sample size

## Extensions

- Dynamic panels with lagged outcomes
  - Bias with short T (Nickell bias); use GMM (Arellano–Bond difference GMM; system GMM)
  - Related notes to create: [[Arellano–Bond]], [[System GMM]], [[Nickell bias]]
- Interactive fixed effects / factor models
  - Allow latent common factors with heterogeneous loadings
  - Related notes to create: [[interactive fixed effects]], common correlated effects
- High-dimensional FE and many-way FE
  - Efficient estimators and software (e.g., reghdfe); careful inference
- Synthetic/augmented methods
  - [[Synthetic Control]] and augmented SC; [[event study]]-compatible SC
- Heterogeneous treatment effects in panels
  - Combine with forests/meta-learners; see [[Treatment Effect Heterogeneity (MOC)]]

## Minimal formulas (copy-ready)

- TWFE regression:
$$
Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + X_{it}'\theta + \varepsilon_{it}
$$

- Within transformation (unit-demeaned):
$$
\tilde{Y}_{it} = \beta \tilde{D}_{it} + \tilde{X}_{it}'\theta + \tilde{\varepsilon}_{it}, \quad \tilde{Z}_{it} = Z_{it} - \bar{Z}_{i\cdot}
$$

- Event-study (relative time k with omitted k = −1):
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k \neq -1} \beta_k \cdot \mathbf{1}\{t - T_i = k\} + X_{it}'\theta + \varepsilon_{it}
$$

- Callaway–Sant’Anna group-time ATT:
  - Report ATT_{g,t} and aggregate with explicit weights; see [[Callaway–Sant’Anna estimator]], [[group-time average treatment effect]]

## Practical workflow

1) Define estimand and design
- Is the target a contemporaneous effect, dynamic path, or cumulative effect?
- Choose identification: FE vs. DiD vs. SC vs. dynamic panel GMM

2) Prepare data
- Construct balanced/unbalanced panel; define treatment timing; create relative-time indicators
- Check missingness/[[Attrition]]; define sample windows; ensure consistent units over time

3) Choose estimator
- TWFE or FD for time-invariant confounding control
- Modern DiD for staggered adoption (Callaway–Sant’Anna / Sun–Abraham / [[drdid]])
- [[Synthetic Control]] for few treated units or idiosyncratic trends
- Dynamic GMM if lagged outcomes are central and T is short

4) Inference
- Cluster by unit (and possibly time); few-cluster corrections if needed
- Account for spatial correlation if units are geographic (Conley / Driscoll–Kraay)

5) Validation and robustness
- Pre-trend tests, placebo policies, alternative windows, alternative controls
- Cohort-specific effects and aggregation transparency
- Spillover diagnostics and buffer tests

6) Reporting
- Number of units, time periods, and clusters
- Treatment timing distribution and cohort sizes
- Estimator(s) used and rationale; event-study plots with CIs
- Sensitivity analyses; inference method; limitations (parallel trends, spillovers)

## Cross-links

- Core topics: [[two-way fixed effects]], [[Difference-in-Differences (DiD)]], [[event study]], [[pre-trends]]
- Staggered adoption: [[staggered adoption]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[group-time average treatment effect]], [[drdid]]
- Alternatives: [[Synthetic Control]]
- Assumptions/diagnostics: [[parallel trends assumption]], [[composition]], [[Anticipatory effects]], [[placebo test]]
- Inference: [[clustered standard errors]], [[few-cluster corrections]], [[wild cluster bootstrap]], [[Conley standard errors]], [[Cameron–Gelbach–Miller]], [[Moulton problem]]
- Complications: [[Spillovers and Interference (MOC)]], [[Missing Data and Selection (MOC)]]

---

Related notes to create:
- [[random effects]]
- [[Hausman test]]
- [[Mundlak adjustment]]
- [[within–between model]]
- [[Arellano–Bond]]
- [[System GMM]]
- [[Nickell bias]]
- [[interactive fixed effects]]
- common correlated effects
- [[Driscoll–Kraay|Driscoll–Kraay standard errors]]
- [[Goodman–Bacon decomposition]]
- [[matrix completion for panels]]