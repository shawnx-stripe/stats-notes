---
title: Manski Bounds
aliases: [worst-case bounds, partial identification, Manski (1990, 1995) bounds]
tags: [causal-inference, bounds, partial-identification, robustness, selection, missing-data, econometrics]
updated: 2025-09-17
---

# Manski Bounds

> [!summary] Quick definition
> Manski bounds are assumption-lean, worst-case bounds on causal parameters (e.g., ATE/ATT) that rely only on observed data and known outcome support (e.g., $Y \in [y_L,y_U]$). They “partially identify” effects without requiring [[Unconfoundedness]], exclusion, or functional-form assumptions. Tightening assumptions (e.g., [[MTR]], [[MIV]]) can narrow the bounds.

Use when strong identification assumptions are doubtful, or as robustness/sensitivity companions to point estimates.

## Setup

- Binary treatment $D \in \{0,1\}$; outcome $Y \in [y_L,y_U]$ (often $[0,1]$ for binary outcomes).
- Observables: $p = \Pr(D=1)$, $\mu_1^{obs} = \mathbb{E}[Y \mid D=1]$, $\mu_0^{obs} = \mathbb{E}[Y \mid D=0]$.
- Target examples:
  - ATE = $\mathbb{E}[Y(1) - Y(0)]$
  - ATT = $\mathbb{E}[Y(1) - Y(0) \mid D=1]$
  - ATU = $\mathbb{E}[Y(1) - Y(0) \mid D=0]$

No assumptions on selection into $D$ beyond outcome support.

## Worst-case (no-assumption) ATE bounds

Let $\mu_{10} = \mathbb{E}[Y(1)\mid D=0]$ and $\mu_{01} = \mathbb{E}[Y(0)\mid D=1]$. With only $Y \in [y_L,y_U]$:
- $\mu_{10},\mu_{01} \in [y_L,y_U]$.

ATE decomposition:
$$
ATE = p(\mu_1^{obs}-\mu_{01}) + (1-p)(\mu_{10}-\mu_0^{obs}).
$$

Thus, worst-case (Manski) bounds:
$$
\underline{ATE}
= p(\mu_1^{obs}-y_U) + (1-p)(y_L-\mu_0^{obs}),
$$
$$
\overline{ATE}
= p(\mu_1^{obs}-y_L) + (1-p)(y_U-\mu_0^{obs}).
$$

- Binary outcome ($y_L=0,y_U=1$) simplifies to:
  - $\underline{ATE} = p\,\mu_1^{obs} - (1-p)\,\mu_0^{obs} - p$
  - $\overline{ATE} = p\,\mu_1^{obs} + (1-p)\,(1-\mu_0^{obs})$

## ATT and ATU worst-case bounds

- ATT:
$$
ATT = \mu_1^{obs} - \mu_{01}, \quad \mu_{01} \in [y_L,y_U]
\Rightarrow ATT \in \big[\mu_1^{obs}-y_U,\ \mu_1^{obs}-y_L\big].
$$

- ATU:
$$
ATU = \mu_{10} - \mu_0^{obs}, \quad \mu_{10} \in [y_L,y_U]
\Rightarrow ATU \in \big[y_L-\mu_0^{obs},\ y_U-\mu_0^{obs}\big].
$$

These can be very wide; additional assumptions or covariate conditioning can tighten them.

## Incorporating covariates (stratified bounds)

Condition on $X$ and average:
- Compute bounds within strata $x$ using $p(x)$, $\mu_1^{obs}(x)$, $\mu_0^{obs}(x)$, then integrate:
$$
[\,\underline{ATE}(x),\overline{ATE}(x)\,] \ \Rightarrow \
[\,\mathbb{E}_X\{\underline{ATE}(X)\},\ \mathbb{E}_X\{\overline{ATE}(X)\}\,].
$$
This leverages observed heterogeneity to reduce width.

## Tightening assumptions (common variants)

- [[MTR]] (Monotone Treatment Response): $Y(1)\ge Y(0)$ a.s. (or $\le$). Implies $ATE \ge 0$ (or $\le 0$) and shrinks bounds accordingly; similarly narrows ATT/ATU bounds.
- [[MTS]] (Monotone Treatment Selection): selection is monotone in potential outcomes (e.g., treated have stochastically higher $Y(0)$). Provides inequality constraints tightening $\mu_{01},\mu_{10}$ ranges.
- [[MIV]] (Monotone Instrumental Variable): an instrument $Z$ orders potential outcomes or selection probabilities; conditioning on $Z$ and using monotonicity yields tighter conditional bounds, then average over $Z$.
- Shape/support restrictions: known ranges or stochastic dominance of outcome distributions by group, Lipschitz constraints, or parametric/semiparametric structure.

> [!tip] Practical strategy
> - Start with worst-case bounds (support-only).
> - Add credible monotonicity (MTR/MTS) or MIV if justified by domain knowledge.
> - Condition on covariates and average.

## Missing outcomes: Manski-style bounds

