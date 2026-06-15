---
title: Difference-in-Differences (DiD)
aliases:
  - DiD
  - DID
  - Diff-in-Diff
  - Difference in Differences
  - Difference of Differences
  - D-I-D
  - difference-in-differences
tags:
  - econometrics
  - causal-inference
  - did
  - policy-evaluation
updated: 2025-09-17
---

# Difference-in-Differences (DiD)

> [!summary] Quick definition
> A [[quasi-experimental design]] that estimates causal effects by comparing changes over time between a [[treated group]] and a [[control group]].

## Core idea and estimator

- Compare the change in outcomes for treated units to the change for control units.
- Block-math (copy/paste as-is):
$$
\text{DiD} = (\bar{Y}_T^{\text{post}} - \bar{Y}_T^{\text{pre}}) - (\bar{Y}_C^{\text{post}} - \bar{Y}_C^{\text{pre}})
$$
- See also: [[DiD estimator]]

### Simple numeric example

| Group   | Pre | Post | Change |
|---------|-----|------|--------|
| Treated | 10  | 15   | +5     |
| Control | 8   | 10   | +2     |

- DiD = 5 − 2 = 3

## Regression specification (two groups, two periods)

- Block-math (copy/paste as-is):
$$
Y_{it} = \alpha_i + \gamma_t + \beta \,(D_i \cdot Post_t) + \varepsilon_{it}
$$

### Notation

| Symbol | Meaning |
|-------:|---------|
| $Y_{it}$ | Outcome for unit $i$ at time $t$ |
| $\alpha_i$ | Unit fixed effect |
| $\gamma_t$ | Time fixed effect |
| $D_i$ | Indicator for treated units (1 = treated) |
| $Post_t$ | Indicator for post-policy period (1 = post) |
| $\beta$ | DiD effect |
| $\varepsilon_{it}$ | Error term |

- This is a [[two-way fixed effects]] model.

## Key assumptions

- [[parallel trends assumption|Parallel trends assumption]]
- [[No spillovers]] / [[interference]] between groups
- [[Anticipatory effects]] are absent or modeled
- Stable sample [[composition]]

> [!check] Pre-analysis checklist
> - [ ] Plot and inspect [[pre-trends]]
> - [ ] Justify similarity of treated vs. control before treatment
> - [ ] Check for differential composition changes
> - [ ] Assess potential spillovers or anticipation

## Good practice

- Use [[clustered standard errors]] at the treatment-assignment level (e.g., unit or region)
- If clusters are few, apply [[few-cluster corrections]]
- Include [[covariates]] for precision (does not replace identification)
- Visualize with an [[event study]] (leads/lags) to assess dynamics

> [!tip] Implementation tips
> - Always report the number of clusters.
> - Show event-study plots with confidence intervals.
> - Pre-register how you’ll test for pre-trends.

## Extensions and pitfalls

> [!warning] Staggered treatment timing
> With [[staggered adoption]] and [[treatment effect heterogeneity]], classic TWFE can be biased.
> - Prefer modern estimators:
>   - [[Callaway–Sant’Anna estimator]]
>   - [[Sun–Abraham estimator]]
> - Report [[group-time average treatment effect]]s

Other considerations:
- Timing effects, [[spillovers]], sample [[composition]] changes
- Sensitivity to alternative control groups and windows

## When to use

- Policy evaluations (minimum wage laws, tax changes, training programs) when randomized experiments are infeasible but you have treated and comparable controls over time.

## Minimal code snippets (optional)

```r
# R (fixest)
library(fixest)
est <- feols(Y ~ i(Post, D, ref = 0) | id + time, cluster = ~id, data = df)
summary(est)
```

```stata
* Stata
xtset id time
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)
```

```python
# Python (linearmodels)
from linearmodels.panel import PanelOLS
df = df.set_index(['id','time'])
df['interaction'] = df['D'] * df['Post']
mod = PanelOLS.from_formula('Y ~ 1 + D + Post + interaction + EntityEffects + TimeEffects', data=df)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res)
```

---

## Related notes
- [[quasi-experimental design]]
- [[treated group]]
- [[control group]]
- [[DiD estimator]]
- [[two-way fixed effects]]
- [[parallel trends assumption]]
- [[No spillovers]]
- [[interference]]
- [[Anticipatory effects]]
- [[composition]]
- [[pre-trends]]
- [[event study]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[covariates]]
- [[staggered adoption]]
- [[treatment effect heterogeneity]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[group-time average treatment effect]]