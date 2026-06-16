---
title: triggered analysis
aliases: [triggered cohort, exposure-based analysis, triggered experiment (analysis), on-exposure analysis]
tags: [experimentation, ab-testing, cohorts, exposure, leakage, selection-bias, cuped, ancova, itt, ipcw]
updated: 2025-09-17
---

# triggered analysis

> [!summary] Quick definition
> Triggered analysis restricts the analysis cohort to units that satisfy a predefined trigger (e.g., “saw the page,” “was eligible,” “opened the app”), rather than analyzing all assigned units (ITT). It is useful for measuring effects among those truly exposed, but can introduce bias if the trigger is influenced by treatment or defined post-exposure. Always define triggers symmetrically and pre-exposure, and report ITT as the primary estimand.

- Typical uses: feature only on a sub-surface, paywalls, eligibility-limited modules, ad or notification exposures, conditional flows.
- Core dependency: clean [[exposure logging]] and symmetric [[bucketing]].

---

## ITT vs triggered (what changes)

- ITT (intent-to-treat): estimand is the effect of assignment on the full assigned population. Preserves randomization and is unbiased by design; can be diluted if many assigned users are not exposed.
- Triggered: estimand is the effect among units meeting the trigger (e.g., exposed). Inference is sharper when the trigger is pre-exposure and symmetric; otherwise can be biased (conditioning on post-treatment variables). Often reported as secondary.

> [!warning] Triggered bias
> If treatment changes the probability of meeting the trigger, conditioning on the triggered subset breaks randomization and can bias effects (a form of selection-on-post-treatment). See [[leakage]] and [[selection bias]].

---

## When triggered analysis is valid (or safer)

> [!check]
> - [ ] Trigger definition is strictly pre-exposure and symmetric in both arms (e.g., pre-existing eligibility rules).  
> - [ ] The trigger event is logged in a way that does not depend on treatment success (e.g., exposure on render, not on click).  
> - [ ] You still report ITT as primary, with triggered as secondary for mechanism/targeting insight.  
> - [ ] You document estimand clearly (effect among triggered population) and caveats.

If the trigger is plausibly affected by treatment (e.g., “clicked the entry point”), the “always-trigger” subgroup (those who would trigger regardless of assignment) is the causal target, which is generally unobserved without strong assumptions (principal stratification/IV needed). Treat such triggered results as descriptive unless additional identification is provided.

---

## Estimands

- ITT: τ_ITT = E[Y | Z=1] − E[Y | Z=0], where Z is assignment.
- Triggered “on-exposure” (descriptive unless trigger ⟂ treatment):
  - τ_trig = E[Y | Z=1, Trigger=1] − E[Y | Z=0, Trigger=1].
- Better-defined secondary estimand (if feasible):
  - Effect among “always-eligible/exposed” (those who would trigger under both arms). Identification typically requires additional design assumptions; otherwise treat as sensitivity.

---

## Design and logging requirements

- Define trigger at decision time (pre-exposure) and identically across arms.
- Log layered events with timestamps and ids: assignment → eligibility → exposure (render/impression) → outcomes.  
- Use idempotent impression_id and left joins for ITT; triggered cohorts should be built from exposure/eligibility logs, not outcomes.

See: [[exposure logging]] · [[bucketing]].

---

## Analysis workflow

1) Pre-specify in [[pre-registration]]: ITT primary; triggered secondary (with exact trigger definition and windows).
2) Build cohorts:
   - ITT: all assigned units.
   - Triggered: units satisfying trigger (e.g., had an exposure event in window).
3) Variance reduction:
   - Use pre-trigger baselines for [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]]. Do not use post-trigger features (avoid [[leakage]]).
4) Inference:
   - Robust or [[clustered standard errors]] at the randomization level (user/session/geo; or time-block in [[switchback experiment]]).
   - Few clusters → [[few-cluster corrections]].
5) Diagnostics:
   - Funnel parity: assignment → eligibility → exposure by arm; layered [[Sample Ratio Mismatch (SRM)|SRM]].
   - Balance on pre-exposure covariates.
   - Seasonality and window alignment.
6) Report: ITT effects first; then triggered effects with caveats and rationale.

---

## Handling missing outcomes and censoring

- If outcome is only observed conditional on subsequent behavior (e.g., “spend among visitors”), consider:
  - ITT with zeros for non-observed outcomes (if meaningful), or
  - [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] for observation probability given pre-exposure history (avoid post-exposure features), and
  - Clearly state the estimand (effect on observed-only vs full population).

---

## Power and MDE impact

- Triggering reduces effective N by the trigger rate r; MDE inflates by ≈ 1/√r (all else equal).
- Plan [[power analysis]] with expected trigger rates, not just total traffic.
- Use CUPED baselines to recover power via R² gains.

---

## Diagnostics and pitfalls

> [!check] Diagnostics
> - [ ] Trigger rate parity across arms (within noise); large differences flag bias risk.  
> - [ ] Layered SRM (assignment, eligibility, exposure).  
> - [ ] AA on triggered logic (before launch or with prior traffic).  
> - [ ] Balance on pre-trigger covariates; uplift limited to triggered cohort should be plausible.  
> - [ ] Sensitivity: alternative trigger windows; include/exclude edge cases; near/far or time-of-day splits.

