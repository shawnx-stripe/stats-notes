---
title: Identification Strategies (MOC)
aliases:
  - Identification in causal inference
  - Causal identification (MOC)
  - ID strategies
tags:
  - MOC
  - causal-inference
  - identification
  - quasi-experimental
  - econometrics
updated: 2025-09-26
---

# Identification Strategies (MOC)

> [!summary] Start here
> Identification is about turning assumptions plus design into causal estimands. This MOC organizes the main strategies—randomization, selection on observables, instruments, discontinuities, and panels—along with their assumptions, diagnostics, and links to estimation and inference.

Related starting points:
- Foundations: [[Causal Inference (MOC)]], [[Econometrics (MOC)]], [[Experimental Design (MOC)]]
- Estimation and ML: [[Machine Learning for Causal Inference (MOC)]]
- Inference: [[Standard Errors and Inference (MOC)]]
- Complications: [[Missing Data and Selection (MOC)]], [[Spillovers and Interference (MOC)]]

## What “identification” means

- Target an estimand (e.g., [[Average Treatment Effect (ATE)]], [[Average Treatment Effect on the Treated (ATT)|ATT]], [[Local Average Treatment Effect (LATE)|LATE]], [[marginal treatment effect (MTE)]]).
- Specify assumptions that make it a function of observables.
- Choose a design/strategy that makes the assumptions plausible.
- Then select estimators and inference methods.

Core cross-cutting assumptions:
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]: well-defined treatment and [[No spillovers]]/[[interference]].
- [[Unconfoundedness]] (selection on observables) + [[Overlap]].
- [[exclusion restriction]], [[relevance]], and [[monotonicity]] for IV/LATE.
- Continuity/no manipulation for [[Regression Discontinuity Design (RDD)]].
- [[parallel trends assumption]] (and stable composition) for [[Difference-in-Differences (DiD)]].
- Integrity of randomization for [[randomized controlled trial (RCT)]].

## Strategy catalog

### 1) Randomized experiments
- Designs: [[randomized controlled trial (RCT)]], clustered RCTs, [[randomized saturation design]], [[switchback experiment]], [[geo experiment]].
- Estimands: ITT ([[Intent-to-Treat (ITT)]]), [[Treatment-on-the-Treated (TOT)]] via compliance, ATE in target sample.
- Assumptions: Proper randomization, compliance mechanism, SUTVA.
- Diagnostics: [[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]], balance tests, protocol adherence, attrition ([[Attrition]]) analysis.
- Notes: With noncompliance ([[noncompliance]]), use IV/encouragement at assignment level; report both ITT and TOT.

### 2) Selection on observables (unconfoundedness)
- Statement: [[Unconfoundedness]] + [[Overlap]] identify ATE/ATT via adjustment.
- Tools: [[propensity score]], [[matching]], [[entropy balancing]], [[Inverse Probability Weighting (IPW)|IPW]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]; ML via [[double machine learning]].
- Diagnostics: Balance before/after weighting, overlap/common support, sensitivity to model choices, placebo outcomes.
- Pitfalls: [[bad controls]] (post-treatment, colliders), poor overlap, extrapolation.

### 3) Instrumental variables (IV)
- Use when unobservables confound treatment.
- Assumptions: [[relevance]] (strong first stage), [[exclusion restriction]], independence; [[monotonicity]] for [[Local Average Treatment Effect (LATE)|LATE]].
- Estimands: [[Local Average Treatment Effect (LATE)|LATE]] (binary Z), [[Local IV]] and [[marginal treatment effect (MTE)]] with continuous/strong Z; [[fuzzy RDD]] as IV at cutoff.
- Diagnostics: First-stage strength ([[weak instruments]]), overidentification (if applicable), heterogeneity interpretation (LATE vs ATE).
- Minimal link: [[Instrumental Variables (IV)]], [[Wald estimator]].

### 4) Regression discontinuity (RD)
- Designs: [[Regression Discontinuity Design (RDD)]] with [[sharp RDD]] and [[fuzzy RDD]]; variants: fuzzy kink/geographic.
- Assumptions: Continuity of potential outcomes at cutoff; no precise manipulation (density [[McCrary test]]/[[density test]]).
- Estimands: Local effect at cutoff; with fuzziness, Wald ratio at cutoff (local [[Local Average Treatment Effect (LATE)|LATE]]).
- Diagnostics: [[bandwidth selection]], [[local linear regression]]/[[local polynomial regression]], covariate continuity, donut/buffer checks, multiple bandwidths.

### 5) Difference-in-Differences (DiD) and panels
- Baseline: [[Difference-in-Differences (DiD)]] with [[two-way fixed effects]].
- Assumptions: [[parallel trends assumption]], stable composition, no anticipation/[[Anticipatory effects]], no differential [[spillovers]].
- Modern staggered adoption: [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], report [[group-time average treatment effect]]s; package [[drdid]].
- Diagnostics: [[pre-trends]], [[event study]] plots (leads/lags), alternative controls/time windows, composition checks.
- Extensions: Synthetic control ([[Synthetic Control]]) when few treated units; hybrid DiD–SC.

