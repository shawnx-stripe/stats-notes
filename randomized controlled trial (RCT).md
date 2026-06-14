---
title: randomized controlled trial (RCT)
aliases: [RCT, randomized clinical trial, randomized trial, cluster randomization]
tags: [experimentation, causal-inference, clinical-trials, design, randomization, power, compliance, cluster, crossover, factorial, stepped-wedge]
updated: 2025-09-25
---

# Randomized controlled trial (RCT)

> [!summary] Quick definition
> An RCT assigns eligible units to interventions at random to estimate causal effects with high internal validity. Key pillars: proper randomization and allocation concealment, blinding where possible, pre-registration and protocol adherence, adequate power, intention-to-treat analysis, and transparent reporting (see [[Consolidated Standards of Reporting Trials (CONSORT)|CONSORT]]). Variants include individually randomized, cluster-randomized, factorial, crossover, and stepped-wedge designs.

- Goals: unbiased estimation of treatment effects; decision-making about efficacy, safety, and implementation.
- Related: [[Experimental Design (MOC)]], [[Causal Inference (MOC)]], [[AB Testing (MOC)]], [[randomization inference]], [[Analysis of Covariance (ANCOVA)|ANCOVA]], [[clustered standard errors]], [[few-cluster corrections]], [[wild cluster bootstrap]].

---

## Core components

- Randomization
  - Unit of randomization: individual, household, clinic, school, site, time-block (see [[switchback experiment]] for online contexts)
  - Scheme: simple, permuted blocks (variable sizes), stratified/blocking, covariate-adaptive (minimization), covariate-constrained re-randomization
- Allocation concealment
  - Prevent foreknowledge of the next assignment (centralized randomization, opaque sealed envelopes, secure IVRS/IWRS)
- Blinding (masking)
  - Participant, caregiver, outcome assessor, analyst; use placebos/sham where ethical/feasible
- Outcomes
  - Pre-specify primary outcome(s), key secondary outcomes, safety endpoints; define measurement timing and adjudication
- Protocol and registration
  - Pre-register (ClinicalTrials.gov/OSF); publish SAP; ethics approval and DSMB for monitoring
- Analysis principle
  - Intention-to-treat (ITT) primary; prespecified per-protocol and as-treated analyses as sensitivity

---

## Design variants

- Individually randomized parallel-group
  - 1:1 (or unequal) allocation; baseline covariate balance improved by stratification/blocking
- Cluster-randomized trials (CRTs)
  - Randomize clusters (e.g., hospitals, schools). Account for ICC in design and analysis; consider [[spillovers]] and partial interference; see [[randomized saturation design]] for network settings
- Factorial trials (2×2, etc.)
  - Efficiently test multiple interventions; watch interaction vs main effects; see [[factorial design]]
- Crossover trials
  - Each participant receives multiple treatments in sequence with washout; analyze within-subject contrasts; beware carryover; see [[Crossover]]
- Stepped-wedge (staggered rollout)
  - Clusters cross from control to treatment over time; analyze with mixed models/[[staggered adoption]] estimators
- Pragmatic vs explanatory
  - Pragmatic: real-world effectiveness; Explanatory: efficacy under ideal conditions; influences eligibility, flexibility, and outcomes

---

## Sample size and power

- Continuous outcome, two-arm, equal allocation (known σ):
$$
n_{\text{per arm}} \;=\; \frac{2\sigma^2\left(z_{1-\alpha/2} + z_{1-\beta}\right)^2}{\delta^2}
$$
where δ is the minimally important difference.
- Binary outcome (proportions p0, p1):
$$
n_{\text{per arm}} \;=\;
\frac{\left[z_{1-\alpha/2}\sqrt{2\bar p(1-\bar p)} + z_{1-\beta}\sqrt{p_0(1-p_0)+p_1(1-p_1)}\right]^2}{(p_1-p_0)^2},
\quad \bar p=\tfrac{p_0+p_1}{2}
$$
- Cluster design effect (inflate n):
$$
\text{DE} \;=\; 1 + (m-1)\rho, \qquad n_{\text{required}} \;=\; n_{\text{iid}}\times \text{DE}
$$
where m is average cluster size and ρ the ICC.
- Variance reduction
  - Baseline adjustment (ANCOVA) increases power; stratification/blocking improves balance; pre-specify covariates

Links: [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]

---

## Analysis

- Primary estimand: ITT average effect of assignment
  - Continuous: difference in means; ANCOVA adjusting for baseline outcome and stratification factors ([[Analysis of Covariance (ANCOVA)|ANCOVA]])
  - Binary: difference in proportions, risk ratio/odds ratio via GLM (identity/log/logit links)
  - Time-to-event: Kaplan–Meier/Cox model (report HR and CIs)
- Cluster RCTs
  - Use mixed-effects models or cluster-aggregated analyses with [[clustered standard errors]]; consider [[few-cluster corrections]]/[[wild cluster bootstrap]] when clusters are few
- Multiplicity
  - Control FWER/FDR across multiple outcomes/looks; pre-specify primary outcomes and families (see [[multiple testing control]], [[False Discovery Rate (FDR)|FDR]], [[sequential testing]])
- Randomization inference
  - Exact/permutation p-values and CIs leveraging the randomization scheme; complements model-based analysis ([[randomization inference]])
- Missing data and intercurrent events
  - Prefer ITT with appropriate imputation/sensitivity; use MI, [[Inverse Probability Weighting (IPW)|IPW]]/[[Inverse Probability of Censoring Weighting (IPCW)|IPCW]], or model-based approaches; document deviations

