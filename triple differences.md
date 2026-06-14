---
title: Triple Differences
aliases: [triple differences, difference-in-difference-in-differences, triple diff]
tags: [causal-inference, did, identification]
updated: 2026-03-05
---

# Triple Differences

> [!summary]
> Extension of [[Difference-in-Differences (DiD)]] using a third differencing dimension (e.g., subgroup, outcome type) to relax the parallel-trends assumption by netting out group-specific trends.

## Overview

Triple differences (DDD or difference-in-difference-in-differences) extends the standard DiD framework by adding a third dimension of comparison. While [[Difference-in-Differences (DiD)|DiD]] requires that treated and control groups would have followed [[parallel trends assumption|parallel trends]] in the absence of treatment, DDD allows for **differential trends** across groups by introducing an additional comparison dimension.

The key insight is to difference out group-specific trends that might violate parallel trends. For example:
- **DiD**: treatment vs control, before vs after
- **DDD**: treatment vs control, before vs after, **subgroup A vs subgroup B**

The third dimension is typically:
1. **Subgroups**: e.g., male vs female, high-income vs low-income
2. **Outcome types**: e.g., placebo outcome vs outcome of interest
3. **Geographic/institutional variation**: e.g., bordering vs non-bordering counties

## Model Specification

The canonical DDD regression specification is:

$$
Y_{igst} = \alpha + \beta_1 \text{Treat}_g + \beta_2 \text{Post}_t + \beta_3 \text{Subgroup}_s + \beta_4 (\text{Treat}_g \times \text{Post}_t)
$$
$$
+ \beta_5 (\text{Treat}_g \times \text{Subgroup}_s) + \beta_6 (\text{Post}_t \times \text{Subgroup}_s)
$$
$$
+ \tau_{\text{DDD}} (\text{Treat}_g \times \text{Post}_t \times \text{Subgroup}_s) + \varepsilon_{igst}
$$

where:
- $i$ indexes individuals, $g$ treatment group, $s$ subgroup, $t$ time
- $\text{Treat}_g = 1$ for treated group
- $\text{Post}_t = 1$ for post-treatment period
- $\text{Subgroup}_s = 1$ for subgroup expected to be more affected
- $\tau_{\text{DDD}}$ is the triple-difference estimator (the **three-way interaction coefficient**)

**Alternative formulation with fixed effects**:

$$
Y_{igst} = \alpha_{gt} + \alpha_{gs} + \alpha_{st} + \tau_{\text{DDD}} (\text{Treat}_g \times \text{Post}_t \times \text{Subgroup}_s) + \varepsilon_{igst}
$$

where $\alpha_{gt}$, $\alpha_{gs}$, $\alpha_{st}$ are two-way fixed effects absorbing the lower-order interactions.

## Identifying Assumption

The DDD estimator $\tau_{\text{DDD}}$ identifies the [[Average Treatment Effect on the Treated (ATT)|ATT]] under:

> [!check] DDD identifying assumption
> The **differential trend** between subgroups in the control group equals the differential trend that would have occurred in the treatment group absent treatment:
> $$
> E[Y_{1st}(0) - Y_{1st'}(0)] - E[Y_{0st}(0) - Y_{0st'}(0)] = E[Y_{1st}(0) - Y_{1st'}(0)] - E[Y_{0st}(0) - Y_{0st'}(0)]
> $$
> for treatment group $g=1$ vs control group $g=0$, subgroups $s$ vs $s'$, and times $t$ vs $t'$.

This is **weaker** than the standard parallel trends assumption because it allows:
- Treated and control groups to have different trends
- As long as the **difference in trends between subgroups** is the same in treatment and control

## When to Use DDD

Use triple differences when:

1. **Parallel trends may be violated**: Treatment and control have differential pre-trends, but those trends are common across subgroups
2. **Subgroup heterogeneity is available**: You can credibly identify a dimension along which treatment effects should differ
3. **Difference-in-trends is plausible**: The differential trend assumption is more defensible than parallel trends

> [!warning] Do not use DDD when
> - The third dimension is mechanically related to treatment assignment
> - Subgroups are themselves affected by treatment (spillovers)
> - You don't have a theoretical reason why one subgroup should be differentially affected
> - Sample sizes become too small after stratification

## Comparison with Standard DiD

| Feature | DiD | DDD |
|---------|-----|-----|
| **Dimensions** | 2 (group × time) | 3 (group × time × subgroup) |
| **Key assumption** | Parallel trends | Parallel differential trends |
| **Allows group trends** | No | Yes (differenced out) |
| **Robustness** | Sensitive to trend violations | More robust to group-specific trends |
| **Interpretation** | Average effect | Differential effect across subgroups |
| **Data requirements** | Moderate | High (need subgroup variation) |

## Diagnostics

1. **Pre-treatment differential trends**: Test whether $(\text{Treat}_g \times t \times \text{Subgroup}_s)$ is zero in pre-period using [[event study]] specification:

$$
Y_{igst} = \alpha_{gs} + \alpha_{st} + \alpha_{gt} + \sum_{k \neq -1} \delta_k \cdot \mathbb{1}[t=k] \cdot \text{Treat}_g \cdot \text{Subgroup}_s + \varepsilon_{igst}
$$

Check that $\delta_k \approx 0$ for all $k < 0$.

2. **Placebo subgroups**: If possible, use a subgroup that should **not** be affected as a placebo test

3. **Robustness to subgroup definition**: Check sensitivity to alternative definitions of the third dimension

4. **Balance in subgroup composition**: Ensure treatment doesn't affect subgroup membership

## Minimal Code Snippets

### R (fixest)

```r
library(fixest)

# DDD with three-way interaction
ddd_model <- feols(
  outcome ~ treat:post:subgroup |
    group^time + group^subgroup + time^subgroup,
  data = panel_data,
  cluster = ~group
)

# Extract DDD coefficient
tau_ddd <- coef(ddd_model)["treat:post:subgroup"]

# Event study for pre-trends (relative time, omit t=-1)
event_ddd <- feols(
  outcome ~ i(rel_time, treat:subgroup, ref = -1) |
    group^subgroup + time^subgroup + group^time,
  data = panel_data,
  cluster = ~group
)

# Plot differential pre-trends
iplot(event_ddd)
```

### Python (pyfixest)

```python
import pyfixest as pf

# DDD specification
ddd_fit = pf.feols(
    "outcome ~ treat:post:subgroup | group^time + group^subgroup + time^subgroup",
    data=panel_data,
    vcov={"CRV1": "group"}
)

# Event study
event_fit = pf.feols(
    "outcome ~ i(rel_time, treat:subgroup, ref=-1) | group^subgroup + time^subgroup + group^time",
    data=panel_data,
    vcov={"CRV1": "group"}
)
```

### Stata

```stata
* Generate three-way interaction
gen treat_post_subgroup = treat * post * subgroup

* DDD with two-way FE
reghdfe outcome treat_post_subgroup, ///
    absorb(i.group#i.time i.group#i.subgroup i.time#i.subgroup) ///
    cluster(group)

* Event study for pre-trends
gen treat_subgroup = treat * subgroup
reghdfe outcome ibn.rel_time#treat_subgroup, ///
    absorb(i.group#i.subgroup i.time#i.subgroup i.group#i.time) ///
    cluster(group) noconstant

* Plot coefficients
coefplot, keep(*treat_subgroup) vertical yline(0) ///
    xline(0, lcolor(red))
```

## Related notes

- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[event study]]
- [[staggered adoption]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[synthetic control]]