### 6) Bounds and partial identification
- When assumptions are weak or MNAR/selection is severe.
- Methods: [[Manski bounds]] (worst-case), [[Lee bounds]] (monotone selection), monotone treatment response.
- Use to report identification regions rather than point estimates.

## Assumptions → estimands (minimal statements)

- Unconfoundedness for ATE:
$$
(Y_1,Y_0) \perp D \mid X, \quad 0 < P(D=1\mid X) < 1 \Rightarrow \text{ATE} = \mathbb{E}\big[m_1(X)-m_0(X)\big]
$$

- IV/Wald for LATE:
$$
\text{LATE} = \frac{\mathbb{E}[Y\mid Z=1]-\mathbb{E}[Y\mid Z=0]}{\mathbb{E}[D\mid Z=1]-\mathbb{E}[D\mid Z=0]}
$$

- Local IV / MTE:
$$
\text{MTE}(x,p) = \frac{\partial}{\partial p}\,\mathbb{E}[Y\mid X=x, P(X,Z)=p]
$$

- Sharp RD (local effect at cutoff c):
$$
\tau = \lim_{x\downarrow c}\mathbb{E}[Y\mid X=x]-\lim_{x\uparrow c}\mathbb{E}[Y\mid X=x]
$$

- Fuzzy RD (local Wald at cutoff):
$$
\tau = \frac{\Delta Y \text{ at } c}{\Delta D \text{ at } c}
$$

- DiD (two periods, two groups):
$$
\text{DiD} = (\bar{Y}_T^{\text{post}}-\bar{Y}_T^{\text{pre}}) - (\bar{Y}_C^{\text{post}}-\bar{Y}_C^{\text{pre}})
$$

## Choosing a strategy (decision aid)

- Can you randomize? → [[randomized controlled trial (RCT)]], or quasi-random (e.g., [[switchback experiment]], [[geo experiment]]).
- Is there a plausible instrument? → [[Instrumental Variables (IV)]], [[Local IV]], [[fuzzy RDD]].
- Is there a sharp rule or threshold? → [[Regression Discontinuity Design (RDD)]].
- Do you have repeated outcomes pre/post with untreated controls? → [[Difference-in-Differences (DiD)]] (modern estimators for [[staggered adoption]]).
- Are selection drivers observable and well measured? → [[Unconfoundedness]] with [[propensity score]] methods.
- Do spillovers threaten SUTVA? → See [[Spillovers and Interference (MOC)]]; consider cluster-level designs.

## Diagnostics and robustness, by strategy

- RCTs: Balance tables, reassignment integrity ([[AA test]], [[Sample Ratio Mismatch (SRM)|SRM]]), attrition ([[Attrition]]) analysis, protocol deviations.
- Unconfoundedness: Overlap plots ([[Overlap]]), standardized differences after [[matching]]/[[entropy balancing]], placebo outcomes, sensitivity to model class ([[double machine learning]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]).
- IV: First-stage F-stat ([[weak instruments]]), alternative instruments/over-ID logic, exclusion discussions, monotonicity plausibility; report [[Intent-to-Treat (ITT)|ITT]], [[Treatment-on-the-Treated (TOT)|TOT]], [[Local Average Treatment Effect (LATE)|LATE]] distinction.
- RD: [[McCrary test]]/[[density test]], covariate continuity, multiple [[bandwidth selection]] rules, polynomial order sensitivity, donut exclusion.
- DiD: [[pre-trends]] tests, [[event study]] with confidence intervals, cohort/event-time heterogeneity (use [[Callaway–Sant’Anna estimator]] or [[Sun–Abraham estimator]]), composition/stable units checks.

## Threats and cross-cutting pitfalls

- [[spillovers|Spillovers]]/[[interference]] violating SUTVA → design for or model exposure.
- [[selection bias]] / attrition → see [[Missing Data and Selection (MOC)]], [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]], [[Lee bounds]].
- [[bad controls]] (post-treatment, colliders) → use DAG logic; avoid conditioning on mediators.
- Poor overlap/positivity → trimming, alternative estimands, [[balancing weights]].
- Timing/anticipation in panels → model [[Anticipatory effects]]; align treatment timing.
- Weak instruments → bias/size distortion; use robust inference; reconsider instrument.

## Linking identification to estimation

