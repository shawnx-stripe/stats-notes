---
title: Causal Inference (MOC)
aliases:
  - Causal Inference
  - CI hub
  - Causal Inference (MOC)
tags:
  - moc
  - causal-inference
  - econometrics
  - design
  - diagnostics
updated: 2025-09-17
---

# Causal Inference (MOC)

> [!summary] Scope
> Designs, estimands, estimators, assumptions, diagnostics, and reporting for empirical causal analysis in economics and data science.

---

## Quick start

> [!tip] One-page workflow
> 1) Pick a design: [[quasi-experimental design]] → [[Difference-in-Differences (DiD)]] / [[Regression Discontinuity Design (RDD)]] / [[Instrumental Variables (IV)]] / [[Synthetic Control]]  
> 2) Define estimand: [[Average Treatment Effect (ATE)]] vs [[Average Treatment Effect on the Treated (ATT)]] vs [[Local Average Treatment Effect (LATE)|LATE]]  
> 3) Check assumptions: [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[Unconfoundedness]]/[[parallel trends assumption]]/[[exclusion restriction]]/[[relevance]]/[[monotonicity]]  
> 4) Choose estimator: [[Inverse Probability Weighting (IPW)|IPW]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[two-way fixed effects]] · [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]]  
> 5) Diagnose: [[event study]] · [[pre-trends]] · [[placebo test]]  
> 6) Inference: [[clustered standard errors]] · [[few-cluster corrections]]  
> 7) Robustness: alternative controls/windows/specs; sensitivity/bounds ([[Lee bounds]] · [[Manski bounds]])  
> 8) Report: design, assumptions, diagnostics, estimator, clustering, limitations

---

## Design selection

- Randomized/encouragement
  - [[Intent-to-Treat (ITT)]] · [[noncompliance]] → [[Instrumental Variables (IV)|IV]] / [[Local Average Treatment Effect (LATE)|LATE]]
- Time and groups
  - [[Difference-in-Differences (DiD)]] · [[two-way fixed effects]]
  - [[staggered adoption]]: [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]] · [[group-time average treatment effect]]
- Threshold/score
  - [[Regression Discontinuity Design (RDD)]] (sharp/fuzzy) · [[fuzzy RDD]]
- Single unit / few units over time
  - [[Synthetic Control]] · augmented/synth-DiD
- When no obvious shock/design
  - [[quasi-experimental design]] with [[Unconfoundedness]] + [[propensity score]] tools

> [!warning] Design pitfalls
> - TWFE with heterogeneous effects and staggered timing → see [[staggered adoption]] and [[Goodman–Bacon decomposition]]
> - Border settings with spillovers → consider [[boundary discontinuity]] and [[Conley standard errors]]

---

## Estimands

- Population
  - [[Average Treatment Effect (ATE)]]
  - [[Average Treatment Effect on the Treated (ATT)]] / [[Treatment-on-the-Treated (TOT)]]
- Compliance local effect
  - [[Local Average Treatment Effect (LATE)|LATE]] (via [[Instrumental Variables (IV)|IV]] with [[exclusion restriction]], [[relevance]], [[monotonicity]])

---

## Assumptions (index)

- General
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]] · [[No spillovers]] / [[interference]] / [[spillovers]]
- Selection-on-observables pathway
  - [[Unconfoundedness]] · [[Overlap]]
- DiD pathway
  - [[parallel trends assumption]] · [[Anticipatory effects]] · [[seasonality]] · [[composition]]
- IV pathway
  - [[exclusion restriction]] · [[relevance]] · [[monotonicity]]
- RD pathway
  - Continuity, no precise manipulation; see [[Regression Discontinuity Design (RDD)]]

---

## Estimators and weighting

- Propensity/weights
  - [[propensity score]] · [[Inverse Probability Weighting (IPW)|IPW]] · [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Doubly Robust estimators]] · [[entropy balancing]] · [[stratification]] · [[matching]]
- DiD-family
  - [[DiD estimator]] · [[two-way fixed effects]] · [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]] · [[group-time average treatment effect]]
  - Alternatives/aux: [[Borusyak–Jaravel–Spiess (imputation)]] · [[Gardner DID2S]] · [[Triple Differences (DDD)|DDD]] / [[triple differences]]
