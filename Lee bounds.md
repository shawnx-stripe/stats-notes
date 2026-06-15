---
title: Lee Bounds
aliases: [Lee (2009) bounds, monotone selection bounds, trimming bounds]
tags: [causal-inference, attrition, selection, bounds, robustness, sensitivity]
updated: 2025-09-17
---

# Lee Bounds

> [!summary] Quick definition
> Lee bounds provide worst-case bounds on treatment effects under differential sample selection/attrition, assuming monotone selection with respect to treatment (treatment weakly increases or weakly decreases selection). They trim the higher-selection arm so effective selection rates match, yielding upper and lower bounds on the effect (e.g., [[Average Treatment Effect on the Treated (ATT)]]).

- Reference: Lee (2009, QJE)
- Use when $Y$ is observed only if selected (e.g., employed/respondent), and selection rates differ by treatment.

## Setup

- Treatment: $D \in \{0,1\}$
- Selection: $S \in \{0,1\}$; observe $Y$ only if $S=1$
- Selection rates: $\pi_d = \Pr(S=1 \mid D=d)$
- Goal (example): ATT among selected units; generally not point-identified without more structure

## Assumption: Monotone selection in treatment

- Either $S(1) \ge S(0)$ for all units (treatment weakly increases selection) or $S(1) \le S(0)$ (weakly decreases)
- No assumptions on how $Y$ relates to $S$; bounds consider worst-case sorting of marginally selected units

> [!note] Determine direction
> - If $\pi_1 \ge \pi_0$: treatment increases selection; trim treated group
> - If $\pi_0 > \pi_1$: control increases selection; trim control group

## Bounding algorithm (ATT)

Case A: Treated has higher selection ($\pi_1 \ge \pi_0$)
1) Excess selection share:
$$
\Delta = \frac{\pi_1 - \pi_0}{\pi_1} \in [0,1)
$$
2) Let $F_1$ be the CDF of $Y$ among $(D=1,S=1)$. Trim a fraction $\Delta$ from treated:
- Lower bound (LB): drop the top $\Delta$ of $Y$ in $(D=1,S=1)$
- Upper bound (UB): drop the bottom $\Delta$ of $Y$ in $(D=1,S=1)$
3) With trimmed means $\mu_1^{LB}, \mu_1^{UB}$ and untrimmed control mean $\mu_0=\mathbb{E}[Y\mid D=0,S=1]$:
$$
ATT \in \big[\ \mu_1^{LB} - \mu_0,\ \mu_1^{UB} - \mu_0\ \big]
$$

Case B: Control has higher selection ($\pi_0 > \pi_1$)
1) $\Delta = \dfrac{\pi_0 - \pi_1}{\pi_0}$
2) Trim the control group:
- LB: drop the bottom $\Delta$ from $(D=0,S=1)$
- UB: drop the top $\Delta$ from $(D=0,S=1)$
3) With trimmed control means $\mu_0^{LB}, \mu_0^{UB}$ and untrimmed treated mean $\mu_1$:
$$
ATT \in \big[\ \mu_1 - \mu_0^{UB},\ \mu_1 - \mu_0^{LB}\ \big]
$$

> [!tip] Intuition
> Trimming removes “marginally selected” observations that exist only in the higher-selection arm. Dropping from the top vs. bottom yields worst/best cases.

## Copy-ready formulas

- Excess selection (treated higher):
$$
\Delta = \frac{\pi_1 - \pi_0}{\pi_1}
$$

- Trimmed means (treated higher):
$$
\mu_1^{LB} = \mathbb{E}[Y \mid D{=}1,S{=}1, Y \le q_1^{1-\Delta}], \quad
\mu_1^{UB} = \mathbb{E}[Y \mid D{=}1,S{=}1, Y \ge q_1^{\Delta}]
$$
where $q_1^\alpha$ is the $\alpha$ quantile of $Y$ in $(D{=}1,S{=}1)$.

