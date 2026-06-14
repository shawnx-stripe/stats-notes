---
title: Composition
aliases:
- sample composition
- compositional change
- changing composition
- Composition
tags:
- causal-inference
- did
- panels
- repeated-cross-sections
- selection
- weighting
updated: 2025-09-17
---

# Composition

> [!summary] Quick definition
> Composition refers to who is in your sample and how the distribution of unit characteristics changes across groups and over time. In designs like [[Difference-in-Differences (DiD)]], differential changes in composition (entry/exit, attrition, migration, shifting covariates) can bias estimates and threaten the [[parallel trends assumption]].

- Examples: workers entering/exiting the labor force, firms entering/exiting a market, demographic shifts, survey sampling changes, selective attrition after treatment.
- Key risk: the observed change in outcomes reflects both true treatment effects and shifts in who is observed (composition), not just within-unit changes.

## Why composition matters for DiD

- Unconditional DiD assumes that, absent treatment, treated and control groups would have similar outcome trends. If group composition changes differentially, this can mimic or mask treatment effects.
- Especially relevant in:
  - [[repeated cross-sections]] DiD: different units each period
  - Unbalanced panels with [[Attrition]] correlated with treatment or outcomes
  - Policy-induced migration or selection into/away from treatment

## Simple decomposition intuition

Let m_t(x) = E[Y | X = x, t] be the conditional outcome and F_{g,t}(x) the covariate distribution for group g at time t. The group’s mean outcome is:
$$
\mathbb{E}[Y \mid g,t] = \int m_t(x) \, dF_{g,t}(x)
$$
A change over time mixes:
- Structural change: m_t(x) − m_{t-1}(x) (within-X outcome change)
- Compositional change: F_{g,t}(x) − F_{g,t-1}(x) (who is in the group)

If F shifts differently for treated vs. control, the DiD contrast can be biased.

## Typical sources of compositional change

- Entry/exit: firm births/deaths, employee turnover, migration between regions
- Survey/sample redesigns or differential response/[[Attrition]]
- Policy-induced selection (eligibility rules change who qualifies)
- Differential mortality or censoring
- Shifts in covariate distributions (age, industry mix, size, pre-trend levels)

## Diagnostics

> [!check] What to examine
> - [ ] Counts and rates: units per group/time, entry/exit, attrition by group
> - [ ] Balance over time: standardized differences in covariates by group×time
> - [ ] DiD of covariates: check whether covariates themselves show treatment-like shifts
> - [ ] Distributional plots: CDFs, quantiles, or kernel densities of key X by group×time
> - [ ] Stability of results when:
>       - Restricting to a [[balanced panel]]
>       - Re-weighting controls to match pre-treatment treated composition
>       - Narrowing time windows

## Strategies to address composition

### 1) Design choices
- Use a balanced panel where feasible; discuss external validity if many units drop.
- Limit the analysis window to reduce turnover-driven shifts.

### 2) Condition on covariates (conditional trends)
- Assume parallel trends conditional on X:
$$
\mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i, X_i] \text{ is equal across groups}
$$
- Implement via regression adjustment, flexible time×covariate interactions, or semiparametric methods.

### 3) Re-weight to a common composition
- Match control (and sometimes treated post) to a reference distribution (often treated pre):
  - [[entropy balancing]], [[propensity score]] weighting, [[Inverse Probability Weighting (IPW)|IPW]] for selection/attrition
  - Goal: align F_{g,t}(x) across groups/times so composition is held constant
- Identity for reweighting:
$$
\mathbb{E}_t[Y] = \mathbb{E}_s\!\left[ Y \cdot \frac{dF_t(X)}{dF_s(X)} \right]
$$
Estimate the density ratio via propensity models or calibration weights.

### 4) Handle attrition explicitly
- Model retention R_{it} and use inverse probability of censoring weights (IPCW):
$$
w_{it} = \frac{1}{\hat{P}(R_{it}=1 \mid \text{history})}
$$
- Check sensitivity to different retention models; consider bounds like [[Lee bounds]].

### 5) Separate composition from treatment (decompositions)
- Use [[Oaxaca–Blinder decomposition]] or [[DFL reweighting]] to attribute outcome changes to structure vs. composition.
- Report both “raw” and “composition-adjusted” DiD.

### 6) Guard against “bad controls”
- Avoid conditioning on post-treatment variables that are themselves affected by treatment, which can induce bias. See [[bad controls]] and [[post-treatment conditioning]].

## Reporting essentials

- Describe sample-building rules, inclusion/exclusion, and attrition by group/time.
- Provide covariate balance and distribution checks over time.
- Document weighting schemes, targets (which distribution is held fixed), and diagnostics.
- Show robustness: balanced panel only, alternative weights, time windows.

## Minimal code sketches

> [!example] Entropy balancing to match treated-pre composition (R)

```r
library(ebal)
# Suppose 'D' is treated-ever, and we match controls at each time to treated-pre distribution
treated_pre <- subset(df, D == 1 & Post == 0)
controls_t  <- subset(df, D == 0 & Post == 1)

X_treat_pre <- as.matrix(treated_pre[, c("age","female","preY")])
X_ctrl_post <- as.matrix(controls_t[, c("age","female","preY")])

eb <- ebalance(Treatment = rep(1, nrow(X_ctrl_post)), X = X_ctrl_post, target.margins = colMeans(X_treat_pre))
controls_t$w <- eb$w
# Use weights in DiD regression combining treated and reweighted controls
```

> [!example] IPCW for attrition (Python)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

# R_it = 1 if unit i observed at time t
X = df[["preY","age","female","D","time"]]
R = df["observed"].astype(int)
probit = LogisticRegression(max_iter=2000).fit(X, R)
p = probit.predict_proba(X)[:,1]
df["w_ipcw"] = 1.0 / np.clip(p, 1e-3, 1-1e-3)
# Use w_ipcw (possibly multiplied by design/PS weights) in FE DiD
```

> [!example] Conditional DiD with flexible time×covariate interactions (R)

```r
library(fixest)
est <- feols(Y ~ D:Post + i(time, age, ref = 0) + i(time, preY, ref = 0) | id + time,
             data = df, cluster = ~id)
etable(est)
```

## Copy-ready snippets

- Mean as structure × composition:
$$
\mathbb{E}[Y \mid g,t] = \int m_t(x)\, dF_{g,t}(x)
$$

- Conditional parallel trends:
$$
\mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=1, X_i] = \mathbb{E}[Y_{it}(0) - Y_{i,t-1}(0) \mid D_i=0, X_i]
$$

- IPCW weight:
$$
w_{it} = \frac{1}{\hat{P}(R_{it}=1 \mid \text{history})}
$$

## When to worry most

- Large and asymmetric entry/exit rates across groups
- Treatment plausibly affects survival/retention in the sample
- Major macro or sectoral shocks that shift group composition differently
- Survey design changes or reweighting revisions mid-study

---

Related notes to create:
- [[Difference-in-Differences (DiD)]]
- [[DiD estimator]]
- [[parallel trends assumption]]
- [[treated group]]
- [[control group]]
- [[repeated cross-sections]]
- [[balanced panel]]
- [[Attrition]]
- [[selection bias]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[entropy balancing]]
- [[propensity score]]
- [[Oaxaca–Blinder decomposition]]
- [[DFL reweighting]]
- [[Lee bounds]]
- [[bad controls]]
- [[post-treatment conditioning]]
- [[covariates]]