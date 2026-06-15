---
title: Treatment-on-the-Treated (TOT)
aliases: [TOT, ETT, treatment on the treated]
tags: [causal-inference, rct, iv, did, policy-evaluation, matching, weighting]
updated: 2025-09-17
---

# Treatment-on-the-Treated (TOT)

> [!summary] Quick definition
> Treatment-on-the-Treated (TOT) is the average causal effect among those who actually received treatment:
> $$
> TOT \equiv ATT = \mathbb{E}[Y(1) - Y(0) \mid D=1].
> $$
> In many program evaluations, TOT and [[Average Treatment Effect on the Treated (ATT)]] are used interchangeably.

- Contrast with:
  - [[Intent-to-Treat (ITT)]]: effect of assignment/offer (Z), regardless of take-up.
  - [[Local Average Treatment Effect (LATE)|LATE]]: effect for compliers when using [[Instrumental Variables (IV)]] under monotonicity and exclusion.

## Why TOT matters

- Policy relevance: measures impact on those actually treated (participants/users).
- Evaluation settings:
  - RCTs with perfect compliance: TOT = ITT = ATE.
  - RCTs with noncompliance: ITT is diluted; TOT generally not point-identified without extra assumptions.
  - Observational designs: estimate ATT/TOT via design (e.g., [[Difference-in-Differences (DiD)]], [[matching]], weighting).

## Identification at a glance

- Fully compliant RCT:
  - Random assignment implies $D=Z$; thus:
  $$
  TOT = \mathbb{E}[Y \mid D=1] - \mathbb{E}[Y \mid D=0] = ITT.
  $$
- Noncompliance with valid IV:
  - Standard Wald ratio identifies [[Local Average Treatment Effect (LATE)|LATE]]:
  $$
  LATE = \frac{ITT}{\mathbb{E}[D \mid Z=1]-\mathbb{E}[D \mid Z=0]}.
  $$
  - When is LATE = TOT?
    - One-sided compliance (no always-takers, so $D(0)=0$ for all), [[monotonicity]], [[exclusion restriction]], and random assignment. Then treated units are compliers when $Z=1$, so:
    $$
    LATE = ATT = TOT.
    $$
  - Otherwise, TOT is not point-identified from Z; consider bounds (e.g., [[Manski bounds]], [[Lee bounds]] if selection monotonicity).

- Selection-on-observables (unconfoundedness):
  - If $\{Y(0),Y(1)\} \perp D \mid X$ and [[Overlap]] holds, ATT/TOT is identifiable via weighting/matching or doubly robust methods.

- Difference-in-Differences:
  - Under the [[parallel trends assumption]] (often conditional on [[covariates]]), DiD typically identifies ATT for treated units, i.e., an effect-on-the-treated.

## Estimation strategies

### 1) Randomized experiments
- Perfect compliance:
  - Difference in means between $D=1$ and $D=0$ estimates TOT.
- Noncompliance (one-sided):
  - Use Wald/2SLS with Z as an instrument; report that LATE = TOT under the additional assumptions above.

### 2) Selection on observables (ATT weighting/matching)
- ATT weighting (controls upweighted where treatment propensity is high):
  - Let $e(X)=P(D=1\mid X)$, then a common ATT-IPW estimator weights controls by $e(X)/(1-e(X))$ and treated by 1.
- Matching on $X$ (e.g., nearest neighbor, caliper) targeting ATT.

### 3) Difference-in-Differences (effect on treated)
- With panel DiD:
$$
Y_{it} = \alpha_i + \gamma_t + \beta \,(D_i \cdot Post_t) + \varepsilon_{it},
$$
- $\beta$ recovers an ATT/TOT-type effect for treated units under parallel trends and no [[Anticipatory effects]]/[[No spillovers]].

### 4) IV/Encouragement (general case)
- Report ITT and LATE. Clarify that TOT is not identified unless extra assumptions (e.g., one-sided compliance) are plausible.
- Provide bounds if appropriate.

## Common pitfalls

> [!warning] Avoid these
> - “As-treated” comparisons that ignore random assignment (bias from endogenous D).
> - Calling a Wald ratio “TOT” without noting that it equals LATE and only matches TOT under one-sided compliance plus IV assumptions.
> - Conditioning on post-treatment variables (see [[bad controls]]), which can distort ATT/TOT.
> - Ignoring [[interference]]/[[No spillovers]] that can affect both treated and controls.

## Minimal code snippets

> [!example] RCT with perfect compliance (difference in means)

