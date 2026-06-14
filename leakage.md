---
title: leakage
aliases: [data leakage, information leakage, post-treatment leakage, label leakage, target leakage]
tags: [experimentation, ab-testing, causal-inference, ml, pipelines, diagnostics, governance]
updated: 2025-09-17
---

# leakage

> [!summary] Quick definition
> Leakage is the use of information that would not be available (or is influenced by treatment) at decision time in training, feature construction, cohort definition, or analysis. It creates optimistic bias, invalid inference, and misleading decisions.

- Where it bites: [[AB Testing (MOC)]], [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]] baselines, uplift/[[policy learning]], [[double machine learning]], [[Difference-in-Differences (DiD)]], time-series models, and logging/joins (e.g., [[exposure logging]]).

---

## Taxonomy of leakage

- Post-treatment covariates (bad controls)
  - Including variables measured after assignment/exposure in models or adjustment. See [[bad controls]].
- Label/target leakage
  - Features built from or correlated with the target via overlapping windows or future data.
- Temporal leakage
  - Using future observations to build features for the past (no time-aware splits).
- Cohort/selection leakage
  - Conditioning the sample on post-assignment outcomes/engagement (e.g., “active-only” analysis), triggered logic that depends on treatment.
- Pipeline/join leakage
  - Inner joins that selectively drop units asymmetrically by arm; logging exposure only upon success (click); identity drift (user↔device).
- Cross-arm contamination
  - Sharing learned parameters or caches across arms; re-bucketing mid-run.
- Cross-fitting leakage (causal ML)
  - Training nuisance models and scoring the same rows without held-out folds; tuning on test data.

---

## Why it’s harmful

- Bias: treatment effects and uplifts look better than they are (optimism); MDE/power appear smaller than reality.
- Invalid inference: p-values/SEs do not reflect true uncertainty; guardrails/OEC may be falsely “safe.”
- Poor decisions: policies learned on leaked signals fail online; rollouts cause harm.

---

## Prototypical examples

- AB tests
  - CUPED baseline computed from post-exposure behavior; estimating θ using treated outcomes.
  - Triggered analysis where eligibility is defined by post-assignment engagement that treatment affects.
  - Scaling or normalizing by outcomes (e.g., revenue per “purchaser only”).
- Uplift/policy learning
  - Using post-exposure features to predict CATE; computing features after the decision point.
  - Training and evaluating on the same folds; hyperparameter tuning on the test set.
- DiD / panels
  - Selecting “controls” based on post-period outcomes; defining affectedness (A) by post-policy behavior.
  - Imputing pre-period with post-period information.
- Time series
  - Feature windows that peek into the future; improper train/validation splits across time.
- Logging
  - Exposure logged only on success (click/view) instead of on render/impression; asymmetric filters by variant.

---

## Detection and diagnostics

> [!check] Audit
> - [ ] Temporal lineage: for every feature and filter, record event time; enforce “feature_ts < decision_ts”  
> - [ ] DAG review: draw causal graph; ensure covariates are not descendants of treatment/outcome  
> - [ ] Layered SRM: test at assignment → eligibility → exposure → analysis  
> - [ ] [[AA test]]: run A/A with current pipeline; look for systematic drifts  
> - [ ] Placebos: train uplift on pre-period to “predict” pre outcomes; look for spurious lift  
> - [ ] Shuffle tests: randomize labels; any remaining “signal” implies leakage  
> - [ ] Cross-fitting sanity: confirm out-of-fold predictions for nuisances/scores

> [!warning] Red flags
> - Pre/post filters differ by arm; triggered eligibility depends on treatment-side code paths  
> - Features joined with future timestamps; inconsistent time zones/windows  
> - Performance collapses in holdout or online A/B vs offline metrics  
> - θ for CUPED estimated on treated post data

---

## Prevention patterns

- Design-time rules
  - Only use pre-assignment/pre-trigger covariates; freeze baseline windows before randomization; pre-register metrics and cohorts.
- Time-aware splits
  - Use rolling or blocked CV for time series; K-fold cross-fitting for DML/uplift.
