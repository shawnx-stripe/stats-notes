---
title: AB Testing (MOC)
aliases: [A/B Testing (MOC), A/B Testing, AB Testing, A-B Testing, Online Experiments, Controlled Experiments (online)]
tags: [moc, experimentation, ab-testing, online, product, causal-inference, sequential, variance-reduction]
updated: 2025-09-17
---

# AB Testing (MOC)

> [!summary] Scope
> Design, run, and analyze online controlled experiments: unit/bucketing, exposure/triggering, ramping/duration, metrics and guardrails, variance reduction (CUPED/CUPAC), SRM/AA, sequential testing, interference/time effects (switchbacks/geo), heterogeneous effects/uplift, and reporting. Linked to [[Experimental Design (MOC)]] and [[Causal Inference (MOC)]].

---

## Quick start

> [!tip] One-page workflow
> 1) Define OEC/primary metrics and guardrails; set eligibility/exposure rules  
> 2) Choose randomization unit (user/session/device/geo) and bucketing strategy  
> 3) Address interference/time effects (switchback/geo if necessary)  
> 4) Plan ramp/duration and sample size/MDE; pre-register analysis and stopping rules  
> 5) Monitor [[AA test]] and [[Sample Ratio Mismatch (SRM)|SRM]]; ensure exposure logging integrity  
> 6) Analyze ITT with difference-in-means/ANCOVA; use variance reduction (CUPED) if applicable  
> 7) Control multiplicity and sequential peeking; report CIs and guardrails  
> 8) Robustness: time windows, triggered bias, spillovers, heterogeneity; document decisions

---

## Design choices

- Randomization unit
  - User/account, device, session, request; cluster (team/org/geo)
  - Hashing/bucketing for stable assignment; salt and namespace management
- Exposure/triggering
  - Eligibility cohorts; triggered experiments (exposed users only) vs. intent-to-treat populations
  - Log exposure events to avoid dilution bias and miscounting
- Buckets and splits
  - 50/50 vs. skewed allocation; multi-arm tests; persistent bucketing across experiments (collision risk)
- Ramping and duration
  - Gradual traffic ramp; run-time sufficient to cover full cycle [[seasonality]] and latency of effects
- Interference considerations
  - Network/marketplace effects; cross-device; shared resources; queueing; cache effects

See: [[leakage]] · [[triggered analysis]] · [[interference]] · [[No spillovers]]

---

## Metrics, OEC, and guardrails

- OEC (overall evaluation criterion)
  - Composite or single primary outcome aligned with long-run value
- Guardrail metrics
  - Latency, error rates, availability, churn; pre-specified bounds and automatic abort rules
- Metric engineering
  - Ratio metrics (delta method/Fieller), winsorization (with care), transformations (log)
- Variance reduction
  - [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] / [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] (pre-exposure covariates/baselines)
  - Stratification by pre-period performance; re-randomization (with pre-spec)
  - User-level covariate adjustment (ANCOVA)

---

## Analysis and inference

- Primary analysis
  - Difference-in-means; [[Analysis of Covariance (ANCOVA)|ANCOVA]] with pre-period baseline for precision (CUPED)
  - Clustered designs: [[clustered standard errors]]; [[few-cluster corrections]] if small G
  - Ratio metrics: delta method; bootstrap for complex metrics
- Multiple testing
  - Families of metrics: [[False Discovery Rate (FDR)|FDR]] or FWER controls; pre-register primary/secondary metrics
- Sequential/peeking
  - Group sequential/alpha spending; mixture SPRT; Bayesian variants (with caution)
  - See [[sequential testing]]
- Heterogeneity and uplift
  - Pre-specified segments; [[treatment effect heterogeneity]]
  - Uplift/[[policy learning]] ; [[causal forests]] (grf)

---

## Diagnostics and monitoring

- Pre-run/in-run checks
  - [[AA test]]; [[Sample Ratio Mismatch (SRM)|SRM]] detection; bucket hash stability; identity/bot filters
  - Exposure logging correctness; sample contamination or collision
- Balance checks
  - Covariate balance and pre-period outcomes; triggered population vs. ITT mismatches
- Metric quality
  - Seasonality/time-of-day/week effects; holiday/outage periods
  - Novelty/learning and carryover/hangover effects
- Post-run consistency
  - Subsample stability; left/right split checks; placebo metrics

---

## Interference and time effects

- When user-level randomization fails
  - Session/request-level randomization; switchback (time-sliced) designs
  - Cluster/geo randomization with [[Synthetic Control]]/DiD analysis
- Time-aware designs
  - [[switchback experiment]]: alternate treatment/control over time blocks; block sizes vs. auto-correlation
  - Geo experiments: matched markets; SCM/DiD; cluster-robust SEs
- Staggered rollouts
  - Analyze with [[staggered adoption]] methods: [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]
  - Monitor spillovers across cohorts

See: [[seasonality]] · [[Difference-in-Differences (DiD)]] · [[Synthetic Control]]

---

## Ramping, duration, and power

