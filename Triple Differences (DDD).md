---
title: Triple Differences (DDD)
aliases: [DDD, 3D DiD, diff-in-diff-in-diff]
tags: [causal-inference, did, triple-differences, identification, panels, rc]
updated: 2025-09-17
---

# Triple Differences (DDD)

> [!summary] Quick definition
> Triple differences (DDD) identify a causal effect by differencing a standard DiD contrast across an additional “unaffected” dimension. It removes time-varying confounding that is common across that dimension, under a strengthened parallel-trends assumption.

- Canonical use: treatment affects only an “affected” subgroup (A) within treated units; an “unaffected” subgroup (B) serves as an internal control. DDD removes shocks that hit treated/control groups similarly across both subgroups.

---

## Set-up and formula

- Two groups: Treated (T=1) vs Control (T=0)
- Two time periods: Post (t=1) vs Pre (t=0)
- Two subgroups: Affected (A=1) vs Unaffected (A=0)

DDD estimand (ATT-like on the affected subgroup):
$$
\begin{aligned}
DDD
&= \Big[(\bar Y_{T,1,A} - \bar Y_{T,0,A}) - (\bar Y_{C,1,A} - \bar Y_{C,0,A})\Big] \\
&\quad - \Big[(\bar Y_{T,1,B} - \bar Y_{T,0,B}) - (\bar Y_{C,1,B} - \bar Y_{C,0,B})\Big].
\end{aligned}
$$

Intuition: subtract the DiD for the “unaffected” subgroup from the DiD for the “affected” subgroup to purge confounding common across A/B.

---

## Regression specification

Let D = Treated (T=1), Post (P=1), and Affected (A=1). A saturated linear model is:
$$
Y = \alpha
+ \beta\, (D \cdot P \cdot A)
+ \theta_1 (D \cdot P) + \theta_2 (D \cdot A) + \theta_3 (P \cdot A)
+ \theta_4 D + \theta_5 P + \theta_6 A + \varepsilon,
$$
where β is the DDD estimand.

With rich fixed effects (preferred in panels), include unit and time FE and the necessary interactions to avoid collinearity while preserving the triple interaction. A practical panel spec when units carry A as a characteristic:
- Unit FE (absorbs D and A main effects)
- Time FE (absorbs P)
- Pairwise interactions as needed (omit those collinear with FE)
- Keep the triple interaction D·P·A; that coefficient is DDD.

> [!tip] Implementation
> Include all lower-order terms of the triple interaction unless they are absorbed by fixed effects. Most software handles the full polynomial (D, P, A, all pairwise, and triple) automatically.

---

## Identification assumptions (DDD-parallel-trends)

- Parallel trends within each subgroup in the absence of treatment:
  - For A=1 (affected) and A=0 (unaffected), treated and control would have shared trends absent the policy.
- Additivity across subgroup:
  - Any time-varying confounders that differ between treated and control do so equally across A and B (so subtracting the “unaffected” DiD removes them).
- No spillovers/interference:
  - [[No spillovers]]/[[interference]] across groups/subgroups; the “unaffected” subgroup truly remains unaffected by treatment.
- Correct timing and no unmodeled anticipation:
  - [[Anticipatory effects]] are absent or modeled (use leads).

> [!warning] Key risk
> If the treated vs control differential trend is not the same in A and B absent treatment, DDD can be biased.

---

## When to use DDD

- Policy affects only a subset of outcomes/people/products/locations (A), leaving a comparable subset (B) unaffected.
- You suspect a time-varying confounder that regular DiD cannot remove, but that confounder influences A and B equally (so it cancels in DDD).
- Examples:
  - Tax on one product category (A) vs untaxed category (B)
  - Regulation affecting firms above a size threshold (A) vs below (B), with a separate treated/control dimension (e.g., states)
  - Gender- or age-specific policy (A) vs other demographic (B) within treated/control regions over time

---

## Event-study (DDD dynamics)

Dynamic DDD checks pre-trends separately for the affected vs unaffected subgroups. Example with cohort/event-time k:
$$
Y_{it} = \alpha_i + \gamma_t + \sum_{k\neq -1}
\big[ \beta^{(A)}_k\,\mathbf{1}\{t-G_i=k\}\cdot A_i
+ \beta^{(B)}_k\,\mathbf{1}\{t-G_i=k\}\cdot (1-A_i)\big] + \varepsilon_{it},
$$
and report $\beta^{(A)}_k - \beta^{(B)}_k$ as the triple-difference event-time effect. Pre-period differences (k<0) should be near zero.

---

