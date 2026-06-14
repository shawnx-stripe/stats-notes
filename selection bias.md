---
title: Selection Bias
aliases: [Selection bias, sample selection bias, selection on unobservables, conditioning bias]
tags: [causal-inference, design, diagnostics, missing-data, attrition, econometrics]
updated: 2025-09-17
---

# Selection Bias

> [!summary] Quick definition
> Selection bias arises when treatment assignment or sample inclusion depends on factors related to the potential outcomes. Then naive comparisons confound causal effects with pre-existing differences or selective observation. It can occur at:
> - Assignment: $D$ correlated with $\{Y(1),Y(0)\}$ (violates [[Unconfoundedness]])
> - Observation: outcome observed only if $S=1$ and $S$ depends on $Y(d)$ or its causes (sample selection/[[Attrition]])
> - Conditioning: controlling on post-treatment variables/colliders (see [[bad controls]])

Common settings: self-selection into programs, nonresponse/attrition, case-control sampling, restricting to “survivors” or “employed,” conditioning on post-treatment mediators.

## Formal views

- Mean difference decomposition (cross-section):
$$
\underbrace{\mathbb{E}[Y \mid D{=}1] - \mathbb{E}[Y \mid D{=}0]}_{\text{naive diff}}
= \underbrace{ATT}_{\mathbb{E}[Y(1)-Y(0)\mid D{=}1]}
+ \underbrace{\big(\mathbb{E}[Y(0)\mid D{=}1]-\mathbb{E}[Y(0)\mid D{=}0]\big)}_{\text{selection bias term}}
$$

- Sample selection: observe $Y$ only if $S=1$.
  - If $S$ depends on $Y(d)$ or unobservables tied to $Y$, then
  $$
  \mathbb{E}[Y \mid D,S{=}1] \neq \mathbb{E}[Y(d) \mid D]
  $$
  leading to bias unless adjusted.

- Collider conditioning (DAG intuition): $D \to M \leftarrow U \to Y$.
  - Conditioning on $M$ (a collider) opens a spurious path $D \leftrightarrow U \to Y$.

## Types of selection bias

- Selection on observables: $D$ depends on $X$ that also affects $Y$; can be addressed under [[Unconfoundedness]] using [[matching]], [[propensity score]], [[Inverse Probability Weighting (IPW)|IPW]], or [[Doubly Robust estimators]] (e.g., [[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]).
- Selection on unobservables: $D$ depends on unobserved $U$ affecting $Y$; requires designs (e.g., [[Instrumental Variables (IV)]], [[Regression Discontinuity Design (RDD)]], [[Synthetic Control]]) or structural assumptions.
- Sample selection/attrition: $S$ depends on $D$ and $Y$ or their determinants (e.g., employment-only earnings).
- Post-treatment conditioning: controlling for mediators or restricting to “survivors” (see [[bad controls]], “truncation by death”).
- Time-varying selection in panels/DiD: composition changes across groups over time (see [[composition]]), differential [[Attrition]], or migration after treatment.

## Missing-data taxonomy (for $S$)

- MCAR: missingness independent of data → unbiased with complete cases (rare).
- MAR: $S \perp Y \mid X$ → recoverable with weighting/modeling (e.g., [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]).
- MNAR: $S$ depends on unobserved outcomes or errors → needs instruments/structure/bounds (e.g., [[Lee bounds]]).

## Consequences in common designs

- RCTs: noncompliance causes treatment endogeneity; analyze [[Intent-to-Treat (ITT)]] and use [[Local Average Treatment Effect (LATE)|LATE]] via [[Instrumental Variables (IV)|IV]]. Attrition → use [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]; consider [[Lee bounds]] if monotone selection plausible.
- [[Difference-in-Differences (DiD)]]: differential entry/exit or measurement changes create composition bias; check counts, covariate [[pre-trends]], and use weighting/stratification; see [[composition]].
- [[Instrumental Variables (IV)|IV]]: selection that directly affects $Y$ can violate the [[exclusion restriction]]; instruments for selection (Heckman-style) require strong assumptions.
- [[Regression Discontinuity Design (RDD)|RDD]]: precise manipulation at the cutoff (sorting) breaks identification; test density/balance (e.g., [[McCrary test|McCrary density test]]/[[rddensity]]).

## Remedies and tools

### Design-first
- Randomization/encouragement; sharp eligibility rules (RDD); exogenous timing (DiD with credible [[parallel trends assumption]]).
- Avoid conditioning on post-treatment variables; restrict to pre-specified samples; pre-register rules.

### Reweighting/adjustment (selection on observables)
- [[Inverse Probability Weighting (IPW)|IPW]] for treatment; [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]] for selection/attrition:
$$
w^{\text{IPCW}}_i = \frac{1}{\hat P(S_i{=}1 \mid \text{history or } X_i)}
$$
- [[entropy balancing]] / calibration to match covariate moments.
- [[Doubly Robust estimators]] ([[Augmented Inverse Probability Weighting (AIPW)|AIPW]], [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]) under ignorability and [[Overlap]].

### Structural selection models (Heckman)
- Outcome $Y^\ast = X\beta + \varepsilon$, observed if $S=1$, with latent selection $S^\ast = Z\gamma + u$.
- Under joint normality, for $S=1$:
$$
\mathbb{E}[Y \mid X,S{=}1] = X\beta + \rho\sigma_\varepsilon \lambda(Z\gamma)
$$
where $\lambda(\cdot)$ is the inverse Mills ratio. Requires exclusion variables in $Z$ for credible identification.

