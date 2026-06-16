---
title: factorial design
aliases: [full factorial, fractional factorial, 2^k design, DOE, design of experiments, interaction design]
tags: [experimentation, design, rct, factorial, interactions, doe, blocking, split-plot, power]
updated: 2025-09-17
---

# factorial design

> [!summary] Quick definition
> A factorial design tests multiple factors (A, B, C, …) simultaneously by running all (or a structured subset of) combinations of factor levels. It estimates main effects and interactions efficiently, often with fewer runs than testing one factor at a time, and is foundational in Design of Experiments (DOE).

- Use for: product experiments with multiple levers, industrial/process optimization, ad/creative variants, algorithm knobs.
- Outputs: effect estimates for each factor and their interactions; guidance on which combination to deploy or which factors matter.

---

## When to use

> [!tip] Good fit
> - You have 2–6 factors with clear levels and want to learn interactions, not just main effects.
> - You can randomize/run multiple combinations concurrently (or sequentially with proper randomization).
> - You need efficient inference: factorials extract more information per run than one-factor-at-a-time.

> [!warning] Consider alternatives
> - Many factors or continuous tuning beyond a local region → [[response surface methodology]], screening designs (Plackett–Burman), or sequential experimentation.
> - Hard-to-change factors (e.g., oven temp) → [[split-plot]] designs.

---

## Basics

- Full factorial (2^k) with k two-level factors: evaluates every combination; main effects and interactions estimable up to order k.
- General factorial: factors can have 3+ levels (e.g., 3×2×4 design).
- Fractional factorial: run a fraction (e.g., 2^(k−p)) using generators; trades off some higher-order interactions in exchange for fewer runs.

### Model (coded −1/+1 for two-level factors)
For k factors A, B, C:
$$
Y = \beta_0 + \beta_A A + \beta_B B + \beta_C C + \beta_{AB} AB + \beta_{AC} AC + \beta_{BC} BC + \beta_{ABC} ABC + \varepsilon.
$$
- Main effects: β_A, β_B, β_C
- Interactions: β_{AB}, β_{AC}, β_{BC}, β_{ABC}
- Use hierarchical modeling: include lower-order terms if a higher-order interaction is in the model.

---

## Fractional factorials and aliasing

- Generator and defining relation: specify how to build the fraction (e.g., for 2^(4−1): D = ABC).
- Alias structure: which effects are confounded (e.g., A is aliased with BCD).
- Resolution:
  - III: main effects may be aliased with two-factor interactions (screening)
  - IV: main effects clear of two-factor; two-factor may alias with two-factor
  - V: main effects and two-factor interactions clear of each other (preferred for interaction estimation)
- Foldover: add a complementary fraction to de-alias confounded effects.

> [!tip] Choose the lowest run count that retains estimability of effects you care about (resolution IV or V for interactions).

---

## Randomization, blocking, split-plot

- Randomization: randomize run order to protect against time trends and nuisance variation.
- Blocking: group runs to control for nuisance factors (day, machine, geo); block effects are included in the model.
- [[split-plot]]: when some factors are hard to change, randomize them at whole-plot level and others at subplot level; analyze with mixed models.

---

## Replication, center points, and curvature

- Replication: repeat runs to estimate pure error and improve precision.
- Center points (quantitative factors): detect curvature (non-linearity). If present, move to [[response surface methodology]] (CCD/Box–Behnken).

---

## Analysis

- ANOVA or regression with factorial terms:
  - Balanced 2^k designs: orthogonal coding (−1/+1) gives uncorrelated effect estimates.
  - Unbalanced/multi-level: regression with appropriate coding (effects/sum coding) and robust SEs if needed.
- Inference:
  - Check assumptions: homoscedasticity, independence; transform Y if strongly non-normal/heavy-tailed.
  - Multiplicity: if many effects are tested, consider [[False Discovery Rate (FDR)|FDR]] for exploratory screening (but retain hierarchical principle).
- Effect plots:
  - Main effect plots (mean response by factor level)
  - Interaction plots (non-parallel lines indicate interaction)
- Hierarchical selection: include main effects when interactions are present; prefer model interpretability consistent with design.

> [!warning] Clustered/geo/online contexts
> If randomization is by cluster (geo/store) or time-block ([[switchback experiment]]), use [[clustered standard errors]] or HAC/[[Conley standard errors]] for valid inference.

---

## Power and sample size

- Power depends on:
  - Number of runs (N), number of factors/levels, replication
  - Error variance and effect sizes of interest
  - Design resolution (aliasing increases uncertainty)
