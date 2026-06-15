---
title: Monotonicity
aliases: [no defiers, instrument monotonicity, monotone treatment selection (selection), monotone IV]
tags: [causal-inference, iv, late, rdd, encouragement, identification, assumptions]
updated: 2025-09-17
---

# Monotonicity

> [!summary] Quick definition
> In the [[Instrumental Variables (IV)]]/[[Local Average Treatment Effect (LATE)|LATE]] framework with a binary instrument $Z$ and binary treatment $D$, monotonicity (no defiers) requires that the instrument weakly increases the probability of treatment for every unit:
> $$
> D_i(1) \ge D_i(0) \quad \text{for all } i.
> $$
> This rules out “defiers” whose treatment moves opposite to the instrument, and is needed (with independence and the [[exclusion restriction]]) for LATE identification.

- Also called “no defiers” or “instrument monotonicity” (Imbens–Angrist).
- Distinct from “monotone treatment response” (MTR), which asserts $Y_i(1)\ge Y_i(0)$; MTR is a different assumption.

## Principal strata and interpretation

- Potential treatments: $D_i(1)$ if $Z=1$ (encouraged/eligible), $D_i(0)$ if $Z=0$.
- Principal strata:
  - [[compliers]]: $D(1)=1, D(0)=0$
  - [[always-takers]]: $D(1)=1, D(0)=1$
  - [[never-takers]]: $D(1)=0, D(0)=0$
  - [[defiers]]: $D(1)=0, D(0)=1$ (ruled out by monotonicity)
- Monotonicity eliminates defiers, allowing the Wald/2SLS estimand to target the effect for compliers (the [[Local Average Treatment Effect (LATE)|LATE]]).

## Role in identification

- With independence (random/as-if random $Z$) and [[exclusion restriction]]:
  - Wald ratio (binary $Z,D$) identifies LATE:
  $$
  LATE = \frac{\mathbb{E}[Y \mid Z=1]-\mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]}
  $$
  provided $D(1)\ge D(0)$ for all units and the first stage is nonzero.

- One-sided noncompliance implies monotonicity automatically (e.g., no [[always-takers]] when $Z=0$ makes access impossible), and under additional conditions LATE can equal [[Treatment-on-the-Treated (TOT)]].

> [!warning] Without monotonicity
> The Wald ratio need not equal a causal effect; it becomes a difference of weighted averages that mixes compliers and defiers.

## Beyond binary instruments

- Stochastic/weak monotonicity for multi-valued or continuous $Z$: treatment propensity is weakly increasing in $Z$ for all units (no rank reversals).
- Monotone Instrumental Variable (MIV): $Z$ orders potential outcomes or selection probabilities; used to derive bounds (Manski-style), not point identification.

## In common designs

- Encouragement/eligibility (RCT-IV): assignment $Z$ should not reduce take-up for anyone (no perverse response).
- [[fuzzy RDD]]: crossing the cutoff should not reduce treatment probability for any unit (no “crossing-induced” discouragement). Local monotonicity near the cutoff supports a local LATE.
- “Fuzzy DiD”: when instrumenting $D \cdot Post$ with $Z \cdot Post$, assume that assignment increases take-up in the post period for everyone (no defiers relative to the policy phase).

## How to argue monotonicity

> [!check] Design-based reasoning
> - Institutional constraints: assignment enables access but cannot reduce it (e.g., eligibility opens a door; ineligibility blocks it).
> - Incentive compatibility: encouragement increases benefits or lowers costs; no subgroup has incentives to do the opposite.
> - Implementation protocol: uniform messaging and absence of perverse penalties.

> [!warning] Red flags
> - Queues/capacity constraints where assignment displaces others into control.
> - Strategic substitution across programs: being encouraged for one program reduces take-up of the target treatment.
> - Information effects that make some units less likely to participate when encouraged.

## Distinctions to keep clear

- Instrument monotonicity (this page): $D(1)\ge D(0)$.
- Monotone Treatment Response (MTR): $Y(1)\ge Y(0)$ for all units (assumption on outcomes, not selection).
- Monotone Treatment Selection (MTS): those with higher $D$ potential outcomes differ systematically; used in partial-identification literature.
- MIV: monotone relationship between instrument and outcomes/selection used for bounds.

## Practical diagnostics and reporting

> [!note]
> Monotonicity is not testable from observed data without strong extra assumptions. Support it with design logic and auxiliary evidence.

- Report first stage by $Z$ (take-up differences).
- Describe mechanisms ruling out defiers; discuss plausible exceptions.
- In RD/DiD contexts, show that treatment probability weakly increases at the cutoff or in post periods for the assigned group.

## Sensitivity and alternatives

- If monotonicity is doubtful:
  - Report [[Intent-to-Treat (ITT)]] as a policy-relevant effect of offer.
  - Provide bounds under weaker assumptions (MIV/MTR-style).
  - Explore heterogeneity where monotonicity is more credible (subgroups).
  - Use designs that directly randomize exposure shares ([[randomized saturation design]]) to estimate direct/indirect effects without relying on no-defiers.

## Minimal code snippets

> [!example] First-stage check (difference in take-up)

```r
# R
with(df, mean(D[Z==1]) - mean(D[Z==0]))  # should be >= 0 under monotonicity and strong first stage
```

```stata
* Stata
ttest D, by(Z)     // report sign and magnitude of first stage
```

```python
# Python
delta_D = df.loc[df.Z==1,'D'].mean() - df.loc[df.Z==0,'D'].mean()
print(delta_D)
```

> [!example] Fuzzy RD: visualize treatment jump at cutoff

```r
library(rdrobust)
rdrobust(y = df$D, x = df$X, c = c0)  # positive jump supports local monotonicity
```

## Copy-ready definitions

- Instrument monotonicity (no defiers):
$$
D_i(1) \ge D_i(0)\ \ \forall i
$$

- LATE (requires independence, [[exclusion restriction]], and monotonicity):
$$
LATE = \frac{\mathbb{E}[Y \mid Z=1]-\mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]}
$$

- One-sided compliance implication:
If $D_i(0)=0$ for all $i$ (no always-takers), then monotonicity holds and, under IV assumptions, LATE equals [[Treatment-on-the-Treated (TOT)]] for compliers.

## Reporting essentials

- Define $Z$ (assignment) and $D$ (received treatment) and the timing.
- Justify monotonicity with institutional details; discuss potential violations.
- Present first-stage evidence (size, sign, F-stat); apply [[clustered standard errors]] and [[few-cluster corrections]] if clustered.
- If using RD/DiD: show treatment probability jumps only in the expected direction.

## Common pitfalls

> [!warning] Avoid these
> - Assuming monotonicity when program design creates winners and losers in access.
> - Equating LATE with ATT/TOT without noting the one-sided compliance case.
> - Ignoring [[interference]] where others’ assignment can reduce a unit’s take-up (capacity constraints).
> - Confusing monotonicity with MTR; they are different assumptions.

---

## Related notes
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Intent-to-Treat (ITT)]]
- [[Treatment-on-the-Treated (TOT)]]
- [[exclusion restriction]]
- [[compliers]]
- [[always-takers]]
- [[never-takers]]
- [[defiers]]
- [[fuzzy RDD]]
- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy DiD]]
- [[Difference-in-Differences (DiD)]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[randomized saturation design]]
- [[interference]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[MTR]]
- [[MIV]]
- [[Manski bounds]]