### Bounds and sensitivity
- [[Lee bounds]] for monotone selection (increase/decrease in selection with treatment).
- Sensitivity to unobserved confounding: [[Rosenbaum sensitivity]], [[Oster’s delta]].
- Placebos/negatives: [[placebo test]] on unaffected outcomes or pre-periods.

## Diagnostics

> [!check] What to examine
> - Balance and overlap on $X$ pre-treatment; PS overlap; weight distributions (ESS).
> - Selection/attrition rates by group/time; compare characteristics of stayers vs. leavers.
> - [[pre-trends]] in outcomes and covariates; event-study leads; counts over time.
> - For RDD: density tests and covariate continuity at the cutoff.
> - For IV: first-stage strength ([[relevance]]) and validity checks (placebo outcomes, exclusion channels).

> [!warning] Red flags
> - Large, asymmetric attrition after treatment onset.
> - Subsetting on post-treatment variables (e.g., only employed, only users).
> - Extreme IPW/IPCW weights (poor [[Overlap]]); unstable estimates.

## Minimal code snippets

> [!example] R: Selection-bias decomposition (pre-treatment outcome proxy)

```r
# Decompose naive diff into ATT + selection term using pre-period Y0 as proxy for Y(0)
naive <- with(df, mean(Y[D==1]) - mean(Y[D==0]))
sel_term <- with(df, mean(Y0[D==1]) - mean(Y0[D==0]))  # proxy for E[Y(0)|D=1]-E[Y(0)|D=0]
c(naive = naive, selection_proxy = sel_term)
```

> [!example] R: IPCW for attrition

```r
# observed = 1 if Y observed
ipcw_mod <- glm(observed ~ X1 + X2 + D + time, family = binomial(), data = df)
p_obs <- pmax(pmin(ipcw_mod$fitted.values, 0.995), 0.005)
df$w_ipcw <- 1 / p_obs

# Use IPCW in outcome model (with FE/DiD as needed)
# library(fixest)
# feols(Y ~ D:Post | id + time, data = subset(df, observed==1), weights = ~w_ipcw, cluster = ~id)
```

> [!example] Stata: Heckman selection model

```stata
* Outcome observed only if employed==1
heckman Y X1 X2, select(employed = Z1 Z2 X1 X2) twostep
* Or MLE:
heckman Y X1 X2, select(employed = Z1 Z2 X1 X2)
```

> [!example] Python: IPCW (sketch)

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

obs = df['observed'].values.astype(int)
X = df[['X1','X2','D','time']].values
p = LogisticRegression(max_iter=2000).fit(X, obs).predict_proba(X)[:,1]
w_ipcw = 1/np.clip(p, 1e-3, 1-1e-3)
df['w_ipcw'] = w_ipcw
# Use weights in regression; cluster SEs appropriately
```

> [!example] Lee bounds linkage
See [[Lee bounds]] for trimming-based bounds under monotone selection when differential attrition is present.

## Copy-ready snippets

- Naive vs. ATT + selection term:
$$
\mathbb{E}[Y \mid D{=}1] - \mathbb{E}[Y \mid D{=}0]
= ATT + \big(\mathbb{E}[Y(0)\mid D{=}1]-\mathbb{E}[Y(0)\mid D{=}0]\big)
$$

- Heckman correction (selected sample expectation):
$$
\mathbb{E}[Y \mid X,S{=}1] = X\beta + \rho\sigma_\varepsilon \lambda(Z\gamma)
$$

- IPCW:
$$
w^{\text{IPCW}} = \frac{1}{\hat P(S{=}1 \mid \text{history or } X)}
$$

## Practical guidance

> [!check] Checklist
> - [ ] Define estimand and population; avoid post-treatment conditioning
> - [ ] Diagnose selection at assignment and observation stages
> - [ ] Choose design/estimator consistent with assumptions (IV/RDD/SCM vs. ignorability)
> - [ ] If attrition: estimate IPCW; consider [[Lee bounds]] and sensitivity analysis
> - [ ] Use clustered/robust SEs; apply [[few-cluster corrections]] when needed
> - [ ] Report balance/overlap, selection rates, and robustness (placebos, alternative samples)

> [!warning] Common pitfalls
> - Treating balance on a few observables as proof against unobserved selection
> - Ignoring composition changes in DiD (see [[composition]])
> - Using different seasonal adjustments across groups (see [[seasonality]])
> - Failing to justify exclusion in selection models (weak/invalid instruments in Heckman)

---

Related notes to create:
- [[Unconfoundedness]]
- [[Stable Unit Treatment Value Assumption (SUTVA)|SUTVA]]
- [[Overlap]]
- [[propensity score]]
- [[matching]]
- [[Inverse Probability Weighting (IPW)|IPW]]
- [[Inverse Probability of Censoring Weighting (IPCW)|IPCW]]
- [[Augmented Inverse Probability Weighting (AIPW)|AIPW]]
- [[Targeted Maximum Likelihood Estimation (TMLE)|TMLE]]
- [[Doubly Robust estimators]]
- [[double machine learning]]
- [[Instrumental Variables (IV)]]
- [[Local Average Treatment Effect (LATE)|LATE]]
- [[exclusion restriction]]
- [[Regression Discontinuity Design (RDD)]]
- [[Synthetic Control]]
- [[Difference-in-Differences (DiD)]]
- [[parallel trends assumption]]
- [[composition]]
- [[Attrition]]
- [[Lee bounds]]
- [[bad controls]]
- [[collider bias]]
- [[placebo test]]
- [[seasonality]]
- [[few-cluster corrections]]
- [[clustered standard errors]]