- Rules of thumb:
  - Plan replication or center points to estimate error.
  - For online multi-factor tests, overall N must support the smallest effect you care about after splitting traffic among cells; use [[power analysis]]/[[Minimum Detectable Effect (MDE)|MDE]].

---

## Factorial design in online experiments

- Pros: parallel learning about multiple levers; detect interactions (e.g., layout×ranking).
- Pitfalls:
  - Traffic dilution: many cells with thin n; consider fractional factorial or restrict factors.
  - Interference/collisions: overlapping tests; use namespaces and exclusion groups (see [[bucketing]]).
  - Sequencing: for time-varying systems, consider [[switchback experiment]] or [[geo experiment]] for hard-to-change factors.
- Variance reduction: include pre-exposure covariates ([[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]]/[[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]/[[Analysis of Covariance (ANCOVA)|ANCOVA]]) to improve precision.

---

## Minimal code snippets

> [!example] R: Full and fractional factorials

```r
# Full factorial 2^3
df <- expand.grid(A = c(-1,1), B = c(-1,1), C = c(-1,1))
# Suppose Y observed; fit full model
fit <- lm(Y ~ A*B*C, data = df)
anova(fit); summary(fit)

# Fractional factorial 2^(4-1) Resolution IV with FrF2
# install.packages("FrF2")
library(FrF2)
des <- FrF2(nruns = 8, nfactors = 4, generators = "D=ABC", randomize = TRUE)
# Run experiment, collect Y, then analyze:
# fit <- lm(Y ~ (A+B+C+D)^2, data = as.data.frame(des))  # up to two-factor
```

> [!example] Python: pyDOE2 and statsmodels

```python
# pip install pyDOE2
from pyDOE2 import ff2n
import pandas as pd
import statsmodels.formula.api as smf

# Full factorial 2^3
A = ff2n(3)  # levels -1,+1
df = pd.DataFrame(A, columns=['A','B','C'])
# Suppose we have Y measurements
# df['Y'] = ...
res = smf.ols('Y ~ A*B*C', data=df).fit()
print(res.summary())
```

> [!example] Stata: factorial ANOVA

```stata
* Two-level factors A B C encoded as -1/+1 or factor variables
anova Y A##B##C
* Or regression style with interactions
reg Y c.A##c.B##c.C
```

---

## Design choices checklist

> [!check]
> - [ ] List factors and levels; code as −1/+1 for two-level quantitative factors  
> - [ ] Choose full vs fractional; set resolution to preserve effects of interest  
> - [ ] Plan randomization order; add blocking if nuisance factors exist  
> - [ ] Decide on replication and center points; detect curvature  
> - [ ] Pre-specify analysis model (effects hierarchy) and multiplicity handling  
> - [ ] If hard-to-change factors: adopt [[split-plot]] design  
> - [ ] For online tests: ensure enough traffic per cell; consider fractional factorial or narrower scope

---

## Reporting essentials

- Design table: factors, levels, coding, number of runs; if fractional, specify generators, defining relation, resolution, alias structure
- Randomization and blocking details; split-plot structure (if any)
- Replication and center points; run order
- Analysis model: included effects, hierarchical rationale; transformation if used
- Results: main effects and interactions with CIs; effect plots; diagnostics
- Recommendations: which factors/levels matter; interaction implications
- Limitations: aliasing, power, potential carryover/time effects

---

## Common pitfalls

> [!warning]
> - Too many factors without enough runs → underpowered, uninterpretable results  
> - Ignoring interactions or violating hierarchy (dropping main effects while keeping interactions)  
> - Mis-specified fractional generators → unintended aliasing  
> - No randomization or blocking → confounded with time/machine effects  
> - Treating −1/+1 codes as labels rather than quantitative levels (misinterpretation)  
> - For online tests: per-session analysis under user-level randomization without clustering

---

## Related notes

- [[Experimental Design (MOC)]] · [[AB Testing (MOC)]]
- [[split-plot]] · [[stratification|blocking]] · [[power analysis]] · [[Minimum Detectable Effect (MDE)|MDE]]
- [[Analysis of Covariance (ANCOVA)|ANCOVA]] · [[Controlled Experiments Using Pre-Experiment Data (CUPED)|CUPED]] · [[Controlled Experiments Using Pre-Experiment Covariates (CUPAC)|CUPAC]]
- [[switchback experiment]] · [[geo experiment]]
- [[response surface methodology]]
- Taguchi methods
- resolution · [[aliasing]]

---
