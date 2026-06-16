---
title: Consolidated Standards of Reporting Trials (CONSORT)
aliases: [CONSORT, Consolidated Standards of Reporting Trials, consolidated standards of reporting trials, CONSORT diagram, CONSORT checklist]
tags: [experimentation, reporting, rct, clinical-trials, governance, transparency, flow-diagram]
updated: 2025-09-17
---

# Consolidated Standards of Reporting Trials (CONSORT)

> [!summary] Quick definition
> CONSORT (Consolidated Standards of Reporting Trials) is a set of guidelines and a flow diagram that standardize the transparent reporting of randomized controlled trials (RCTs). It covers trial design, participants, interventions, outcomes, sample size, randomization, blinding, analyses, and harms. The hallmark is the four-stage flow diagram: Enrollment → Allocation → Follow-Up → Analysis.

- Purpose: improve reproducibility, detect bias, and enable critical appraisal and synthesis (meta-analyses).
- Adaptable beyond clinical trials: “CONSORT-style” reporting is useful for field experiments and large-scale [[AB Testing (MOC)]].

---

## Core components

- Title/abstract: identify as randomized; structured summary of design, methods, results, conclusions.
- Introduction: scientific background, rationale, prespecified objectives/hypotheses.
- Methods:
  - Trial design: parallel, cluster, crossover/[[switchback experiment]]; allocation ratio; any changes.
  - Participants: eligibility criteria; settings/locations.
  - Interventions: precisely describe variants (what, when, how long).
  - Outcomes: primary and secondary endpoints with precise definitions and windows; any changes with reasons.
  - Sample size: [[power analysis]] and assumptions; [[Minimum Detectable Effect (MDE)|MDE]] targets.
  - Randomization:
    - Sequence generation (method; random seed/algorithm; blocking/[[stratification]]).
    - Allocation concealment mechanism (e.g., centralized, sealed envelopes, system allocation).
    - Implementation (who generated sequence; who enrolled; who assigned).
  - Blinding/masking: who was blinded (participants, personnel, assessors); how; if not possible, say so.
  - Statistical methods: primary analysis (e.g., ITT); covariate adjustment ([[Analysis of Covariance (ANCOVA)|ANCOVA]]/[[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]); handling of missingness ([[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]); multiplicity control ([[False Discovery Rate (FDR)|FDR]]/FWER); [[sequential testing]] if interim looks; cluster-robust inference in cluster/geo trials.
- Results:
  - Participant flow (CONSORT diagram): numbers screened, eligible, randomized, received intervention, lost to follow-up, analyzed (per arm).
  - Recruitment: dates defining periods of recruitment and follow-up; why trial ended.
  - Baseline data: table of demographics and key covariates by arm.
  - Numbers analyzed: ITT set (all randomized), per-protocol as secondary if used; reasons for exclusions.
  - Outcomes and estimation: effect size with CIs; adjusted/unadjusted; subgroup analyses (prespecified vs exploratory).
  - Harms/adverse events: by arm; severity; stopping for harm.
- Discussion:
  - Limitations: sources of bias/uncertainty, generalizability, adherence, spillovers/interference.
  - Interpretation: balance of benefits/harms; consistency with other evidence.
- Other:
  - Registration: registry ID (e.g., ClinicalTrials.gov/OSF/AEA).
  - Protocol: availability and amendments.
  - Funding: role of funders; competing interests; data/code sharing.

---

## Flow diagram (four stages)

1) Enrollment
   - Assessed for eligibility (n)
   - Excluded (n): not meeting criteria, declined, other
2) Allocation
   - Randomized (n)
   - Allocated to Intervention A (n): received (n), did not receive (n) (reasons)
   - Allocated to Intervention B (n): received (n), did not receive (n) (reasons)
3) Follow-Up
   - Lost to follow-up (n) per arm (reasons)
   - Discontinued intervention (n) per arm (reasons)
4) Analysis
   - Analyzed (n) per arm (and whether ITT); excluded from analysis (n) (reasons)

> [!tip] Cluster/geo/switchback trials
> Use the appropriate CONSORT extensions (cluster/stepped-wedge), and report numbers at both cluster and individual levels. For switchbacks, describe block schedule and adherence.

---

## CONSORT extensions (selected)

- Cluster randomised trials (CONSORT-Cluster)
- Noninferiority/equivalence
- Pragmatic trials
- Harms reporting
- Adaptive/response-adaptive designs
- Pilot/feasibility
- N-of-1 trials
- Stepped-wedge (staggered cluster rollout)
- Equity (CONSORT-Equity), mHealth/eHealth, AI/ML interventions (emerging guidance)

For digital experiments and platform trials, adopt the spirit: report allocation, logging, adherence, guardrails, and bias risks (e.g., [[Sample Ratio Mismatch (SRM)|SRM]], [[leakage]]).