- Feature stores and lineage
  - Store feature timestamps, freshness SLAs, and “allowed use” (pre/post); enforce “no post-treatment” contracts.
- CUPED/CUPAC
  - Estimate θ using only control or pre-period; document windows; validate R² out-of-sample.
- Triggered experiments
  - Define eligibility symmetrically across arms, based on pre-trigger conditions; keep and report ITT alongside triggered.
- Logging
  - Log assignment, eligibility, exposure, and outcomes with idempotent IDs; avoid success-conditional logging; prefer left joins for ITT.

---

## Minimal code patterns

> [!example] SQL: enforce pre-decision features

```sql
-- Keep only features before assignment_ts
SELECT f.user_id, f.feature_ts, f.x1, f.x2
FROM feature_table f
JOIN assignment a ON a.user_id = f.user_id
WHERE f.feature_ts < a.assignment_ts;
```

> [!example] Python: time-aware CV

```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    model.fit(X[train_idx], y[train_idx])
    y_pred = model.predict(X[test_idx])  # never train on future folds
```

> [!example] DML cross-fitting (sketch)

```python
# Fit nuisances on folds != i, predict on fold i
# Never evaluate score ψ_i with nuisances trained on the same rows.
```

> [!example] R: CUPED θ on controls only

```r
theta <- coef(lm(Y ~ X, data = subset(df, D==0)))[["X"]]
df$Y_star <- df$Y - theta * (df$X - mean(df$X))
```

> [!example] SQL: ITT left-join outcomes

```sql
SELECT a.user_id, a.variant, o.metric
FROM assignment a
LEFT JOIN outcomes o
  ON o.user_id = a.user_id AND o.window_id = a.window_id; -- keep non-responders
```

---

## Checklist by context

> [!check] AB testing
> - [ ] Baselines strictly pre-exposure; θ from control/pre only (CUPED/CUPAC)  
> - [ ] Eligibility symmetric; exposure logging on render/impression  
> - [ ] ITT preserved; triggered analysis documented and matched  
> - [ ] SRM at all layers; AA passes; seasonality aligned

> [!check] Uplift/policy learning
> - [ ] Cross-fitted nuisances/scores; no post-treatment features  
> - [ ] OPE propensities logged/estimated; overlap checked (ESS)  
> - [ ] Separate data for policy selection and OPE evaluation (nested CV)  
> - [ ] Online validation plan with guardrails

> [!check] DiD/panels
> - [ ] Controls not chosen by post outcomes; affectedness defined pre-policy  
> - [ ] Leads in [[event study]] near zero; no anticipatory edges  
> - [ ] Composition stable or adjusted; no post-treatment covariates

> [!check] Time series
> - [ ] Rolling splits; feature windows do not peek; time zones consistent  
> - [ ] Release/holiday calendars handled (see [[seasonality]])

---

## Common pitfalls

> [!warning]
> - Estimating CUPED θ on treated post data (bias)  
> - Including post-exposure engagement as uplift features (anti-causal)  
> - Hyperparameter tuning on test data; reporting best-of-many without nested validation  
> - Filtering to “active” or “buyers” after assignment (truncation-by-usage)  
> - Client-only exposure logs triggered on click success  
> - Using already-treated periods to fit DiD comparators

---

## Reporting essentials

- Decision time definition; feature windows and lineage; which fields are pre vs post
- Eligibility, exposure, and analysis cohort rules; ITT vs triggered
- CUPED/CUPAC details (θ estimation sample, R², baseline window)
- CV scheme (time-aware or cross-fit); OPE propensities and overlap diagnostics
- SRM/AA outcomes; seasonality coverage; outages/deploys affecting logs
- Known residual risks and mitigations; governance approvals

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]]
- [[exposure logging]] · [[bucketing]] · [[Sample Ratio Mismatch (SRM)|SRM]] · [[AA test]]
- [[sequential testing]] · [[guardrail metric]]
- [[uplift]] · [[policy learning]] · [[double machine learning]]
- [[Difference-in-Differences (DiD)]] · [[event study]] · [[Anticipatory effects]]
- [[bad controls]] · [[seasonality]] · [[composition]] · [[Unconfoundedness]] · [[Overlap]]

---