## Code examples

> [!example] R: saturated triple interaction (simple two-period setup)

```r
# D = Treated (0/1), P = Post (0/1), A = Affected (0/1)
fit <- lm(Y ~ D*P*A, data = df)  # includes main, pairwise, and triple
summary(fit)  # coef on D:P:A is DDD
```

> [!example] R: panel with FE (fixest)

```r
library(fixest)
# Suppose A is a unit-invariant attribute (e.g., product category fixed per unit)
# Include unit and time FE; keep triple and pairwise interactions as needed
fit <- feols(Y ~ D:P:A + D:P + D:A + P:A | unit + time, cluster = ~unit, data = df)
etable(fit)  # coef on D:P:A is DDD
```

> [!example] Stata

```stata
* Saturated triple interaction
reg Y c.D##i.P##i.A, vce(cluster unit)

* Panel with FE
reghdfe Y c.D##i.P##i.A, absorb(unit time) vce(cluster unit)
```

> [!example] Python (statsmodels)

```python
import statsmodels.formula.api as smf
# Saturated polynomial
res = smf.ols('Y ~ D*P*A', data=df).fit(cov_type='HC1')
print(res.summary())
```

---

## Diagnostics and good practice

> [!check]
> - [ ] Pre-trends within A and within B: run subgroup-specific event studies; then examine the DDD pre-leads (A minus B)  
> - [ ] Verify “unaffected” subgroup truly unaffected (no cross-over or substitution)  
> - [ ] Balance and composition: check that A vs B composition does not change differentially by treated/control over time ([[composition]])  
> - [ ] Spillovers: test near/far, border checks; exclude likely contaminated observations  
> - [ ] Seasonality/calendar: include appropriate controls ([[seasonality]])

---

## Extensions and variants

- More than two subgroups:
  - The third difference can be extended to multiple unaffected/affected categories (e.g., using interactions with categorical A).
- Continuous “affectedness”:
  - Replace A with a continuous intensity (dose); the triple interaction generalizes to D·P·Intensity.
- Staggered adoption DDD:
  - Combine with cohort-time ATT frameworks ([[Callaway–Sant’Anna estimator]]) using valid comparison sets, and interact affectedness with cohort-time indicators.

---

## Inference

- Cluster SEs at the treatment-assignment level (often unit or higher-level cluster) and along the A dimension if clustered there.
- If few clusters (G small), use [[few-cluster corrections]] (CR2, wild cluster bootstrap).
- With spatial correlation (geo settings), consider [[Conley standard errors]].

---

## Common pitfalls

> [!warning]
> - Assuming the “unaffected” subgroup is truly unaffected (e.g., substitution into the untaxed good)  
> - Ignoring that treated vs control trend differences might vary across A and B (violates DDD parallel trends)  
> - Over-saturating with FE and pairwise interactions that make the triple term collinear  
> - Composition shifts that differ across A/B and treated/control over time  
> - Using post-treatment variables to define A (see [[bad controls]])

---

## Reporting essentials

- Define D (treated), P (post), and A (affected) clearly; justify why A is unaffected absent treatment
- Present the DDD formula, regression specification, and how lower-order terms/FE are handled
- Diagnostics: subgroup pre-trends and DDD pre-leads; placebo tests
- Inference: clustering level, small-sample corrections, spatial adjustments if relevant
- Robustness: alternative A definitions, excluding likely spillover cases, alternative time windows
- Discuss limitations: potential substitution, varying trends across A/B

---

## Copy-ready snippets

- DDD estimand:
$$
DDD = \big[\Delta^{DiD}_{A}\big] - \big[\Delta^{DiD}_{B}\big]
$$
where
$$
\Delta^{DiD}_{A} = (\bar Y_{T,1,A} - \bar Y_{T,0,A}) - (\bar Y_{C,1,A} - \bar Y_{C,0,A}).
$$

- Regression (saturated):
$$
Y = \alpha + \beta\,DPA + \theta_1 DP + \theta_2 DA + \theta_3 PA + \theta_4 D + \theta_5 P + \theta_6 A + \varepsilon.
$$

---

## Related notes

- [[Difference-in-Differences (DiD)]] · [[DiD estimator]] · [[event study]]  
- [[Callaway–Sant’Anna estimator]] · [[Sun–Abraham estimator]]  
- [[clustered standard errors]] · [[few-cluster corrections]] · [[Conley standard errors]]  
- [[No spillovers]] · [[interference]] · [[Anticipatory effects]] · [[composition]] · [[seasonality]]  
- [[bad controls]]

---
