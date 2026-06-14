---
title: AA test
aliases: [A/A test, AA sanity check, control-control test]
tags: [experimentation, ab-testing, diagnostics, srm, randomization, variance, power]
updated: 2025-09-17
---

# AA test

> [!summary] Quick definition
> An AA test runs two (or more) groups under identical conditions (no treatment difference) to validate the experimentation pipeline: randomization, bucketing, exposure logging, identity stability, metric computation, and inference. Any significant difference should occur only at the nominal rate (α), after accounting for multiple looks/metrics.

- Used in: [[AB Testing (MOC)]], platform validation, pre-launch pipelines, new metrics/guardrails onboarding.

---

## Why run AA tests?

- Sanity-check randomization and assignment (no [[Sample Ratio Mismatch (SRM)|SRM]]), [[bucketing]] stability, and [[exposure logging]].
- Validate metric definitions (no leakage, correct windows, no unit miscounting).
- Empirically calibrate variance and tails (inform [[power analysis]]/[[Minimum Detectable Effect (MDE)|MDE]]).
- Dry-run sequential monitoring and dashboards ([[sequential testing]]).

> [!tip] When
> - Before a big A/B: pre-experiment AA (one or more cycles)  
> - When changing logging, bucketing, or identity logic  
> - When onboarding new metrics/guardrails  
> - Periodically as a platform health signal

---

## What to check

- Sample Ratio Mismatch ([[Sample Ratio Mismatch (SRM)|SRM]]): observed allocation vs. planned split (χ² test).
- Metric equivalence: primary and guardrail metrics show no systematic differences (beyond α).
- Covariate balance: demographics, pre-period baselines (if available).
- Data integrity: identity stability, duplicate users/sessions, exposure correctness, time windows, [[seasonality]] coverage.
- Inference plumbing: SEs (iid vs [[clustered standard errors]]), CUPED/[[Analysis of Covariance (ANCOVA)|ANCOVA]] implementation.

---

## Interpreting AA tests

- With m independent tests at α, expect ~ m·α false positives. Use [[False Discovery Rate (FDR)|FDR]]/FWER control or pre-specify families.
- Continuous monitoring inflates false positives unless using [[sequential testing]] or always-valid p-values.
- A single “significant” metric in a large metric set is not automatically a platform failure. Investigate patterns:
  - Many related metrics move in the same direction?
  - Fails recur across repeated AAs?
  - SRM present? Logging change coincident?

---

## Common failure modes and remedies

- SRM or allocation drift → fix randomization, throttling, traffic filters, namespace collisions.
- Identity instability (user↔device swaps; bot traffic) → strengthen identity resolution and bot filters.
- Exposure mis-logging/triggering bias → align eligibility vs. analysis population; validate exposure clocks.
- Time-window misalignment / seasonality → ensure full cycle coverage; align cohort windows.
- Cluster/session designs analyzed with iid SEs → switch to cluster-robust or block-aware variance.

---

## Test plan (practical)

> [!check] Recommended AA protocol
> - [ ] Choose unit of analysis (user/session/device/geo) and bucketing; verify persistence  
> - [ ] Cover at least one weekly cycle (better: multiple) to capture [[seasonality]]  
> - [ ] Pre-specify metrics and families (primary vs guardrails) and α/FDR  
> - [ ] Use correct SEs (cluster/time) and variance reduction (optional: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]) with strictly pre-exposure baselines  
> - [ ] Monitor SRM continuously; pause if SRM persists  
> - [ ] Log anomalies (outages, deployments); exclude blackout periods in a sensitivity cut  
> - [ ] Repeat AA on changes to logging, bucketing, identities, or metric definitions

---

## Minimal tests and code

> [!example] R: SRM and difference-in-means

```r
# df: D (0/1 assignment), Y (metric), optionally cluster_id, preY (baseline)
# SRM (chi-square)
tab <- table(df$D)
chisq.test(tab, p = c(0.5, 0.5))

# Diff-in-means (robust)
library(sandwich); library(lmtest)
fit <- lm(Y ~ D, data = df)
coeftest(fit, vcov = vcovHC(fit, type = "HC1"))

# Cluster-robust (e.g., session/user/geo)
library(clubSandwich)
fit_cl <- lm(Y ~ D, data = df)
clubSandwich::coef_test(fit_cl, vcov = vcovCR(fit_cl, type = "CR2", cluster = df$cluster_id), test = "Satterthwaite")
```

> [!example] Python: SRM and ANCOVA/CUPED

```python
import numpy as np, pandas as pd
from scipy.stats import chisquare
import statsmodels.formula.api as smf

# SRM (expected 50/50)
n0 = (df['D']==0).sum(); n1 = (df['D']==1).sum()
chisquare([n0, n1], f_exp=[(n0+n1)/2, (n0+n1)/2])

# ANCOVA (variance reduction with baseline)
res = smf.ols('Y ~ D + preY', data=df).fit(cov_type='HC1')
print(res.summary())
```

> [!example] Stata: SRM and robust t-test

```stata
* SRM
tab D
* Expected counts (50/50): Pearson chi2 manually or use 'tab, chi2'

* Diff in means (robust)
reg Y D, vce(robust)

* Cluster-robust by user/geo
reg Y D, vce(cluster cluster_id)
```

> [!example] Multiple metrics with FDR (R)

```r
metrics <- c("Y1","Y2","Y3","guardrail1","guardrail2")
pvals <- sapply(metrics, function(m) summary(lm(reformulate("D", m), df))$coef["D","Pr(>|t|)"])
p.adjust(pvals, method = "BH")  # FDR-adjusted
```

---

## Power and duration

- Plan AA length to cover a full calendar cycle and achieve reasonable power to detect egregious issues (large SRM, big drifts). Calibrate with historical variance or prior AAs.
- For AA “fails,” consider whether the observed difference is practically meaningful vs. a statistical blip at α. If practically negligible but statistically significant, revisit variance model/SEs and multiplicity handling.

---

## Do’s and don’ts

> [!tip] Do
> - Treat AA as a platform diagnostic, not a hypothesis hunt  
> - Control multiplicity (families, FDR), especially with many guardrails  
> - Use appropriate variance (cluster, CUPED, stratification) matching the intended AB analysis  
> - Repeat after pipeline changes; keep an AA registry

> [!warning] Don’t
> - Declare failure from a single p < 0.05 among many metrics without SRM or pattern checks  
> - Mix triggered exposure with ITT analysis undefinedly  
> - Ignore [[seasonality]] and event confounds (holidays, outages)  
> - Use post-exposure features in CUPED/[[Analysis of Covariance (ANCOVA)|ANCOVA]] (leakage)

---

## Reporting essentials

- Design: unit, bucketing strategy, duration, cycles covered
- Metrics: primary/guardrails; baselines for CUPED/ANCOVA; clustering level
- Inference: SE type; α/FDR; sequential monitoring yes/no
- Diagnostics: SRM results, balance, seasonality/outage notes
- Outcomes: number of significant metrics (raw and FDR-adjusted), magnitudes, patterns
- Actions: fixes or sign-offs; next AA schedule

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Sample Ratio Mismatch (SRM)|SRM]] · [[bucketing]] · [[exposure logging]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[seasonality]] · [[sequential testing]]
- [[guardrail metric]] · [[stratification]]