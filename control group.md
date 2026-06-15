---
title: Control Group
aliases: [comparison group, counterfactual group]
tags: [causal-inference, design, did, rct]
updated: 2025-09-17
---

# Control Group

> [!summary] Quick definition
> Units that do not receive the treatment. They approximate the counterfactual outcomes the [[treated group]] would have experienced without the intervention.

- Purpose: establish a baseline level/trend to contrast with treated outcomes.
- Contexts: [[randomized controlled trial (RCT)]]s and [[quasi-experimental design]]s (e.g., [[Difference-in-Differences (DiD)]], [[Regression Discontinuity Design (RDD)]], [[Synthetic Control]], [[Instrumental Variables (IV)]]).

## Role in causal inference

- Counterfactual logic: treated outcomes reflect $Y(1)$, controls aim to represent $Y(0)$ for comparable units.
- Validity rests on design-specific assumptions (e.g., [[parallel trends assumption]] for DiD; local comparability at the cutoff for RDD; no direct effect of the instrument for IV).

## Choosing a control group

### In RCTs
- Random assignment yields controls comparable in expectation on observed and unobserved characteristics.

### In quasi-experiments
- DiD: use never-treated or not-yet-treated units that share pre-treatment trends with treated units.
- RDD: units just on the other side of the cutoff serve as local controls.
- Synthetic Control: form a weighted combination of donor units to match pre-treatment paths.
- IV: “compliers” are implicitly compared; ensure [[exclusion restriction]] and [[relevance]].

> [!tip] Practical guidance
> - Prefer controls from the same data-generating context (geography, market, cohort).
> - Match or weight on key pre-treatment covariates and pre-trends when appropriate ([[matching]], [[propensity score]], [[stratification]], [[entropy balancing]]).

## Types of control groups

- Never-treated: remain unexposed throughout the study window.
- Not-yet-treated: become treated later; useful for pre-period comparisons in DiD.
- External controls: from other regions/markets; justify structural similarity.
- Synthetic controls: convex combination that best matches the treated unit’s pre-period features.
- Within-unit controls: unaffected cohorts/products/outcomes inside the same unit (use with care to avoid “bad controls”).

## Diagnostics and validation

> [!check] What to verify
> - [ ] Covariate balance pre-treatment (tables, standardized differences, visuals)
> - [ ] Outcome pre-trend similarity (plots, [[event study]] leads)
> - [ ] No exposure/[[spillovers]] or [[interference]] affecting controls
> - [ ] Stable sample [[composition]] and measurement
> - [ ] Placebo tests (fake treatment dates, unaffected outcomes)
> - [ ] Sensitivity to alternative control sets/windows

## Common pitfalls

> [!warning] Avoid these
> - Contaminated controls (partial exposure, geographic spillovers, information diffusion)
> - Different seasonality or macro shocks not shared with treated units
> - Post-treatment selection of controls or conditioning on post-treatment variables (creates [[bad controls]])
> - Anticipation effects in controls
> - Overfitting the control selection to outcomes (data snooping)

## Reporting essentials

- Explicit definition of “control” (eligibility rule, geography, time window).
- Rationale for comparability to the treated group and the identification assumption invoked.
- Evidence: pre-trend plots, balance tables, and robustness/sensitivity checks.
- Estimation details: clustering level aligned with assignment, sample restrictions, weights.

## Minimal examples

> [!example] DiD: never-treated vs not-yet-treated (pseudo-code)

```r
# R
df$Post <- as.integer(df$time >= policy_date[df$unit])
df$TreatedEver <- as.integer(!is.na(policy_date[df$unit]))
# Controls can be: never-treated (TreatedEver == 0) or not-yet-treated in pre-period (TreatedEver == 1 & Post == 0)
```

```python
# Python
df["Post"] = (df["time"] >= df["policy_date"]).astype(int)
df["TreatedEver"] = df["policy_date"].notna().astype(int)
# Define control mask:
control_mask = (df["TreatedEver"] == 0) | ((df["TreatedEver"] == 1) & (df["Post"] == 0))
```

> [!example] Balance via weighting (sketch)

```r
# R: entropy balancing to align controls to treated on covariates
library(ebal)
balance <- ebalance(Treatment = df$D, X = as.matrix(df[, c("X1","X2","preY")]))
df$w <- ifelse(df$D == 1, 1, balance$w)
```

```python
# Python: simple propensity-score ATT weights for controls
from sklearn.linear_model import LogisticRegression
import numpy as np
X = df[["X1","X2","preY"]].values
ps = LogisticRegression(max_iter=2000).fit(X, df["D"]).predict_proba(X)[:,1]
df["w"] = np.where(df["D"]==1, 1.0, ps/(1-ps))
```

## Small checklist by design

- DiD: demonstrate [[parallel trends assumption]]; consider cohort-specific estimators ([[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]) when adoption is staggered.
- RDD: test for bunching at the cutoff, covariate continuity, and bandwidth robustness.
- Synthetic Control: show pre-fit quality and post-treatment gaps with placebo tests across donors.
- IV: report first-stage strength, discuss [[exclusion restriction]] and likely complier group.

---

## Related notes
- [[treated group]]
- [[quasi-experimental design]]
- [[Difference-in-Differences (DiD)]]
- [[Regression Discontinuity Design (RDD)]]
- [[Synthetic Control]]
- [[Instrumental Variables (IV)]]
- [[parallel trends assumption]]
- [[matching]]
- [[propensity score]]
- [[stratification]]
- [[entropy balancing]]
- [[event study]]
- [[spillovers]]
- [[interference]]
- [[composition]]
- [[bad controls]]
- [[placebo test]]
- [[seasonality]]
- [[clustering]]
- [[exclusion restriction]]
- [[relevance]]