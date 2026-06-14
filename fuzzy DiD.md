---
title: Fuzzy DiD
aliases: [fuzzy DiD, fuzzy difference-in-differences, fuzzy diff-in-diff]
tags: [causal-inference, did, iv, identification]
updated: 2026-03-05
---

# Fuzzy DiD

> [!summary]
> DiD design where treatment assignment shifts probability of treatment (rather than switching it on/off deterministically). Combines DiD variation with an IV-style first stage; yields a [[Local Average Treatment Effect (LATE)|LATE]]-type estimand for compliers.

## Setup and estimation

**Sharp DiD**: $D_{it} = \mathbb{1}\{\text{Group}_i = \text{Treated} \land t \geq t_0\}$ (all treated units switch on at $t_0$).

**Fuzzy DiD**: Treatment assignment $Z_{it}$ affects but does not perfectly determine $D_{it}$.

**Two stages**:
1. **First stage**: $D_{it} = \alpha_i + \lambda_t + \delta \cdot Z_{it} + v_{it}$
2. **Second stage (reduced form)**: $Y_{it} = \alpha_i + \lambda_t + \beta \cdot Z_{it} + \epsilon_{it}$

**IV-DiD estimand**: $\hat{\tau}^{\text{IV-DiD}} = \hat{\beta} / \hat{\delta}$ = effect for compliers (those induced to switch by $Z$).

> [!tip]
> Fuzzy DiD is common when:
> - Policy rollout is staggered or imperfect (e.g., eligibility vs. actual take-up)
> - Some units self-select out of treatment
> - Intent-to-treat ($Z$) differs from actual treatment received ($D$)

## Minimal code snippets

```r
# R: fuzzy DiD with ivreg
library(ivreg)
iv_did <- ivreg(outcome ~ treatment + factor(unit) + factor(time) |
                         z_instrument + factor(unit) + factor(time),
                data = panel_df)
summary(iv_did)
```

```python
# Python: fuzzy DiD with linearmodels
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS

# Construct instrument from time × group interaction
panel_df['Z'] = (panel_df['treated_group'] == 1) & (panel_df['post'] == 1)
iv = IV2SLS.from_formula('y ~ 1 + [treatment ~ Z] + EntityEffects + TimeEffects', data=panel_df).fit()
print(iv)
```

## Related notes

- [[Difference-in-Differences (DiD)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Instrumental Variables (IV)]]
- [[noncompliance]]
- [[fuzzy RDD]]
