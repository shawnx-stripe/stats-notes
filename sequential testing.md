---
title: Sequential Testing
aliases:
- sequential analysis
- group-sequential tests
- continuous monitoring
- Sequential Testing
- Sequential testing
tags:
- experimentation
- sequential
- alpha-spending
- ab-testing
- clinical-trials
- power
- inference
updated: 2025-09-17
---

# Sequential Testing

> [!summary] Quick definition
> Sequential testing lets you analyze accumulating data and stop early for efficacy or futility while controlling Type I error. Two major families:
> - Group-sequential (alpha-spending at pre-planned interim looks)
> - Sequential likelihood/martingale-based tests (e.g., Wald SPRT, mSPRT, always-valid p-values/e-values)

Use to avoid “peeking” inflation in [[AB Testing (MOC)]] and clinical/field experiments.

---

## Why sequential testing?

- Practical: stop early when large effects appear, or stop for futility to save time/cost.
- Statistical: allows interim looks without inflating false positives, unlike naive repeated testing.
- Outputs: stopping boundaries and adjusted inference (p-values/intervals) that are valid under sequential monitoring.

---

## Core approaches

### 1) Group-sequential tests (fixed number/timing of looks)
- Plan K interim looks (including final). Control overall α via:
  - Spending functions (Lan–DeMets), or named boundaries:
    - Pocock: constant, more permissive early stopping
    - O’Brien–Fleming (OBF): very conservative early, liberal late
    - Haybittle–Peto: very stringent early z (≈3), conventional at end
- At look k, compare z-statistic to efficacy/futility boundaries; stop if crossed.
- Compatible with z/t tests, means/proportions, regression (use information fraction).

### 2) Sequential likelihood / martingale tests
- Wald SPRT (Sequential Probability Ratio Test)
  - For simple H0 vs H1, compute likelihood ratio LR_n; stop when LR_n ≥ A (accept H1) or ≤ B (accept H0), where A=(1−β)/α, B=β/(1−α).
- Mixture SPRT (mSPRT)
  - Robust to unknown effect sizes via prior mixing; useful for online A/B.
- Always-valid p-values / e-values
  - Test martingales yield p-values valid under continuous monitoring; form confidence sequences.

---

## Error control and planning

- Familywise α is set once (e.g., 0.05); sequential design ensures global Type I ≤ α across all looks.
- Power planning inflates expected sample size slightly vs. fixed-horizon; expected sample size can be lower if early stopping common.
- Information fraction for looks (e.g., 25/50/75/100%) determines boundaries with an alpha-spending function.

---

## Peeking and stopping rules

> [!warning] Naive peeking inflates Type I error.
> Use one of:
> - Pre-specified group-sequential design (spending function)
> - Always-valid/martingale-based procedures (mSPRT, e-values/SAFE tests)

Stopping rules must be documented pre-launch (or tightly controlled platform defaults).

---

## Typical choices

- Clinical trials: OBF or Pocock with Lan–DeMets spending; efficacy and futility boundaries, DSMB oversight.
- Online experiments: mSPRT / always-valid p-values; or discrete group-sequential checks (daily/weekly) with alpha-spending.
- Geo/switchback: prefer group-sequential at cluster-level; use cluster-robust stats.

---

## Formulas (copy-ready)

- Wald SPRT boundaries (H0: θ=θ0 vs H1: θ=θ1), likelihood ratio LR_n:
$$
\text{Accept H1 if } LR_n \ge \frac{1-\beta}{\alpha},\quad
\text{Accept H0 if } LR_n \le \frac{\beta}{1-\alpha}.
$$

- Alpha-spending (Lan–DeMets):
  - Choose spending function g(t) with t∈[0,1] the information fraction. Cumulative alpha at look k: α_k = g(t_k).
  - Examples:
    - Pocock-like: g_P(t) ≈ α \cdot \log(1 + (e−1)t)
    - OBF-like: g_OBF(t) ≈ 2 − 2Φ(z_{α/2}/√t)

- Always-valid p-values (concept):
  - Construct a nonnegative supermartingale M_t under H0 with E[M_t] ≤ 1; define p_t = 1 / sup_{s≤t} M_s (valid at any stopping time).

---

## Analysis outputs

- Stopping decision at interim k (efficacy/futility/continue).
- Sequentially adjusted p-values and confidence intervals (or confidence sequences).
- Final report includes plan, looks, boundaries, information fractions, stopping rationale.

---

## Sequential testing in AB testing

