---
title: Local Average Treatment Effect (LATE)
aliases:
  - LATE
  - local average treatment effect
  - complier average causal effect
  - CACE
  - Wald estimand
  - Local Average Treatment Effect (LATE)
  - Local Average Treatment Effect
tags:
  - causal-inference
  - iv
  - rct
  - noncompliance
  - policy-evaluation
  - econometrics
updated: 2025-09-17
---

# Local Average Treatment Effect (LATE)

> [!summary] Quick definition
> LATE is the average causal effect of treatment on the subpopulation of compliers—units whose treatment status is changed by the instrument (assignment/offer). With a binary instrument $Z$ and binary treatment $D$, the LATE equals the Wald ratio:
> $$
> LATE = \frac{\mathbb{E}[Y \mid Z=1]-\mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]},
> $$
> under independence, [[exclusion restriction]], and [[monotonicity]].

- ITT relation: $ITT = LATE \times \Delta_D$, where $\Delta_D = \mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]$ is the first stage.
- Policy meaning: effect of treatment for those induced to take it by the offer/assignment.

## Setup and principal strata

- Assignment (instrument): $Z \in \{0,1\}$
- Treatment received: $D \in \{0,1\}$ (or continuous)
- Outcome: $Y$
- Principal strata by potential treatments:
  - [[compliers]]: $D(1)=1$, $D(0)=0$
  - [[always-takers]]: $D(1)=1$, $D(0)=1$
  - [[never-takers]]: $D(1)=0$, $D(0)=0$
  - [[defiers]]: $D(1)=0$, $D(0)=1$ (ruled out by monotonicity)

> [!tip] Interpretation
> LATE targets the causal effect for compliers only—not for always-/never-takers—and need not equal ATE or [[Treatment-on-the-Treated (TOT)]].

## Identification assumptions (binary Z and D)

- Independence (random/as-if random assignment):
$$
Z \perp \{Y(0),Y(1),D(0),D(1)\}
$$
- [[exclusion restriction]]:
$$
Y(z,d) = Y(d) \quad \text{(Z affects Y only via D)}
$$
- [[monotonicity]]:
$$
D(1) \ge D(0) \quad \text{(no defiers)}
$$
- Relevance (first stage): $\mathbb{E}[D \mid Z=1] \ne \mathbb{E}[D \mid Z=0]$ and $0<P(Z=1)<1$.

Under these, the Wald ratio identifies LATE.

## Estimators

### Wald estimator (binary Z and D)
- Copy-ready:
$$
\widehat{LATE} = \frac{\bar Y_{Z=1} - \bar Y_{Z=0}}{\bar D_{Z=1} - \bar D_{Z=0}}
$$

### Two-Stage Least Squares (2SLS)
- With additional covariates $X$:
$$
\text{1st stage: } D = \pi_0 + \pi_1 Z + X'\pi + v,\quad
\text{2nd stage: } Y = \alpha + \beta \hat D + X'\gamma + u
$$
- In heterogeneous-effects settings, 2SLS recovers a weighted average of LATEs across covariate cells, with weights proportional to how strongly Z shifts D. See [[Instrumental Variables (IV)]].

> [!note] Local to instrument
> With multi-valued or continuous instruments, 2SLS still identifies a weighted average of local effects for those moved at the instrument margins. See [[Local IV]] and [[marginal treatment effect (MTE)]].

## When does LATE equal TOT?

- One-sided noncompliance (no [[always-takers]]), plus independence, exclusion, and monotonicity:
  - Treated units under $Z=1$ are compliers, so
  $$
  LATE = [[Treatment-on-the-Treated (TOT)]] = [[Average Treatment Effect on the Treated (ATT)]] \text{ (for compliers)}.
  $$
- Otherwise, LATE generally differs from ATT/TOT and ATE.

## LATE in designs beyond simple RCTs

- Fuzzy [[Regression Discontinuity Design (RDD)]]: local Wald ratio of reduced-form to first-stage at the cutoff identifies a local LATE.
- “Fuzzy” DiD (panel IV): instrument the treated interaction (e.g., $D \cdot Post$) with an assignment interaction ($Z \cdot Post$) to obtain a DiD-LATE for compliers. Requires [[parallel trends assumption]] with respect to assignment groups and a strong first stage.

