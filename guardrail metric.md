---
title: guardrail metric
aliases: [guardrail, safety metric, fail-safe metric, canary guardrail]
tags: [experimentation, ab-testing, guardrails, safety, diagnostics, sequential, multiplicity]
updated: 2025-09-17
---

# guardrail metric

> [!summary] Quick definition
> A guardrail metric is a safety/health metric monitored during experiments to prevent harmful launches (e.g., crash rate, latency, error rate, churn). Guardrails are pre-specified with thresholds and decision rules (stop, pause, or proceed). They are distinct from the OEC (primary success metric) and are typically tested for “no meaningful harm” via non-inferiority or equivalence.

- Where used: [[AB Testing (MOC)]], canaries, rollouts, geo/switchback experiments, field trials.
- Examples: availability, error/crash rates, p95 latency, spam/abuse, complaint rate, cancellations, privacy/security rule hits, fairness constraints.

---

## Purpose and principles

- Safety first: prevent shipping changes that degrade reliability, user trust, or compliance.
- Pre-specification: define guardrails, thresholds (non-inferiority margins), families, and sequential rules before the run.
- Separate from OEC: guardrails gate rollout even if OEC improves.
- “No worse than” framing: typically one-sided non-inferiority or two one-sided tests (TOST) for equivalence.

> [!tip] Typical stance
> - Non-inferiority: New − Control ≥ −m (allow at most m harm)
> - Equivalence: |New − Control| ≤ m (both sides constrained)

---

## Selecting guardrails

- Relevance: tie directly to risk (uptime, latency, errors, security, fairness, legal).
- Sensitivity and stability: low noise at planned horizons; measurable for enough units (avoid extremely sparse).
- Actionability: clear stop/pause guidance when violated.
- Coverage: include both platform health (system-level) and user harm (behavioral) metrics when appropriate.

> [!example] Common guardrails
> - Reliability: request error rate (4xx/5xx), crash rate, p95/p99 latency, timeouts.
> - Data quality: logging completeness, identity stability, [[Sample Ratio Mismatch (SRM)|SRM]] absence.
> - User trust: complaint/abuse flags, unsubscribe, refunds/chargebacks.
> - Business safety: cannibalization rate, inventory shortages.
> - Fairness: disparate impact metrics across key groups.

---

## Thresholds and margins

- Non-inferiority margin m: maximum acceptable harm (absolute or relative). Justify with historical variability, SLO/SLA, risk tolerance.
- Quantiles (p95 latency): set bounds relative to SLO (e.g., must not exceed SLO or exceed control by more than m ms).
- Proportions/rates: absolute Δ or relative ratio bound; consider baseline levels (small baselines → use absolute % points).

> [!warning] Don’t set m post hoc
> Choose m before the test; post-hoc tuning undermines error control and governance.

---

## Statistical handling

- Hypotheses (non-inferiority, one-sided)
  - H0: Δ ≤ −m (harm exceeds margin) vs. H1: Δ > −m.
  - Decision: if lower CI bound for Δ is > −m, pass guardrail; else fail or inconclusive.
- Equivalence (TOST)
  - Two one-sided tests: H0a: Δ ≤ −m and H0b: Δ ≥ m. Reject both to claim |Δ| < m.
- Sequential monitoring
  - Use [[sequential testing]] (group-sequential with alpha-spending or always-valid p-values) to avoid peeking inflation.
- Multiplicity
  - Treat guardrails as a family; control FWER (Bonferroni/Holm) or [[False Discovery Rate (FDR)|FDR]] on guardrails separately from OEC.

> [!tip] Variance/SEs
> - Cluster/session/geo designs: use [[clustered standard errors]]; apply [[few-cluster corrections]] when G is small.
> - Ratio/quantile metrics: use delta method or bootstrap for CIs; quantile CIs via distribution-free or smoothed bootstrap.

---

## Operational rules

- Pre-launch doc: metric definitions, units, windows; margins; α and power; sequential cadence; abort/pause conditions; adjudication process.
- During run: monitor dashboards; log SRM, outages, releases; ensure [[AA test]] sanity if platform changes.
- Decisions: pause on clear violations; consider futility/need for longer run if noisy; document.

---

## Examples and templates

- Non-inferiority in error rate (absolute Δ in pp)
  - Margin m = 0.2 pp. If 95% lower CI of (err_treat − err_ctrl) > −0.2 pp, pass.
