---
title: Sample Ratio Mismatch (SRM)
aliases: [SRM, Sample Ratio Mismatch, sample ratio mismatch, sample-ratio mismatch]
tags: [experimentation, ab-testing, diagnostics, randomization, bucketing, exposure, srm, aa-test]
updated: 2025-09-17
---

# Sample Ratio Mismatch (SRM)

> [!summary] Quick definition
> SRM (Sample Ratio Mismatch) occurs when the observed allocation of units across variants differs significantly from the planned split (e.g., 50/50, 33/33/33), after accounting for random variation. It signals problems in randomization, bucketing, traffic routing, exposure logging, eligibility, or analysis populations.

- Where used: [[AB Testing (MOC)]], canaries, geo/switchback experiments
- Always check SRM alongside [[AA test]] and metric sanity before reading effects

---

## Why SRM matters

- Bias: SRM often indicates differential inclusion/exclusion or routing, which can bias estimates even when treatment has no effect.
- Integrity: Common root causes include bucketing bugs, throttling, identity instability, broken exposure logging, time-window misalignment, or pipeline joins that drop one arm disproportionately.

> [!tip] Gating
> Treat “SRM = fail” as a gate: do not interpret treatment effects until resolved or convincingly explained.

---

## How to test for SRM

### Two-arm (e.g., 50/50)

- Null: observed counts (n0, n1) follow planned split p0, p1 (e.g., p0=p1=0.5)
- Pearson χ² goodness-of-fit:
$$
\chi^2 = \sum_{k=0}^{1} \frac{(n_k - N p_k)^2}{N p_k}, \quad \text{df}=1
$$
Reject at small p-value (e.g., < 10^{-3} in large platforms) to flag SRM.

### Multi-arm (m variants)

- Same χ² with df = m − 1 and planned proportions p_k:
$$
\chi^2 = \sum_{k=1}^{m} \frac{(n_k - N p_k)^2}{N p_k}
$$

### Triggers/eligibility and exposure

- Test SRM on the analysis population you use for effect (e.g., exposed/eligible users), but also check upstream:
  - Assignment-level SRM (all assigned users)
  - Eligibility-level SRM (eligible)
  - Exposure-level SRM (actually exposed)
Differing passes/fails help localize the issue (assignment vs. eligibility vs. logging).

> [!warning] Sequential monitoring
> Repeated SRM checks inflate false positives. Use stringent thresholds (e.g., p < 10^{-4}) or apply [[sequential testing]] for SRM monitors.

---

## Common root causes

- Randomization/bucketing
  - Non-uniform hash, wrong modulus, missing salt/namespace collisions, sticky bucketing conflicts
- Traffic routing / throttling
  - One arm gated by feature flags, capacity limits, asymmetric rollouts, canary filters
- Identity and deduplication
  - User–device conflation, cross-device instability, bot filters asymmetrically applied
- Eligibility/triggering
  - Eligibility logic differs by arm; triggered analysis includes only treatment-exposed units
- Exposure logging / joins
  - Logging dropped for one arm; late joins; window mismatches; schema changes
- Time windows / seasonality
  - Start/stop misalignment, day-of-week skew affecting one arm, timezone errors
- Geo/cluster constraints
  - Uneven cluster sizes with fixed cluster counts; late enrolling clusters

---

## Triage and remediation

> [!check] Diagnose
> - [ ] Compute SRM at multiple layers: assigned → eligible → exposed → analyzed
> - [ ] Break down by key dimensions: device, browser, geo, app version, time buckets
> - [ ] Inspect ramp logs, feature flags, throttles, outages, and deploys
> - [ ] Verify consistent hashing (seed/salt), namespace isolation, sticky bucketing
> - [ ] Validate identity stability and bot filtering symmetry

> [!wrench] Remediate
> - Fix routing/bucketing/config, relaunch if needed
> - If deterministic imbalance (e.g., uneven cluster sizes), switch to cluster-aware analysis and redesign split
> - If only analysis filtering caused SRM, realign the estimand (ITT vs triggered) and ensure symmetric inclusion rules

> [!warning] Do not “weight your way out”
> Post-hoc weighting to fix SRM can change the estimand and often fails to address underlying bias. Prefer fixing the pipeline/design.

---

## Minimal code snippets

> [!example] R: χ² SRM test (two-arm or multi-arm)

```r
# counts per arm
tab <- table(df$D)                 # D is assignment 0..m-1
N <- sum(tab)
p <- rep(1/length(tab), length(tab))  # planned split; customize if unequal
chisq.test(x = as.numeric(tab), p = p)  # SRM p-value
```

> [!example] Python: χ² SRM test

```python
import numpy as np
from scipy.stats import chisquare

counts = np.bincount(df['D'])       # D in {0,...,m-1}
N = counts.sum()
p = np.ones_like(counts) / len(counts)   # planned split
expected = N * p
res = chisquare(f_obs=counts, f_exp=expected)
print(res.statistic, res.pvalue)
```

> [!example] Stata: χ² SRM test (two-arm 50/50)

```stata
tab D, chi2                // Pearson chi2 test against equal split
```

> [!example] Layered SRM (exposed-only)

```r
# exposed == 1 if user/session actually saw the feature
tab_exp <- table(df$D[df$exposed == 1])
chisq.test(as.numeric(tab_exp), p = p)
```

---

## Thresholds and practice

- At large scale, tiny imbalances become statistically significant; use engineering judgment:
  - Keep a strict p-value threshold for SRM monitoring (e.g., 1e−4 or 1e−5), or
  - Combine with practical imbalance thresholds (e.g., absolute difference > 0.2 pp)
- In small trials, power is low to detect subtle SRM; complement with [[AA test]], balance checks, and pipeline validation.

---

## SRM in special designs

- Cluster/geo experiments
  - Test SRM at cluster-level counts; consider cluster sizes variability—imbalance can be expected if clusters are unequal
- Switchback/time-sliced
  - Imbalance by time block can appear with outages/traffic spikes; test SRM per block and overall
- Multi-armed bandits
  - Allocation is intentionally unequal and adaptive; SRM concept does not apply—ensure analysis matches bandit estimand

---

## Reporting essentials

- Planned split and observed counts (with χ² statistic and p-value)
- Layers tested (assigned/eligible/exposed/analyzed) and which failed/passed
- Breakdowns (device/geo/time) and any co-occurring anomalies (SRM spikes)
- Root cause and fix; decision (pause/restart/continue under watch)
- Link to AA and guardrail dashboards; note any outages/deploys

---

## Common pitfalls

> [!warning]
> - Treating SRM as a minor warning—often it indicates serious bias
> - Testing SRM only on the final analysis cohort, not upstream layers
> - Ignoring time-zone/cycle misalignment (e.g., variant starts hours later)
> - Using per-session analysis with per-user bucketing (unit mismatch)
> - Failing to adjust SRM monitoring for sequential looks
> - Assuming “big N means all good”—χ² flags can be both too sensitive (practically negligible) and life-saving (real misrouting); investigate patterns

---

## Related notes

- [[AB Testing (MOC)]] · [[AA test]] · [[guardrail metric]]
- [[bucketing]] · [[exposure logging]] · [[sequential testing]]
- [[Experimental Design (MOC)]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- [[seasonality]] · [[clustered standard errors]] · [[few-cluster corrections]]