If $Y \in [y_L,y_U]$ and only a fraction $s$ is observed with observed mean $\bar{y}_{obs}$, then
$$
\mathbb{E}[Y] \in \big[\, s\,\bar{y}_{obs} + (1-s) y_L,\ \ s\,\bar{y}_{obs} + (1-s) y_U \,\big].
$$
Apply by group (treated/controls) to bound group means, then derive bounds for mean differences. See also [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] and [[Lee bounds]].

## Minimal code snippets

> [!example] R: Worst-case ATE, ATT (given yL,yU)

```r
manski_ate <- function(p, mu1, mu0, yL=0, yU=1){
  LB <- p*(mu1 - yU) + (1-p)*(yL - mu0)
  UB <- p*(mu1 - yL) + (1-p)*(yU - mu0)
  c(LB=LB, UB=UB)
}
manski_att <- function(mu1, yL=0, yU=1){
  c(LB = mu1 - yU, UB = mu1 - yL)
}

# Example
p  <- mean(df$D==1)
mu1 <- with(df, mean(Y[D==1]))
mu0 <- with(df, mean(Y[D==0]))
manski_ate(p, mu1, mu0, yL=0, yU=1)
manski_att(mu1, yL=0, yU=1)
```

> [!example] Python: Worst-case ATE, ATT

```python
def manski_ate(p, mu1, mu0, yL=0.0, yU=1.0):
    LB = p*(mu1 - yU) + (1-p)*(yL - mu0)
    UB = p*(mu1 - yL) + (1-p)*(yU - mu0)
    return LB, UB

def manski_att(mu1, yL=0.0, yU=1.0):
    return mu1 - yU, mu1 - yL

p  = (df['D']==1).mean()
mu1 = df.loc[df.D==1, 'Y'].mean()
mu0 = df.loc[df.D==0, 'Y'].mean()
LB, UB = manski_ate(p, mu1, mu0, yL=0, yU=1)
LB_att, UB_att = manski_att(mu1, yL=0, yU=1)
print("ATE bounds:", LB, UB)
print("ATT bounds:", LB_att, UB_att)
```

> [!example] R: Stratified bounds (by X strata)

```r
library(dplyr)
bounds_by_x <- df %>%
  group_by(X) %>%
  summarise(
    p = mean(D==1),
    mu1 = mean(Y[D==1]),
    mu0 = mean(Y[D==0]),
    LB = p*(mu1-1) + (1-p)*(0-mu0),
    UB = p*(mu1-0) + (1-p)*(1-mu0),
    .groups="drop"
  )
LB_overall <- with(bounds_by_x, sum(LB * prop.table(table(df$X))))
UB_overall <- with(bounds_by_x, sum(UB * prop.table(table(df$X))))
```

## Interpretation and reporting

> [!check] Report
> - Outcome support $[y_L, y_U]$ (and justification, e.g., binary 0–1, truncation)
> - Observed $\Pr(D{=}1)$, $\mathbb{E}[Y\mid D]$ by group
> - Bound endpoints (ATE/ATT/ATU), and any conditioning (by $X$ or $Z$)
> - Additional assumptions used (e.g., [[MTR]], [[MIV]]), and how they tighten bounds
> - Sensitivity: alternative supports, coarser/finer stratification, different monotonicity directions

> [!warning] Common pitfalls
> - Using bounds as point estimates; they quantify identification limits.
> - Declaring bounds “too wide” without exploring credible tightening (MTR/MIV/strata).
> - Inconsistent outcome supports across groups or post-hoc support choices.
> - Ignoring uncertainty: if you bootstrap, do so at the appropriate cluster level.

## Inference

- Bootstrap bound endpoints (unit- or cluster-level resampling) to form CIs for bounds.
- For stratified/MIV-based bounds, bootstrap the whole pipeline (stratification, conditional calculations, averaging).

## Relation to other partial-identification tools

- [[Lee bounds]]: assumes monotone selection with respect to treatment to address differential attrition; trims distributions to match selection rates.
- [[MTR]] / [[MTS]] / [[MIV]]: structure that tightens Manski bounds without point identification.
- [[Local Average Treatment Effect (LATE)|LATE]]: point-identifies a local effect under IV assumptions ([[exclusion restriction]], [[monotonicity]], [[relevance]]); complementary to bounds.
- Missing-data bounds: Manski-style worst-case bounds vs. model-based [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]/[[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]].

## Copy-ready formulas

- ATE bounds:
$$
\underline{ATE}=p(\mu_1^{obs}-y_U) + (1-p)(y_L-\mu_0^{obs}), \quad
\overline{ATE}=p(\mu_1^{obs}-y_L) + (1-p)(y_U-\mu_0^{obs}).
$$

- ATT bounds:
$$
ATT \in \big[\mu_1^{obs}-y_U,\ \mu_1^{obs}-y_L\big].
$$

- Missing-data mean bounds:
$$
\mathbb{E}[Y] \in \big[\, s\,\bar{y}_{obs} + (1-s) y_L,\ \ s\,\bar{y}_{obs} + (1-s) y_U \,\big].
$$

---

## Related notes
- [[Average Treatment Effect (ATE)]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[MTR]]
- [[MIV]]
- [[MTS]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[Lee bounds]]
- [[selection bias]]
- [[Attrition]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Doubly Robust estimators]]