- Latency p95 (ms)
  - Margin m = +10 ms. If 95% lower CI of (−Δ) < 10 ms (equivalently Δ < 10 ms with CI), pass; else fail or extend.
- Availability
  - Must remain ≥ SLO (e.g., 99.9%) with CI including ≥ SLO; treat as one-sided.

---

## Minimal code snippets

> [!example] R: Non-inferiority (proportions, Wald CI with continuity correction optional)

```r
p0 <- 0.020  # control error rate
p1 <- 0.0212 # treatment
n0 <- 100000; n1 <- 100000
m <- 0.002   # 0.2 pp margin (0.002)

# Wald CI for difference
se <- sqrt(p0*(1-p0)/n0 + p1*(1-p1)/n1)
delta <- p1 - p0
z <- qnorm(0.975)
ci <- c(delta - z*se, delta + z*se)

pass_noninf <- (ci[1] > -m)
list(delta=delta, CI=ci, pass=pass_noninf)
```

> [!example] Python: TOST equivalence for mean difference

```python
import numpy as np
from scipy.stats import norm

delta_hat = 1.5     # ms
se = 0.8
m = 3.0
alpha = 0.05
z = norm.ppf(1-alpha)

t1 = (delta_hat - (-m)) / se  # > z to reject H0: Δ <= -m
t2 = (m - delta_hat) / se     # > z to reject H0: Δ >= m
pass_equiv = (t1 > z) and (t2 > z)
pass_equiv
```

> [!example] R: Bootstrap CI for p95 latency

```r
lat0 <- df$lat[df$D==0]; lat1 <- df$lat[df$D==1]
p <- 0.95; B <- 2000
qdiff <- function(x,y,p){ quantile(y,p,na.rm=TRUE) - quantile(x,p,na.rm=TRUE) }
delta_hat <- qdiff(lat0, lat1, p)

set.seed(1)
boot <- replicate(B, {
  x <- sample(lat0, replace=TRUE)
  y <- sample(lat1, replace=TRUE)
  qdiff(x,y,p)
})
ci <- quantile(boot, c(0.025, 0.975), na.rm=TRUE)
list(delta=delta_hat, CI=ci)
```

> [!example] Stata: Non-inferiority for proportions (New − Control ≥ −m)

```stata
* Inputs
local p0 = 0.020
local p1 = 0.0212
local n0 = 100000
local n1 = 100000
local m  = 0.002

scalar delta = `p1' - `p0'
scalar se = sqrt(`p0'*(1-`p0')/`n0' + `p1'*(1-`p1')/`n1')
scalar z = invnormal(0.975)
scalar lo = delta - z*se
scalar hi = delta + z*se
display "delta=" %6.4f delta "  CI=[" %6.4f lo ", " %6.4f hi "]"
display "Pass non-inferiority? " (lo > -`m')
```

---

## Interpretation and governance

- Pass: evidence of no meaningful harm within margin; proceed if OEC acceptable.
- Fail: pause/rollback; investigate root causes; consider whether margin should be revisited only with strong justification and governance approval.
- Inconclusive: extend duration or increase sample if feasible; consider variance reduction ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]]) or alternative design (cluster, geo, switchback).

---

## Common pitfalls

> [!warning]
> - Setting margins after seeing data (p-hacking governance)  
> - Ignoring clustering/serial correlation in guardrail tests (iid SEs too optimistic)  
> - Treating many guardrails at α=0.05 without multiplicity control  
> - Using post-treatment covariates in adjustment (leakage)  
> - Not covering [[seasonality]]; comparing non-comparable windows  
> - Overreacting to one-off blips without considering sequential plan/guardrails family

---

## Reporting essentials

- Definitions (units, windows, transformations), directionality, and margins m (abs/relative)
- Statistical plan: non-inferiority/equivalence, α, multiplicity, sequential method
- Results: estimates with CIs, pass/fail decisions, SRM/[[AA test]] health checks
- Diagnostics: variance stability, clustering, seasonality, outages/exceptions
- Actions: pause/rollback/escalate; follow-up analyses and owners

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[bucketing]] · [[exposure logging]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]]
- [[seasonality]] · [[clustered standard errors]] · [[few-cluster corrections]]
- [[treatment effect heterogeneity]] · [[switchback experiment]] · [[geo experiment]]