## Diagnostics and reporting

> [!check] Good practice
> - [ ] Report compliance/take-up: $\mathbb{E}[D \mid Z=1], \mathbb{E}[D \mid Z=0]$, first-stage $\Delta_D$, and F-stat (rule of thumb > 10).
> - [ ] Discuss exclusion: channels by which Z might affect Y besides D; show reduced-form on likely mediators if possible.
> - [ ] Argue monotonicity: why defiers are implausible.
> - [ ] Address [[interference]]/[[No spillovers]] of Z.
> - [ ] If overidentified, report Sargan/Hansen tests with caution (valid only if at least one instrument is truly valid).
> - [ ] Use appropriate clustering (assignment level); apply [[few-cluster corrections]] when G is small.

## Common pitfalls

> [!warning] Avoid these
> - Weak instruments (low first-stage): biased 2SLS and misleading inference.
> - Declaring external validity: LATE applies to compliers; don’t generalize to all units without argument.
> - Violated exclusion (Z affects Y directly) or interference across units.
> - Assuming LATE = TOT without one-sided compliance and IV assumptions.
> - Conditioning on post-instrument variables (creates [[bad controls]]).

## Minimal code snippets

```r
# R: Wald and 2SLS (AER)
ITT_y <- with(df, mean(Y[Z==1]) - mean(Y[Z==0]))
ITT_d <- with(df, mean(D[Z==1]) - mean(D[Z==0]))
LATE  <- ITT_y / ITT_d

library(AER)
summary(ivreg(Y ~ D | Z, data = df))  # 2SLS estimate of LATE under IV assumptions
```

```stata
* Stata: Wald and 2SLS
ttest Y, by(Z)
ttest D, by(Z)
local LATE = (r(mu_1)-r(mu_2)) / (r(mu_1_2)-r(mu_2_2))   // illustrative; compute means carefully
ivregress 2sls Y (D = Z), robust
estat firststage
```

```python
# Python: 2SLS
from linearmodels.iv import IV2SLS
res = IV2SLS.from_formula('Y ~ 1 + [D ~ Z]', data=df).fit(cov_type='robust')
print(res.summary)
```

## Copy-ready formulas

- Wald LATE:
$$
LATE = \frac{\mathbb{E}[Y \mid Z=1]-\mathbb{E}[Y \mid Z=0]}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]}
$$

- ITT to LATE:
$$
ITT = LATE \times \Delta_D, \quad \Delta_D = \mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]
$$

- 2SLS (concept):
$$
\hat\beta^{2SLS} = \frac{\operatorname{Cov}(Y,\hat D)}{\operatorname{Var}(\hat D)}
$$
interpretable as a weighted average of local effects.

## Relation to other estimands

- [[Intent-to-Treat (ITT)]]: offer/assignment effect; policy-relevant even with exclusion doubts.
- [[Treatment-on-the-Treated (TOT)]] / ATT: effect among treated; equals LATE only under extra conditions.
- [[Average Treatment Effect (ATE)|ATE]]: average effect in the whole population; generally not identified by a single binary instrument without stronger assumptions.
- [[marginal treatment effect (MTE)]]: LATE is the average of MTE over the complier region.

## When to use LATE

- Imperfect take-up under randomized encouragement/eligibility.
- Natural experiments where an instrument shifts treatment probability.
- Fuzzy RDD and fuzzy DiD contexts.

---

Related notes to create:
- [[Instrumental Variables (IV)]]
- [[Intent-to-Treat (ITT)]]
- [[Treatment-on-the-Treated (TOT)]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[compliers]]
- [[always-takers]]
- [[never-takers]]
- [[defiers]]
- [[first stage]]
- [[weak instruments]]
- [[Two-Stage Least Squares (2SLS)|two-stage least squares (2SLS)]]
- [[Wald estimator]]
- [[marginal treatment effect (MTE)]]
- [[Local IV]]
- [[Regression Discontinuity Design (RDD)]]
- [[fuzzy RDD]]
- [[Difference-in-Differences (DiD)]]
- [[fuzzy DiD]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[No spillovers]]
- [[interference]]
- [[bad controls]]
- [[few-cluster corrections]]
- [[clustered standard errors]]