- ATT bounds (treated higher):
$$
ATT \in \left[\mu_1^{LB} - \mu_0,\ \mu_1^{UB} - \mu_0\right], \quad \mu_0 = \mathbb{E}[Y \mid D{=}0,S{=}1]
$$

(Swap roles if control has higher selection.)

## Inference

- Use nonparametric bootstrap to form CIs for bound endpoints:
  - Resample observations at the unit level (cluster-level if clustered)
  - Recompute $\pi_d$, $\Delta$, quantiles, trimmed means, bounds in each replicate
  - Use percentile or BCa intervals for each endpoint

> [!warning] Discrete outcomes / ties
> If many observations equal the trimming quantile, randomize trimming among ties or use fractional weights to hit the exact fraction.

## With covariates (sharper bounds)

- Stratify by $X$ (or use predicted selection $\hat\pi_d(x)$), trim within strata, then average across $X$ using the treated-selected distribution
- Alternatively, reweight controls to match treated $X$ (e.g., [[entropy balancing]]), then apply Lee trimming

## Practical workflow

> [!check] Steps
> - [ ] Compute $\pi_1$ and $\pi_0$; decide direction of monotonicity
> - [ ] Work on selected sample ($S=1$)
> - [ ] Compute $\Delta$; trim higher-selection arm’s tails to match selection rates
> - [ ] Compute trimmed means; form LB/UB
> - [ ] Bootstrap CIs; cluster if needed
> - [ ] Sensitivity: covariate stratification, alternative monotonicity direction (if ambiguous)

## Common pitfalls

> [!warning] Avoid these
> - Assuming monotonicity direction without checking selection rates
> - Mixing trimming definitions across groups (must trim the higher-selection arm)
> - Reporting a single point estimate when only bounds are identified
> - Ignoring clustering in bootstrap when selection/treatment is clustered

## Minimal code snippets

> [!example] R: Lee bounds (treated higher or control higher)

```r
# df: D (0/1), S (0/1), Y (NA allowed when S==0)
pi1 <- with(df, mean(S[D==1], na.rm=TRUE))
pi0 <- with(df, mean(S[D==0], na.rm=TRUE))

dsel <- subset(df, S==1)

if (pi1 >= pi0) {
  Delta <- (pi1 - pi0) / pi1
  y1 <- subset(dsel, D==1)$Y
  y0 <- subset(dsel, D==0)$Y
  q_top <- quantile(y1, 1-Delta, na.rm=TRUE)
  q_bot <- quantile(y1, Delta,   na.rm=TRUE)
  mu1_LB <- mean(y1[y1 <= q_top], na.rm=TRUE)
  mu1_UB <- mean(y1[y1 >= q_bot], na.rm=TRUE)
  mu0    <- mean(y0, na.rm=TRUE)
  LB <- mu1_LB - mu0
  UB <- mu1_UB - mu0
} else {
  Delta <- (pi0 - pi1) / pi0
  y1 <- subset(dsel, D==1)$Y
  y0 <- subset(dsel, D==0)$Y
  q_top <- quantile(y0, 1-Delta, na.rm=TRUE)
  q_bot <- quantile(y0, Delta,   na.rm=TRUE)
  mu0_UB <- mean(y0[y0 <= q_top], na.rm=TRUE)
  mu0_LB <- mean(y0[y0 >= q_bot], na.rm=TRUE)
  mu1    <- mean(y1, na.rm=TRUE)
  LB <- mu1 - mu0_UB
  UB <- mu1 - mu0_LB
}
c(LB=LB, UB=UB)
```

> [!example] Stata: Lee bounds (complete)

