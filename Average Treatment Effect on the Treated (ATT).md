---
title: Average Treatment Effect on the Treated (ATT)
aliases: [ATT, treatment-on-the-treated, effect on the treated, ATE on treated]
tags: [causal-inference, att, matching, weighting, did, iv, estimation]
updated: 2025-09-17
---

# Average Treatment Effect on the Treated (ATT)

> [!summary] Quick definition
> The ATT is the average causal effect for units that actually received treatment:
> $$
> ATT = \mathbb{E}[Y(1) - Y(0) \mid D=1].
> $$
> In many contexts, ATT equals [[Treatment-on-the-Treated (TOT)]].

- Focuses on the treated population’s benefit, often the policy-relevant group.
- Contrast with [[Average Treatment Effect (ATE)|ATE]] (whole population) and [[Local Average Treatment Effect (LATE)|LATE]] (compliers under IV).

## Identification at a glance

- RCT with perfect compliance: ATT = ATE = [[Intent-to-Treat (ITT)]].
- Selection on observables (unconfoundedness):
  - {Y(1), Y(0)} ⟂ D | X and [[Overlap]] → identify ATT via [[matching]], [[propensity score]] [[Inverse Probability Weighting (IPW)|IPW]], or [[Augmented Inverse Probability Weighting (AIPW)|AIPW]].
- [[Difference-in-Differences (DiD)]]:
  - Under the [[parallel trends assumption]] (possibly conditional on [[covariates]]), DiD typically identifies an ATT for treated units.
- IV/Encouragement with [[noncompliance]]:
  - ATT is generally not point-identified. [[Local Average Treatment Effect (LATE)|LATE]] equals ATT only under additional conditions (e.g., one-sided compliance, [[exclusion restriction]], [[monotonicity]]).

## Core formulas

- Definition:
$$
ATT = \mathbb{E}[Y(1) \mid D=1] - \mathbb{E}[Y(0) \mid D=1]
$$

- ATT via weighting (controls reweighted to treated composition):
$$
\widehat{ATT} =
\frac{\sum_{i:D_i=1} Y_i}{N_1}
\;-\;
\frac{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)}\, Y_i}{\sum_{i:D_i=0} \frac{\hat e(X_i)}{1-\hat e(X_i)}}
$$
where $e(X)=P(D=1\mid X)$ and $N_1$ is the number treated.

- ATT via DiD (two groups, two periods):
$$
ATT = \big(\bar Y^{post}_{T} - \bar Y^{pre}_{T}\big) - \big(\bar Y^{post}_{C} - \bar Y^{pre}_{C}\big)
$$

## Estimation strategies

### 1) Selection on observables

- Matching (nearest neighbor, Mahalanobis, PS within calipers)
- IPW (ATT weights: treated = 1; controls = e(X)/(1−e(X)))
- Doubly robust (AIPW/DR): combine outcome regression and PS weighting for consistency if either model is correct. See [[Augmented Inverse Probability Weighting (AIPW)|AIPW]] and [[Doubly Robust estimators]].

> [!check] Diagnostics
> - Balance after matching/weighting (SMDs, variance ratios, eCDF).
> - Overlap/common support; trim extreme PS or weights.
> - Sensitivity to unobserved confounding (e.g., [[Rosenbaum sensitivity]]).

### 2) Difference-in-Differences (ATT for treated)

- Panel TWFE:
$$
Y_{it} = \alpha_i + \gamma_t + \beta \,(D_i \cdot Post_t) + \varepsilon_{it}
$$
- β is an ATT under parallel trends (no/handled [[Anticipatory effects]], [[No spillovers]], stable [[composition]]).
- [[staggered adoption]]: use modern estimators ([[Callaway–Sant’Anna estimator]], [[Sun–Abraham estimator]]) that recover cohort-time ATT(g,t) and valid aggregates.

> [!check] Diagnostics
> - [[pre-trends]] plots; robust [[event study]] with leads/lags.
> - Appropriate [[clustered standard errors]]; [[few-cluster corrections]] if clusters are few.

### 3) IV/Encouragement

- Report ITT and LATE. ATT equals LATE only with additional assumptions (e.g., one-sided compliance).
- If ATT is the target but only LATE is identified, be explicit about the target population (compliers) and external validity limits.

## Good practice

> [!check] ATT workflow
> - [ ] Define target population (which “treated”? timing/intensity)
> - [ ] Choose identification (unconfoundedness vs. DiD vs. IV)
> - [ ] For unconfoundedness: specify pre-treatment X; achieve covariate balance and overlap
> - [ ] For DiD: justify parallel trends; show pre-trends and event studies
> - [ ] Use clustered or small-sample-robust inference as needed
> - [ ] Report sensitivity (alternative controls, windows, specs; unobserved bias)