```r
with(df, mean(Y[D==1]) - mean(Y[D==0]))    # TOT = ATT
t.test(Y ~ D, data = df)
```

> [!example] ATT weighting (selection on observables)

```r
# R: ATT-IPW with propensity score
library(glmnet)
ps <- glm(D ~ X1 + X2 + X3, family = binomial(), data = df)$fitted.values
w <- ifelse(df$D == 1, 1, ps / (1 - ps))
att_ipw <- with(df, weighted.mean(Y[D==1], w[D==1]) - weighted.mean(Y[D==0], w[D==0]))
att_ipw
```

```python
# Python: ATT-IPW (sketch)
from sklearn.linear_model import LogisticRegression
import numpy as np

X = df[['X1','X2','X3']].values
ps = LogisticRegression(max_iter=2000).fit(X, df['D']).predict_proba(X)[:,1]
w = np.where(df['D']==1, 1.0, ps/(1-ps))
att_ipw = (df.loc[df.D==1, 'Y']*w[df.D==1]).sum()/w[df.D==1].sum() \
          - (df.loc[df.D==0, 'Y']*w[df.D==0]).sum()/w[df.D==0].sum()
print(att_ipw)
```

> [!example] DiD ATT/TOT

```r
# R (fixest)
library(fixest)
est <- feols(Y ~ D:Post | id + time, cluster = ~id, data = df)
etable(est)   # beta is ATT/TOT under DiD assumptions
```

> [!example] One-sided noncompliance: LATE = TOT (Wald)

```r
# R
ITT_y <- with(df, mean(Y[Z==1]) - mean(Y[Z==0]))
ITT_d <- with(df, mean(D[Z==1]) - mean(D[Z==0]))
LATE  <- ITT_y / ITT_d  # equals TOT if no always-takers, plus exclusion & monotonicity
LATE
```

```stata
* Stata: 2SLS (LATE) equals TOT under one-sided compliance + IV assumptions
ivregress 2sls Y (D = Z), robust
```

## Assumptions to state (by approach)

- RCT perfect compliance: randomization, [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]], no attrition bias.
- ATT weighting/matching: [[Unconfoundedness]] and [[Overlap]]; correct PS model or doubly robust methods (e.g., [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]], [[Doubly Robust estimators]]).
- DiD: [[parallel trends assumption]], no (or modeled) [[Anticipatory effects]], [[No spillovers]]/[[interference]], stable [[composition]].
- IV LATE→TOT equivalence: random assignment, [[exclusion restriction]], [[monotonicity]], and one-sided compliance (no always-takers).

## Reporting essentials

- Define estimand clearly (TOT/ATT) and population (who is “treated”?).
- Describe the identification strategy and its assumptions.
- Provide diagnostics: balance (for observables), [[pre-trends]]/[[event study]] (for DiD), first-stage strength (for IV).
- Report uncertainty with appropriate [[clustered standard errors]] and [[few-cluster corrections]] if needed.
- If using IV, report compliance rates and discuss whether LATE plausibly equals TOT.

## Copy-ready formulas

- Definition:
$$
TOT = ATT = \mathbb{E}[Y(1) - Y(0) \mid D=1]
$$

- ATT-IPW form (schematic):
$$
\widehat{ATT} = \frac{\sum_{i:D_i=1} Y_i}{N_1} - 
\frac{\sum_{i:D_i=0} \frac{e(X_i)}{1-e(X_i)}\, Y_i}{\sum_{i:D_i=0} \frac{e(X_i)}{1-e(X_i)}}
$$

- DiD ATT (two-period, two-group contrast):
$$
ATT = (\bar{Y}^{post}_{T} - \bar{Y}^{pre}_{T}) - (\bar{Y}^{post}_{C} - \bar{Y}^{pre}_{C})
$$

- IV equivalence (one-sided compliance):
$$
LATE = \frac{ITT}{\Delta_D} = TOT \quad \text{if no always-takers, plus exclusion and monotonicity.}
$$

---

## Related notes
- [[Intent-to-Treat (ITT)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[Instrumental Variables (IV)]]
- [[exclusion restriction]]
- [[monotonicity]]
- [[Average Treatment Effect on the Treated (ATT)]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[event study]]
- [[pre-trends]]
- [[matching]]
- [[propensity score]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[Unconfoundedness]]
- [[Overlap]]
- [[No spillovers]]
- [[interference]]
- [[composition]]
- [[bad controls]]
- [[clustered standard errors]]
- [[few-cluster corrections]]
- [[Lee bounds]]
- [[Manski bounds]]