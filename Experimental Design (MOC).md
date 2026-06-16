---
title: Experimental Design (MOC)
aliases: [Experimental Design, RCTs, randomized experiments, experimentation hub]
tags: [moc, causal-inference, experimentation, rct, design, power, interference]
updated: 2025-09-17
---

# Experimental Design (MOC)

> [!summary] Scope
> Planning, running, and analyzing randomized experiments: individual and cluster RCTs, blocking/stratification, factorials, interference-aware designs, power/MDE, variance reduction, sequential testing, reporting, and ethics. Linked to [[Causal Inference (MOC)]] and specialized [[AB Testing (MOC)]].

---

## Quick start

> [!tip] One-page workflow
> 1) Define estimand: [[Intent-to-Treat (ITT)]] vs [[Treatment-on-the-Treated (TOT)]] / [[Average Treatment Effect (ATE)]]  
> 2) Choose unit and method of randomization: individual vs cluster; consider [[stratification]]/blocking  
> 3) Address interference/SUTVA: buffers, [[randomized saturation design]], cluster design  
> 4) Plan sample size/power/MDE; duration (if longitudinal)  
> 5) Pre-register outcomes, analysis, stopping rules; set guardrails and data QA  
> 6) Run and monitor: SRM/A/A where applicable; exposure/logging integrity  
> 7) Analyze: difference-in-means or ANCOVA; cluster-robust SEs; multiplicity control; sensitivity/robustness  
> 8) Report: design, randomization, power, assumptions, diagnostics, harms/benefits, limitations

---

## Core designs

- Individual-level RCT
  - Simple randomization; complete randomization; Bernoulli vs fixed-split
  - Analysis: difference-in-means; [[Analysis of Covariance (ANCOVA)|ANCOVA]] for precision
- Cluster/group randomization
  - Schools, firms, regions, platforms; stepped-wedge (staggered) designs
  - Inference: [[clustered standard errors]]; [[few-cluster corrections]] if small G
- Blocked/Stratified randomization
  - Pre-specify strata (e.g., covariates, geos); randomize within strata
  - Analysis uses [[stratification]]/blocking factors; gains precision
- Factorial and fractional factorial
  - 2^k designs; main effects and interactions; [[split-plot|split-plot constraints]]
- Saturation/network designs
  - [[randomized saturation design]] to estimate direct and spillover effects
  - Network/peer experiments; exposure mapping; partial interference
- Longitudinal/stepped designs
  - Stepped-wedge (randomized rollout over time); crossover (beware carryover)

> [!warning] Interference threats
> Violations of [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]/[[No spillovers]]/[[interference]] require cluster design, buffers, or saturation designs; model exposure if needed.

---

## Estimands and analysis

- ITT, TOT/ATT, and LATE
  - ITT: offer/assignment effect (default causal estimand)
  - Noncompliance: report [[Intent-to-Treat (ITT)]], and optionally [[Local Average Treatment Effect (LATE)|LATE]] via [[Instrumental Variables (IV)]] with [[exclusion restriction]] + [[monotonicity]]
- Primary analysis
  - Difference-in-means; [[Analysis of Covariance (ANCOVA)|ANCOVA]] with pre-treatment covariates/baselines for precision
  - Clustered designs: cluster-level means or unit-level with cluster-robust SEs
- Variance reduction
  - [[stratification]]/blocking; regression adjustment; [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]; re-randomization/optimal design
- Multiplicity
  - Family-wise error or [[False Discovery Rate (FDR)|FDR]]; pre-specify primary vs secondary outcomes
- Sequential/peeking
  - Alpha-spending / group-sequential; [[sequential testing]]; Bayesian sequential (optional)

---

## Interference-aware designs

- Spatial/network exposure
  - Buffers and donut designs; exposure mapping; near/far guardrails
- Saturation and partial interference
  - Vary treated share within clusters to identify spillovers
- Switchbacks/temporal randomization
  - Useful where cross-unit interference is severe; see [[AB Testing (MOC)]]

See: [[No spillovers]] · [[interference]] · [[spillovers]]

---

## Power, sample size, MDE

- Inputs
  - Baseline variance; ICC (intraclass correlation) for clusters; expected effect size; alpha/power; allocation ratio
- Outputs
  - Minimum Detectable Effect (MDE) or required N/clusters
- Tools
  - Analytical formulas (CRD/cluster/block); simulation-based power; cluster-adjusted power
- Design levers
  - Blocking, covariate adjustment (ANCOVA), increased cluster count (more critical than cluster size when ICC>0), longer duration

Links: [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]

---

## Threats and logistics

- SUTVA/interference: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] · [[No spillovers]] · [[interference]]
- Anticipation/novelty and carryover: [[Anticipatory effects]]
- Seasonality and calendar effects: [[seasonality]]; ensure comparable windows
- Data issues: exposure logging, eligibility/triggering, compliance, contamination
- Differential attrition: [[Attrition]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Lee bounds]] if monotone selection plausible
- Ethics and compliance: consent, harms/benefits, stopping for harm, debriefing

---

## Diagnostics and monitoring

- A/A tests and SRM
  - [[AA test|A/A tests]] for pipeline sanity; [[Sample Ratio Mismatch (SRM)|SRM]] to detect allocation mismatches