> [!warning] Common pitfalls
> - Using post-treatment variables (see [[bad controls]]).
> - Severe lack of overlap (huge weights); untrimmed IPW instability.
> - Relying on naive TWFE with [[staggered adoption]] and heterogeneous effects.
> - Confusing ATT with [[Local Average Treatment Effect (LATE)|LATE]] or assuming they are the same without conditions.

## Minimal code snippets

> [!example] R: ATT-IPW and matching

```r
# ATT-IPW
ps_mod <- glm(D ~ X1 + X2 + poly(X3,2) + X1:X2, data = df, family = binomial())
ps <- ps_mod$fitted.values
w <- ifelse(df$D==1, 1, ps/(1-ps))
ATT <- with(df, weighted.mean(Y[D==1], w[D==1]) -
                 weighted.mean(Y[D==0], w[D==0]))

# Matching (MatchIt)
library(MatchIt); library(cobalt)
m <- matchit(D ~ X1 + X2 + X3, data = df, method = "nearest", replace = TRUE, caliper = .2)
dfm <- match.data(m)
ATT_match <- with(dfm, weighted.mean(Y[D==1], weights[D==1]) -
                        weighted.mean(Y[D==0], weights[D==0]))
```

> [!example] R: ATT via DiD (panel)

```r
library(fixest)
est <- feols(Y ~ D:Post | id + time, cluster = ~id, data = df)
etable(est)  # beta = ATT under DiD assumptions
```

> [!example] R: Staggered DiD (Callaway–Sant’Anna)

```r
library(did)
att <- att_gt(yname="Y", tname="time", idname="id", gname="G", data=df, panel=TRUE)
overall <- aggte(att, type="simple")    # aggregated ATT
summary(overall)
```

> [!example] Stata

```stata
* ATT-IPW (teffects)
teffects ipw (Y) (D X1 X2 X3), atet vce(robust)

* Matching
teffects psmatch (Y) (D X1 X2 X3), atet vce(robust)

* DiD ATT (TWFE)
reghdfe Y c.Post##i.D, absorb(id time) vce(cluster id)
```

> [!example] Python (IPW, sketch)

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

X = df[['X1','X2','X3']].values
ps = LogisticRegression(max_iter=2000).fit(X, df['D']).predict_proba(X)[:,1]
df['w'] = np.where(df['D']==1, 1.0, ps/(1-ps))
mu1 = (df.loc[df.D==1, 'Y']*df.loc[df.D==1,'w']).sum()/df.loc[df.D==1,'w'].sum()
mu0 = (df.loc[df.D==0, 'Y']*df.loc[df.D==0,'w']).sum()/df.loc[df.D==0,'w'].sum()
ATT = mu1 - mu0
print(ATT)
```

## Copy-ready snippets

- ATT:
$$
ATT = \mathbb{E}[Y(1)-Y(0) \mid D=1]
$$

- ATT-IPW control weights:
$$
w_i =
\begin{cases}
1, & D_i=1 \\
\frac{\hat e(X_i)}{1-\hat e(X_i)}, & D_i=0
\end{cases}
$$

- DiD contrast:
$$
ATT = (\bar Y^{post}_{T} - \bar Y^{pre}_{T}) - (\bar Y^{post}_{C} - \bar Y^{pre}_{C})
$$

## Reporting essentials

- Define treated population, timing/intensity, and estimand (ATT/TOT).
- Identification strategy and assumptions (unconfoundedness, parallel trends, IV assumptions).
- Diagnostics: balance/overlap (matching/weighting), pre-trends/event studies (DiD), first stage/exclusion (IV).
- Inference details: clustering level, [[few-cluster corrections]] if applicable.
- Sensitivity analyses: alternative specs, trimming/calipers, control sets/windows.

---

## Related notes
- [[Treatment-on-the-Treated (TOT)]]
- [[Average Treatment Effect (ATE)]]
- [[Local Average Treatment Effect (LATE)|Local Average Treatment Effect (LATE)]]
- [[Intent-to-Treat (ITT)]]
- [[matching]]
- [[propensity score]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Doubly Robust estimators]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[event study]]
- [[staggered adoption]]
- [[Callaway–Sant’Anna estimator]]
- [[Sun–Abraham estimator]]
- [[covariates]]
- [[bad controls]]
- [[composition]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Rosenbaum sensitivity]]
- [[Overlap]]