- Once identified, choose estimators aligned with design:
  - RCTs: difference-in-means, adjusted [[Analysis of Covariance (ANCOVA)|ANCOVA]], variance reduction ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]], [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]).
  - Unconfoundedness: [[Inverse Probability Weighting (IPW)|IPW]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[double machine learning]]. See [[Machine Learning for Causal Inference (MOC)]].
  - IV/RD: 2SLS/local polynomial; [[fuzzy RDD]] uses local Wald; continuous IV → [[Local IV]]/MTE.
  - DiD: modern cohort-specific estimators ([[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]), [[drdid]].
- Inference: use appropriate SEs and corrections (see [[Standard Errors and Inference (MOC)]], [[clustered standard errors]], [[wild cluster bootstrap]], [[Conley standard errors]]).

## Reporting checklist

> [!check] Minimum reporting items
> - [ ] Estimand (ATE/ATT/LATE/MTE, etc.) and target population
> - [ ] Identification strategy and key assumptions (explicitly stated)
> - [ ] Diagnostics and falsification tests (pre-trends, density, first stage)
> - [ ] Robustness (alternative bandwidths/specs/windows/instruments)
> - [ ] Handling of spillovers, attrition, and composition
> - [ ] Overlap/support and any trimming rules
> - [ ] Inference method and number of clusters (if applicable)
> - [ ] Limitations and external validity discussion

## Quick crosswalk (strategy → core links)

- Randomization: [[randomized controlled trial (RCT)]], [[Intent-to-Treat (ITT)]], [[Treatment-on-the-Treated (TOT)]], [[randomization inference]]
- Unconfoundedness: [[propensity score]], [[matching]], [[entropy balancing]], [[Inverse Probability Weighting (IPW)|IPW]], [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[Overlap]]
- Instruments: [[Instrumental Variables (IV)]], [[exclusion restriction]], [[relevance]], [[weak instruments]], [[Local Average Treatment Effect (LATE)|LATE]], [[Local IV]], [[marginal treatment effect (MTE)]], [[Wald estimator]], [[fuzzy RDD]]
- Discontinuities: [[Regression Discontinuity Design (RDD)]], [[sharp RDD]], [[fuzzy RDD]], [[bandwidth selection]], [[local linear regression]], [[local polynomial regression]], [[McCrary test]], [[density test]]
- Panels: [[Difference-in-Differences (DiD)]], [[two-way fixed effects]], [[staggered adoption]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[event study]], [[pre-trends]], [[drdid]], [[composition]]
- Bounds: [[Manski bounds]], [[Lee bounds]]

## Related

- Designs and estimands
  - [[randomized controlled trial (RCT)]], [[Intent-to-Treat (ITT)]], [[Treatment-on-the-Treated (TOT)]]
  - [[Unconfoundedness]], [[propensity score]], [[Overlap]], [[matching]], [[entropy balancing]]
  - [[Instrumental Variables (IV)]], [[Local Average Treatment Effect (LATE)|LATE]], [[Local IV]], [[marginal treatment effect (MTE)]], [[Wald estimator]]
  - [[Regression Discontinuity Design (RDD)]], [[sharp RDD]], [[fuzzy RDD]], [[bandwidth selection]]
  - [[Difference-in-Differences (DiD)]], [[two-way fixed effects]], [[staggered adoption]], [[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]], [[drdid]], [[event study]], [[pre-trends]]
  - Bounds: [[Manski bounds]], [[Lee bounds]]
- Assumptions and threats
  - [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], [[No spillovers]], [[interference]]
  - [[exclusion restriction]], [[relevance]], [[weak instruments]], [[monotonicity]]
  - [[parallel trends assumption]], [[Anticipatory effects]], [[composition]]
  - [[selection bias]], [[Attrition]], [[bad controls]]
- Inference and diagnostics
  - [[clustered standard errors]], [[wild cluster bootstrap]], [[Conley standard errors]], [[Cameron–Gelbach–Miller]], [[few-cluster corrections]]
  - [[randomization inference]], [[placebo test]], [[density test]], [[McCrary test]]

## Further reading (quick map)

- Randomization and design: Gerber & Green; CONSORT; [[pre-registration]]
- Selection on observables: Rosenbaum & Rubin; Imbens & Rubin
- IV/LATE: Angrist & Imbens; Angrist & Pischke; Heckman & Vytlacil ([[marginal treatment effect (MTE)|MTE]], [[Local IV]])
- RD: Imbens & Lemieux; Cattaneo et al. (robust RD)
- DiD: Angrist & Pischke; Callaway–Sant’Anna; Sun–Abraham (heterogeneous DiD)
- Partial identification: Manski; Lee
- Practice-oriented: “Mastering ‘Metrics”; Athey & Imbens on modern causal methods

## Compact decision reminders

- Prefer experiments when feasible; otherwise, align the strategy to the available quasi-random variation (IV, RD, DiD).
- State and defend assumptions in the language of your design (continuity, exclusion, parallel trends, monotonicity).
- Run design-specific falsification tests and report sensitivity (pre-trends, bandwidths, first stage strength, density).
- Align inference with the design’s dependence structure (clustering, spatial, staggered timing).
- When assumptions are weak, prefer bounds and transparent identification regions.

---

Related notes to create:
- [[identification region]]
- [[transportability]]
- [[external validity]]
- [[front-door criterion]]
- [[back-door criterion]]
- [[causal DAGs|DAG]]
- [[placebo test|placebo outcomes]]
- [[Regression Discontinuity Design (RDD)|donut RD]]
- [[policy invariance]]
- [[falsification tests]]
- [[support and extrapolation]]