- Use always-valid p-values (mSPRT/e-values) for continuous monitoring.
- Or run group-sequential checks once per day/week with Lan–DeMets spending.
- Combine with variance reduction ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]) and proper SEs ([[clustered standard errors]] for cluster/session).
- Guard against:
  - [[Sample Ratio Mismatch (SRM)|SRM]] (sample ratio mismatch)
  - [[AA test]] failures
  - Triggered-exposure bias; document [[leakage]]

---

## Practical guidance

> [!check] Design checklist
> - [ ] Choose framework (group-sequential vs. always-valid) and document stopping rules  
> - [ ] Set α, target power 1−β, max sample/looks; pick spending function (Pocock/OBF) or mSPRT prior  
> - [ ] Define information schedule (t_k) or monitoring cadence  
> - [ ] Plan futility rules and minimum run-time (cover [[seasonality]])  
> - [ ] Pre-register metrics, analysis variants, multiplicity handling ([[False Discovery Rate (FDR)|FDR]] if many metrics)

> [!check] Monitoring checklist
> - [ ] Use platform-generated sequential p-values or boundary checks; no ad-hoc peeking  
> - [ ] Log looks and decisions; monitor guardrails  
> - [ ] If using mSPRT, ensure correct variance/overdispersion modeling

---

## Minimal code snippets

> [!example] R: Group-sequential design with gsDesign

```r
# install.packages("gsDesign")
library(gsDesign)
alpha <- 0.05; beta <- 0.2; K <- 4        # 3 interims + final
# Pocock-like spending
gs_poc <- gsDesign(k = K, alpha = alpha, beta = beta, sfu = "Pocock")
# O'Brien-Fleming-like
gs_obf <- gsDesign(k = K, alpha = alpha, beta = beta, sfu = "OF")

gs_poc$upper$bound   # z-boundaries per look
gs_obf$upper$bound
```

> [!example] R: Simple Wald SPRT (means with known σ; illustration)

```r
sprt_mean <- function(x, mu0, mu1, sigma, alpha=0.05, beta=0.2){
  A <- (1 - beta) / alpha
  B <- beta / (1 - alpha)
  lr <- 1
  for (n in seq_along(x)){
    # Gaussian LR increment
    inc <- exp( ( (mu1 - mu0) * (x[n] - (mu0 + mu1)/2) ) / (sigma^2) )
    lr <- lr * inc
    if (lr >= A) return(list(decision="Accept H1", n=n, LR=lr))
    if (lr <= B) return(list(decision="Accept H0", n=n, LR=lr))
  }
  list(decision="Continue", n=length(x), LR=lr)
}
```

> [!example] Python: Pocock-like alpha spending (illustrative)

```python
import numpy as np
from scipy.stats import norm

alpha = 0.05
t = np.array([0.25, 0.5, 0.75, 1.0])  # information fractions
# Pocock-like cumulative spending (approx)
alpha_cum = alpha * np.log(1 + (np.e - 1) * t)
alpha_inc = np.diff(np.insert(alpha_cum, 0, 0.0))
z_bounds = norm.isf(alpha_inc / 2.0)   # two-sided efficacy z per look (illustrative)
```

---

## Multiplicity and families

- If monitoring multiple primary metrics, pre-specify a gatekeeping or [[False Discovery Rate (FDR)|FDR]] strategy.
- Per-look alpha allocation can be split across metrics (hierarchical spending) or combined via combination tests.

---

## Confidence sequences (always-valid intervals)

- Provide intervals valid at all times under continuous monitoring.
- Construct via nonparametric or parametric test martingales; widths shrink with t.
- Useful for dashboards with “stop when CS excludes zero” logic.

---

## Common pitfalls

> [!warning]
> - “Peeking” without a sequential method → inflated false positives  
> - Post-hoc changing #looks/spending after seeing data  
> - Mis-specified variance in mSPRT (heavy tails/overdispersion) → invalid p-values  
> - Treating daily correlated looks as iid; mismatched information fractions  
> - Using iid SEs in cluster/switchback/geo designs (need [[clustered standard errors]])  
> - Ignoring [[seasonality]]/calendar when deciding minimum runtime

---

## Reporting essentials

- Design: framework (group-seq vs. always-valid), α, power, max N, looks/monitoring cadence
- Boundaries: spending function; z/p boundaries per look; futility criteria
- Decision log: looks taken, statistics, decisions and rationale
- Final inference: adjusted p-value/CI or confidence sequence
- Deviations: any changes from plan and justifications
- Reproducibility: code, seeds, software versions

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[False Discovery Rate (FDR)|FDR]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[seasonality]]
- [[clustered standard errors]] · [[few-cluster corrections]]
- [[Difference-in-Differences (DiD)]] (for staggered rollouts) · [[Synthetic Control]]

---