---

## CONSORT-style for product/online experiments

Map clinical items to digital experimentation:
- Randomization & [[bucketing]]: namespace, salt/seed, persistent assignment, ramp schedule.
- Blinding: usually impossible; document mitigations (e.g., guardrails firewalls).
- Outcomes: define [[Overall Evaluation Criterion (OEC)|OEC]] and [[guardrail metric]]s with windows and attribution.
- Harms: latency, errors, churn; non-inferiority margins and stop rules.
- Adherence/compliance: exposure rates; [[exposure logging]]; triggered vs ITT cohorts (pre-registered definitions).
- Interference: network/market effects → [[switchback experiment]] or [[geo experiment]]; report spillover tests.
- Inference: robust/[[clustered standard errors]]; [[few-cluster corrections]] for cluster/switchback; multiplicity ([[False Discovery Rate (FDR)|FDR]]); interim looks ([[sequential testing]]).
- Governance: [[pre-registration]], registration IDs (internal registry), code/data versioning.

---

## Minimal templates

> [!example] CONSORT flow (markdown checklist)

```
Enrollment
- Assessed for eligibility: n=
- Excluded: n= (not meeting criteria= ; declined= ; other= )

Allocation
- Randomized: n=
- Allocated to A: n= ; received A: n= ; did not receive A: n= (reasons)
- Allocated to B: n= ; received B: n= ; did not receive B: n= (reasons)

Follow-Up
- Lost to follow-up (A): n= (reasons)
- Lost to follow-up (B): n= (reasons)
- Discontinued intervention (A/B): n= (reasons)

Analysis
- Analyzed (A): n= ; excluded from analysis: n= (reasons)
- Analyzed (B): n= ; excluded from analysis: n= (reasons)
- Analysis set: ITT primary; per-protocol secondary (if applicable)
```

> [!example] CONSORT-style reporting bullets (digital)

- Randomization: user-level; 50/50; salted SHA256; persistent; ramp 1→5→50%  
- Pre-reg: OSF/AEA registry ID; protocol vX; hypotheses and families; sequential plan  
- Outcomes: OEC (definition, window, unit); guardrails (latency p95 noninferiority +10ms); secondary metrics  
- Variance reduction: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] baseline window; θ estimated on control  
- Inference: robust or clustered SEs (by user/session/geo); FDR (BH) for guardrails  
- Diagnostics: [[AA test]] pass; no [[Sample Ratio Mismatch (SRM)|SRM]]; exposure parity; seasonality coverage  
- Results: ITT effect (Δ, 95% CI), adj/non-adj; guardrails pass/fail; subgroup prespecified vs exploratory  
- Harms/adverse events: summary; stoppage decisions; mitigations  
- Data/code: repo links; reproducible randomization seed; logs schema

---

## Good practice and governance

> [!check]
> - [ ] Follow CONSORT checklist and include diagram  
> - [ ] Use the right extension (cluster, noninferiority, pragmatic, stepped-wedge)  
> - [ ] Align with [[pre-registration]]; declare deviations transparently  
> - [ ] Report ITT primarily; as-treated/per-protocol secondary with caveats  
> - [ ] Include harms/adverse events and stopping decisions  
> - [ ] Provide data/code availability statements and registry IDs

---

## Common pitfalls

> [!warning]
> - Opaque randomization (no sequence/concealment details)  
> - Vague outcome definitions or post-hoc switching  
> - Missing flow diagram or incomplete numbers per arm  
> - Ignoring attrition/missingness (fail to report [[Attrition]] and [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]/imputation)  
> - No multiplicity or sequential control while testing many outcomes/looks  
> - No harms reporting or incomplete adverse event data  
> - For digital trials: failure to report SRM, bucketing, exposure, guardrails, interference

---

## Related notes

- Design/reporting: [[Experimental Design (MOC)]] · [[AB Testing (MOC)]] · [[pre-registration]] · [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]]
- Outcomes/precision: [[Overall Evaluation Criterion (OEC)|OEC]] · [[guardrail metric]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- Integrity/diagnostics: [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[exposure logging]] · [[bucketing]]
- Causal panels/special designs: [[Difference-in-Differences (DiD)]] · [[geo experiment]] · [[switchback experiment]]
- Inference: [[clustered standard errors]] · [[few-cluster corrections]]

---

## References and resources

- CONSORT official: https://www.consort-statement.org/ (checklists, flow diagram, extensions)
- Schulz, Altman, Moher et al. (CONSORT Group) — various updates
- CONSORT extensions (cluster, noninferiority/equivalence, pragmatic, harms, pilot/feasibility, adaptive designs)
- Adaptations for digital experiments (industry best practices, platform experiment registries)

---