- Single/few treated units
  - [[Synthetic Control]] (and augmented/synth-DiD)
- IV-family
  - [[Instrumental Variables (IV)]] · [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[Local IV]] · [[weak instruments]]

---

## Diagnostics and robustness

- Trend/dynamics
  - [[event study]] · [[pre-trends]] · [[placebo test]]
- Inference/SEs
  - [[clustered standard errors]] · [[clustering]] · [[few-cluster corrections]] · [[wild cluster bootstrap]] · [[Conley standard errors]]
- Selection and missingness
  - [[selection bias]] · [[Attrition]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Lee bounds]] · [[Manski bounds]]
- Panel/data pitfalls
  - [[composition]] · [[seasonality]] · [[Moulton problem]]

> [!check] Minimal diagnostic list
> - Pre-treatment trends similar?  
> - Placebo dates/units null?  
> - Covariate/PS balance and overlap OK?  
> - Spillovers/anticipation addressed?  
> - SEs clustered at assignment level; small-G handled?  
> - Robust to alt. windows/specs/controls?

---

## Reporting essentials

- Design and timing (who/when/where/how)
- Estimand (ATE/ATT/LATE) and population
- Identification assumptions and why plausible
- Diagnostics (plots/tests) and robustness
- Estimator details (weights, learners for PS/OR), clustering level, number of clusters
- Limitations (external validity, threats not ruled out)

> [!example] Reproducible skeleton
> - Design: [[Difference-in-Differences (DiD)]] with [[staggered adoption]]  
> - Estimand: [[Average Treatment Effect on the Treated (ATT)]] aggregated from [[group-time average treatment effect]]  
> - Assumptions: [[parallel trends assumption]] (conditional on [[covariates]]), no [[spillovers]], no strong [[Anticipatory effects]]  
> - Estimator: [[Callaway–Sant’Anna estimator]] (DR-IPW), cohort-time aggregation  
> - Inference: [[clustered standard errors]] by region; [[few-cluster corrections]] if G<30  
> - Diagnostics: [[event study]] with pre-leads ~ 0; [[placebo test]]; balance/overlap checks  
> - Robustness: alternative donor sets; narrower windows; seasonality controls; bounds if attrition ([[Lee bounds]])

---

## Building blocks and glossary

- Units and roles: [[treated group]] · [[control group]]
- Heterogeneity/dynamics: [[treatment effect heterogeneity]] · [[group-time average treatment effect]] · [[staggered adoption]]
- Sensitivity/bounds: [[Manski bounds]] · [[Lee bounds]]
- Common add-ons: [[Goodman–Bacon decomposition]] · [[boundary discontinuity]] · [[Conley standard errors]] · [[Moulton problem]]

---

## Method maps

- DiD universe
  - Classic: [[DiD estimator]] / [[two-way fixed effects]]  
  - Staggered-safe: [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]]  
  - Imputation/2-stage: [[Borusyak–Jaravel–Spiess (imputation)]] · [[Gardner DID2S]]
- IV universe
  - [[Instrumental Variables (IV)]] → [[exclusion restriction]] · [[relevance]] · [[monotonicity]] → [[Local Average Treatment Effect (LATE)|LATE]]  
  - Strength/robustness: [[weak instruments]] (KP/MOP tests), [[Anderson–Rubin]]
- RDD universe
  - [[Regression Discontinuity Design (RDD)]]: density/balance tests, local polynomial, RBC inference; [[fuzzy RDD]]
- Weighting/DR universe
  - [[propensity score]] → [[Inverse Probability Weighting (IPW)|IPW]] / [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] / [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]  
  - Deterministic balance: [[entropy balancing]]  
  - Stratified: [[stratification]]

---

## Checklists

> [!check] DiD pre-commit checklist
> - [ ] Define cohorts (G) and event time; set reference period  
> - [ ] Choose never vs. not-yet-treated controls  
> - [ ] Include time FE and seasonality; consider covariate×time interactions  
> - [ ] Plot event-study leads/lags with CIs  
> - [ ] Cluster SEs properly; address small G  
> - [ ] Robustness: alt. windows/controls; placebo dates; near/far (spillovers)