- Power/MDE
  - Baseline variance; expected lift; unit of analysis; cluster ICC if clustered/switchback/geo
- Duration planning
  - Ensure coverage of key calendar cycles; stabilize exposure/eligibility
- Interim looks
  - Pre-specified alpha-spending if peeking; guardrail-driven abort rules

Links: [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]

---

## Common pitfalls

> [!warning]
> - SRM or AA failures ignored; traffic throttling or bucketing bugs  
> - Triggered design analyzed as ITT (or vice versa) without clarity  
> - Interference across users/geos unaddressed; contamination by shared resources  
> - Peeking without sequential control; post-hoc metric shopping (multiple testing)  
> - Ignoring [[seasonality]] or event confounds; run too short  
> - CUPED with post-treatment features (leakage); mis-logged exposure  
> - Clustered designs analyzed with iid SEs; few clusters without corrections

---

## Reporting essentials

- Randomization and unit/bucketing; eligibility/triggering rules; exposure definition
- Ramping plan and achieved durations; SRM/AA diagnostics and resolutions
- Primary/secondary metrics (OEC, guardrails); variance reduction methods (CUPED)
- Analysis choices: difference-in-means/ANCOVA; SEs and clustering; sequential/multiplicity control
- Interference handling (switchback/geo), seasonality alignment
- Results: effect sizes, CIs, guardrails; heterogeneity (pre-specified)
- Robustness: alternative windows, triggered vs. ITT, near–far/exposure, time-of-day
- Decision and rollout plan; deprecations; learnings; reproducibility (hash/seed/code)

---

## Checklists

> [!check] Pre-launch
> - [ ] OEC + guardrails defined; eligibility/triggering pre-specified  
> - [ ] Unit and bucketing chosen; hash stability verified; namespaces reserved  
> - [ ] Interference assessed; switchback/geo if needed  
> - [ ] Power/MDE and run-time planned to cover cycles; ramp strategy set  
> - [ ] Pre-registration (metrics, analysis, sequential rules); dashboards configured  
> - [ ] Data QA for exposure logging, identity, bots; SRM/AA monitors active

> [!check] During run
> - [ ] SRM and AA within thresholds; no asymmetric throttling  
> - [ ] Exposure/eligibility stable; no unexpected traffic shifts  
> - [ ] Guardrails monitored; pause/abort as pre-specified  
> - [ ] Log anomalies (outages, releases, holidays)

> [!check] Analysis
> - [ ] ITT vs triggered population consistent; CUPED covariates pre-exposure  
> - [ ] Proper SEs (cluster if needed); sequential/multiplicity controls applied  
> - [ ] Sensitivity: alternative windows, weekday/weekend, exclusion of outages  
> - [ ] Heterogeneity per pre-spec; uplift policy evaluation if relevant  
> - [ ] Document limitations, interference, seasonality confounds

---

## Special designs

- Multi-armed and bandits
  - Bandit algorithms (epsilon-greedy/Thompson); beware exploration bias and inference
- Marketplace/network experiments
  - Two-sided markets; shadow prices, pacing; interference-aware analysis
- Holdouts and long-term tests
  - Persistent holdouts for model personalization; cohort tracking

---

## Reading list

- Kohavi, Tang, Xu, and Chen (Trustworthy Online Controlled Experiments)
- Deng et al. (CUPED/CUPAC); Johari et al. (Peeking & sequential methods)
- Bakshy & Eckles (Geo experiments); Xu et al. (Switchback and ramping)
- Athey & Imbens (Causal ML); Wager & Athey (Causal forests)

---

## Index of topics (A–Z)

- [[AA test]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[Attrition]] · [[Average Treatment Effect (ATE)]]  
- [[bandits]] · [[bucketing]]
- [[Callaway–Sant’Anna estimator]] · [[clustered standard errors]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]  
- [[Difference-in-Differences (DiD)]] · [[event study]] · [[exposure logging]] · [[False Discovery Rate (FDR)|FDR]] · [[few-cluster corrections]]  
- [[geo experiment]] · [[guardrail metric]]  
- [[interference]] · [[Intent-to-Treat (ITT)]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]  
- [[leakage]] · [[Lee bounds]] · [[Minimum Detectable Effect (MDE)|MDE]] · [[Manski bounds]]  
- [[Overall Evaluation Criterion (OEC)|OEC]] · [[policy learning]] · [[pre-registration]] · [[Prophet]]  
- [[Regression Discontinuity Design (RDD)]] · [[relevance]]  
- [[seasonality]] · [[sequential testing]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[staggered adoption]] · [[stratification]] · [[switchback experiment]] · [[Synthetic Control]] · [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]  
- [[Treatment-on-the-Treated (TOT)]] [[treatment effect heterogeneity]] · [[two-way fixed effects]] · [[uplift]] · [[triggered analysis]]

---

## Related hubs

- [[Experimental Design (MOC)]]
- [[Causal Inference (MOC)]]
- [[Econometrics (MOC)]]
- [[ML for Econometrics (MOC)]]
- [[Time Series (MOC)]]
