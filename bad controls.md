---
title: Bad Controls
aliases: [post-treatment controls, conditioning on mediators, conditioning on colliders]
tags: [causal-inference, regression, dag, identification, did, iv, mediation]
updated: 2025-09-17
---

# Bad Controls

> [!summary] Quick definition
> “Bad controls” are variables you condition on that are affected by treatment or that open spurious paths (colliders), thereby biasing causal estimates. Typical cases:
> - Post-treatment variables (mediators, outcomes of treatment)
> - Colliders or descendants of colliders
> - Sampling/conditioning decisions based on post-treatment status

See also: [[covariates]], [[post-treatment conditioning]], [[collider bias]], [[causal DAGs]].

## Why bad controls bias estimates

- If a variable M is downstream of treatment D (D → M), conditioning on M blocks part of the true effect of D on Y (mediator) and can induce selection bias through backdoors involving M’s causes.
- If M is a collider on a path between D and Y (D → M ← U → Y), conditioning on M opens a spurious association between D and Y via U.

> [!note] DAG intuition (text)
> - Mediator case: D → M → Y. Regressing Y on D and M yields only the “direct effect,” not the total effect; plus bias if M shares unobserved causes with Y.
> - Collider case: D → M ← U → Y. Conditioning on M opens D ↔ U ↔ Y.

## Recognize bad controls

- Variables measured after treatment assignment or after policy starts (even if recorded at the same time as outcomes).
- Intermediate outcomes, behaviors, or exposures that the treatment can change (hours worked, take-up intensity, prices, inputs).
- Sample restrictions determined post-treatment (e.g., “only employed,” “only users”).
- Controls constructed from the outcome itself (e.g., using Y to scale or normalize regressors contemporaneously).

> [!warning] Common examples
> - Education → wages: controlling for occupation or industry (often affected by education) can be bad.
> - Training program → earnings: conditioning on post-program employment status introduces selection.
> - Policy → prices → sales: controlling for prices may remove part of the policy effect and add bias if price has its own shocks.

## When controls are OK (or preferred)

- Pre-treatment covariates: demographics, baseline levels, and predetermined characteristics.
- In panels/DiD:
  - Unit and time fixed effects are safe.
  - Interactions of pre-treatment covariates with time FE can support conditional parallel trends.
  - Baseline outcomes (pre-period Y) are typically safe; contemporaneous M_t affected by D_t (or by earlier D) are not.

> [!tip] Safe rule of thumb
> Ask: “Could treatment have changed this variable by the time it enters the model?” If yes or possibly, do not include it unless you are explicitly doing mediation analysis with appropriate identification.

## Relation to designs

### Difference-in-Differences (DiD)
- Do not add time-varying controls that respond to the treatment (e.g., price, staffing) unless modeling mechanisms.
- Safer: pre-treatment covariates and flexible time interactions; see [[parallel trends assumption]], [[covariates]].

### Instrumental Variables (IV)
- Conditioning on variables on the instrument’s causal path to treatment or on colliders can violate the [[exclusion restriction]].
- Avoid post-instrument controls that absorb the instrument’s effect on D.

### Regression Discontinuity (RDD)
- Balance tests should use pre-determined covariates. Controlling for covariates is optional; avoid variables that jump due to treatment at the cutoff.

## What to do instead

- Articulate the estimand:
  - Total effect: do not control for mediators.
  - Direct effect: use mediation/causal path methods (e.g., [[mediation analysis]], [[front-door criterion]], structural models) with strong assumptions.
- Design for identification:
  - Use instruments or designs that isolate exogenous variation, obviating the need for risky controls.
  - Restrict the sample or time window to reduce channels that would require bad controls.
- Sensitivity:
  - Show robustness excluding suspect controls.
  - Report results with and without post-treatment variables to illustrate mechanism vs. total effect.

## Minimal examples

> [!example] DiD with a post-treatment mediator (don’t do this)

```r
# R: M_it is affected by treatment D_i*Post_t
# BAD: adds M_it that is downstream of treatment
feols(Y ~ D:Post + M + Xpre | id + time, cluster = ~id, data = df)
```

> [!example] Safer DiD alternative

```r
# R: only pre-treatment covariates and their time interactions
feols(Y ~ D:Post + i(time, Xpre1) + i(time, Xpre2) | id + time, cluster = ~id, data = df)
```

```stata
* Stata: avoid post-treatment M
reghdfe Y c.Post##i.D /* + i.time#c.Xpre1 i.time#c.Xpre2 */ , absorb(id time) vce(cluster id)
```

```python
# Python: linearmodels PanelOLS; no post-treatment mediators
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
res = PanelOLS.from_formula('Y ~ 1 + D + Post + D:Post + Xpre1_t + Xpre2_t + EntityEffects + TimeEffects',
                            data=df).fit(cov_type='clustered', cluster_entity=True)
```

## Copy-ready checklist

> [!check] Before adding a control
> - [ ] Is it measured pre-treatment?
> - [ ] Could treatment affect it (directly or indirectly)?
> - [ ] Is it a collider or descendant of one in your DAG?
> - [ ] Does adding it change the estimand (total vs. direct effect)?
> - [ ] If included, can you justify via a mediation framework with its assumptions?

## Special cases and nuances

- Lagged outcomes: including Y_{t−1} in panels can be problematic if past treatment affects Y_{t−1} (dynamic panel bias, bad control risk). Use designs tailored to dynamics (Arellano–Bond, g-methods) if necessary.
- Normalizations using contemporaneous Y: avoid creating regressors that are functions of the outcome you model.
- Composition-based controls: variables reflecting selection (e.g., “only employed”) induce conditioning on post-treatment status; consider [[composition]] issues and use weighting/bounds (e.g., [[Lee bounds]]).

## References and terms

- Angrist & Pischke’s “bad controls” concept (Mostly Harmless Econometrics).
- Related: [[collider bias]], [[mediation analysis|mediation]], [[front-door criterion]], [[post-treatment conditioning]].

---

## Related notes
- [[covariates]]
- [[post-treatment conditioning]]
- [[collider bias]]
- [[mediation analysis]]
- [[front-door criterion]]
- [[causal DAGs]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[Regression Discontinuity Design (RDD)]]
- [[composition]]
- [[Lee bounds]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]