---

## Noncompliance and estimands

- ITT vs as-treated vs per-protocol
  - ITT preserves randomization; as-treated/per-protocol can be biased if departures relate to outcomes
- Instrumental variables (assignment Z as instrument for received treatment D) for LATE among compliers ([[Instrumental Variables (IV)|IV]], [[Local Average Treatment Effect (LATE)|LATE]])
$$
\widehat{\text{LATE}}
\;=\;
\frac{\mathbb{E}[Y\mid Z=1]-\mathbb{E}[Y\mid Z=0]}
{\mathbb{E}[D\mid Z=1]-\mathbb{E}[D\mid Z=0]}
$$
Assumptions: relevance, exclusion, monotonicity; report [[Treatment-on-the-Treated (TOT)]] where relevant; see [[noncompliance]]

---

## Bias and validity threats

- Allocation concealment failures → selection bias
- Blinding failures → performance and ascertainment bias
- Attrition/missing outcomes → bias; see [[Attrition]], use sensitivity analyses (e.g., [[Lee bounds]] for truncation)
- Contamination and interference → bias ITT estimates; design for minimal cross-arm spillovers (see [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[No spillovers]], [[interference]])
- Post-randomization changes and protocol deviations → define strategies for intercurrent events (treatment policy, hypothetical, composite, etc.; see ICH E9(R1))

---

## Interim monitoring and stopping

- Data monitoring
  - DSMB oversight; pre-specified interim looks for efficacy/futility/harm
- Methods
  - Group-sequential designs (O’Brien–Fleming, Pocock), alpha spending, Bayesian monitoring with posterior odds/Bayes factors
- Reporting
  - Document boundaries, timing, and decisions; adjust for multiplicity across looks (see [[sequential testing]], [[Bayesian Testing]])

---

## Outcomes and reporting

- Define and justify primary/secondary endpoints; avoid post-hoc switching
- Use standardized effect sizes and 95% CIs; report absolute and relative effects
- Harms and safety endpoints with appropriate multiplicity handling
- Follow [[Consolidated Standards of Reporting Trials (CONSORT)|CONSORT]] checklist and flow diagram; share protocol, SAP, and deviations

---

## Ethical considerations

- Equipoise and scientific merit; favorable risk–benefit
- Informed consent; special populations safeguards
- Early stopping for harm/overwhelming benefit; access to effective treatment
- Transparency: registration, data sharing, and publication of negative results

---

## Practical checklists

> [!check] Planning and setup
> - [ ] Eligibility criteria, setting, and recruitment strategy  
> - [ ] Randomization unit and scheme (stratification factors, block sizes)  
> - [ ] Allocation concealment mechanism and blinding plan  
> - [ ] Primary outcome(s), timing, and measurement; SAP drafted and registered ([[pre-registration]])  
> - [ ] Power/MDE with ICC if clustered; variance reduction via baseline covariates  
> - [ ] Data capture, QA, and monitoring; DSMB charter and interim plan; ethics approval

> [!check] Conduct
> - [ ] Adherence monitoring and protocol deviation logging  
> - [ ] Maintain concealment/blinding; audit unblinding events  
> - [ ] Track attrition, crossovers, and exposure; predefine handling of intercurrent events  
> - [ ] Record adverse events and guardrails ([[guardrail metric]])

> [!check] Analysis and reporting
> - [ ] ITT primary; prespecified covariate adjustment; matching analysis to estimand  
> - [ ] Correct SEs (cluster-robust/mixed models), multiplicity, and interim adjustments  
> - [ ] Sensitivity: as-treated/per-protocol, IV/LATE for noncompliance, missing-data scenarios  
> - [ ] CONSORT flow, effect sizes with CIs, harms, limitations, and reproducibility

---

## Connections and contrasts

- RCT vs [[AB Testing (MOC)]]
  - AB tests are online RCTs with high velocity, often focusing on short-term outcomes and operational guardrails; both rely on randomization but differ in setting and logistics
- RCT vs observational causal studies
  - RCTs avoid confounding by design; observational studies require assumptions and methods ([[Unconfoundedness]], [[double machine learning]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]])

---

## Related notes

- Identification and assumptions: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] · [[No spillovers]] · [[interference]]  
- Noncompliance and estimands: [[Intent-to-Treat (ITT)]] · [[Treatment-on-the-Treated (TOT)]] · [[Instrumental Variables (IV)]] · [[Local Average Treatment Effect (LATE)|LATE]] · [[noncompliance]]  
- Design and analysis: [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]] · [[randomization inference]] · [[clustered standard errors]] · [[few-cluster corrections]] · [[wild cluster bootstrap]]  
- Designs: [[factorial design]] · [[Crossover]] · [[randomized saturation design]] · [[staggered adoption]]

---

## References

- Schulz, Altman, & Moher (CONSORT Group). CONSORT 2010 Statement (and extensions).  
- ICH E9 (1998) and E9(R1) (2019): Statistical Principles and Estimands for Clinical Trials.  
- Pocock (1983/2013). Clinical Trials: A Practical Approach.  
- Friedman, Furberg, & DeMets (2010). Fundamentals of Clinical Trials.  
- Rosenberger & Lachin (2016). Randomization in Clinical Trials: Theory and Practice.  
- Jennison & Turnbull (2000). Group Sequential Methods with Applications to Clinical Trials.  
- Hayes & Moulton (2009). Cluster Randomised Trials.  
- Hussey & Hughes (2007). Design and analysis of stepped wedge cluster randomized trials.

---
