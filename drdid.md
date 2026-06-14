---
title: drdid
aliases: [doubly robust diff-in-diff, doubly robust difference-in-differences, DR-DiD, Sant’Anna–Zhao, drdid package]
tags: [causal-inference, did, doubly-robust, panel, repeated-cross-sections, propensity, outcome-model, R, Stata]
updated: 2025-09-17
---

# drdid

> [!summary] Quick definition
> drdid refers to doubly robust Difference-in-Differences (DR-DiD) estimators (Sant’Anna & Zhao, 2020/2022) and to the R/Stata implementations that estimate DiD ATT while being consistent if either the outcome regression or the propensity model is correctly specified (not necessarily both). It covers two common data structures:
> - Panel: same units observed pre and post
> - Repeated cross-sections: different samples in each period

- Why it’s useful: compared to plain DiD, DR-DiD adds covariate adjustment and remains consistent if one nuisance model is right; compared to IPW-only or regression-only DiD, it is doubly robust and often more efficient.

---

## What it estimates

- Primary estimand: ATT = average treatment effect on the treated (post vs pre), under DiD identification.
- Settings:
  - Panel DR-DiD ATT
  - Repeated cross-sections DR-DiD ATT (RC-DR-DiD)

> [!note] Staggered timing
> For staggered adoption (multiple groups treated at different times), use cohort-time ATTs and aggregations (e.g., [[Callaway–Sant’Anna estimator]]). DR weighting is available there too (Stata csdid, method(dripw)).

---

## Identification and assumptions

- DiD identification:
  - [[parallel trends assumption]] for untreated potential outcomes, typically conditional on X
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] and [[No spillovers]]/[[interference]] across groups
  - Correct timing (no or modeled [[Anticipatory effects]])
- DR-DiD requires:
  - Either the outcome regression(s) for the control group or the propensity of treatment (treated group indicator) is correctly specified (not necessarily both)
  - [[Overlap]]/positivity: treated units’ X support lies within the controls’ X support
- Repeated cross-sections: additional sampling assumptions (stationarity-type conditions) and/or reweighting to make groups comparable across time given X (handled inside the estimator)

---

## Intuition (scores, not full derivation)

Let G=1 denote “treated group” (ever-treated), t=0 pre, t=1 post.

- Outcome regressions in controls: m0,1(x)=E[Y|G=0,t=1,X=x], m0,0(x)=E[Y|G=0,t=0,X=x]; Δm0(x)=m0,1(x)−m0,0(x).
- Propensity of being in the treated group: p(x)=P(G=1|X=x) (for two-group DiD)
- DR-DiD compares the treated group’s outcome change to a reweighted/adjusted control group change, using both Δm0(X) and weights based on p(X). If either Δm0(.) or p(.) is correct, the bias cancels out.

You can think of the estimator as:
- Treated avg change minus predicted counterfactual change using control outcome model (OR term), corrected by a weighted control residual term (IPW term), with normalization weights.

---

## When to prefer DR-DiD vs alternatives

- Versus plain TWFE/DiD: DR-DiD is robust to covariate imbalances and misspecification of either nuisance; often tighter CIs.
- Versus IPW-only or regression-only DiD: DR-DiD stays consistent if one nuisance is wrong.
- Staggered adoption: don’t use a single TWFE coefficient; use [[Callaway–Sant’Anna estimator]] (can be DR) or [[Sun–Abraham estimator]] for event studies.

---

## R implementation (drdid)

> [!example] R: panel data (same units pre/post)

```r
# install.packages("drdid")
library(drdid)

# Panel (two periods per unit or more)
# df columns (example): id, time (0/1), D (treated=1 for treated group in post), G (ever-treated group indicator),
# Y (outcome), covariates X...
# Wrapper handles both designs; for panel set panel = TRUE
out_panel <- drdid::drdid(yname   = "Y",
                          tname   = "time",
                          idname  = "id",
                          dname   = "G",         # group indicator (ever-treated)
                          xformla = ~ X1 + X2 + X3,
                          data    = df,
                          panel   = TRUE,
                          est_method = "dr")     # "dr", "ipw", or "reg"
summary(out_panel)
```

> [!example] R: repeated cross-sections

```r
library(drdid)
# Repeated cross-sections (different units pre/post). time=0/1, G=ever-treated group indicator.
out_rc <- drdid::drdid(yname   = "Y",
                       tname   = "time",
                       idname  = NULL,          # no panel id
                       dname   = "G",
                       xformla = ~ X1 + X2 + X3,
                       data    = df_rc,
                       panel   = FALSE,
                       est_method = "dr")
summary(out_rc)
```