> [!check] IV pre-commit checklist
> - [ ] Exclusion channels enumerated and argued away  
> - [ ] First-stage strength (KP/MOP F) reported  
> - [ ] Monotonicity plausible; LATE interpretation clear  
> - [ ] Placebo outcomes/pre-periods clean  
> - [ ] Overid tests (if applicable) with caveats

> [!check] Unconfoundedness/weighting
> - [ ] Covariates pre-treatment only; PS model flexible  
> - [ ] Overlap/weights stable; ESS acceptable; trimming rules set  
> - [ ] Post-weighting balance (SMDs) acceptable  
> - [ ] DR estimator (AIPW/TMLE) planned; cross-fitting if ML

---

## Common pitfalls

> [!warning]
> - Using all treated as controls after they’re treated (TWFE contamination)  
> - Treating covariates as a fix for violated identification assumptions  
> - Ignoring few-cluster issues or clustering at the wrong level  
> - Conditioning on post-treatment variables (see [[bad controls]])  
> - Overinterpreting overid tests as proof of validity  
> - Neglecting [[seasonality]] and calendar effects

---

## Reading list

- Core texts: [[Angrist and Pischke]] · [[Imbens and Rubin]] · [[Hernán and Robins]] · [[Cunningham (Mixtape)]]
- DiD modern: CS, SA, BJS, Goodman–Bacon (see corresponding pages)
- RDD/SCM: Imbens–Lemieux; Abadie et al.; CCT RBC methods
- IV/Weak IV: Stock–Yogo; KP/MOP; Anderson–Rubin

---

## Related hubs

- [[Econometrics (MOC)]]
- [[Time Series (MOC)]]

---

## Index of pages (A–Z)

- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] · [[Anticipatory effects]] · [[Attrition]] · [[Average Treatment Effect (ATE)]] · [[Average Treatment Effect on the Treated (ATT)]]  
- [[bad controls]] · [[Borusyak–Jaravel–Spiess (imputation)]]  
- [[Callaway–Sant’Anna estimator]] · [[clustering]] · [[clustered standard errors]] · [[composition]] · [[Conley standard errors]]  
- [[Triple Differences (DDD)|DDD]] · [[Difference-in-Differences (DiD)]] · [[DiD estimator]] · [[double machine learning]] · [[Doubly Robust estimators]]  
- [[entropy balancing]] · [[event study]] · [[exclusion restriction]]  
- [[few-cluster corrections]] · [[fuzzy RDD]]  
- [[Gardner DID2S]] · [[Goodman–Bacon decomposition]] · [[group-time average treatment effect]]  
- [[Instrumental Variables (IV)]] · [[Intent-to-Treat (ITT)]] · [[interference]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] · [[Inverse Probability Weighting (IPW)|IPW]]  
- [[Local Average Treatment Effect (LATE)|LATE]] · [[Lee bounds]] · [[Limited Information Maximum Likelihood (LIML)|LIML]] · [[Local IV]]  
- [[matching]] · [[Manski bounds]] · [[monotonicity]] · [[Moulton problem]]  
- [[noncompliance]] · [[No spillovers]]  
- [[Overlap]]  
- [[parallel trends assumption]] · [[placebo test]] · [[potential outcomes]] · [[propensity score]] · [[pre-trends]]  
- [[Regression Discontinuity Design (RDD)]] · [[relevance]]  
- [[seasonality]] · [[selection bias]] · [[spillovers]] · [[staggered adoption]] · [[stratification]] · [[Sun–Abraham estimator]] · [[Synthetic Control]] · [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]  
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]] · [[Treatment-on-the-Treated (TOT)]] · [[treated group]] · [[control group]] · [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]] · [[two-way fixed effects]]
- [[weak instruments]] · [[wild cluster bootstrap]]
- [[Average Treatment Effect on the Untreated (ATU)|ATU]] · [[Interrupted Time Series (ITS)]] · [[Propensity Score Matching (PSM)]] · [[causal DAGs]] · [[collider bias]] · [[common support]] · [[compliers]] · [[defiers]] · [[fuzzy DiD]] · [[g-formula]] · [[mediation analysis]] · [[never-takers]] · [[post-treatment conditioning]] · [[principal stratification]] · [[sequential ignorability]]  

---

> [!info] Status
> This hub links to living notes. Pages marked “placeholder” are stubs to be filled as needed.