```stata
* Variables: D (0/1), S (0/1), Y (only observed if S==1)

summ S if D==1
scalar pi1 = r(mean)
summ S if D==0
scalar pi0 = r(mean)

preserve
keep if S==1

tempname LB UB
if (pi1 >= pi0) {
    scalar Delta = (pi1 - pi0)/pi1
    local ptop = 100*(1-Delta)
    local pbot = 100*(Delta)
    quietly _pctile Y if D==1, p(`pbot' `ptop')
    scalar q_bot = r(r1)
    scalar q_top = r(r2)
    quietly su Y if D==1 & Y <= q_top
    scalar mu1_LB = r(mean)
    quietly su Y if D==1 & Y >= q_bot
    scalar mu1_UB = r(mean)
    quietly su Y if D==0
    scalar mu0 = r(mean)
    scalar `LB' = mu1_LB - mu0
    scalar `UB' = mu1_UB - mu0
}
else {
    scalar Delta = (pi0 - pi1)/pi0
    local ptop = 100*(1-Delta)
    local pbot = 100*(Delta)
    quietly _pctile Y if D==0, p(`pbot' `ptop')
    scalar q_bot = r(r1)
    scalar q_top = r(r2)
    quietly su Y if D==0 & Y <= q_top
    scalar mu0_UB = r(mean)
    quietly su Y if D==0 & Y >= q_bot
    scalar mu0_LB = r(mean)
    quietly su Y if D==1
    scalar mu1 = r(mean)
    scalar `LB' = mu1 - mu0_UB
    scalar `UB' = mu1 - mu0_LB
}
di as txt "Lee bounds (ATT):"
di as res "  Lower bound: " %9.4f scalar(`LB')
di as res "  Upper bound: " %9.4f scalar(`UB')
restore
```

> [!example] Stata: Bootstrap CIs
> Wrap the Lee bounds computation (see Stata block above) in a `program ... rclass` that returns `r(LB)` and `r(UB)`, then:

```stata
bootstrap r(LB) r(UB), reps(999) seed(12345): leebounds
* Cluster bootstrap: add cluster(clusterid)
```

> [!example] Python: Lee bounds (both cases)

```python
import numpy as np
import pandas as pd

def lee_bounds(df):
    pi1 = df.loc[df.D==1, 'S'].mean()
    pi0 = df.loc[df.D==0, 'S'].mean()
    dsel = df[df.S==1].copy()

    y1 = dsel.loc[dsel.D==1, 'Y'].dropna().values
    y0 = dsel.loc[dsel.D==0, 'Y'].dropna().values
    if len(y1)==0 or len(y0)==0:
        return np.nan, np.nan

    if pi1 >= pi0:
        Delta = (pi1 - pi0) / max(pi1, 1e-12)
        q_top = np.quantile(y1, 1-Delta)
        q_bot = np.quantile(y1, Delta)
        mu1_LB = y1[y1 <= q_top].mean()
        mu1_UB = y1[y1 >= q_bot].mean()
        mu0    = y0.mean()
        LB = mu1_LB - mu0
        UB = mu1_UB - mu0
    else:
        Delta = (pi0 - pi1) / max(pi0, 1e-12)
        q_top = np.quantile(y0, 1-Delta)
        q_bot = np.quantile(y0, Delta)
        mu0_UB = y0[y0 <= q_top].mean()
        mu0_LB = y0[y0 >= q_bot].mean()
        mu1    = y1.mean()
        LB = mu1 - mu0_UB
        UB = mu1 - mu0_LB
    return LB, UB

LB, UB = lee_bounds(df)
print(f"Lee bounds (ATT): LB={LB:.4f}, UB={UB:.4f}")
```

## Reporting essentials

- Direction of monotonicity and selection rates ($\pi_1,\pi_0$)
- Trimming fraction $\Delta$ and which group was trimmed
- Bound endpoints with bootstrap CIs (and clustering level if applicable)
- Any covariate stratification or reweighting used pre-trimming
- Sensitivity to alternative stratifications or monotonicity direction

---

## Related notes
- [[Average Treatment Effect on the Treated (ATT)]]
- [[composition]]
- [[entropy balancing]]
- [[propensity score]]
- [[Unconfoundedness]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Difference-in-Differences (DiD)]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[placebo test]]
- [[selection bias]]
- [[Attrition]]