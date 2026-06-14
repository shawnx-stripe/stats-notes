---
title: pre-registration
aliases: [preregistration, preanalysis plan, PAP, registered analysis plan, registered report]
tags: [experimentation, causal-inference, reproducibility, governance, ab-testing, power, multiplicity, sequential]
updated: 2025-09-17
---

# pre-registration

> [!summary] Quick definition
> Pre-registration (a pre-analysis plan, PAP) is a time-stamped document created before seeing outcomes (or before unblinding) that specifies the study’s design, hypotheses/estimands, data collection, analysis plan, and decision rules. It separates confirmatory analyses from exploratory work, curbs p-hacking and outcome switching, and improves credibility and reproducibility.

- Applies to: field/lab RCTs, [[AB Testing (MOC)]], [[geo experiment]]s, [[switchback experiment]]s, and observational causal studies (design-anchored prereg).
- Complements: registered reports (peer-reviewed PAP before data collection).

---

## Why pre-register?

- Reduces researcher degrees of freedom (outcomes, windows, subgroups, models).
- Maintains proper Type I error with declared [[False Discovery Rate (FDR)|FDR]]/FWER and [[sequential testing]] plans.
- Clarifies estimands and design choices upfront (ITT vs triggered, cluster level, guardrails).
- Improves institutional memory and auditability (hash/salt seeds, [[bucketing]] namespaces, [[exposure logging]]).

---

## What to pre-register (core components)

1) Study overview
- Title, purpose, short abstract, team, conflicts, governance approvals

2) Design and estimands
- Design: RCT vs cluster vs geo vs switchback; unit of randomization
- Estimands: [[Average Treatment Effect (ATE)]], [[Average Treatment Effect on the Treated (ATT)]], [[Local Average Treatment Effect (LATE)|LATE]] (if IV), policy value (for [[policy learning]])
- SUTVA/interference risk; if present, chosen design (buffers, saturation, switchback)

3) Assignment and bucketing
- Namespace, seed/salt policy, split ratios/remaps, mutual exclusion rules
- Ramp strategy and schedule; sticky assignment guarantees

4) Outcomes and guardrails
- Primary outcome(s) (OEC), exact definitions/units/windows
- Secondary/exploratory metrics; transformation rules (log, winsorization)
- [[guardrail metric]]s, thresholds (non-inferiority/equivalence margins), decision rules

5) Cohorts and windows
- ITT vs triggered definitions; eligibility criteria (strictly pre-exposure)
- Start/stop timestamps, time zones, [[seasonality]] coverage (days-of-week/holidays)
- Exclusions: bots, test traffic, outages; pre-specified blackout windows

6) Variance reduction and covariates
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] or [[Analysis of Covariance (ANCOVA)|ANCOVA]] plans (define baselines; θ estimated on control/pre only)
- Blocks/[[stratification]]; pre-registered subgroup flags; minimum leaf sizes if policy trees

7) Inference and multiplicity
- SEs: robust vs [[clustered standard errors]]; cluster level; [[few-cluster corrections]]
- Multiple testing control: FWER/FDR (BH/BY/weighted/hierarchical), families and α levels
- Sequential plan: group-sequential α-spending or always-valid p-values; stopping rules

8) Power and MDE
- [[power analysis]] inputs (α, 1−β, variance, [[ICC]] for clusters), target [[Minimum Detectable Effect (MDE)|MDE]]
- Allocation ratio; expected N/duration; assumptions and sensitivity

9) Data management
- Logging schemas (assignment, eligibility, exposure, outcomes) and join keys
- Idempotency (impression_id); late-arrival policy; identity resolution
- Privacy/compliance; retention and access controls

10) Analysis details
- Model formulas; fixed effects; covariates; handling missing data ([[Inverse Probability of Censoring Weighting (IPCW)|IPCW]])
- Robustness set: alternative windows, near/far, placebo dates, pre-trend/event-study checks
- For DiD/staggered designs: estimator choice ([[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[drdid]]), clustering, pre-trends

11) Deviations and exploratory work
- How deviations will be documented; separate section for exploratory analyses
- Versioning policy for amendments (time-stamped with rationale)

12) Reproducibility
- Software and versions; seeds; code repos; data versioning (schemas, dictionaries)
- Links to registries and internal artifact locations

---

## Where to pre-register