> [!warning] Pitfalls
> - Trigger defined by post-assignment engagement that treatment can influence (e.g., click to open) → selection bias.  
> - Exposure logged only on success (e.g., only after click) → pipeline/join leakage.  
> - Mismatch of units (per-session analysis with user-level randomization) without clustering.  
> - Using post-trigger features in CUPED/ANCOVA (leakage).  
> - Exclusive reliance on triggered results; always include ITT.

---

## Minimal code snippets

> [!example] SQL: build ITT and triggered cohorts

```sql
-- ITT cohort: all assigned users in window
WITH itt AS (
  SELECT a.user_id, a.variant, a.assignment_ts
  FROM assignment a
  WHERE a.assignment_ts BETWEEN :start AND :end
),

-- Triggered cohort: exposure occurred (render/impression), symmetric across arms
trig AS (
  SELECT DISTINCT e.user_id
  FROM exposure e
  WHERE e.event_ts BETWEEN :start AND :end
),

-- Outcomes (joined left for ITT; inner for triggered by design)
outcomes AS (
  SELECT o.user_id, SUM(o.metric) AS y, COUNT(*) AS n_events
  FROM outcome o
  WHERE o.event_ts BETWEEN :start AND :end
  GROUP BY o.user_id
)

-- ITT analysis frame
SELECT i.user_id, i.variant, o.y
FROM itt i
LEFT JOIN outcomes o ON o.user_id = i.user_id;

-- Triggered analysis frame
SELECT i.user_id, i.variant, o.y
FROM itt i
JOIN trig t ON t.user_id = i.user_id
LEFT JOIN outcomes o ON o.user_id = i.user_id;
```

> [!example] R: ITT vs triggered with CUPED (baseline pre-trigger)

```r
library(sandwich); library(lmtest)

# df_itt: user_id, D (0/1), Y, preY (pre-trigger baseline)
fit_itt <- lm(Y ~ D + preY, data = df_itt)
coeftest(fit_itt, vcov = vcovHC(fit_itt, type = "HC1"))

# df_trig: subset of df_itt where Trigger==1 (pre-specified)
fit_trig <- lm(Y ~ D + preY, data = df_trig)
coeftest(fit_trig, vcov = vcovHC(fit_trig, type = "HC1"))
```

> [!example] Python: cluster-robust SEs for triggered cohort

```python
import statsmodels.formula.api as smf

# df_trig with columns: Y, D, preY, user_id
res = smf.ols('Y ~ D + preY', data=df_trig).fit(cov_type='cluster', cov_kwds={'groups': df_trig['user_id']})
print(res.summary())
```

> [!example] R: IPCW for missing outcomes (if observation depends on pre-exposure history)

```r
# observed==1 if outcome Y is recorded; model P(S=1 | preX, D) with pre features only
ipcw <- glm(observed ~ D + preX1 + preX2, family = binomial(), data = df_trig)
w <- 1 / pmax(pmin(fitted(ipcw), 0.995), 0.005)
fit_ipcw <- lm(Y ~ D + preY, data = subset(df_trig, observed==1), weights = w)
coeftest(fit_ipcw, vcov = vcovHC(fit_ipcw, type="HC1"))
```

---

## Reporting essentials

- Precise trigger definition and window; symmetric application across variants.
- Primary (ITT) and secondary (triggered) estimands; rationale for triggered reporting.
- Cohort sizes, trigger rates by arm; funnel diagram (assignment→eligibility→exposure→analysis).
- Variance reduction (CUPED/CUPAC) with baseline window; θ estimated on control/pre only.
- Inference details: SE type (robust/clustered), clustering level, few-cluster corrections if applicable.
- Diagnostics: layered SRM, AA, seasonality coverage, parity, leakage checks.
- Sensitivity analyses: alternative triggers or windows; inclusion/exclusion criteria; IPCW if missingness.

---

## Related notes

- [[AB Testing (MOC)]] · [[Experimental Design (MOC)]]
- [[Overall Evaluation Criterion (OEC)|OEC]] · [[guardrail metric]]  
- [[bucketing]] · [[exposure logging]] · [[AA test]] · [[Sample Ratio Mismatch (SRM)|SRM]]
- [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]] · [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[sequential testing]]
- [[leakage]] · [[selection bias]] · [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[switchback experiment]] · [[geo experiment]]

---

## FAQs

- Is triggered analysis ever causal? Yes, if the trigger is pre-exposure and independent of treatment (or applied symmetrically so that assignment is retained within the triggered set). Otherwise, treat as descriptive or use advanced designs (principal stratification/IV) for causal interpretation.
- Should I report only triggered? No—always report ITT. Triggered can illuminate mechanisms or targeted value but can be biased.
- How does it affect power? Effective N is multiplied by the trigger rate; use variance reduction and plan runtime accordingly.

---