- Balance checks
  - Covariate balance by arm/strata; exposure rates; missingness patterns
- Event/time diagnostics
  - Pre-period equivalence when available; trend/seasonality checks; contamination monitoring
- Integrity
  - Bucket/hashing stability; unit consistency; triggered vs assigned populations

---

## Reporting essentials

- Design rationale: unit, randomization scheme, blocking/strata, cluster definition
- Power plan: alpha, power, MDE, ICC, assumptions; deviations
- Pre-registration: hypotheses, primary/secondary outcomes, covariates, analysis/stop rules
- Analysis: ITT primary; adjustments; SEs and clustering; multiplicity control
- Diagnostics: A/A, SRM, balance; interference checks; attrition handling
- Results: effects with CIs; harms; subgroup pre-specifications; robustness/sensitivity
- Ethics: consent/deception, data governance, adverse events, debrief
- Reproducibility: code, seeds, versions, randomization reproducibility

---

## Checklists

> [!check] Pre-launch checklist
> - [ ] Estimand defined (ITT/TOT/LATE) and unit of randomization chosen  
> - [ ] Interference assessed; cluster/buffer/saturation if needed  
> - [ ] Blocking/strata selected; randomization reproducible (seeded)  
> - [ ] Power/MDE computed (incl. ICC); duration/window covers a full cycle or controlled seasonality  
> - [ ] Pre-registration: outcomes, covariates, analysis, multiplicity, stopping rules  
> - [ ] Data QA: exposure logging, eligibility/trigger rules, identity stability  
> - [ ] Guardrails and SRM/A/A monitors configured

> [!check] Analysis checklist
> - [ ] ITT primary; noncompliance summarized; IV/LATE only if assumptions plausible  
> - [ ] Difference-in-means and ANCOVA; cluster-robust SEs; stratification accounted for  
> - [ ] Variance reduction documented (CUPED/strata/ANCOVA)  
> - [ ] Multiplicity control for families; sequential adjustments if peeking  
> - [ ] Diagnostics: SRM/A/A, balance, attrition/[[Inverse Probability of Censoring Weighting (IPCW)|IPCW]], interference/near–far, seasonality  
> - [ ] Robustness: alternative windows, pretrend checks, leave-one-cluster-out

---

## Variance reduction and precision

- Covariate adjustment
  - Baseline Y and key X in ANCOVA; pre-treatment means for [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]
- Design-side
  - Blocking/stratification; re-randomization within tolerance
- Analysis-side
  - [[entropy balancing]] or regression weighting if random imbalances arise (use cautiously; preserve ITT)

---

## Multiplicity and sequential testing

- Families and control
  - [[False Discovery Rate (FDR)|FDR]]; Holm/Bonferroni; Westfall-Young
- Sequential/peeking
  - [[sequential testing]]: alpha-spending, Pocock/O’Brien–Fleming boundaries
- Guardrails
  - Pre-specified operational metrics; escalation rules

---

## Special topics

- [[Crossover|Crossover/washout]]; carryover effects
- Stepped-wedge analysis and relation to [[Difference-in-Differences (DiD)]] / [[staggered adoption]]
- Geo-/market-level experiments: link with [[Synthetic Control]], [[event study]], clustered inference
- Network experiments: design with partial interference; exposure mapping; saturation levels

---

## Reading list

- Core: Gerber & Green (Field Experiments); Imbens & Rubin (Causal Inference); List et al. (Field Experiments)
- Practice: Kohavi et al. (Trustworthy Online Controlled Experiments)
- Cluster/stepped wedge: Hayes & Moulton (Cluster Randomised Trials)
- Interference: Hudgens & Halloran; Aronow & Samii (exposure mappings)

---

## Index of topics (A–Z)

- [[AB Testing (MOC)]] · [[AA test]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[Attrition]] · [[Average Treatment Effect (ATE)]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]  
- [[clustered standard errors]] · [[clustering]] · [[composition]] · [[Consolidated Standards of Reporting Trials (CONSORT)|CONSORT]] · [[Crossover]]  
- [[Difference-in-Differences (DiD)]] · [[event study]]  
- [[False Discovery Rate (FDR)|FDR]] · [[factorial design]] · [[few-cluster corrections]]  
- [[Instrumental Variables (IV)]] · [[Intent-to-Treat (ITT)]] · [[interference]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]  
- [[Local Average Treatment Effect (LATE)|LATE]] · [[Lee bounds]] · [[Minimum Detectable Effect (MDE)|MDE]] · [[Manski bounds]] · [[monotonicity]] · [[No spillovers]]  
- [[power analysis]] · [[pre-registration]] · [[placebo test]]  
- [[randomized saturation design]] · [[Regression Discontinuity Design (RDD)]] · [[relevance]]  
- [[seasonality]] · [[sequential testing]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[stratification]] · [[Synthetic Control]] · [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]  
- [[Treatment-on-the-Treated (TOT)]] · [[two-way fixed effects]]
- [[ICC]] · [[response surface methodology]] · [[split-plot]]  

---

## Related hubs

- [[Causal Inference (MOC)]]
- [[AB Testing (MOC)]]
- [[Econometrics (MOC)]]
- [[ML for Econometrics (MOC)]]
- [[Time Series (MOC)]]