- Public registries: OSF, AEA RCT Registry (economics), ClinicalTrials.gov (health), AsPredicted (short form)
- Internal registry: org-wide experiment registry or wiki with immutable timestamps
- Registered reports: journal-based prereg with peer review before data collection

---

## Templates

> [!example] Minimal PAP outline (paste and fill)

```markdown
# Study title and ID
- Purpose:
- Design: (unit, randomization, ramp)
- Estimands:
- Primary outcomes:
- Guardrails:

## Assignment & bucketing
- Namespace / seed / split:
- Exclusion groups:

## Cohorts & windows
- ITT definition:
- Triggered definition:
- Start/stop; TZ; seasonality coverage:
- Exclusions/blackouts:

## Variance reduction & covariates
- CUPED/CUPAC: baseline window, θ estimation sample:
- Blocks/strata:

## Inference, multiplicity, sequential
- SEs/clustering:
- Multiplicity control (families, BH/BY/hierarchical):
- Sequential testing plan:

## Power & MDE
- Alpha, power, variance, ICC:
- Expected N/duration:
- MDE targets:

## Data & logging
- Event schemas (assignment, exposure, outcomes):
- Joins and idempotency:
- Privacy/compliance:

## Analysis plan
- Model specs:
- Robustness/diagnostics:
- Deviations handling:

## Reproducibility
- Software versions:
- Code/data locations:
- Registry links:
```

---

## Good practice

> [!check]
> - [ ] Time-stamp before unblinding outcomes; freeze any non-pre features/baselines  
> - [ ] Be specific: metric SQL/definitions, windows, time zones, transformations  
> - [ ] Separate confirmatory vs exploratory; register multiplicity & sequential choices  
> - [ ] Declare clustering and cluster counts; plan for small-G corrections  
> - [ ] Provide power/MDE and ramp schedule; avoid underpowered “peeks”  
> - [ ] Share code templates for logging and assignment reproducibility

---

## Common pitfalls

> [!warning]
> - Vague outcomes (“engagement”) without precise definition  
> - Post-hoc redefining families or margins to pass guardrails  
> - CUPED leakage (θ estimated on treated post data)  
> - Triggered eligibility defined by post-treatment engagement  
> - Ignoring [[seasonality]] or mismatched time zones  
> - No plan for sequential looks → inflated Type I error  
> - Not documenting deviations; blending exploratory with confirmatory

---

## Reporting deviations transparently

- Log any changes (date, reason, expected direction of bias).
- Distinguish “amendments before seeing outcomes” vs “after”.
- Present prereg results first; exploratory analyses clearly labeled.

---

## Relation to other pages

- Design and inference: [[Experimental Design (MOC)]] · [[AB Testing (MOC)]] · [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]]  
- Precision: [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]  
- Cohorts and logging: [[bucketing]] · [[exposure logging]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]]  
- Causal designs: [[Difference-in-Differences (DiD)]] · [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]] · [[drdid]]  
- Governance: privacy/compliance, code/data versioning (internal)

---

## Example confirmatory statements (copy-ready)

- “Primary estimand is the ITT effect on OEC over [start, stop] UTC. We will use difference-in-means with CUPED (baseline = pre-14-day mean), θ estimated on control only, robust SEs clustered by user. We will control FDR at 5% within the guardrail family via BH. One interim look will use Lan–DeMets OBF spending; stopping for harm on guardrail breaches.”

- “For geo experiment ATT, we will use cohort-time DiD (Callaway–Sant’Anna) with clustering by geo and CR2 correction (few clusters). Pre-trends will be assessed via event study. Seasonality will be handled by week and holiday FE. Spillover-prone border geos are excluded a priori.”

---

## FAQs

- Can I amend a prereg? Yes—time-stamp amendments before seeing data relevant to the change; keep an audit trail.
- Do I need prereg for exploratory dashboards? It helps to maintain separate “exploration” tracks and to use [[sequential testing]]/online FDR for streams.
- Does prereg fix bias? No; it makes assumptions and choices transparent and reduces p-hacking. Identification still matters.

---

## Related notes

- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]
- [[sequential testing]] · [[False Discovery Rate (FDR)|FDR]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- [[bucketing]] · [[exposure logging]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]]
- [[Difference-in-Differences (DiD)]] · [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]] · [[drdid]]
- [[leakage]] · [[seasonality]] · [[clustered standard errors]] · [[few-cluster corrections]]

---