Notes
- est_method: "dr" (doubly robust), "ipw" (inverse probability weighting), "reg" (outcome regression).
- The package also offers lower-level functions (e.g., drdid_panel(), drdid_rc()) for customization.

---

## Stata implementation

Two relevant commands:

1) drdid (Sant’Anna & Zhao’s DR-DiD estimators; panel and repeated cross-sections)
```stata
* Install if needed: ssc install drdid
* Panel example (two periods; id and time)
drdid Y, time(time) treat(G) id(id) cluster(id) ///
    controls(X1 X2 X3) method(dr)

* Repeated cross-sections
drdid Y, time(time) treat(G) controls(X1 X2 X3) method(dr)
```

2) csdid (Callaway–Sant’Anna for staggered timing; DR-IPW via method(dripw))
```stata
* Staggered adoption with group-time ATTs
csdid Y, ivar(id) time(time) gvar(Gfirst) method(dripw) vce(cluster id)
estat event
```

---

## Python (sketch)

There is no single turnkey “drdid” package; you can approximate panel DR-DiD:

```python
# Step 1: Fit control outcome models pre and post
# Step 2: Fit propensity p(x)=P(G=1|X) (treated group membership)
# Step 3: Compute Δm0(X)=m0,1(X)-m0,0(X) and DR weights; form ATT via treated change minus
#         weighted/adjusted control change. Prefer robust libraries (R/Stata) for production.
```

Alternatively, for staggered settings use Python wrappers to R (rpy2) or rely on did (R) or csdid (Stata). For standard DiD with covariates and DR flavor, consider econml’s DR learners within a DiD workflow, but be careful with identification and timing.

---

## Diagnostics and good practice

> [!check]
> - [ ] Pre-trends: visualize and test pre-period dynamics (see [[event study]])  
> - [ ] Overlap: check propensity tails and effective sample size; trim if necessary  
> - [ ] Model fit: try alternative nuisance models (logit vs GBM for p; linear vs RF for outcomes)  
> - [ ] Clustered inference: cluster at the treatment-assignment level (often unit or group); use [[few-cluster corrections]] when clusters are few  
> - [ ] Robustness: compare "dr" to "ipw" and "reg"; vary covariate sets; try RC vs panel when applicable  
> - [ ] Spillovers & anticipation: examine near/far units; add leads in event-study for anticipation

---

## Common pitfalls

> [!warning]
> - Treating DR-DiD as a fix for parallel trends—identification still hinges on (conditional) parallel trends  
> - Using post-treatment covariates (see [[bad controls]])  
> - Mislabeling design (panel vs repeated cross-sections) in the API  
> - Severe lack of overlap leading to unstable weights; consider trimming or alternative control sets  
> - Few treated clusters with conventional SEs → anti-conservative; use [[few-cluster corrections]]

---

## Reporting essentials

- Design (panel vs repeated cross-sections), time windows, group definitions
- Estimand (ATT) and identification assumptions (conditional parallel trends)
- Nuisance specification: models for p(X) and m0,t(X); how chosen (logit/ML), any cross-validation
- Inference: clustering level; small-sample corrections if any
- Sensitivity: alternative nuisances, trimmed samples, robustness across "dr"/"ipw"/"reg"
- Diagnostics: pre-trends/event-study, overlap plots, spillover checks

---

## Relation to other DiD estimators

- [[two-way fixed effects]]: simple but can be biased under heterogeneity/staggered adoption
- [[Callaway–Sant’Anna estimator]]: group-time ATTs for staggered settings (DR-IPW available)
- [[Sun–Abraham estimator]]: robust event-study for staggered designs
- [[Borusyak–Jaravel–Spiess (imputation)]] and [[Gardner DID2S]]: imputation/two-stage approaches

---

## Minimal references

- Sant’Anna & Zhao (2020, 2022), “Doubly Robust Difference-in-Differences Estimators”
- Callaway & Sant’Anna (2021), “Difference-in-Differences with Multiple Time Periods”
- Package docs: R drdid; Stata drdid / csdid

---

## Related notes

- [[Difference-in-Differences (DiD)]] · [[DiD estimator]] · [[event study]]
- [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[covariates]] · [[composition]] · [[No spillovers]] · [[Anticipatory effects]]

---